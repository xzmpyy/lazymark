from PIL import Image


class LazyMarkIn(object):
    def __init__(self, path, code_str, is_delete=False):
        self.path = path
        self.code_str = code_str
        self.is_delete = is_delete
        # r校验码
        self.r_check_list = [1, 1, 0, 1]
        # g校验码
        self.g_check_list = [1, 1, 0, 0, 1, 1, 1, 0]

    # 水印码转二进制
    def __code_to_bin(self):
        # 字符串拆分成列表
        code_list = []
        for i in self.code_str:
            code_list.append(i)
        self.code_str = code_list
        # 字符转二进制(8位补0)
        for j in range(len(self.code_str)):
            self.code_str[j] = '0' + format(ord(self.code_str[j]), 'b')
        print(self.code_str)

    # 获取最低有效位为0的图像二进制像素列表
    @staticmethod
    def __get_zero(image, image_list):
        for i in image:
            a = i[0] >> 1 << 1
            b = i[1] >> 1 << 1
            c = i[2] >> 1 << 1
            d = (a, b, c)
            image_list.append(d)

    # 提取图像像素
    def __pixel_get(self):
        image_file = Image.open(self.path.strip())
        image_pixel = list(image_file.getdata())
        image_len = len(image_pixel)
        # 返回图片像素、长度
        image_zero = []
        # 获取像素最低有效位为0的多进程
        self.__get_zero(image_pixel, image_zero)
        return image_zero, image_len

    # 水印嵌入
    def __processing(self, image, image_len):
        code_len = len(self.code_str)
        # 循环嵌入次数
        loop_num = image_len / (code_len * 8)
        # image分为RGB三个列表分别处理
        r = []
        g = []
        b = []
        for pixel in image:
            r.append(pixel[0])
            g.append(pixel[0])
            b.append(pixel[0])
        # 顺序码列表
        order = list(range(code_len))
        for num in range(code_len):
            order[num] = bin(order[num])
        print(order)

    def water_mark_in(self):
        self.__code_to_bin()
        image_pixel, image_len = self.__pixel_get()
        # 校验图片是否足够嵌入水印
        if (len(self.code_str) * 8) > (image_len / 10):
            # 返回101 表示图片过小
            return 101
        self.__processing(image_pixel, image_len)


if __name__ == '__main__':
    LazyMarkIn('D:\design\watermark\image\pyy.jpg', 'This is a test').water_mark_in()
