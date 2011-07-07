import contextlib


class BaseZMQTests(object):
    @contextlib.contextmanager
    # TODO support sockopts
    def create_socket(self, context, socket_type, **sockopts):
        with contextlib.closing(context.Context()) as ctx:
            socket = ctx.socket(socket_type)
        try:
            yield
        finally:
            with contextlib.closing(context.Context()) as ctx:
                #close socket
                ctx.term()
