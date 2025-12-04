# pipeline/pipeline.py
import os
from tfx.orchestration.local.local_dag_runner import LocalDagRunner
from tfx.orchestration import pipeline as tfx_pipeline
from tfx.orchestration import metadata
from pipline.components import create_components

# Paths
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
PIPELINE_ROOT = os.path.join(PROJECT_DIR, "tfx_pipeline_output")
METADATA_PATH = os.path.join(PROJECT_DIR, "metadata.db")
DATA_ROOT = os.path.join(PROJECT_DIR, "data")

PIPELINE_NAME = "diabetes_pipeline"

def create_pipeline():
    components = create_components(DATA_ROOT)

    return tfx_pipeline.Pipeline(
        pipeline_name=PIPELINE_NAME,
        pipeline_root=PIPELINE_ROOT,
        components=components,
        # Berikan konfigurasi metadata sqlite yang valid (bukan None)
        metadata_connection_config=metadata.sqlite_metadata_connection_config(METADATA_PATH),
        enable_cache=True
    )

def run_pipeline():
    print("🚀 Menjalankan TFX Pipeline Lokal...")
    LocalDagRunner().run(create_pipeline())
    print("🎉 Pipeline selesai!")

if __name__ == "__main__":
    run_pipeline()
