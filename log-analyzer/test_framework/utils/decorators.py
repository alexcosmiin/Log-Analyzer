from functools import wraps

def step(name=None, description=""):
    """Fixed step decorator without .start() call"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            step_name = name or func.__name__.replace('_', ' ').title()
            with self.add_step(step_name):
                return func(self, *args, **kwargs)
        return wrapper
    return decorator