import os
from tfx.orchestration import metadata
from tfx.orchestration.local.local_dag_runner import LocalDagRunner
from tfx.proto import example_gen_pb2
from tfx.components import (
    CsvExampleGen,
    StatisticsGen,
    SchemaGen,
    ExampleValidator
)
from tfx.orchestration.pipeline import Pipeline

# ======================================================
# 1. PATH KONFIGURASI
# ======================================================
PIPELINE_NAME = "diabetes_analysis_pipeline"

BASE_DIR = os.getcwd()
PIPELINE_ROOT = os.path.join(BASE_DIR, "pipline", PIPELINE_NAME)
METADATA_PATH = os.path.join(PIPELINE_ROOT, "metadata.sqlite")

# Dataset kamu
DATA_PATH = os.path.join(BASE_DIR, "data", "diabetes.csv")

# ======================================================
# 2. MEMBUAT PIPELINE
# ======================================================
def create_pipeline():

    # ExampleGen hanya membaca CSV bernama diabetes.csv
    input_config = example_gen_pb2.Input(splits=[
        example_gen_pb2.Input.Split(name='train', pattern='diabetes.csv')
    ])

    example_gen = CsvExampleGen(
        input_base=os.path.dirname(DATA_PATH),
        input_config=input_config
    )

    # Generate statistik dataset
    statistics_gen = StatisticsGen(
        examples=example_gen.outputs['examples']
    )

    # Auto schema inference
    schema_gen = SchemaGen(
        statistics=statistics_gen.outputs['statistics'],
        infer_feature_shape=True
    )

    # Validasi data berdasarkan schema
    validator = ExampleValidator(
        statistics=statistics_gen.outputs['statistics'],
        schema=schema_gen.outputs['schema']
    )

    return Pipeline(
        pipeline_name=PIPELINE_NAME,
        pipeline_root=PIPELINE_ROOT,
        components=[
            example_gen,
            statistics_gen,
            schema_gen,
            validator
        ],
        metadata_connection_config=metadata.sqlite_metadata_connection_config(METADATA_PATH)
    )

# ======================================================
# 3. RUN PIPELINE
# ======================================================
if __name__ == "__main__":
    print("Menjalankan TFX untuk analisis data diabetes.csv...")

    LocalDagRunner().run(create_pipeline())

    print("\nPipeline selesai ✓")
    print("Hasil tersedia di folder:")
    print(f"📂 {PIPELINE_ROOT}")

