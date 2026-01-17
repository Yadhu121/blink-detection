import cv2
import mediapipe as mp
import numpy as np

def euclidean(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def eye_aspect_ratio(eye):
    A = euclidean(eye[1], eye[5])
    B = euclidean(eye[2], eye[4])
    C = euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

cap = cv2.VideoCapture(1)

EAR_THRESHOLD = 0.20
CLOSED_FRAMES = 2
closed_counter = 0
blink_total = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    
    if results.multi_face_landmarks:
        lm = results.multi_face_landmarks[0].landmark
        
        left_eye = [(int(lm[i].x * w), int(lm[i].y * h)) for i in LEFT_EYE]
        right_eye = [(int(lm[i].x * w), int(lm[i].y * h)) for i in RIGHT_EYE]
        
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
            
        if left_ear < EAR_THRESHOLD and right_ear < EAR_THRESHOLD:
            closed_counter += 1
        else:
            if closed_counter >= CLOSED_FRAMES:
                blink_total += 1
                print("Blink count:", blink_total)
            closed_counter = 0
    
    cv2.imshow("Blink Detection", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
