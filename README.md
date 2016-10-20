# flask_nsfw

To ensure a reproducible execution environment for this app, development has
proceeded in Docker from the start. The base image used is `caffe:cpu`, which
can take some time to build if you don't have it cached.

The `scripts/` directory contains a Bash script, `flask_nsfw`, which saves you
the headache of having to remember the exact Docker CLI invocations that start
the app container. Available commands are `build`, `test`, `run`, and `shell`.

First, run:

  $ flask_nsfw build

This will prepare a Docker image tagged `flask_nsfw`. If this label doesn't
suit you, edit the `NAME` variable in `scripts/flask_nsfw` before building.

To test the image:

  $ flask_nsfw test

The contents of the `src/` directory are copied into the image during `build`.
If you make any changes to the source, either rebuild the image, or, preferably,
by passing `dev` as first argument, for example:

  $ flask_nsfw dev run

The above command will start Flask with the `src/` directory mounted as a Docker
volume. Thus any changes made to the source will be immediately reflected inside
the container. Therefore, it is recommended to start the container in production
via:

  $ flask_nsfw run

To get a Bash prompt in the container, use:

  $ flask_nsfw shell

Again, if you don't pass `dev` as first argument, you'll be stuck with the
original version of the app code.
