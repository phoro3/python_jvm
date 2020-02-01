import sys
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

CAFABABE = b'\xca\xfe\xba\xbe'

def is_class_file(magic):
    return magic == CAFABABE

class Parser():
    constant_pool_tags = {
        'CONSTANT_Utf8': 1,
        'CONSTANT_Class': 7,
        'CONSTANT_String': 8,
        'CONSTANT_Fieldref': 9,
        'CONSTANT_Methodref': 10,
        'CONSTANT_NameAndType': 12
    }
    def __init__(self):
        self.constant_parser = {
            self.constant_pool_tags['CONSTANT_Utf8']: lambda f: self.parse_utf8(f),
            self.constant_pool_tags['CONSTANT_Class']: lambda f: self.parse_class(f),
            self.constant_pool_tags['CONSTANT_String']: lambda f: self.parse_string(f),
            self.constant_pool_tags['CONSTANT_Fieldref']: lambda f: self.parse_field_ref(f),
            self.constant_pool_tags['CONSTANT_Methodref']: lambda f: self.parse_method_ref(f),
            self.constant_pool_tags['CONSTANT_NameAndType']: lambda f: self.parse_name_and_type(f) 
        }

    def main(self, filename):
        class_file = ClassFile()
        with open(filename, "rb") as f:
            class_file.set_magic(f.read(4))
            class_file.set_minor_version(int.from_bytes(f.read(2), 'big'))
            class_file.set_major_version(int.from_bytes(f.read(2), 'big'))
            class_file.set_constant_pool_count(int.from_bytes(f.read(2), 'big'))
            for _ in range(class_file.constant_pool_count - 1):
                class_file.add_constant_pool(self.parse_constant_pool(f))
        return class_file
 
    def parse_constant_pool(self, file_object):
        tag = int.from_bytes(file_object.read(1), 'big')
        return self.constant_parser[tag](file_object)

    def parse_utf8(self, file_object):
        length = int.from_bytes(file_object.read(2), 'big')
        bytes_list = [file_object.read(1) for _ in range(length)]
        return {
            'tag': self.constant_pool_tags['CONSTANT_Utf8'],
            'length': length,
            'bytes': bytes_list
        }

    def parse_class(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_Class'],
            'name_index': int.from_bytes(file_object.read(2), 'big')
        }

    def parse_string(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_String'],
            'string_index': int.from_bytes(file_object.read(2), 'big')
        }
           
    def parse_field_ref(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_Fieldref'],
            'class_index': int.from_bytes(file_object.read(2), 'big'),
            'name_ant_type_index': int.from_bytes(file_object.read(2), 'big')
        }

    def parse_method_ref(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_Methodref'],
            'class_index': int.from_bytes(file_object.read(2), 'big'),
            'name_and_type_index': int.from_bytes(file_object.read(2), 'big')
        }
    
    def parse_name_and_type(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_NameAndType'],
            'name_index': int.from_bytes(file_object.read(2), 'big'),
            'descriptor_index': int.from_bytes(file_object.read(2), 'big')
        }

if __name__ == "__main__":
    filename = sys.argv[1]
    parser = Parser()
    print(parser.main(filename).__dict__)
    