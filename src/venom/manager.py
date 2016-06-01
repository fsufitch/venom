from contextlib import contextmanager

from venom.scope import Scope

class DependencyManager:
    def __init__(self):
        self._root = Scope()
        self._scope = self._root

    @contextmanager
    def define(self, req, service):
        old_scope = self._scope
        new_scope = Scope(old_scope)
        new_scope.set_requirements({req: service})
        self._scope = new_scope
        yield
        self._scope =  old_scope

    @contextmanager
    def define_many(self, req_map):
        old_scope = self._scope
        new_scope = Scope(old_scope)
        new_scope.set_requirements(req_map)
        self._scope = new_scope
        yield
        self._scope =  old_scope

    @property
    def scope(self):
        return self._scope

    def inject(self, *spec_args, **spec_kwargs):
        def decorator(callable):
            def call(*args, **kwargs):
                inject_args = []
                for i, req in enumerate(spec_args):
                    if i < len(args): # Positional arg specified
                        arg = args[i]
                    elif self._scope.has_requirement(req):
                        arg = self._scope.get_requirement(req)
                    else:
                        raise TypeError("Positional argument #%d has no explicit or injected value" % (i+1))
                    inject_args.append(arg)

                inject_kwargs = {}
                for k,v in spec_kwargs.items():
                    inject_kwargs[k] = self._scope.get_requirement(v)
                inject_kwargs.update(kwargs)
                return callable(*inject_args, **inject_kwargs)
            return call
        return decorator

    def with_definitions(self, req_map):
        def decorator(callable):
            def call(*args, **kwargs):
                with self.define_many(req_map):
                    return callable(*args, **kwargs)
            return call
        return decorator
