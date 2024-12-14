from werkzeug.middleware.dispatcher import DispatcherMiddleware
from wsgi import application  # Import from the WSGI file

if __name__ == "__main__":
    from werkzeug.serving import run_simple

    run_simple("localhost", 5000, application)
