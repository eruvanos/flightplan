

# Flight plan - Plan your Concourse Pipeline with ease

AWS CDK like tool to code Concourse pipelines, (with autocompletion and validation.)

## Why not stick with YAML

Writing YAML files feels not as heavy as XML, 
but still lacks the comfort of autocompletion and some kind of structuring 
(Beside anchors or tools like [YTT](https://get-ytt.io/)).

The vision of Flightplan does not stop with replacing YAML, the real benefit
starts with component libraries, which ease the setup of pipelines.

Furthermore these components can be updated, which make all improvements 
automatically available to all pipelines.  

## Features

* Convert:
  * YAML -> Python
  * Python -> YAML
* Fly integration
  * Set pipeline
  * Get pipeline
* Shiped examples
  * Hello world
  * more to come

## Upcoming

* Provide high level components that handle common use cases

## Setup 

Flightplan requires Python 3.8 and higher.

### Install FlightPlan

```bash
pip3 install git+https://github.com/eruvanos/flightplan.git
```

## Usage

If you start with Flightplan it is recommended to have a look on the quickstart examples, 
which are shipped within the cli.

If you want to migrate an existing pipeline you can use 
 * `fp import` - to convert YAML to Python
 * `fp get ...` - to get and convert a running pipeline 

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

> Static and dynamic vars will be imported as `Var(str)`, if the type of the field is limited to an int or Enum type.

### Synthesize yaml from flightplan `.py` file

```bash
fp synth <src.py> <target.yaml>
```

### Direct Fly Set Pipeline

```bash
fp set <fly-target> <pipeline_name> <src.py>
```



## Examples

Quickstart hello world example:

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
                            source=dict(
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
