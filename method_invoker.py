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

    def invoke(self):
        while self.program_counter < self.code_length:
            op_code = self.read_codes()
            self.instruction_set[op_code]()

    def _getstatic(self):
        index_byte1 = int.from_bytes(self.read_codes(), 'big')
        index_byte2 = int.from_bytes(self.read_codes(), 'big')
        index = index_byte1 << 8 | index_byte2
        print('getstatic')      

    def _ldc(self):
        index = int.from_bytes(self.read_codes(), 'big')
        print('ldc')      


    def _invokevirtual(self):
        index_byte1 = int.from_bytes(self.read_codes(), 'big')
        index_byte2 = int.from_bytes(self.read_codes(), 'big')
        print('invokevirtual')      

    def _return(self):
        print('return')


  