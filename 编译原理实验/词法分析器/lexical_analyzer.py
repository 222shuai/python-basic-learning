import sys
import tkinter
from tkinter import filedialog

# 运算符(可手动扩展)
Operation = ['*', '-', '/', '=', '>', '<', '>=', '==', '<=', '%', '+', '+=', '-=', '*=', '/=', '&', '|', '!', '!=', ]
# 界符(可手动扩展)
Delimiter = ['(', ')', '[', ']', ',', ';', '.', '{', '}', '<_', '>_', '"', "'"]  # <_,>_区分运算符中的<、>
# 关键词(可手动扩展)
KeyWord = ['define', 'bool', 'char', 'char[', 'class', 'double', 'false', 'float', 'getchar', 'include', 'int', 'long',
           'main', 'null', 'open', 'printf', 'while', 'if', 'else', 'private', 'public', 'put', 'read', 'return',
           'short', 'scanf', 'signed', 'static', 'stdio', 'string', 'struct', 'true', 'unsigned', 'void']
# 关键字(符号)表(此处仅供形式上的参考，因为每次分析前会根据上面三个列表动态生成，方便扩展)
Key_Dict = {'*': 2, '-': 3, '/': 4, '=': 5, '>': 6, '<': 7, '>=': 8, '==': 9, '<=': 10, '%': 11, '+': 12, '+=': 13,
            '-=': 14, '*=': 15, '/=': 16, '(': 17, ')': 18, ',': 19, ';': 20, '.': 21, '{': 22, '}': 23, '"': 26,
            'bool': 27, 'char': 28, 'char[': 29, 'class': 30, 'double': 31, 'false': 32, 'float': 33, 'getchar': 34,
            'include': 35, 'int': 36, 'long': 37, 'main': 38, 'null': 39, 'open': 40, 'printf': 41, 'private': 42,
            'public': 43, 'put': 44, 'read': 45, 'return': 46, 'short': 47, 'scanf': 48, 'signed': 49, 'static': 50,
            'stdio': 51, 'string': 52, 'struct': 53, 'true': 54, 'unsigned': 55, 'void': 56}
# 常量字典：分析过程中记录程序中的常量
Constant_Dict = {

}
# 变量标识符：分析过程中记录程序中变量
Variable_Dict = {

}
Class_Dict = {  # 分类表
    'constant': 0,  # 常量class为0
    'variable': 1,  # 变量class为1
    'Key_Dict': Key_Dict,  # 保留字、算符和分隔符class进一步查询符号表
}

# 由于//注释只管开头，/**/注释则需要头尾兼顾，因此需要标志变量来辅助判断：
LeftNoteFlag = 0  # 用于/*注释清除的标记
RightNoteFlag = 0  # 用于*/注释清除的标记


