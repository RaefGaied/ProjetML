import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from create_model import create_model, get_callbacks
import os

def train_model(train_dir, val_dir, epochs=20, batch_size=32):
    """
    Train the pneumonia detection model with optimized parameters
    """
    # Data preprocessing and augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )

    # Only rescaling for validation
    val_datagen = ImageDataGenerator(rescale=1./255)

    # Create data generators
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='binary'
    )

    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='binary'
    )

    # Create and compile model
    model = create_model()
    
    # Get callbacks for training optimization
    callbacks = get_callbacks()

    # Train the model
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        epochs=epochs,
        validation_data=val_generator,
        validation_steps=val_generator.samples // batch_size,
        callbacks=callbacks
    )

    return model, history

if __name__ == '__main__':
    # Set paths
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    train_dir = os.path.join(base_dir, 'train')
    val_dir = os.path.join(base_dir, 'val')
    
    # Train model
    model, history = train_model(train_dir, val_dir)
    
    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(model_dir, exist_ok=True)
    model.save(os.path.join(model_dir, 'pneumonia_model.h5'))
    
    print("\nTraining completed successfully!")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")
    print(f"Final validation AUC: {history.history['val_auc'][-1]:.4f}") 