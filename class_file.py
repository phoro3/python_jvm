class ClassFile:
    def __init__(self):
        # Add None to adjust index
        self.constant_pool = [None]
        self.interfaces = []
        self.fields = []
        self.methods = []
        self.attributes = []
    def set_magic(self, magic):
        self.magic = magic
    def set_minor_version(self, minor_version):
        self.minor_version = minor_version
    def set_major_version(self, major_version):
        self.major_version = major_version
    def set_constant_pool_count(self, constant_pool_count):
        self.constant_pool_count = constant_pool_count
    def add_constant_pool(self, constant_pool):
        self.constant_pool.append(constant_pool)
    def set_access_flags(self, access_flags):
        self.access_flags = access_flags
    def set_this_class(self, this_class):
        self.this_class = this_class
    def set_super_class(self, super_class):
        self.super_class = super_class
    def set_interfaces_count(self, interfaces_count):
        self.interfaces_count = interfaces_count
    def add_interfaces(self, interface):
        self.interfaces.append(interface)
    def set_fields_count(self, fields_count):
        self.fields_count = fields_count
    def add_field(self, field):
        self.fields.append(field)
    def set_methods_count(self, methods_count):
        self.methods_count = methods_count
    def add_method(self, method):
        self.methods.append(method)
    def set_attirbutes_count(self, attributes_count):
        self.attributes_count = attributes_count
    def add_attribute(self, attribute):
        self.attributes.append(attribute)
