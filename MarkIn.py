import os
from PIL import Image
import math


class LazyMarkIn(object):
    # 图片路径，嵌入水印码，图片保存名，保存路径，是否删除原图
    def __init__(self, path, code_str, pic_name, save_path, is_delete=False):
        self.path = path
        self.code_str = code_str.replace(' ', '@')
        self.is_delete = is_delete
        # r校验码
        self.r_check_list = [1, 1, 0, 1]
        # g校验码
        self.g_check_list = [1, 1, 0, 0, 1, 1, 1, 0]
        self.pic_name = save_path + '\\' + pic_name + '.png'

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
        # 获取像素最低有效位为0
        self.__get_zero(image_pixel, image_zero)
        return image_zero, image_len

    # 水印嵌入
    def __processing(self, image, image_len):
        code_len = len(self.code_str)
        # 循环嵌入次数
        loop_num = int(math.floor(image_len / (code_len * 8)))
        # image分为RGB三个列表分别处理
        r = []
        g = []
        b = []
        for pixel in image:
            r.append(pixel[0])
            g.append(pixel[1])
            b.append(pixel[2])
        # 顺序码列表
        order = list(range(code_len))
        for num in range(code_len):
            # 顺序码转4位二进制，高位补零
            order[num] = '{:04b}'.format(order[num])
        # 嵌入
        # 最外层循环，整个图片重复嵌入loop_num次水印
        for outside_loop in range(loop_num):
            # 一次完整嵌入起始点
            index_start = outside_loop * (code_len * 8)
            # 中间层循环，一次需要嵌入code_len个字符
            for middle_loop in range(code_len):
                # 当前嵌入字符起始点
                index_char = index_start + middle_loop * 8
                # 最里层循环，一个字符嵌入8位像素点
                for inside_loop in range(8):
                    # 当前操作像素点
                    pixel_now = index_char + inside_loop
                    # R点顺序码嵌入,前四位固定，后四位为顺序码
                    if inside_loop < 4:
                        if self.r_check_list[inside_loop] == 1:
                            r[pixel_now] += 1
                    else:
                        if order[middle_loop][inside_loop-4] == '1':
                            r[pixel_now] += 1
                    # G点校验码嵌入
                    if self.g_check_list[inside_loop] == 1:
                        g[pixel_now] += 1
                    # B点水印信息嵌入
                    if self.code_str[middle_loop][inside_loop] == '1':
                        b[pixel_now] += 1
        image_done = []
        for done_index in range(image_len):
            image_done.append((r[done_index], g[done_index], b[done_index]))
        # 创建相同大小的图片副本
        deal_image = Image.new(Image.open(self.path.strip()).mode, Image.open(self.path.strip()).size)
        deal_image.putdata(image_done)
        deal_image.save(self.pic_name)

    def water_mark_in(self):
        self.__code_to_bin()
        image_pixel, image_len = self.__pixel_get()
        # 校验图片是否足够嵌入水印
        if (len(self.code_str) * 8) > (image_len / 10):
            # 返回101 表示图片过小
            return 101
        self.__processing(image_pixel, image_len)
        if self.is_delete:
            os.remove(os.path.join(self.path))


if __name__ == '__main__':
    LM = LazyMarkIn('D:\design\watermark\image\pyy.jpg', 'This is a test', 'test_pic', 'C:\\Users\zhangjie\Desktop')
    LM.water_mark_in()


