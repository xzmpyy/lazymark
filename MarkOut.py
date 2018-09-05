from PIL import Image


class LazyMarkOut(object):
    def __init__(self, path):
        self.path = path

    # 提取像素
    def __get_pixel(self):
        image_file = Image.open(self.path.strip())
        image_pixel = list(image_file.getdata())
        image_len = len(image_pixel)
        r = []
        g = []
        b = []
        # print(type(image_pixel[0][0]))
        for i in range(image_len):
            r.append(image_pixel[i][0] % 2)
            g.append(image_pixel[i][1] % 2)
            b.append(image_pixel[i][2] % 2)
        # 返回图片像素(二进制列表)、长度
        return r, g, b, image_len

    @staticmethod
    def __bin_to_str(code_list):
        mark_str = ''
        # 二进制转字符串
        for m in code_list:
            mark_str += chr(int('0b' + str(m), 2))
        return mark_str.replace('@', ' ')

    # 提取细节
    @staticmethod
    def __process(r, g, b, image_len):
        # print(r)
        # 确定一个提取点
        start = 0
        while start < (image_len - 8):
            verify = ''
            for i in range(start, start+8):
                verify += str(g[i])
            if verify == '11001110':
                break
            else:
                start += 8
        # 每8位提取一次
        while start < (image_len - 8):
            confirm = ''
            for i in range(start, start + 8):
                confirm += str(g[i])
            # 判断该8位是否提取
            if confirm == '11001110':
                r_info = ''
                b_info = ''
                # 如果校验码无误，提取R，B信息
                for j in range(start, start + 8):
                    r_info += str(r[j])
                    b_info += str(b[j])
                r_info = r_info[4:8]

            start += 8

    # 解码主函数
    def decode(self):
        r, g, b, image_len = self.__get_pixel()
        self.__process(r, g, b, image_len)


if __name__ == '__main__':
    LazyMarkOut(r'C:\Users\zhangjie\Desktop\test_pic2.png').decode()
