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

from flightplan.render import Pipeline, Get, Put

app = Typer()


def load_file(src_py: Path):
    import importlib.util

    spec = importlib.util.spec_from_file_location("module.name", src_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return Pipeline.pipelines


def write_file(pipeline: Pipeline, target_yaml: Path):
    def str_presenter(dumper, data):
        try:
            dlen = len(data.splitlines())
            if dlen > 1:
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        except TypeError:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data)
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    yaml.add_representer(str, str_presenter)

    with target_yaml.open("wt") as f:
        yaml.dump(pipeline.synth(), f)


def write_py_file(pipeline: Pipeline, target: Path):
    with target.open("wt") as f:
        f.write("from flightplan.render import *\n")
        f.write("\n")
        f.write("pipe = ")
        f.write(pipeline.__repr__())
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("if __name__ == '__main__':\n")
        f.write("    pipe.synth()\n")


def format_py_file(target: Path):
    black.format_file_in_place(
        target, fast=False, mode=black.FileMode(), write_back=WriteBack.YES
    )


def _export_py(raw_data: dict, target: Path):
    typer.echo(f"✨ Prepare some magic")
    # Disable Enum representation as string
    Get.Config.use_enum_values = False
    Put.Config.use_enum_values = False

    typer.echo(f"🗂 Convert to Python")
    pipe = Pipeline.parse_obj(raw_data)

    typer.echo(f"📝 Write Python file")
    write_py_file(pipe, target)

    typer.echo(f"🌇 Format code")
    format_py_file(target)

    typer.echo(f"✅ Done")


@app.command(help="Generate a basic pipeline.py example",)
def quickstart(output: Path = Path("pipeline.py")):
    from flightplan.quickstart import hello

    src = Path(hello.__file__)

    if output.exists():
        typer.echo(f"{output} already exists, will not overwrite your existing work!")
        raise typer.Abort()

    shutil.copy(src, output)
    typer.echo(f"✅ Find the example in `pipeline.py`")


@app.command(
    "import", help="Imports a YAML file and renders a Flightplan .py file",
)
def _import(source: Path, target: Path):
    typer.echo(f"📖 Read YAML")
    with source.open() as f:
        raw = yaml.safe_load(f)

    _export_py(raw, target)


@app.command(help="Renders a Concourse YAML file from given .py file")
def synth(src_py: Path, target_yaml: Path):
    typer.echo(f"📖 Read Python file")
    pipelines = load_file(src_py)
    assert len(pipelines) == 1

    typer.echo(f"📝 Write YAML file")
    for pipeline in pipelines[-1:]:
        write_file(pipeline, target_yaml)

    typer.echo(f"✅ Done")


@app.command(help="Fly set-pipeline from py. file")
def set(fly_target: str, pipeline_name: str, src_py: Path):
    pipelines = load_file(src_py)
    assert len(pipelines) == 1

    with tempfile.TemporaryDirectory() as tmpdirname:
        file = Path(tmpdirname) / f"pipeline.yaml"
        write_file(pipelines[0], file)

        run(
            [
                "fly",
                "-t",
                fly_target,
                "set-pipeline",
                "-p",
                pipeline_name,
                "-c",
                str(file.absolute()),
            ]
        )


@app.command(help="Import a pipeline directly from fly get-pipeline")
def get(fly_target: str, pipeline_name: str, target_py: Path):
    typer.echo(f"📖 Read pipeline from Concourse")
    execution = run(
        ["fly", "-t", fly_target, "get-pipeline", "-p", pipeline_name,], stdout=PIPE
    )

    raw = yaml.safe_load(io.StringIO(execution.stdout.decode()))
    _export_py(raw, target_py)


def main():
    app()


if __name__ == "__main__":
    main()
