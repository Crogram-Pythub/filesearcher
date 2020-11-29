# -*- coding:utf-8 -*-
'''
文件搜索工具
'''

__author__ = 'Pythub Team'
__version__ = '0.0.1'
__license__ = 'BSD'

import os
import re
from os.path import isdir, join
from tkinter import (Tk, Button, BooleanVar, Checkbutton, Entry, Frame, Label,
                     Listbox, Scrollbar, StringVar, Toplevel, messagebox)
from tkinter.filedialog import askdirectory

from utils import set_window_center


class App:
    def __init__(self, master):
        self.master = master
        self.fname = StringVar(value='')  # 搜索文件名
        self.ftype = StringVar(value='')  # 搜索文件类型
        self.fpath = StringVar(value=os.environ['HOME'])  # 搜索路径
        self.advance = BooleanVar(value=False)  # 遍历子目录

        self.view()

    def about(self):
        '''关于'''
        txt = '作者：%s\n版本：%s' % (__author__, __version__)
        self.showinfo(title='关于', message=txt)

    def close(self):
        '''关闭应用'''
        self.master.quit()
        exit()

    def showinfo(self, title, message):
        '''显示提示'''
        messagebox.showinfo(parent=self.master, title=title, message=message)

    def showerror(self, title, message):
        '''显示报错'''
        messagebox.showerror(parent=self.master, title=title, message=message)

    def view(self):
        '''加载视图'''

        # 区域：文件名
        row_1 = Frame(self.master)
        row_1.pack(side='top', fill='x', expand=True)
        Label(row_1, text='文件名：', width=13, justify='left').pack(side='left')
        # 文件名输入框
        self.entry_fname = Entry(row_1,
                                 textvariable=self.fname,
                                 borderwidth=1,
                                 highlightcolor='#ddd',
                                 width=60)
        self.entry_fname.pack(side='right', fill='x', expand=True)

        # 区域：文件类型
        row_2 = Frame(self.master)
        row_2.pack(side='top', fill='x', expand=True)
        Label(row_2, text='文件后缀：', width=13, justify='left').pack(side='left')
        # 文件类型输入框
        self.entry_ftype = Entry(row_2,
                                 textvariable=self.ftype,
                                 borderwidth=1,
                                 highlightcolor='#ddd')
        self.entry_ftype.pack(side='left', fill='x', expand=True)

        # 区域：搜索路径
        row_3 = Frame(self.master)
        row_3.pack(side='top', fill='x', expand=True)
        Label(row_3, text='搜索位置：', width=13, justify='left').pack(side='left')
        # 路径输入框
        self.entry_fpath = Entry(row_3,
                                 textvariable=self.fpath,
                                 borderwidth=1,
                                 highlightcolor='#ddd')
        self.entry_fpath.pack(side='left', fill='x', expand=True)

        # 按钮：选择路径按钮
        # bbb = Label(row_3, text='...', justify='left')
        # bbb.bind('<Button-1>', self.select_path)  # 绑定双击事件
        # bbb.pack(side='left')
        button_path = Button(row_3, text='选择', command=self.select_path)
        button_path.pack(side='right')

        # 区域：选项配置
        row_4 = Frame(self.master)
        row_4.pack(side='top', fill='x', expand=True)
        Label(row_4, text='选项', width=13, justify='left').pack(side='left')
        # 是否查找子目录
        Checkbutton(row_4, text='高级功能',
                    variable=self.advance).pack(side='left')

        # 区域：操作按钮
        row_5 = Frame(self.master)
        row_5.pack(side='top', fill='x', expand=True)
        # 按钮
        Label(row_5, text='操作', width=13, justify='left').pack(side='left')
        button = Button(row_5, text='搜索', command=self.do_search)
        button.pack(side='left')
        button = Button(row_5, text='清理结果', command=self.do_clean)
        button.pack(side='left')
        button = Button(row_5, text='重置', command=self.do_reset)
        button.pack(side='left')
        button = Button(row_5, text='关于', command=self.about)
        button.pack(side='left')
        button = Button(row_5, text='关闭', command=self.close)
        button.pack(side='left')

        # 区域：搜索结果
        row_6 = Frame(
            self.master,
            # relief='raised', borderwidth=1,highlightbackground='#ddd'
        )
        row_6.pack(side='bottom', fill='both', expand=True)
        # 滚动条
        # scroll_x = Scrollbar(row_6)
        # scroll_x.pack(side='bottom', fill='x', expand=True)
        scroll_y = Scrollbar(row_6)
        scroll_y.pack(side='right', fill='y')
        # 列表
        self.result = Listbox(
            row_6,
            width=40,
            height=200,
            relief='ridge',
            borderwidth=1,
            highlightcolor='#ddd',
            # foreground='#ddd',
        )
        self.result.pack(side='left', fill='both', expand=True)
        # 列表与滚动绑定
        # self.result['xscrollcommand'] = scroll_x.set
        # scroll_x.config(command=self.result.xview)
        self.result['yscrollcommand'] = scroll_y.set
        scroll_y.config(command=self.result.yview)
        # 双击打开
        self.result.bind('<Double-Button-1>', self.opendir)

    def select_path(self):
        '''选择文件夹'''
        fpath = askdirectory(parent=self.master,
                             message='选择搜索位置',
                             title='选择搜索位置')
        if isdir(fpath):
            self.fpath.set(fpath)

    def do_search(self):
        '''搜索'''
        fname = self.fname.get()
        ftype = self.ftype.get()
        fpath = self.fpath.get()
        advance = self.advance.get()

        if advance:
            self.showinfo(title='错误提示', message='高级功能还没想好。。')
        elif not ftype:
            self.showinfo(title='错误提示', message='文件后缀不能为空')
        elif not fpath:
            self.showinfo(title='错误提示', message='搜索路径不能为空')
        else:
            ftype = '.' + ftype
            self.result.delete(0, 'end')
            fileList = os.walk(fpath)  # 所有文件目录
            resList = []
            for path, _, file in fileList:
                # path:路径,_:文件夹,file:文件
                for filename in file:
                    # re.I不区分大小写
                    rr = re.compile(r'.*?(%s).*(%s)$' % (fname, ftype), re.I)
                    res = rr.search(filename)
                    if res != None:
                        resList.append(filename)
                        self.result.insert('end', join(path, filename))
            if len(resList) == 0:
                self.showerror('错误提示', '没有找到相关的文件')
                return

    def do_reset(self):
        '''重置'''
        self.fname.set('')
        self.ftype.set('')
        self.fpath.set(value=os.environ['HOME'])
        self.advance.set(False)
        self.result.delete(0, 'end')

    def do_clean(self):
        '''清理结果'''
        self.result.delete(0, 'end')

    def opendir(self, event):
        '''打开所在文件夹'''
        index = self.result.curselection()  # 获取文件列表索引
        print('index', index)
        if index == ():
            self.showerror('错误提示', '没有找到相关的文件')
        else:
            p = self.result.get(index)
            d = os.path.dirname(p)
            # for Mac
            os.system('open ' + d)


def run():
    master = Tk()
    master.title('文件搜索工具 %s' % __version__)
    set_window_center(master, 600, 500, resize=True)
    App(master)
    master.mainloop()


if __name__ == '__main__':
    run()
