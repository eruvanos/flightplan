import tempfile
from pathlib import Path
from subprocess import run

import black
import yaml
from black import WriteBack
from typer import Typer

from flightplan.render import Pipeline

app = Typer()


def load_file(src_py: Path):
    import importlib.util
    spec = importlib.util.spec_from_file_location("module.name", src_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return Pipeline.pipelines


def write_file(pipeline: Pipeline, target_yaml: Path):
    with target_yaml.open('wt') as f:
        yaml.safe_dump(pipeline.synth(), f)


@app.command(
    'import',
    help='Imports a YAML file and renders a Flightplan .py file',
)
def _import(source: Path, target: Path):
    with source.open() as f:
        raw = yaml.safe_load(f)

    pipe = Pipeline.parse_obj(raw)

    with target.open('wt') as f:
        f.write('from flightplan.render import *\n')
        f.write('\n')
        f.write('pipe = ')
        f.write(repr(pipe))
        f.write('\n')
        f.write('\n')
        f.write('\n')
        f.write('if __name__ == \'__main__\':\n')
        f.write('    pipe.synth()\n')

    black.format_file_in_place(
        target,
        fast=False,
        mode=black.FileMode(),
        write_back=WriteBack.YES
    )


@app.command()
def synth(src_py: Path, target_yaml: Path):
    pipelines = load_file(src_py)
    assert len(pipelines) == 1

    for pipeline in pipelines[-1:]:
        write_file(pipeline, target_yaml)


@app.command()
def set(fly_target: str, pipeline_name: str, src_py: Path):
    pipelines = load_file(src_py)
    assert len(pipelines) == 1

    with tempfile.TemporaryDirectory() as tmpdirname:
        file = Path(tmpdirname) / 'pipeline.yaml'
        write_file(pipelines[0], file)

        run([
            'fly',
            '-t',
            fly_target,
            'set-pipeline',
            '-p',
            pipeline_name,
            '-c',
            str(file.absolute())
        ])

def main():
    app()

if __name__ == '__main__':
    main()
