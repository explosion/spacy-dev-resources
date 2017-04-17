from contextlib import contextmanager

from fabtools.python import virtualenv


@contextmanager
def optional_venv(directory, local):
    if directory is None:
        yield
    else:
        with virtualenv(directory, local):
            yield
