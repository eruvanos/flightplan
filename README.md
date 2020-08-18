

# Flight plan - Plan your Concourse Pipeline with ease

AWS CDK like tool to code Concourse pipelines, (with autocompletion and validation.)


## Planed features

* Generate pipeline YAML from cli (or Python)
* Set pipeline from cli
* Predefined code constructs to simplify common pipelines

## Setup 

```bash
pip install git+https://github.com/eruvanos/flightplan.git
```


## Usage

### Quickstart
Generate a basic pipeline example.

```bash
fp quickstart
```

### Import existing pipeline file
Convert a pipeline yaml and render a flightplan `.py` file.

```bash
fp import <src.yaml> <target.py>
```

### Import existing pipeline from fly
Convert a pipeline from fly and render a flightplan `.py` file.

```bash
fp get <fly_target> <pipeline_name> <target.py>
```


### Synthesize yaml from flightplan `.py` file

```bash
fp synth <src.py> <target.yaml>
```

### Direct Fly Set Pipeline

```bash
fp set <fly-target> <pipeline_name> <src.py>
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
