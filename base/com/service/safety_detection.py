import os
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from app import app


def create_rect(image, text, position, box_coordinates, font, color):
    draw = ImageDraw.Draw(image)
    draw.rectangle(box_coordinates, outline=color, width=2)
    draw.text(position, text, font=font, fill=color)
    return image


def detection(input_video_path):
    model = YOLO(r"static/model/best1.pt")
    video_name = os.path.basename(input_video_path)

    try:
        cap = cv2.VideoCapture(input_video_path)

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'avc1')

        output_video_path = f"{app.config['OUTPUT_FOLDER']}\{video_name}"
        out = cv2.VideoWriter(output_video_path, fourcc, fps, (int(cap.get(3)), int(cap.get(4))))

        frames = 0
        class_count = {}

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            try:
                results = model.predict(frame)
                result = results[0]

                font_size = 20
                font = ImageFont.truetype("arial.ttf", font_size)

                detection_occurred = False

                safety_classes = ["Vest", "Helmet"]  # Vest, Helmet
                for idx, box in enumerate(result.boxes):
                    class_id = result.names[box.cls[0].item()]
                    # conf = box.conf[0].item()
                    cords = box.xyxy[0].tolist()
                    cords = [round(x) for x in cords]
                    conf = round(box.conf[0].item(), 2)

                    if class_id == "Helmet":  # Helmet
                        bounding_box_color = (255, 255, 0)  # Yellow
                        text_color = (255, 255, 0)  # Yellow
                    elif class_id == "NOHelmet":  # NOHelmet
                        bounding_box_color = (0, 0, 255)  # Blue
                        text_color = (0, 0, 255)  # Blue
                    elif class_id == "NOVest":  # NOVest
                        bounding_box_color = (255, 0, 0)  # Red
                        text_color = (255, 0, 0)  # Red
                    elif class_id == "Vest":
                        bounding_box_color = (0, 255, 0)  # Green
                        text_color = (0, 255, 0)  # Green
                    else:
                        bounding_box_color = (128, 128, 128)  # Gray
                        text_color = (128, 128, 128)  # Gray

                    text = f"{class_id}({conf})"
                    position = (cords[0], cords[1] - 22)
                    image_with_text_and_box = create_rect(image, text, position, cords, font, text_color)

                    modified_frame = cv2.cvtColor(np.array(image_with_text_and_box), cv2.COLOR_RGB2BGR)

                    if not detection_occurred:
                        detection_occurred = True

                    if class_id not in class_count:
                        class_count[class_id] = 0

                    class_count[class_id] += 1

                    if detection_occurred:
                        out.write(modified_frame)
                    else:
                        out.write(frame)

                if detection_occurred:
                    modified_frame = modified_frame
                else:
                    modified_frame = frame

                display_frame = cv2.resize(modified_frame, (width, height), interpolation=cv2.INTER_AREA)
                cv2.imshow('Safety Detection', display_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            except Exception as e:
                print(f"Error processing frame {frames}: {e}")

            frames += 1

    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    print("Class Count---->", class_count)

    return output_video_path, class_count
