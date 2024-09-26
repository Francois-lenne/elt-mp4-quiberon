import cv2
import numpy as np
import time


# Start time
start_time = time.time()

# Charger les poids et la configuration de YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
layer_names = net.getLayerNames()

# Handle both scalar and list cases for getUnconnectedOutLayers
unconnected_out_layers = net.getUnconnectedOutLayers()
if isinstance(unconnected_out_layers, np.ndarray):
    output_layers = [layer_names[i - 1] for i in unconnected_out_layers.flatten()]
else:
    output_layers = [layer_names[unconnected_out_layers - 1]]

# Charger les classes de COCO
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Lire la vidéo
cap = cv2.VideoCapture("downloaded_video_2024-09-24_08_04.mp4")

print("Analyse de la vidéo...", cap.get(cv2.CAP_PROP_FRAME_COUNT), "frames")

# Initialiser les variables
frame_count = 0
person_detected = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    height, width, channels = frame.shape

    # Détecter les objets
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Initialiser les listes pour les boîtes, les confidences et les IDs des classes
    class_ids = []
    confidences = []
    boxes = []

    print(f"Frame {frame_count}: ", end="")
    # Analyser les sorties
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == "person":
                # Obtenir les coordonnées de la boîte
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Calculer les coordonnées de la boîte
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Appliquer la suppression non maximale
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Vérifier si une personne est détectée
    if len(indexes) > 0:
        person_detected = True
    else:
        person_detected = False

    # Afficher les résultats
    print(f"Frame {frame_count}: Person detected = {person_detected}")

# Libérer les ressources
cap.release()
cv2.destroyAllWindows()

# End time
end_time = time.time()

# Calculate and print the execution time
execution_time = end_time - start_time
print(f"Le temps d'exécution du programme est de {execution_time} secondes.")