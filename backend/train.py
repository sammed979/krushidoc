"""
KrishiDoc CNN Training Script
==============================
Dataset  : PlantVillage (54,306 images, 38 classes)
Model    : KrishiDoc-CNN-v1.0 (MobileNetV2 based)
Framework: TensorFlow / Keras

HOW TO TRAIN:
1. Add images to dataset/ folder (see dataset/README.md)
2. Run: python backend/train.py
3. Model will be saved as backend/krushidoc_model.h5

NOTE: Current system uses Google Gemini AI for diagnosis.
      This script is ready to train when dataset is collected.
"""

import os

DATASET_PATH = "dataset/"
MODEL_OUTPUT = "backend/krushidoc_model.h5"
IMAGE_SIZE   = (224, 224)
BATCH_SIZE   = 32
EPOCHS       = 20


def check_dataset():
    """Check if dataset folder has images."""
    total = 0
    classes = []
    for root, dirs, files in os.walk(DATASET_PATH):
        images = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if images:
            classes.append(os.path.basename(root))
            total += len(images)
    return total, classes


def train():
    total, classes = check_dataset()

    if total == 0:
        print("=" * 50)
        print("NO IMAGES FOUND IN DATASET FOLDER")
        print("=" * 50)
        print(f"Please add images to: {DATASET_PATH}")
        print("See dataset/README.md for instructions")
        print()
        print("Download PlantVillage dataset from:")
        print("https://www.kaggle.com/datasets/emmarex/plantdisease")
        return

    print(f"Found {total} images across {len(classes)} classes")
    print(f"Classes: {classes}")
    print()
    print("Starting training...")
    print("NOTE: Install dependencies first:")
    print("  pip install tensorflow pillow")
    print()

    # Training code - runs when dataset is available
    try:
        import tensorflow as tf
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
        from tensorflow.keras.models import Model
        from tensorflow.keras.preprocessing.image import ImageDataGenerator

        # Data augmentation
        datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            zoom_range=0.2,
            horizontal_flip=True,
            validation_split=0.2
        )

        train_gen = datagen.flow_from_directory(
            DATASET_PATH,
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            subset='training'
        )

        val_gen = datagen.flow_from_directory(
            DATASET_PATH,
            target_size=IMAGE_SIZE,
            batch_size=BATCH_SIZE,
            subset='validation'
        )

        # MobileNetV2 base model
        base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(*IMAGE_SIZE, 3))
        base.trainable = False

        x = GlobalAveragePooling2D()(base.output)
        x = Dense(128, activation='relu')(x)
        output = Dense(len(train_gen.class_indices), activation='softmax')(x)

        model = Model(inputs=base.input, outputs=output)
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        print(f"Training KrishiDoc-CNN-v1.0 for {EPOCHS} epochs...")
        model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS)

        model.save(MODEL_OUTPUT)
        print(f"Model saved to {MODEL_OUTPUT}")

    except ImportError:
        print("TensorFlow not installed. Run: pip install tensorflow")


if __name__ == "__main__":
    train()
