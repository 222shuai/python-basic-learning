from tkinter import *
from tkinter import ttk

pressure_dict = {  # 血压标准表{年龄段下限:{'man':(高压,低压),'woman':(高压,低压)}}
    '16-20': {'man': (115, 73), 'woman': (110, 70)},
    '21-25': {'man': (115, 73), 'woman': (110, 71)},
    '26-30': {'man': (115, 75), 'woman': (112, 73)},
    '31-35': {'man': (117, 76), 'woman': (114, 74)},
    '36-40': {'man': (120, 80), 'woman': (116, 77)},
    '41-45': {'man': (124, 81), 'woman': (122, 78)},
    '46-50': {'man': (128, 82), 'woman': (128, 79)},
    '51-55': {'man': (134, 84), 'woman': (134, 82)},
    '56-60': {'man': (137, 84), 'woman': (139, 82)},
    '61-65': {'man': (148, 86), 'woman': (145, 83)},
}


def difference_calculate(input_value, sex_):  # 计算差值
    base_dict = {'man': (115, 73), 'woman': (110, 70)}
    return input_value[0] - base_dict[sex_][0], input_value[1] - base_dict[sex_][1]


def blood_pressure(value1=None, value2=None, age=None, sex_=None):  # 血压测试主体部分
    result = ''
    age = str(age_select.get()) if not age else str(age)
    sex_ = sex_value if not sex_ else sex_
    high, low = difference_calculate(pressure_dict[age][sex_], sex_)  # 接收计算后的差值作为上下限依据

    if value1 >= 140 + high or value2 >= 90 + low:
        result = '高血压！'
    elif 120 + high <= value1 <= 139 + high or 80 + low <= value2 <= 89 + low:
        result = '正常高值血压！'
    elif value1 < 120 + high and value2 < 80 + low:
        result = '正常血压！'
        if value1 < 90 + high and value2 < 60 + low:
            result = '低血压！'

    return result


def run_main(val1=None, val2=None, age=None, sex_=None):  # 程序主函数
    txt.delete(1.0, END) if not (val1 and val2) else print('单元测试开始!')
    value1, value2 = (txt1.get('0.0', 'end'), txt2.get('0.0', 'end')) if not (val1 and val2) else (val1, val2)
    if not (isinstance(value1, int) and isinstance(value2, int)):
        result = '请输入整数！'
    elif value1 > value2:
        result = blood_pressure(value1, value2, age, sex_) if value1 > 0 and value2 > 0 else '请输入正整数！'
    else:
        result = '输入异常！'
    txt_set(result) if not (val1 and val2) else print('单元测试结束!')
    return result


def txt_set(string1):  # 用于向测试结果文本框中输出内容
    txt.insert(END, string1)
    txt.see(END)
    txt.update()


def sex_choose(choice):  # 根据性别选择进行性别取值的更新
    global sex_value
    sex_value = 'woman' if choice == 'woman' else 'man'


def key_handle(event):
    # print(event.keysym)
    if event.keysym == 'Control_L':
        run_main()


# 界面
if __name__ == '__main__':  # 程序启动入口
    root = Tk()
    root.geometry('400x200+500+300')
    root.title('血压测试')

    frame1 = Frame(root, width=600, height=300)
    frame2 = Frame(root, width=600, height=300)
    x = StringVar()

    allow_type = ['16-20', '21-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61-65', ]  # 年龄可选列表
    age_lab = Label(frame1, text="年龄:", relief=GROOVE, font=20, fg='blue', anchor='e')
    age_select = ttk.Combobox(frame1, state='readonly', width=15)  # 设置为可输入的下拉框
    age_select['value'] = allow_type  # 选项列表
    age_select.current(0)  # 默认为第一项
    age_lab.grid(row=2, column=1)
    age_select.grid(row=2, column=2)

    sex = StringVar()
    sex.set('man')
    sex_value = 'man'  # 默认为男
    sex_lab = Label(frame1, text="性别:",
                    relief=GROOVE, font=20, fg='blue', anchor='e')
    man_choice = Radiobutton(frame1, text="男", width=2,
                             variable=sex, value='man',
                             command=lambda: sex_choose('man'),
                             font=20, anchor='w')
    woman_choice = Radiobutton(frame1, text="女", width=2,
                               variable=sex, value='woman',
                               command=lambda: sex_choose('woman'),
                               font=20, anchor='w')
    sex_lab.grid(row=3, column=1)
    man_choice.grid(row=3, column=2)
    woman_choice.grid(row=3, column=3)

    lb1 = Label(frame1, text="收缩压(高压):",
                relief=GROOVE, font=20, fg='blue', anchor='e')
    txt1 = Text(frame1, width=15, height=1, relief=GROOVE, font=20, fg='red')
    lb1.grid(row=4, column=1)
    txt1.grid(row=4, column=2)

    lb2 = Label(frame1, text="舒张压(低压):",
                relief=GROOVE, font=20, fg='blue', anchor='e')
    txt2 = Text(frame1, width=15, height=1, relief=GROOVE, font=20, fg='red')
    lb2.grid(row=5, column=1)
    txt2.grid(row=5, column=2)

    test_btn = Button(frame2, text='测试', command=run_main
                      , width=10, height=1, fg='red').grid(row=2, column=2)
    frame2.bind("<Button-1>", run_main)
    frame1.pack()

    lb3 = Label(frame2, text="测试结果：",
                relief=GROOVE, font=20, fg='blue', anchor='e')
    lb3.grid(row=1, column=1)
    txt = Text(frame2, width=15, height=1, relief=GROOVE, font=20, fg='blue')
    txt.grid(row=1, column=2)

    Label(frame2, textvariable=x, fg='blue').grid(row=13, column=3)

    frame2.pack()

    root.bind_all("<KeyPress>", key_handle)
    root = root.mainloop()
