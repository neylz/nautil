

from nautil.core.artifact import Artifact


def action(method_name: str):
    def decorator(plugin_func):
        def chainable_method(self, *args, **kwargs):
            step_execution = plugin_func(self, *args, **kwargs)
            if callable(step_execution):
                step_execution(self.path)
            return self
        
        setattr(Artifact, method_name, chainable_method)
        return plugin_func
    return decorator
