import json
from pathlib import Path

import yaml

from flightplan import *

TEST_DATA = Path(__file__).parent / 'data'


def load_yaml(file: str):
    with (TEST_DATA / file).open() as f:
        return yaml.load(f)


def assert_dict_equal(expected: dict, actual: dict):
    dict_a_str = json.dumps(expected, sort_keys=True, indent=2)
    dict_b_str = json.dumps(actual, sort_keys=True, indent=2)

    assert dict_a_str == dict_b_str


def test_version():
    from flightplan import __version__
    assert __version__ == '0.1.0'


def test_render_hello_world():
    pipeline = Pipeline(
        name='mypipeline',
        jobs=[
            Job(
                name='job-hello-world',
                public=True,
                plan=[
                    Task(
                        name='hello-world',
                        config=TaskConfig(
                            platform='linux',
                            image_resource=ImageResource(
                                type='docker-image',
                                source=Source(
                                    repository='busybox',
                                    tag='latest'
                                )
                            ),
                            run=Command(
                                path='echo',
                                args=['hello world']
                            )
                        )
                    )
                ]
            )
        ]
    )

    result = pipeline.synth()
    assert_dict_equal(result, load_yaml('hello_world.yaml'))


def test_render_hello_world_dynamic():
    echo_hello_world = Task(name='hello-world',
                            config=TaskConfig(
                                platform='linux',
                                image_resource=ImageResource(
                                    type='docker-image',
                                    source=Source(repository='busybox', tag='latest')),
                                run=Command(
                                    path='echo',
                                    args=['hello world']
                                )
                            ))

    hello_world = Job(name='job-hello-world',
                      public=True,
                      plan=[echo_hello_world]
                      )

    pipeline = Pipeline(name='mypipeline')
    pipeline.add_job(
        hello_world
    )

    result = pipeline.synth()
    assert_dict_equal(result, load_yaml('hello_world.yaml'))


def test_render_hello_world_with_construct():
    with Pipeline(name='mypipeline') as pipeline:
        with Job(name='job-hello-world', public=True):
            with Task(name='hello-world'):
                TaskConfig(
                    platform='linux',
                    image_resource=ImageResource(
                        type='docker-image',
                        source=Source(repository='busybox', tag='latest')),
                    run=Command(
                        path='echo',
                        args=['hello world']
                    )
                )

    result = pipeline.synth()
    assert_dict_equal(result, load_yaml('hello_world.yaml'))
