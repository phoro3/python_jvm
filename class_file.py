class ClassFile:
    def __init__(self):
        # Add None to adjust index
        self.constant_pool = [None]
        self.interfaces = []
        self.fields = []
        self.methods = []
        self.attributes = []
    def add_constant_pool(self, constant_pool):
        self.constant_pool.append(constant_pool)
    def add_interfaces(self, interface):
        self.interfaces.append(interface)
    def add_field(self, field):
        self.fields.append(field)
    def add_method(self, method):
        self.methods.append(method)
    def add_attribute(self, attribute):
        self.attributes.append(attribute)
