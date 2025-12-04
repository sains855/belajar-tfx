import warnings
warnings.filterwarnings("ignore")

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import tfx as tfx
import tensorflow as tf
print("TFX version:", tfx.__version__)
print("TF version :", tf.__version__)
print("🚀 OK! TensorFlow & TFX working on CPU.")
