from functools import wraps

def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            retval = func(*args, **kwargs)
            return retval
        except Exception: # TODO: as e:
            return {
                "status": 503,
                "description": "Server encountered unhandled exception."
                # TODO: Include exception message if debug mode enabled
                "error": True
            }
