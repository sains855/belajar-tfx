import tensorflow as tf
from tensorflow_transform.tf_metadata import schema_utils
from tensorflow_transform import TFTransformOutput  # ✔ FIX
from tfx_bsl.public import tfxio

_LABEL_KEY = "Outcome"   # Ganti sesuai nama label datasetmu


def _input_fn(file_pattern, data_accessor, tf_transform_output, batch_size=32):
    """Membuat tf.data.Dataset dari TFRecord hasil Transform."""

    # Ambil schema hasil Transform
    schema = tf_transform_output.transformed_metadata.schema

    # Dataset factory — TFX versi kamu membutuhkan schema
    dataset = data_accessor.tf_dataset_factory(
        file_pattern,
        tfxio.TensorFlowDatasetOptions(
            batch_size=batch_size,
            label_key=_LABEL_KEY,
        ),
        schema=schema  # ✔ FIX WAJIB
    )

    return dataset


def run_fn(fn_args):
    """Fungsi utama training yang dipanggil oleh TFX Trainer."""

    # LOAD transform_output dengan cara yang benar
    tf_transform_output = TFTransformOutput(fn_args.transform_output)

    # Ambil dataset training & eval
    train_ds = _input_fn(
        fn_args.train_files,
        fn_args.data_accessor,
        tf_transform_output,
        batch_size=32
    )

    eval_ds = _input_fn(
        fn_args.eval_files,
        fn_args.data_accessor,
        tf_transform_output,
        batch_size=32
    )

    # Buat model
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(8,)),  # ganti sesuai fitur kamu
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    # Training
    model.fit(
        train_ds,
        validation_data=eval_ds,
        steps_per_epoch=fn_args.train_steps,
        validation_steps=fn_args.eval_steps
    )

    # Save model ke serving directory
    model.save(fn_args.serving_model_dir, save_format='tf')
