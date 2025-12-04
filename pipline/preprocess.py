import tensorflow_transform as tft

LABEL_KEY = 'Outcome'
FEATURE_KEYS = [
    'Pregnancies','Glucose','BloodPressure','SkinThickness',
    'Insulin','BMI','DiabetesPedigreeFunction','Age'
]
# Jika ingin bucket Age untuk slice, tambahkan AGE_BUCKET
AGE_BUCKETS = 3

def preprocessing_fn(inputs):
    """TFX preprocessing_fn.
    - Skala numerik ke z-score menggunakan tft.scale_to_z_score
    - Keep label as-is
    - Buat bucketized age untuk slicing (Age_bucket)
    """
    outputs = {}
    for key in FEATURE_KEYS:
        value = inputs[key]
        # Asumsi dataset sudah dibersihkan (no empty strings in numeric cols)
        outputs[key] = tft.scale_to_z_score(value)

    age = inputs['Age']
    outputs['Age_bucket'] = tft.bucketize(age, num_buckets=AGE_BUCKETS)

    outputs[LABEL_KEY] = inputs[LABEL_KEY]
    return outputs
