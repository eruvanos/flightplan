from flightplan import *
from tests import load_yaml, assert_dict_equal


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
    assert result == load_yaml('hello_world.yaml')


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
    assert result == load_yaml('hello_world.yaml')


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
    assert result == load_yaml('hello_world.yaml')
