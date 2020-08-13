import pytest

from flightplan import *
from tests import load_yaml


def test_render_deploy_pipeline():
    pipeline = Pipeline(
        name='mypipeline',
        resource_types=[
            ResourceType(
                name='cf-cli',
                type='docker-image',
                source=Source(
                    repository='nulldriver/cf-cli-resource',
                    tag='latest'
                )
            )
        ],
        resources=[
            Resource(
                name='src',
                type='git',
                source=dict(
                    uri='git@github.com:eruvanos/flightplan.git',
                    branch='master'
                )
            ),
            Resource(
                name='cf-dev',
                type='cf-cli',
                source=dict(cf_dial_timeout=300)
            )
        ],
        jobs=[
            Job(
                name='deploy-app',
                public=False,
                plan=[
                    Get(name='src', resource='src', trigger=True),
                    Put(
                        name='deploy',
                        resource='cf-dev',
                        params=dict(
                            command='zero-downtime-push',
                            current_app_name='concourse',
                            manifest='src/ci/manifest.yml',
                            path='src/.'
                        )
                    )
                ]
            )
        ]
    )

    result = pipeline.synth()
    assert result == load_yaml('simple_cf_deploy.yaml')


@pytest.mark.skip('WIP')
def test_render_deploy_pipeline_pythonic():
    with Pipeline(name='mypipeline') as pipeline:
        with ResourceType(
                name='cf-cli',
                type='docker-image',
                source=Source(
                    repository='nulldriver/cf-cli-resource',
                    tag='latest'
                )
        ) as CfCli:
            cf_dev = CfCli(
                name='cf-dev',
                type='cf-cli',
                source=dict(cf_dial_timeout=300)
            )

        with GitResource() as Git:
            src = Git(
                name='src',
                type='git',
                source=dict(
                    uri='git@github.com:eruvanos/flightplan.git',
                    branch='master'
                )
            )

        with Job(name='deploy-app', public=False):
            Get(name='src', resource=cf_dev, trigger=True),

            Put(
                name='deploy',
                resource=src,
                params=dict(
                    command='zero-downtime-push',
                    current_app_name='concourse',
                    manifest='src/ci/manifest.yml',
                    path='src/.'
                )
            )

    result = pipeline.synth()
    assert result == load_yaml('simple_cf_deploy.yaml')
