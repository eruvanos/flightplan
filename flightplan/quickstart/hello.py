from flightplan.render import *

pipe = Pipeline(
    resource_types=[],
    resources=[],
    jobs=[
        Job(
            name="job-hello-world",
            public=True,
            plan=[
                Task(
                    task="hello-world",
                    config=TaskConfig(
                        platform="linux",
                        image_resource=ImageResource(
                            type="docker-image",
                            source=dict(repository="busybox", tag="latest"),
                        ),
                        run=Command(path="echo", args=["hello world"]),
                        inputs=[],
                        outputs=[],
                    ),
                )
            ],
        )
    ],
)

if __name__ == "__main__":
    print(pipe.synth())