class lexical_analyzer:  # 词法分析器类
    def __init__(self):
        self.FormatFlag = 1

    def IsLetter(self, char_):  # 字母合法性检验
        if 'a' <= char_ <= 'z' or 'A' <= char_ <= 'Z':
            return True
        else:
            return False

    def IsChinese(self, char_):  # 汉字
        if '\u4e00' <= char_ <= '\u9fff':  # ASCII码 约定用扩展位的128～255范围的编码连续2～3甚至4个来进行汉字编码
            return True
        else:
            return False

    def IsDigit(self, char_):  # 数字合法性检验
        if '0' <= char_ <= '9':
            return True
        else:
            return False

    def IsSpace(self, char_):  # 空格检验
        if char_ == ' ':
            return True
        else:
            return False

    def RemoveSpace(self, str_list):  # 移除空格方法
        index = 0
        for str_ in str_list:
            str_list[index] = str_.strip()  # 修剪字符串前后空格
            index += 1
        return str_list

    def IsNote(self, str_):  # 注释字符串检验
        global LeftNoteFlag, RightNoteFlag  # 引入注释清除辅助标记变量
        index = 0  # 用作字符串索引
        for char_ in str_:
            if index < len(str_):
                index += 1  # 索引后移一位(索引总是指向当前char_的后一个位置)
            if char_ == '/':  # 检测到注释开始字符
                if str_[index] == '/':  # 进一步判断char_的后一位字符
                    return 2  # 1.检测到是'//'则直接返回状态码2
                elif str_[index] == '*':  # 2.检测到/**/格式的注释
                    if LeftNoteFlag == 0:  # 左标志为0，说明是/*
                        LeftNoteFlag += 1
                    return 1  # 返回状态码1
            elif char_ == '*':  # 检测到*则可能是 */右注释
                if str_[index] == '/':  # 进一步判断为 */
                    if RightNoteFlag == 0:
                        RightNoteFlag += 1
                    return 3  # 返回状态码3
            if len(str_) == index + 1:
                return False  # 已经是字符串最后一位，直接返回

    def DeleteNote(self, str_list):  # 删除注释方法
        global LeftNoteFlag, RightNoteFlag
        remove_list = []
        LeftNote_num = 0  # 左注释字符索引标记(相对固定，作为参考)
        LeftNote_num1 = 0  # 左注释字符索引标记1(相对动态，用于字符串遍历及切片)
        list_index = 0  # 待处理列表索引
        for str_ in str_list:
            flag = self.IsNote(str_)  # 通过IsNote方法判断字符串是否是注释内容并接受返回值(1,2,3)
            str_index = 0  # 重置字符串索引为0
            LeftNote_num1 = 0  # 重置左注释标记1
            if flag:  # 标志为1,2,3均表示是三种注释情况的一种
                for char_ in str_:
                    if str_index < len(str_) - 1:
                        str_index += 1  # 确保当前索引是当前遍历字符的后一位
                    if flag == 1:  # 情况1: '/*'开头注释
                        if char_ == '/' and str_[str_index] == '*':
                            if str_index != 1:  # 索引不等于1，说明在注释符号不在开头：exp/*xxx
                                LeftNote_num1 = str_index - 2  # 让左注释字符索引1变为当前索引前两个位置
                            else:
                                LeftNote_num = str_index - 1  # 否则让左注释字符索引为当前索引-1：/*xxx
                            if LeftNote_num1 == 0:  # 如果左注释字符索引1为零，说明当前处于字符串刚开始
                                LeftNote_num1 = LeftNote_num  # 重置左注释字符索引1为左注释索引位置
                                LeftNoteFlag = 1  # 保持左注释标志为情况1
                            else:
                                pass
                        if char_ == '*' and str_[str_index] == '/':  # 识别到 '*/'
                            if str_index != len(str_) - 1:  # 判断索引是否为字符串最后一个字符位置
                                str_ = str_[0:LeftNote_num1] + str_[str_index + 1:]  # 不是则进行切片重组(跳过/**/之间的注释内容)
                            else:
                                str_ = str_[0:LeftNote_num1]  # 否则只读取到当前/**/之前的部分，说明/**/之后没有有效内容
                            LeftNoteFlag = 0  # 恢复左注释标志为0
                            break  # 结束本字符串遍历
                        if str_index + 1 == len(str_) and RightNoteFlag == 0 and LeftNoteFlag == 1:  # 只有/*,没有*/
                            if LeftNote_num1 == 0:  # 如果左注释索引1仍在起始位置
                                remove_list.append(str_)  # 说明字符串整体属于注释部分，将字符串整体加入待移除列表
                            else:
                                str_ = str_[0:LeftNote_num1]  # 否则截取左注释索引位置之前的部分为有效字符串
                            break
                    elif flag == 2:  # 情况2: '//'类型注释
                        if char_ == '/' and str_[str_index] == '/':
                            str_ = str_[0:str_index - 1]  # 截取到当前索引前一个位置为有效字符串
                            break
                    elif flag == 3:  # 情况3: '*/'类型
                        if char_ == '*' and str_[str_index] == '/':
                            if LeftNoteFlag != 0 and str_index != len(str_) - 1:  # 如果有左注释/*且当前索引不是字符串最后
                                str_ = str_[str_index:]  # 截取当前*/索引之后的部分为有效字符串
                            elif LeftNoteFlag != 0 and str_index + 1 == len(str_):  # 如果有左注释/*且当前索引已是字符串最后
                                remove_list.append(str_)  # 说明字符串整体属于注释内容，将其添加到待移除列表
                            elif LeftNoteFlag == 0:  # 如果没有左注释/*:^xxx */ xxx$ # 则属于错误
                                error_exit(  # 调用异常处理程序
                                    f"{list_index + 1}行{str_index}列: [Error] expected identifier or '(' before '/' token")
                            LeftNoteFlag = 0
                            RightNoteFlag = 0
                            break
            else:  # 除三种情况之外
                if LeftNoteFlag != 0 and RightNoteFlag == 0:
                    remove_list.append(str_)  # 有左注释无右注释，整体为无效字符串
                elif LeftNoteFlag != 0 and RightNoteFlag != 0:  # 左右注释标志均不为0，将其重置为0
                    LeftNoteFlag = 0
                    RightNoteFlag = 0
                else:
                    pass
            str_list[list_index] = str_  # 用处理过后的有效字符串替换旧字符串
            if list_index < len(str_list) - 1:  # 待处理列表还有字符串
                list_index += 1  # 继续待处理字符串列表索引
        for str_remove in remove_list:
            str_list.remove(str_remove)  # 从待处理列表中移除先前保存的待移除字符串
        return str_list

    def Reader(self, str_list):  # 读程序方法
        result_list = []  # 处理结果列表
        for str_ in str_list:  # 遍历待处理字符串列表
            Letter = ''  # 普通字符串
            Digit = ''  # 数字串
            letter = ''  # 其他特殊字符串(#xxx或运算符、界符等)
            index = 0
            for char_ in str_:
                if index < len(str_) - 1:
                    index += 1
                if self.IsLetter(char_):  # 判断为普通字符
                    if self.IsLetter(str_[index]) or self.IsDigit(str_[index]):  # 判断下一位字符是否为字符或数字
                        Letter += char_
                    elif self.IsSpace(str_[index]) or str_[index] in Delimiter \
                            or str_[index] in Operation or str_[index:index + 2] in Operation:
                        # 否则其后一至两位如果为界符或运算符，也将其加入
                        Letter += char_
                        result_list.append(Letter)
                        Letter = ''
                    elif str_[index] != '_':  # 例如：abc@xxx
                        error_exit(  # 调用异常处理程序
                            f"{str_list.index(str_) + 1}行{index}列: [Error] unknown symbol '{str_[index]}'")
                elif self.IsDigit(char_):  # 判断为数字字符，同上处理
                    if self.IsLetter(str_[index]) or self.IsDigit(str_[index]):
                        Digit += char_
                    elif self.IsSpace(str_[index]) or str_[index] in Delimiter \
                            or str_[index] in Operation or str_[index:index + 2] in Operation:
                        Digit += char_
                        result_list.append(Digit)
                        Digit = ''
                    else:  # 例如：34@xxx
                        error_exit(  # 调用异常处理程序
                            f"{str_list.index(str_) + 1}行{index}列: [Error] unknown symbol '{str_[index]}'")
                else:  # 非数字字符
                    if char_ == '#':  # 检测到'#'
                        result_list.append('#')
                    elif char_ in Delimiter:  # 界符
                        result_list.append(char_)
                    elif char_ in Operation:  # 运算符
                        letter += char_
                        if str_[index] in Operation:  # 运算符可能占两位字符
                            letter += str_[index]
                            result_list.append(letter)
                            letter = ''
                        else:
                            result_list.append(letter)
                            letter = ''
                    elif self.IsSpace(char_):  # 检测到空格
                        pass
                    else:  # 其他字符
                        if char_ == '_' and index != 1 and self.IsLetter(str_[index - 2]):  # '_' 判断前一位是普通字符
                            Letter += str_[index]  # 向字符序列加入 '_'
                        elif self.IsChinese(char_) and index > 1 and \
                                (self.IsChinese(str_[index]) or str_[index] == '"') and \
                                (self.IsChinese(str_[index - 2]) or str_[index - 2] == '"'):
                            # 汉字判断前后是引号或汉字："汉字"
                            Letter += str_[index]  # 向字符序列加入该汉字
                        else:
                            error_exit(  # 调用异常处理程序
                                f"{str_list.index(str_) + 1}行{index}列: [Error] unknown symbol '{str_[index - 1]}'")
        return result_list

    def JugeMent(self, str_list):  # 程序判断方法
        global Constant_Dict, Variable_Dict
        self.FormatFlag = 0  # 格式标志
        index = 0  # 索引初始化
        result_list = []  # 分析结果初始化
        Constant_Dict = {}  # 常量表初始化
        Variable_Dict = {}  # 变量表初始化
        for str_ in str_list:
            if index < len(str_) - 1:
                index += 1
            if len(str_) == 1:  # 一位字符串
                if str_ == '#':
                    result_list.append('(#, 宏定义符号)')
                    print('(#, 宏定义符号)')
                elif str_ in Delimiter:  # 分界符
                    if str_ == '<':  # 如果下一位是关键字则为分界符，防止误判为运算符小于号
                        if str_list[index] in KeyWord:
                            result_list.append(f'({Key_Dict["<_"]}, 分界符<)')
                            print(f'({Key_Dict["<_"]}, 分界符<)')
                    elif str_ == '>':  # 防止误判为运算符大于号
                        if str_list[index - 3] in Delimiter or str_list[index - 4] in KeyWord:
                            result_list.append(f'({Key_Dict[">_"]}, 分界符：>)')
                            print(f'({Key_Dict[">_"]}, 分界符：>)')
                    else:  # 其他分界符
                        result_list.append(f'({Key_Dict[str_]}, 分界符：{str_})')
                        print(f'({Key_Dict[str_]}, 分界符：{str_})')
                elif str_ in Operation:  # 运算符
                    if str_ == '%':  # 格式符，根据下一位是否是数字，与除余运算符区分
                        if not (str_list[index].isdigit()):
                            result_list.append(f'({Key_Dict[str_]}, 格式符：{str_})')
                            print(f'({Key_Dict[str_]}, 格式符：{str_})')
                            self.FormatFlag = 1  # 下一位不是数字则为格式符，标记置1
                            continue  # 跳过本次循环
                    result_list.append(f'({Key_Dict[str_]}, 运算符：{str_})')
                    print(f'({Key_Dict[str_]}, 运算符：{str_})')
                else:
                    self.constant_or_variable(str_, result_list)
            else:  # 一位以上字符串
                if str_ in KeyWord:
                    result_list.append(f'({Key_Dict[str_]}, 关键字：{str_})')
                    print(f'({Key_Dict[str_]}, 关键字：{str_})')
                elif str_ in Operation:
                    result_list.append(f'({Key_Dict[str_]}, 运算符：{str_})')
                    print(f'({Key_Dict[str_]}, 运算符：{str_})')
                else:
                    self.constant_or_variable(str_, result_list)
        return result_list

    def constant_or_variable(self, str_, result_list):  # 处理常量或变量
        if str_.isdigit():
            self.IsExist(Constant_Dict, bin(int(str_)))
            result_list.append(f'({Class_Dict["constant"]}, 表内序号：{Constant_Dict[str(bin(int(str_)))]})')
            print(f'({Class_Dict["constant"]}, 表内序号：{Constant_Dict[str(bin(int(str_)))]})')
        elif str_.isalnum():
            if self.FormatFlag == 0:
                self.IsExist(Variable_Dict, str_)
                result_list.append(f'({Class_Dict["variable"]}, 普通变量：{Variable_Dict[str_]})')
                print(f'({Class_Dict["variable"]}, 普通变量：{Variable_Dict[str_]})')
            else:
                self.IsExist(Variable_Dict, str_)
                result_list.append(f'({Class_Dict["variable"]}, 格式化变量：{Variable_Dict[str_]})')
                print(f'({Class_Dict["variable"]}, 格式化变量：{Variable_Dict[str_]})')
                self.FormatFlag = 0

    def IsExist(self, dict_, str_):  # 通用方法，用以判断常量表或变量表是否已存在该字符串
        if dict_.get(str_) is None:  # 判断变量表中是否存在该值
            dict_[str_] = len(list(dict_))  # None说明不存在，则临时加入


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


