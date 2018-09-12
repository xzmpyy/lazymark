from PIL import Image
import os
from collections import Counter


class LazyMarkOut(object):
    def __init__(self, path, is_delete=False):
        self.path = path
        self.is_delete = is_delete

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
        # 存储RB值列表，列表第一位为R
        r_b_list = []
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
                # print(r_info)
                # 第一次时直接存储
                if not r_b_list:
                    r_b_list.append([r_info, b_info])
                else:
                    add_flag = True
                    for child_index in range(len(r_b_list)):
                        # 该顺序位已在其中
                        if r_b_list[child_index][0] == r_info:
                            r_b_list[child_index].append(b_info)
                            add_flag = False
                            break
                    # 该顺序为不在其中，需添加顺序位
                    if add_flag:
                        r_b_list.append([r_info, b_info])
            start += 8
        # 列表顺序码转10进制再排序
        for order_index in range(len(r_b_list)):
            # 字符串转整型
            r_b_list[order_index][0] = int(r_b_list[order_index][0], 2)
        # 计算结果列表平均值，低于平均值的舍弃
        average = 0
        for list_len in r_b_list:
            average += len(list_len)
        average = average / len(r_b_list)
        # 统计结果字典
        count_dic = {}
        for count in r_b_list:
            if len(count) < average:
                continue
            else:
                # 取出现频率最高的值
                max_code = Counter(count[1:]).most_common(1)[0][0]
                count_dic[count[0]] = max_code
        # 按顺序形成最终列表
        deal_list = []
        # print(count_dic)
        for num in range(len(count_dic)):
            if num in count_dic:
                deal_list.append(count_dic[num])
        return deal_list

    # 解码主函数
    def decode(self):
        r, g, b, image_len = self.__get_pixel()
        deal_list = self.__process(r, g, b, image_len)
        # 无解码内容时，返回400错误类型
        if not deal_list:
            return 400
        code_str = self.__bin_to_str(deal_list)
        if self.is_delete:
            os.remove(self.path)
        # print(code_str)
        return code_str


if __name__ == '__main__':
    LazyMarkOut(r'C:\Users\zhangjie\Desktop\pyy1536649939.png').decode()
