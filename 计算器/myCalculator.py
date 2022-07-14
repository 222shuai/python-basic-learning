from tkinter import *


class myCalculator:
    def __init__(self):
        tk = Tk()
        # 设置窗口信息
        tk.geometry('420x500+700+100')
        tk.title("Shuai @ calculators")
        tk.config(background="light grey")
        # 不允许改变窗口大小(注释后可改变）
        tk.resizable(False, False)
        # 运算框
        self.string = StringVar()
        entry = Entry(tk, textvariable=self.string, )
        entry.grid(row=0, column=0, columnspan=6)
        entry.configure(background="white", font=('微软雅黑', 20), width=25)
        entry.focus()

        # 按钮及事件设置
        bvalue = ['9', '8', '7', '+',
                  '6', '5', '4', '-',
                  '3', '2', '1', '*',
                  '0', '.', 'AC', '/',
                  '(', ')', '←', '=']
        text = 1
        i = 0
        row = 1
        col = 0
        for text in bvalue:
            padx = 10
            pady = 10
            if i == 4:
                row = 2
                col = 0
            if i == 8:
                row = 3
                col = 0
            if i == 12:
                row = 4
                col = 0
            if i == 16:
                row = 5
                col = 0
            if i == 20:
                row = 6
                col = 0

            if text == '=':
                btn = Button(tk, height=1, width=4, padx=padx, pady=pady, text=text,
                             command=lambda txt=text: self.equals())
                btn.grid(row=row, column=col, padx=6, pady=5)
                btn.configure(background="yellow", font=('微软雅黑', 20))

            elif text == '←':
                btn = Button(tk, height=1, width=4, padx=padx, pady=pady, text=text,
                             command=lambda txt=text: self.delete())
                btn.grid(row=row, column=col, padx=6, pady=5)
                btn.configure(background="red", font=('微软雅黑', 20))
            elif text == 'AC':
                btn = Button(tk, height=1, width=4, padx=padx, pady=pady, text=text,
                             command=lambda txt=text: self.clearall())
                btn.grid(row=row, column=col, padx=6, pady=5)
                btn.configure(background="red", font=('微软雅黑', 20))
            elif text in ['+', '-', '*', '/', '.', '(', ')']:
                btn = Button(tk, height=1, width=4, padx=padx, pady=pady, text=text,
                             command=lambda txt=text: self.addChar(txt))
                btn.grid(row=row, column=col, padx=6, pady=5)
                btn.configure(background="red", font=('微软雅黑', 20))
            else:
                btn = Button(tk, height=1, width=4, padx=padx, pady=pady, text=text,
                             command=lambda txt=text: self.addChar(txt))
                btn.grid(row=row, column=col, padx=6, pady=5)
                btn.configure(background="light blue", font=('微软雅黑', 20))

            col += 1
            i += 1

        tk.mainloop()

    def clearall(self):  # 清屏
        self.string.set("")

    def equals(self):  # 结果计算

        try:
            result = eval(self.string.get())
            self.string.set(result)
        except:  # 异常处理
            result = "ERROR！！！"
        self.string.set(result)

    def addChar(self, char):  # 读取数据
        self.string.set(self.string.get() + (str(char)))

    def delete(self):  # 退格
        self.string.set(self.string.get()[0:-1])


myCalculator()
