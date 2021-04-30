from views import ping, task


def setup_routes(app):
    app.router.add_get('/ping', ping)

    app.router.add_get('/task', task)
