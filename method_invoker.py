from util import convert_bytes_to_string
import importlib

class MethodInvoker:
    def __init__(self, constant_pool, method_info):
        self.instruction_set = {
            b'\xb2': self._getstatic,
            b'\xb6': self._invokevirtual,
            b'\x12': self._ldc,
            b'\xb1': self._return
        }
        self.constant_pool = constant_pool
        self.code_length = method_info['attributes']['code_length']
        self.codes = method_info['attributes']['codes']
        self.stack = []
        self.program_counter = 0

    def read_codes(self):
        data = self.codes[self.program_counter]
        self.program_counter += 1
        return data

    def get_class_name(self, class_index):
        return convert_bytes_to_string(
            self.constant_pool[self.constant_pool[class_index]['name_index']]['bytes']
            )

    def get_name_and_type(self, name_and_type_index):
        name_and_type_info = self.constant_pool[name_and_type_index]
        name_index = name_and_type_info['name_index']
        descriptor_index = name_and_type_info['descriptor_index']
        return {
            'name': convert_bytes_to_string(self.constant_pool[name_index]['bytes']),
            'type': convert_bytes_to_string(self.constant_pool[descriptor_index]['bytes'])
        }

    def invoke(self):
        while self.program_counter < self.code_length:
            op_code = self.read_codes()
            self.instruction_set[op_code]()

    def _getstatic(self):
        index_byte1 = int.from_bytes(self.read_codes(), 'big')
        index_byte2 = int.from_bytes(self.read_codes(), 'big')
        index = index_byte1 << 8 | index_byte2

        field_ref = self.constant_pool[index]
        class_name = self.get_class_name(field_ref['class_index'])
        name_and_type_index = field_ref['name_and_type_index']
        name_and_type = self.get_name_and_type(name_and_type_index)

        # convert to python module path
        class_name = class_name.replace('/', '.')
        target_class = importlib.import_module(class_name)
        target_field = getattr(target_class, name_and_type['name'])
        self.stack.append(target_field)

    def _ldc(self):
        index = int.from_bytes(self.read_codes(), 'big')
        # TODO: implement other than string
        string = convert_bytes_to_string(
            self.constant_pool[self.constant_pool[index]['string_index']]['bytes']
        )
        self.stack.append(string)

    def _invokevirtual(self):
        index_byte1 = int.from_bytes(self.read_codes(), 'big')
        index_byte2 = int.from_bytes(self.read_codes(), 'big')
        index = index_byte1 << 8 | index_byte2

        # get method name from constant_pool
        method_ref = self.constant_pool[index]
        name_and_type = self.get_name_and_type(method_ref['name_and_type_index'])
        method_name = name_and_type['name']

        # get args from stack
        arg_types = name_and_type['type']
        arg_num = len(arg_types.split(';')) - 1
        args = [self.stack.pop() for _ in range(arg_num)]
        args.reverse()

        # call method
        target_method = getattr(self.stack.pop(), method_name)
        target_method(*args)

    def _return(self):
        pass

