

# Flight plan - Plan your Concourse Pipeline with ease

AWS CDK like tool to code Concourse pipelines, (with autocompletion and validation.)


## Planed features

* Generate pipeline YAML from cli (or Python)
* Set pipeline from cli
* Predefined code constructs to simplify common pipelines


## Usage

### Import existing pipeline file
Convert a pipeline yaml and render a flightplan `.py` file.

```bash
python cli.py import <src.yaml> <target.py>
```

### Synthesize yaml from flightplan `.py` file

```bash
python cli.py synth <src.py> <target.yaml>
```

### Direct Fly Set Pipeline

```bash
python cli.py set <fly-target> <pipeline_name> <src.py>
```



## Examples

Constructor definitions:
```python
from flightplan.render import *

Pipeline(
    jobs=[
        Job(
            name='job-hello-world',
            public=True,
            plan=[
                Task(
                    task='hello-world',
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



## Backlog
