import cv2
import numpy as np

class PersonDetector:
    def __init__(self, video_path):
        self.video_path = video_path
        self.net, self.output_layers = self.set_up_output_layer()
        self.classes = self.set_up_classes()

    @staticmethod
    def set_up_output_layer():
        # Load YOLO weights and configuration
        net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
        layer_names = net.getLayerNames()

        # Handle both scalar and list cases for getUnconnectedOutLayers
        unconnected_out_layers = net.getUnconnectedOutLayers()
        if isinstance(unconnected_out_layers, np.ndarray):
            output_layers = [layer_names[i - 1] for i in unconnected_out_layers.flatten()]
        else:
            output_layers = [layer_names[i - 1] for i in unconnected_out_layers]
        
        print("Output layer set up successfully.")
        return net, output_layers

    @staticmethod
    def set_up_classes():
        # Load COCO classes
        with open("coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        print("Classes loaded successfully.")
        return classes

    def set_up_capture(self):
        cap = cv2.VideoCapture(self.video_path)
        print(f"Analyzing video... {int(cap.get(cv2.CAP_PROP_FRAME_COUNT))} frames")
        return cap

    def process_video(self):
        cap = self.set_up_capture()
        frame_count = 0
        detection_results = {}

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1

            # Process only every 20th frame
            if frame_count % 20 != 0:
                continue

            height, width, _ = frame.shape

            # Detect objects
            blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            # Initialize lists for boxes, confidences, and class IDs
            class_ids = []
            confidences = []
            boxes = []

            # Analyze outputs
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5 and self.classes[class_id] == "person":
                        # Get box coordinates
                        center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
                        x, y = int(center_x - w / 2), int(center_y - h / 2)

                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)

            # Apply non-maximum suppression
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            # Check if a person is detected
            person_detected = len(indexes) > 0

            # Store results for this frame
            detection_results[frame_count] = {"person_present": person_detected}

            # Display results (optional, can be commented out for faster processing)
            print(f"Frame {frame_count}: Person detected = {person_detected}")

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

        return detection_results

    def check_person(self):
        detection_results = self.process_video()
        print(detection_results)
        return detection_results

def analyze_video_for_persons(video_path):
    """
    Analyze a video file for the presence of persons.
    
    :param video_path: Path to the MP4 video file
    :return: Dictionary with frame numbers as keys and person detection results as values
    """
    detector = PersonDetector(video_path)
    results = detector.check_person()
    return results

# Example usage
if __name__ == "__main__":
    video_path = "downloaded_video_2024-09-29_10_34.mp4"
    results = analyze_video_for_persons(video_path)
    print(results)