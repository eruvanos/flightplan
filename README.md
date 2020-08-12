

# Flight plan - Plan your Concourse Pipeline with ease

AWS CDK like tool to code Concourse pipelines, (with autocompletion and validation.)


## Planed features

* Generate pipeline YAML from cli (or Python)
* Set pipeline from cli
* Predefined code constructs to simplify common pipelines

## Examples

Pythonic definition:
```python
from flightplan import *

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

pipeline.synth()
```

Constructor definitions:
```python
from flightplan import *

Pipeline(
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
).synth()
``` 

More dynamic definitions:
```python
from flightplan import *

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

pipeline.synth()
``` 


## Backlog

* [ ] Pipeline 1: "echo hello world"
* [ ] Pipeline 2: check out git and run test


* [ ] Add Types
    * [ ] Pipeline*
        * [ ] Jobs*
            * [ ] name*
            * [ ] plan*
            * [ ] old_name
            * [ ] serial
            * [ ] build_log_retention
            * [ ] build_logs_to_retain
            * [ ] serial_groups
            * [ ] max_in_flight
            * [ ] public
            * [ ] disable_manual_trigger
            * [ ] interruptible
            * [ ] on_success
            * [ ] on_failure
            * [ ] on_error
            * [ ] on_abort
            * [ ] ensure
            
            * [ ] Step*
                * [ ] Task*
                * [ ] Get*
                * [ ] Put*
                * [ ] set_pipeline*
            
        * [ ] Resources*
        * [ ] ResourceTypes*
        * [ ] VarSource
        * [ ] Groups*

