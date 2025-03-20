# tfds-docker
Docker image building and publishing for The Free Data Stack docker repo `tfds`.

[Docker repo]( https://hub.docker.com/repository/docker/tfds/spark-base/general)

[The Free Data Stack](https://github.com/jens-koster/the-free-data-stack)

The main purpose of having my own docker repo is to avoid downloading some random image with the same name, this would happen when you for some reason don't have a locally built one.

# building

    docker tag spark-base tfds/spark-base:1.0.n
    docker tag spark-base tfds/spark-base:1.0
    docker login -u xxxx
    # enter PAT as password
    docker push tfds/spark-base:1.0.0

# versioning
Let's think of this as stack versions. All images of a given minor version, like 1.2, should all be compatible with each other, there should be an image for all parts of the stack, so eventually we'll specify an env variable to spin up the entire stack. Like 1.0 always having the latest version of the 1.0 stack, all working flawlessly together...
The revision is used to track bug fix versions.
