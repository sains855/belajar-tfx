import os
from tfx.components import CsvExampleGen, StatisticsGen, SchemaGen, ExampleValidator
from tfx.components import Transform, Trainer, Evaluator, Pusher
from tfx.proto import trainer_pb2, pusher_pb2

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_ROOT = os.path.join(PROJECT_DIR, 'data')
MODULE_FILE = os.path.join(PROJECT_DIR, 'pipeline', 'trainer_module.py')


def create_components(root):

    # === ExampleGen ===
    example_gen = CsvExampleGen(input_base=DATA_ROOT)

    # === StatisticsGen ===
    stats_gen = StatisticsGen(examples=example_gen.outputs['examples'])

    # === SchemaGen ===
    schema_gen = SchemaGen(
        statistics=stats_gen.outputs['statistics'],
        infer_feature_shape=False
    )

    # === ExampleValidator ===
    example_validator = ExampleValidator(
        statistics=stats_gen.outputs['statistics'],
        schema=schema_gen.outputs['schema']
    )

    # === Transform ===
    transform = Transform(
        examples=example_gen.outputs['examples'],
        schema=schema_gen.outputs['schema'],
        module_file=os.path.join(os.path.dirname(__file__), "preprocess.py")
    )

    # === Trainer ===
    trainer = Trainer(
        module_file=MODULE_FILE,
        examples=transform.outputs['transformed_examples'],
        transform_graph=transform.outputs['transform_graph'],
        schema=schema_gen.outputs['schema'],
        train_args=trainer_pb2.TrainArgs(num_steps=1000),
        eval_args=trainer_pb2.EvalArgs(num_steps=200)
    )

    # === Evaluator (Versi Simplified untuk TFX lawas) ===
    evaluator = Evaluator(
        examples=example_gen.outputs['examples'],
        model=trainer.outputs['model']   # Jika error -> ganti ke model_exports
    )

    # === Pusher ===
    pusher = Pusher(
        model=trainer.outputs['model'],
        model_blessing=evaluator.outputs['blessing'],
        push_destination=pusher_pb2.PushDestination(
            filesystem=pusher_pb2.PushDestination.Filesystem(
                base_directory=os.path.join(PROJECT_DIR, 'serving_model')
            )
        )
    )

    # Return semua komponen
    return [
        example_gen,
        stats_gen,
        schema_gen,
        example_validator,
        transform,
        trainer,
        evaluator,
        pusher
    ]
