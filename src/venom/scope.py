
class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.services = {}

    def get_requirement(self, req):
        if req in self.services:
            return self.services[req]
        if self.parent is not None:
            try:
                return parent.get_requirement(req)
            except KeyError as e:
                raise e
        raise KeyError("No such requirement: %s" % req)

    def has_requirement(self, req):
        if req in self.services:
            return True
        if self.parent is None:
            return False
        return self.parent.has_requirement(req)

    def set_requirements(self, service_map):
        self.services.update(service_map)

    def inject(self, req):
        sentinel = object()
        valuecache = {'_': sentinel}
        def getter():
            if valuecache['_'] is sentinel:
                valuecache['_'] = self.get_requirement(req)
            return valuecache['_']
        prop = property(fget=getter)
        return prop
