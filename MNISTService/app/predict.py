import tensorflow as tf
import numpy as np
from PIL import Image

model = None


def load_model() -> tf.keras.models.Sequential:
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(input_shape=(28, 28)),
      tf.keras.layers.Dense(128, activation='relu'),
      tf.keras.layers.Dense(10)
    ])
    model.compile(
    optimizer=tf.keras.optimizers.Adam(0.001),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()],
    )
    model.load_weights('app/trained_model/mnist_weights.h5')
    return model


def preprocess_image(img: Image.Image) -> np.array:
    img_arr = np.asarray(img)
    img_arr = np.expand_dims(img_arr, axis=0)
    return tf.cast(img_arr, tf.float32) / 255.


def predict_number(img: Image.Image) -> int:
    global model
    if model is None:
        model = load_model()
    img = preprocess_image(img)
    probs = model.predict(img)
    return int(probs.argmax(axis=-1)[0])
