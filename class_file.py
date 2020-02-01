class ClassFile:
    def __init__(self):
        self.constant_pool = []
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