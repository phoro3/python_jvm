from class_file import ClassFile
from util import convert_bytes_to_int

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
            self.class_file.minor_version = convert_bytes_to_int(f.read(2))
            self.class_file.major_versio =convert_bytes_to_int(f.read(2))
            self.class_file.constant_pool_count =convert_bytes_to_int(f.read(2))
            for _ in range(self.class_file.constant_pool_count - 1):
                self.class_file.add_constant_pool(self.parse_constant_pool(f))
            self.class_file.access_flags =convert_bytes_to_int(f.read(2))
            self.class_file.this_class =convert_bytes_to_int(f.read(2))
            self.class_file.super_class =convert_bytes_to_int(f.read(2))
            self.class_file.interfaces_count =convert_bytes_to_int(f.read(2))
            for _ in range(self.class_file.interfaces_count):
                self.class_file.add_interfaces(int.from_bytes(f.read(2)))
            self.class_file.fields_count =convert_bytes_to_int(f.read(2))
            for _ in range(self.class_file.fields_count):
                self.class_file.add_field(self.parse_field())
            self.class_file.methods_count =convert_bytes_to_int(f.read(2))
            for _ in range(self.class_file.methods_count):
                self.class_file.add_method(self.parse_methods(f))
            self.class_file.attributes_count =convert_bytes_to_int(f.read(2))
            for _ in range(self.class_file.attributes_count):
                self.class_file.add_attribute(self.parse_attributes(f))
        return self.class_file

    def parse_constant_pool(self, file_object):
        tag =convert_bytes_to_int(file_object.read(1))
        return self.constant_parser[tag](file_object)

    def parse_utf8(self, file_object):
        length =convert_bytes_to_int(file_object.read(2))
        bytes_list = [file_object.read(1) for _ in range(length)]
        return {
            'tag': self.constant_pool_tags['CONSTANT_Utf8'],
            'length': length,
            'bytes': bytes_list
        }

    def parse_class(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_Class'],
            'name_index':convert_bytes_to_int(file_object.read(2))
        }

    def parse_string(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_String'],
            'string_index':convert_bytes_to_int(file_object.read(2))
        }

    def parse_field_ref(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_Fieldref'],
            'class_index':convert_bytes_to_int(file_object.read(2)),
            'name_and_type_index':convert_bytes_to_int(file_object.read(2))
        }

    def parse_method_ref(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_Methodref'],
            'class_index':convert_bytes_to_int(file_object.read(2)),
            'name_and_type_index':convert_bytes_to_int(file_object.read(2))
        }

    def parse_name_and_type(self, file_object):
        return {
            'tag': self.constant_pool_tags['CONSTANT_NameAndType'],
            'name_index':convert_bytes_to_int(file_object.read(2)),
            'descriptor_index':convert_bytes_to_int(file_object.read(2))
        }

    def parse_field(self):
        # Not implemented because this isn't used in hello world
        pass

    def parse_methods(self, file_object):
        return {
            'access_flags':convert_bytes_to_int(file_object.read(2)),
            'name_index':convert_bytes_to_int(file_object.read(2)),
            'descriptor_index':convert_bytes_to_int(file_object.read(2)),
            'attributes_count':convert_bytes_to_int(file_object.read(2)),
            'attributes': self.parse_attributes(file_object)
        }

    def parse_attributes(self, file_object):
        attribute_name_index =convert_bytes_to_int(file_object.read(2))
        attribute_length =convert_bytes_to_int(file_object.read(4))
        attribute_name = self.class_file.constant_pool[attribute_name_index]['bytes']
        attribute_name = ''.join(map(lambda x: x.decode('UTF-8'), attribute_name))
        attributes = {
            'attribute_name_index': attribute_name_index,
            'attribute_length': attribute_length,
        }
        attributes.update(self.attribute_parser[attribute_name](file_object))
        return attributes

    def parse_code(self, file_object):
        max_stack =convert_bytes_to_int(file_object.read(2))
        max_locals =convert_bytes_to_int(file_object.read(2))
        code_length =convert_bytes_to_int(file_object.read(4))
        codes = [file_object.read(1) for _ in range(code_length)]
        exception_table_length =convert_bytes_to_int(file_object.read(2))
        exception_table = [file_object.read(1) for _ in range(exception_table_length)]
        attributes_count =convert_bytes_to_int(file_object.read(2))
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
            'start_pc':convert_bytes_to_int(file_object.read(2)),
            'end_pc':convert_bytes_to_int(file_object.read(2)),
            'handler_pc':convert_bytes_to_int(file_object.read(2)),
            'catch_type':convert_bytes_to_int(file_object.read(2))
        }

    def parse_line_number_table(self, file_object):
        line_number_table_length =convert_bytes_to_int(file_object.read(2))
        line_number_table = [
            {
            'start_pc':convert_bytes_to_int(file_object.read(2)),
            'line_number':convert_bytes_to_int(file_object.read(2))
            }
            for _ in range(line_number_table_length)
        ]
        return {
            'line_number_table_length': line_number_table_length,
            'line_number_table': line_number_table
        }

    def parse_source_file(self, file_object):
        return {
            'sourcefile_index':convert_bytes_to_int(file_object.read(2))
        }