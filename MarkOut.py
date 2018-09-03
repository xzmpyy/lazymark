class LazyMarkOut(object):
    def __init__(self):
        self.code_str = ''

    def bin_to_str(self):
        # 二进制转字符串
        for m in self.code_str:
            print(chr(int('0b' + str(m), 2)), end='')
