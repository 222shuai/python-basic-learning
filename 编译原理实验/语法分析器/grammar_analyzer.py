import sys
import tkinter
from tkinter import filedialog


class Stack(object):  # 堆栈类
    def __init__(self):
        self.__list = []

    def push(self, item):
        self.__list.append(item)

    def pop(self):
        return self.__list.pop()

    def top(self):
        if self.__list:
            return self.__list[-1]
        return None

    def is_empty(self):
        return self.__list == []

    def size(self):
        return len(self.__list)

    def show(self):
        return ''.join(self.__list)


def modify_left_recursion(exp_key, exp_value, now_item, result):
    if exp_key + "'" not in result:
        result[exp_key + "'"] = {'right': [], 'terminator': []}
    for item in exp_value['right'] + exp_value['terminator']:
        if item != now_item and item + exp_key + "'" not in result[exp_key]['right']:  # 替换需要跳过当前的串
            result[exp_key]['right'].append(item + exp_key + "'")
    if now_item.replace(exp_key, '', 1) + exp_key + "'" not in result[exp_key + "'"]['right']:
        result[exp_key + "'"]['right'].append(now_item.replace(exp_key, '', 1) + exp_key + "'")
    if '@' not in result[exp_key + "'"]['terminator']:
        result[exp_key + "'"]['terminator'].append('@')
    return result


def get_replace_result(exp_value, length, result):  # 获取替换后的产生式列表
    replace_list = []  # 记录被替换的串,后期需要移除
    replace_flag = False  # 是否被替换的标志
    for item in exp_value['right'][:length]:
        value1 = value2 = item
        for pre_key, pre_value in result.items():
            for pre_item in pre_value['right']:
                value_pre = value1
                value1 = value1.replace(pre_key, pre_item)  # 用非终结串替换后也是非终结串
                if value1 != value_pre:
                    replace_flag = True  # 标志是否被替换
                    if value_pre not in replace_list:
                        replace_list.append(value_pre)  # 加入待删除列表
                    exp_value['right'].append(value1)
            for pre_item in pre_value['terminator']:
                value_pre = value2
                value2 = value2.replace(pre_key, pre_item)
                if value2 != value_pre:
                    replace_flag = True  # 标志是否被替换
                    if value_pre not in replace_list:
                        replace_list.append(value_pre)
                    if (value2.islower() or value2 == '@') and value2 not in exp_value['terminator']:  # 全小写说明为终结串
                        exp_value['terminator'].append(value2)
                        value2 = value1  # 如果当前value2已为终结串，则应将其更新为当前value1的值(当前阶段的非终结串)
                    elif not (value2.islower() or value2 == '@' or value2 in exp_value['right']):
                        exp_value['right'].append(value2)
    if replace_flag:
        for remove_item in replace_list:
            if remove_item in exp_value['right']:
                exp_value['right'].remove(remove_item)

    return exp_value


def remove_left_recursion(grammar):
    result = {}  # 用于存储返回结果
    exp_index = 0  # 用于存储当前处理的产生式索引
    keys = list(grammar.keys())  # 由于字典不能直接切片，因此对其所有键构成的列表进行切片，然后生成一个临时的子字典
    for exp_key, exp_value in grammar.items():
        right_length = len(exp_value['right'])  # 记录原产生式右部非终结串的长度(1个长度代表有一个右部)
        exp_index = keys.index(exp_key)
        exp_value = get_replace_result(exp_value, right_length, result)
        left_recursion_flag = False  # 标志是否存在左递归，不存在左递归则要专门对右部终结串进行处理
        if exp_key not in result:
            result[exp_key] = {'right': [], 'terminator': []}
        for item in exp_value['right']:
            if item[0] == exp_key:
                left_recursion_flag = True
                result.update(modify_left_recursion(exp_key, exp_value, item, result))
        if not left_recursion_flag:  # 没有左递归：
            for item in exp_value['right']:
                if item not in result[exp_key]['right']:
                    result[exp_key]['right'].append(item)
            result[exp_key]['terminator'] = list(set(result[exp_key]['terminator'] + exp_value['terminator']))

    del grammar  # 彻底删除grammar变量，释放内存，提高性能
    return result


def error_exit(error_tip):  # 错误处理方法
    printRed(error_tip)  # 高亮打印报错信息
    sys.exit(0)  # 正常退出程序


def printRed(mess):  # 让控制台输出红色高亮字体
    print(f'\033[1;31;40m{mess}\033[0m')


def select_file():
    root = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
    root.withdraw()  # 将Tkinter.Tk()实例隐藏
    file_path = tkinter.filedialog.askopenfilename(title='选择一个文件', filetypes=[('所有文件', '.*'), ('文本文件', '.txt')])
    if file_path != '':
        print("您选择的文件是：" + file_path)
        return file_path
    else:
        print("您没有选择任何文件")
        return ''


def main():
    grammar = {}
    print("请选择文件路径：")
    Filepath = select_file()
    if Filepath != '':
        for line in open(Filepath, 'r', encoding='gbk'):
            line = line.replace('\n', '')
            if len(line.split('->')) > 2:
                error_exit('同一行不能出现多个产生式！')
            else:
                left = line.split('->')[0]  # 提取左部
                right = line.split('->')[1].split('|')  # 提取右部
                right_terminator = []
                for item in right:
                    if item.islower() or item == '@':  # 全小写说明为终结串
                        right_terminator.append(item)
                for item in right_terminator:
                    right.remove(item)  # 默认right只存放终结串之外的产生式
                # 以字典形式存放产生式，键为产生式左部非终结符，值为右部可选列表
                grammar[left] = {'right': right, 'terminator': right_terminator}
    grammar = remove_left_recursion(grammar)  # 消除左递归
    print(grammar)
    for Vn, value in grammar.items():
        for Vt in value['right'] + value['terminator']:
            print(Vn + '->' + Vt)


if __name__ == '__main__':
    main()
