import zmqpy

def pytest_funcarg__context(request):
    ctx = zmqpy.Context()

    def close_ctx():
        if not ctx.closed:
            ctx.term()

    request.addfinalizer(close_ctx)
    return ctx
