import sys

CAFABABE = b'\xca\xfe\xba\xbe'

def is_class_file(magic):
    return magic == CAFABABE

def main(filename):
    with open(filename, "rb") as f:
        if not is_class_file(f.read(4)):
            return

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
    