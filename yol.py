from ultralytics import YOLO
import cv2
import math


def video_detection(path_x):
    cap = cv2.VideoCapture(path_x)
    if not cap.isOpened():
        print(f"Error opening video stream or file: {path_x}")
        return

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    model = YOLO("../YOLO-Weights/fireacc.pt")
    classNames = ["fire", "accident"]
    detection_flag = False

    while True:
        success, img = cap.read()
        if not success:
            break
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                print(x1, y1, x2, y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                conf = math.ceil((box.conf[0] * 100)) / 100
                cls = int(box.cls[0])
                class_name = classNames[cls]
                label = f'{class_name} {conf}'
                t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]
                c2 = x1 + t_size[0], y1 - t_size[1] - 3
                cv2.rectangle(img, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)
                cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)
                detection_flag = True  # Set detection flag to True
        yield img, detection_flag
    cap.release()
    cv2.destroyAllWindows()
