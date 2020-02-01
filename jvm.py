import sys
from parser import Parser

CAFABABE = b'\xca\xfe\xba\xbe'

def is_class_file(magic):
    return magic == CAFABABE

if __name__ == "__main__":
    filename = sys.argv[1]
    parser = Parser()
    print(parser.main(filename).__dict__)
    