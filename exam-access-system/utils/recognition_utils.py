import cv2
import numpy as np
from keras.models import load_model

# Load pretrained model (admin has trained and placed it here)
model = load_model(""C:\Users\taha ihmadi\OneDrive\Bureau\exam-access-system\model\EfficientNetV2L_model.h5"")
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def preprocess_face(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        face = cv2.resize(face, (300, 300))
        face = face / 255.0
        return np.expand_dims(face, axis=0)
    return None


def predict_identity(image):
    """
    Returns (label, confidence) or (None, 0)
    """
    face = preprocess_face(image)
    if face is not None:
        preds = model.predict(face)
        label = int(np.argmax(preds))
        confidence = float(np.max(preds))
        return label, confidence
    return None, 0.0