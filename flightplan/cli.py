import io
import shutil
import tempfile
from pathlib import Path
from subprocess import run, PIPE
from typing import Dict
from warnings import warn

import black
import typer
import yaml
from black import WriteBack
from typer import Typer

from flightplan.render import Pipeline, Var

app = Typer()


def _load_py_file(src_py: Path):
    import importlib.util

    spec = importlib.util.spec_from_file_location("module.name", src_py)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return Pipeline.pipelines


def _write_yaml_file(data: Dict, target_yaml: Path):
    # https://github.com/yaml/pyyaml/issues/103
    class NoAliasDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    # https://github.com/yaml/pyyaml/issues/240
    def str_presenter(dumper, data):
        try:
            dlen = len(data.splitlines())
            if dlen > 1:
                return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        except TypeError:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data)
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)

    def var_presenter(dumper, data):
        return dumper.represent_scalar("tag:yaml.org,2002:str", str(data))

    yaml.add_representer(str, str_presenter, Dumper=NoAliasDumper)
    yaml.add_representer(Var, var_presenter, Dumper=NoAliasDumper)

    with target_yaml.open("wt") as f:
        yaml.dump(data, f, Dumper=NoAliasDumper)


def _write_py_file(pipeline: Pipeline, target: Path):
    with target.open("wt") as f:
        f.write("from flightplan.render import *\n")
        f.write("\n")
        f.write("pipe = ")
        f.write(pipeline.__repr__())
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("if __name__ == '__main__':\n")
        f.write("    print(pipe.synth())\n")


def _format_py_file(target: Path):
    black.format_file_in_place(
        target, fast=False, mode=black.FileMode(), write_back=WriteBack.YES
    )


def _export_py(raw_data: dict, target: Path):
    typer.echo(f"🗂 Convert to Python")
    pipe = Pipeline.parse_obj(raw_data)

    typer.echo(f"📝 Write Python file")
    _write_py_file(pipe, target)

    typer.echo(f"🌇 Format code")
    _format_py_file(target)

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
def import_yaml(source: Path, target: Path):
    typer.echo(f"📖 Read YAML")
    with source.open() as f:
        raw = yaml.safe_load(f)

    _export_py(raw, target)


@app.command(help="Renders a Concourse YAML file from given .py file")
def synth(src_py: Path, target_yaml: Path):
    typer.echo(f"📖 Read Python file")
    pipelines = _load_py_file(src_py)
    if len(pipelines) > 0:
        warn("Multiple pipelines found, will use last one")

    typer.echo(f"📝 Write YAML file")
    for pipeline in pipelines[-1:]:
        _write_yaml_file(pipeline.synth(), target_yaml)

    typer.echo(f"✅ Done")


@app.command(help="Fly set-pipeline from py. file")
def set(fly_target: str, pipeline_name: str, src_py: Path):
    pipelines = _load_py_file(src_py)
    assert len(pipelines) == 1

    with tempfile.TemporaryDirectory() as tmpdirname:
        file = Path(tmpdirname) / f"pipeline.yaml"
        _write_yaml_file(pipelines[0].synth(), file)

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


@app.command(help="Sort keys of a yaml, in place", hidden=True)
def sort(yaml_file: Path):
    typer.echo(f"📖 Read 💫 YAML")
    with yaml_file.open() as f:
        raw = yaml.safe_load(f)

    typer.echo(f"📝 Write ✨ YAML")
    with yaml_file.open("w") as f:
        yaml.safe_dump(raw, f)

    typer.echo(f"✅ Done")


def main():
    app()


if __name__ == "__main__":
    main()
