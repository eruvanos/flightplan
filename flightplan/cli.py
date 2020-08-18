import io
import shutil
import tempfile
from pathlib import Path
from subprocess import run, PIPE

import black
import typer
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


def write_py_file(pipeline: Pipeline, target: Path):
    with target.open('wt') as f:
        f.write('from flightplan.render import *\n')
        f.write('\n')
        f.write('pipe = ')
        f.write(repr(pipeline))
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


@app.command(
    help='Generate a basic pipeline.py example',
)
def quickstart(output: Path = Path('pipeline.py')):
    from flightplan.quickstart import hello
    src = Path(hello.__file__)

    if output.exists():
        typer.echo(f'{output} already exists, will not overwrite your existing work!')
        raise typer.Abort()

    shutil.copy(src, output)


@app.command(
    'import',
    help='Imports a YAML file and renders a Flightplan .py file',
)
def _import(source: Path, target: Path):
    with source.open() as f:
        raw = yaml.safe_load(f)

    pipe = Pipeline.parse_obj(raw)

    write_py_file(pipe, target)


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


@app.command()
def get(fly_target: str, pipeline_name: str, target_py: Path):
    execution = run([
        'fly',
        '-t',
        fly_target,
        'get-pipeline',
        '-p',
        pipeline_name,
    ],
        stdout=PIPE
    )

    raw = yaml.safe_load(io.StringIO(execution.stdout.decode()))
    pipe = Pipeline.parse_obj(raw)

    write_py_file(pipe, target_py)


def main():
    app()


if __name__ == '__main__':
    main()
