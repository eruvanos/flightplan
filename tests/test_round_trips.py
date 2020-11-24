import difflib
import secrets
import tempfile
from pathlib import Path

import pytest
import yaml

from flightplan import cli
from flightplan.render import Pipeline
from tests import T, get_resource


@pytest.fixture()
def tmp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield Path(tmpdirname)


@pytest.fixture()
def tmp_py(tmp_dir: Path):
    yield tmp_dir / f"{secrets.token_hex(8)}.py"


@pytest.fixture()
def tmp_yaml(tmp_dir: Path):
    yield tmp_dir / f"{secrets.token_hex(8)}.yaml"


@pytest.mark.parametrize(
    "pipeline_yaml",
    [
        T("Hello World", get_resource("hello_world.yaml")),
        T("CF Deployment", get_resource("simple_cf_deploy.yaml")),
        T("Simple Python pipeline", get_resource("simple_python.yaml")),
        # Testflight ymls from https://github.com/concourse/concourse/tree/master/testflight/fixtures
        T("archive-pipeline-1.yml", "archive-pipeline-1.yml"),
        T("archive-pipeline-2.yml", "archive-pipeline-2.yml"),
        T("archive-pipeline-3.yml", "archive-pipeline-3.yml"),
        T("caching.yml", "caching.yml"),
        T("clear-task-cache.yml", "clear-task-cache.yml"),
        T("config-test.yml", "config-test.yml"),
        T("config_params.yml", "config_params.yml"),
        T(
            "container_limits.yml", "container_limits.yml"
        ),  # Memory limit not int -> 1GB
        T(
            "container_limits_failing.yml", "container_limits_failing.yml"
        ),  # Memory limit not int -> 1GB
        T("custom-resource-type.yml", "custom-resource-type.yml"),
        T("do.yml", "do.yml"),
        T("fail.yml", "fail.yml"),
        T("hooks.yml", "hooks.yml"),
        T("http-proxy-task.yml", "http-proxy-task.yml"),
        T("image-resource-test.yml", "image-resource-test.yml"),
        T("image-resource-with-params.yml", "image-resource-with-params.yml"),
        T("input-mapping-test.yml", "input-mapping-test.yml"),
        T("inputs_outputs.yml", "inputs_outputs.yml"),
        T("load-var-step.yml", "load-var-step.yml"),
        T("many-inputs.yml", "many-inputs.yml"),
        # T("matrix.yml", "matrix.yml"), Uses deprecated aggregate
        # T("nested-config-test.yml", "nested-config-test.yml"), missing source in resource 1
        T("optional-inputs.yml", "optional-inputs.yml"),
        T("pinned-resource-simple-trigger.yml", "pinned-resource-simple-trigger.yml"),
        T("pinned-version.yml", "pinned-version.yml"),
        T("propagation.yml", "propagation.yml"),
        T("put-inputs.yml", "put-inputs.yml"),
        T("reconfiguring.yml", "reconfiguring.yml"),
        T("recursive-resource-checking.yml", "recursive-resource-checking.yml"),
        T("rename-resource.yml", "rename-resource.yml"),
        T("rename-simple.yml", "rename-simple.yml"),
        # T("resource-check-timeouts.yml", "resource-check-timeouts.yml"), check-timeout not in docs
        T(
            "resource-type-named-as-base-type.yml",
            "resource-type-named-as-base-type.yml",
        ),
        T("resource-type-versions.yml", "resource-type-versions.yml"),
        # T("resource-types.yml", "resource-types.yml"), Missing image_resource
        T("resource-types-privileged.yml", "resource-types-privileged.yml"),
        T("resource-types-with-params.yml", "resource-types-with-params.yml"),
        T("resource-version-every.yml", "resource-version-every.yml"),
        T("resource-version-latest.yml", "resource-version-latest.yml"),
        T("resource-with-params.yml", "resource-with-params.yml"),
        T("resource-with-versions.yml", "resource-with-versions.yml"),
        T("retry.yml", "retry.yml"),
        T("serial-groups.yml", "serial-groups.yml"),
        T("serial-groups-inputs-updated.yml", "serial-groups-inputs-updated.yml"),
        T("set-pipeline.yml", "set-pipeline.yml"),
        T("simple.yml", "simple.yml"),
        T("simple-trigger.yml", "simple-trigger.yml"),
        T("task-caches.yml", "task-caches.yml"),
        T("task-missing-outputs.yml", "task-missing-outputs.yml"),
        T("task-outputs.yml", "task-outputs.yml"),
        T("task_vars.yml", "task_vars.yml"),
        # T("timeout.yml", "timeout.yml"), missing image_resource in jobs
        T("timeout_hooks.yml", "timeout_hooks.yml"),
        T("try.yml", "try.yml"),
        T("var-sources.yml", "var-sources.yml"),
        T("volume-mounting.yml", "volume-mounting.yml"),

        # Custom
        T("in_parallel_simple_array.yml", "in_parallel_simple_array.yml"),
    ],
)
def test_round_trip(tmp_py, tmp_yaml, pipeline_yaml):
    if isinstance(pipeline_yaml, str):
        pipeline_yaml = get_resource("testflight-fixtures/" + pipeline_yaml)

    # YAML -> PY
    cli.import_yaml(pipeline_yaml, tmp_py)

    # PY -> YAML
    cli.synth(tmp_py, tmp_yaml)

    # load expected, remove anchors, write back and read as str
    with pipeline_yaml.open() as f:
        raw = yaml.safe_load(f)

    base_obj = Pipeline()
    for key in list(raw.keys()):
        if not hasattr(base_obj, key):
            del raw[key]

    cli._write_yaml_file(raw, pipeline_yaml)
    expected = pipeline_yaml.read_text()

    # get actual and compare
    actual = tmp_yaml.read_text()
    print("Len of expected", len(expected))
    assert actual == expected, "\n".join(
        difflib.unified_diff(expected.splitlines(), actual.splitlines())
    )


# TODO resource-types: no image-resource in one job
# TODO resource-check-timeouts: no image-resource in one job
