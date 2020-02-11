import sys
from parser import Parser
from method_invoker import MethodInvoker
from util import convert_bytes_to_string

CAFABABE = b'\xca\xfe\xba\xbe'

def is_class_file(magic):
    return magic == CAFABABE

def find_main_codes(class_file):
    for method in class_file.methods:
        method_name = convert_bytes_to_string(
            class_file.constant_pool[method['name_index']]['bytes']
        )
        if method_name == 'main':
            return method
    raise Exception



if __name__ == "__main__":
    filename = sys.argv[1]
    parser = Parser()
    class_file = parser.main(filename)

    for k, v in class_file.__dict__.items():
        print(k)
        print(v)
        print()

    constant_pool = class_file.constant_pool
    main_method_info = find_main_codes(class_file)
    method_invoker = MethodInvoker(constant_pool, main_method_info)
    method_invoker.invoke()
