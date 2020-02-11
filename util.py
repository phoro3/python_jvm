def convert_bytes_to_string(bytes_list):
    return ''.join(map(lambda x: x.decode('UTF-8'), bytes_list))