def save_result(filepath, result_list):  # 保存分析结果方法
    global Key_Dict, Constant_Dict, Variable_Dict
    # 1.保存分析结果
    with open(filepath.split('.')[0] + '分析结果.txt', mode='w', encoding='utf-8') as f:
        for result in result_list:
            f.writelines(result + '\n')
    f.close()
    # 2.保存符号表
    with open(filepath.split('.')[0] + '所用符号表.txt', mode='w', encoding='utf-8') as f:
        for result in [(key, value) for key, value in Key_Dict.items()]:
            f.writelines(f'{result}\n')
    f.close()
    # 3.保存常量表
    with open(filepath.split('.')[0] + '常量表结果.txt', mode='w', encoding='utf-8') as f:
        for result in [(key, value) for key, value in Constant_Dict.items()]:
            f.writelines(f'{result}\n')
    f.close()
    # 4.保存变量表
    with open(filepath.split('.')[0] + '变量表结果.txt', mode='w', encoding='utf-8') as f:
        for result in [(key, value) for key, value in Variable_Dict.items()]:
            f.writelines(f'{result}\n')
    f.close()


def main():
    Compiler = lexical_analyzer()
    SourceProgram = []
    print("请选择文件路径：")
    Filepath = select_file()
    if Filepath != '':
        for line in open(Filepath, 'r', encoding='gbk'):
            try:
                if line.index('\n') != 0:  # 换行符不在行开始则替换为''
                    line = line.replace('\n', '')
                else:  # 否则跳过该行
                    continue
            except:
                pass
            SourceProgram.append(line)  # 1.逐行读取文件到待处理字符串列表并去除换行符
        SourceProgram = Compiler.DeleteNote(SourceProgram)  # 2.删除注释操作处理
        print(SourceProgram)  # 打印注释删除后的结果
        SourceProgram = Compiler.RemoveSpace(SourceProgram)  # 3.移除空格操作处理
        SourceProgram = Compiler.Reader(SourceProgram)  # 4.读取操作处理
        result_list = Compiler.JugeMent(SourceProgram)  # 5.执行判断操作
        save_result(Filepath, result_list)


if __name__ == "__main__":
    # 初始化各类符号表
    Key_Dict = {}
    Constant_Dict = {}
    Variable_Dict = {}
    # 每次开始分析前都重新生成一个符号表(这样在有新的关键字时不必手动添加到符号表，只需在其相应的列表中添加即可)
    d0 = Operation + Delimiter + KeyWord
    for item in d0:
        Key_Dict[item] = d0.index(item) + 2
    main()  # 启动分析主程序
