from CodeWriter import Writer

writer = Writer()

with writer:
    with writer:
        raise Exception
