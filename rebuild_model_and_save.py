import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense

# Define the same model architecture used during training
def build_model():
    model = Sequential()
    model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(64, 64, 1)))
    model.add(Conv2D(32, kernel_size=3, activation='relu'))
    model.add(Flatten())
    model.add(Dense(2, activation='softmax'))
    return model

# Build and load weights
model = build_model()
model.load_weights("25APRFALLDtection.h5")

# Save it as a modern .keras zip-based format
model.save("FALLModel_cleaned.keras")

print("✅ Model rebuilt and saved as 'FALLModel_cleaned.keras'")
