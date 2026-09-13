"""
Freshness detection model — trains a small CNN (transfer learning on
MobileNetV2) to score food-photo freshness from 0 (spoiled) to 1 (fresh).

Not wired into the backend yet — backend/app/services/freshness_ai.py
currently stubs this out. Once you've trained and saved a model here,
update that service to load and call it.

Requires: pip install tensorflow opencv-python-headless
"""
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models


IMG_SIZE = (224, 224)


def build_model():
    base = tf.keras.applications.MobileNetV2(
        input_shape=IMG_SIZE + (3,), include_top=False, weights="imagenet"
    )
    base.trainable = False  # fine-tune later once the head is trained

    model = models.Sequential([
        base,
        layers.GlobalAveragePooling2D(),
        layers.Dense(64, activation="relu"),
        layers.Dropout(0.3),
        layers.Dense(1, activation="sigmoid"),  # freshness score 0-1
    ])
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["mae"])
    return model


def preprocess_image(path: str) -> np.ndarray:
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, IMG_SIZE)
    return img / 255.0


def predict_freshness(model, image_path: str) -> float:
    img = preprocess_image(image_path)
    score = model.predict(np.expand_dims(img, axis=0), verbose=0)[0][0]
    return float(score)


if __name__ == "__main__":
    # Placeholder training entrypoint — point at your labeled dataset directory
    # (e.g. a Kaggle fresh/rotten fruit-veg dataset) using
    # tf.keras.utils.image_dataset_from_directory before calling model.fit().
    model = build_model()
    model.summary()
