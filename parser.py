from class_file import ClassFile

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
        self.attribute_parser = {
            'Code': lambda f: self.parse_code(f),
            'LineNumberTable': lambda f: self.parse_line_number_table(f),
            'SourceFile': lambda f: self.parse_source_file(f)
        }

    def parse(self, filename):
        self.class_file = ClassFile()
        with open(filename, "rb") as f:
            self.class_file.magic = f.read(4)
            self.class_file.minor_version = int.from_bytes(f.read(2), 'big')
            self.class_file.major_versio = int.from_bytes(f.read(2), 'big')
            self.class_file.constant_pool_count = int.from_bytes(f.read(2), 'big')
            for _ in range(self.class_file.constant_pool_count - 1):
                self.class_file.add_constant_pool(self.parse_constant_pool(f))
            self.class_file.access_flags = int.from_bytes(f.read(2), 'big')
            self.class_file.this_class = int.from_bytes(f.read(2), 'big')
            self.class_file.super_class = int.from_bytes(f.read(2), 'big')
            self.class_file.interfaces_count = int.from_bytes(f.read(2), 'big')
            for _ in range(self.class_file.interfaces_count):
                self.class_file.add_interfaces(int.from_bytes(f.read(2), 'big'))
            self.class_file.fields_count = int.from_bytes(f.read(2), 'big')
            for _ in range(self.class_file.fields_count):
                self.class_file.add_field(self.parse_field())
            self.class_file.methods_count = int.from_bytes(f.read(2), 'big')
            for _ in range(self.class_file.methods_count):
                self.class_file.add_method(self.parse_methods(f))
            self.class_file.attributes_count = int.from_bytes(f.read(2), 'big')
            for _ in range(self.class_file.attributes_count):
                self.class_file.add_attribute(self.parse_attributes(f))
        return self.class_file

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
            'name_and_type_index': int.from_bytes(file_object.read(2), 'big')
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

    def parse_field(self):
        # Not implemented because this isn't used in hello world
        pass

    def parse_methods(self, file_object):
        return {
            'access_flags': int.from_bytes(file_object.read(2), 'big'),
            'name_index': int.from_bytes(file_object.read(2), 'big'),
            'descriptor_index': int.from_bytes(file_object.read(2), 'big'),
            'attributes_count': int.from_bytes(file_object.read(2), 'big'),
            'attributes': self.parse_attributes(file_object)
        }

    def parse_attributes(self, file_object):
        attribute_name_index = int.from_bytes(file_object.read(2), 'big')
        attribute_length = int.from_bytes(file_object.read(4), 'big')
        attribute_name = self.class_file.constant_pool[attribute_name_index]['bytes']
        attribute_name = ''.join(map(lambda x: x.decode('UTF-8'), attribute_name))
        attributes = {
            'attribute_name_index': attribute_name_index,
            'attribute_length': attribute_length,
        }
        attributes.update(self.attribute_parser[attribute_name](file_object))
        return attributes

    def parse_code(self, file_object):
        max_stack = int.from_bytes(file_object.read(2), 'big')
        max_locals = int.from_bytes(file_object.read(2), 'big')
        code_length = int.from_bytes(file_object.read(4), 'big')
        codes = [file_object.read(1) for _ in range(code_length)]
        exception_table_length = int.from_bytes(file_object.read(2), 'big')
        exception_table = [file_object.read(1) for _ in range(exception_table_length)]
        attributes_count = int.from_bytes(file_object.read(2), 'big')
        attributes = [self.parse_attributes(file_object) for _ in range(attributes_count)]

        return {
            'max_stack': max_stack,
            'max_locals': max_locals,
            'code_length': code_length,
            'codes': codes,
            'exception_table_length': exception_table_length,
            'exception_table': exception_table,
            'attributes_count': attributes_count,
            'attributes': attributes
        }

    def parse_exception_table(self, file_object):
        return {
            'start_pc': int.from_bytes(file_object.read(2), 'big'),
            'end_pc': int.from_bytes(file_object.read(2), 'big'),
            'handler_pc': int.from_bytes(file_object.read(2), 'big'),
            'catch_type': int.from_bytes(file_object.read(2), 'big')
        }

    def parse_line_number_table(self, file_object):
        line_number_table_length = int.from_bytes(file_object.read(2), 'big')
        line_number_table = [
            {
            'start_pc': int.from_bytes(file_object.read(2), 'big'),
            'line_number': int.from_bytes(file_object.read(2), 'big')
            }
            for _ in range(line_number_table_length)
        ]
        return {
            'line_number_table_length': line_number_table_length,
            'line_number_table': line_number_table
        }

    def parse_source_file(self, file_object):
        return {
            'sourcefile_index': int.from_bytes(file_object.read(2), 'big')
        }