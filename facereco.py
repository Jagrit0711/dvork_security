import cv2
import face_recognition
import numpy as np
# Load known images and encode faces
known_image_paths = ["known_image1.jpg", "known_image2.jpg", ...]  # Replace with your image paths
known_images = []
known_encodings = []
# Copyright (c) DVORK BBPSRH JAGRIT SACHDEV
# All rights reserved.
for image_path in known_image_paths:
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
    known_images.append(image)
    known_encodings.extend(face_encodings)

# Load unknown image and encode faces
unknown_image_path = "unknown_image.jpg"  # Replace with your unknown image path
unknown_image = cv2.imread(unknown_image_path)
rgb_unknown_image = cv2.cvtColor(unknown_image, cv2.COLOR_BGR2RGB)
unknown_face_locations = face_recognition.face_locations(rgb_unknown_image)
unknown_face_encodings = face_recognition.face_encodings(rgb_unknown_image, unknown_face_locations)

# Compare known faces with unknown faces
for unknown_face_encoding in unknown_face_encodings:
    matches = face_recognition.compare_faces(known_encodings, unknown_face_encoding)
    face_distances = face_recognition.face_distance(known_encodings, unknown_face_encoding)
    best_match_index = np.argmin(face_distances)

    if matches[best_match_index]:
        name = known_image_paths[best_match_index].split("/")[-1].split(".")[0]
        print("Face recognized: ", name)
        # Draw a rectangle around the face and label it
        top, right, bottom, left = unknown_face_locations[0]
        cv2.rectangle(unknown_image, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(unknown_image, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    else:
        print("Face not recognized")

# Display the image
cv2.imshow('Image', unknown_image)
cv2.waitKey(0)
cv2.destroyAllWindows()