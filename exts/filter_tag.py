# -*- coding:utf-8 -*-
#    author    :   丁雪峰
#    time      :   2015-08-06 19:08:33
#    email     :   fengidri@yeah.net
#    version   :   1.0.1

import os
import pyvim
from frainui import SearchWIN
import vim

def ctag(filename):
    cmd = "ctags --sort=no -f - -n --fields=-lzf %s" % filename
    f = os.popen(cmd)

    tags = {}

    for line in f.readlines():
        tmp = line.split()

        keyword        = tmp[0] #tag name
        tp             = tmp[3] # 类型如 f
        linenu         = int(tmp[2][0: -2])# 行号, ctag 输出如: 114;"
        if not tp in 'fvm':
            continue

        tags[keyword] = linenu

    return tags



class tag_filter(object):
    INSTANCE = None
    def __init__(self):
        tag_filter.INSTANCE = self

        self.edit_win = vim.current.window

        vim.command('update')
        self.tags = ctag(self.edit_win.buffer.name)

        self.win = SearchWIN(self.tags.keys())

        self.win.FREventBind("quit", self.quit)

        self.search_win = vim.current.window


    def quit(self, win, line):
        tag_filter.INSTANCE = None


        vim.current.window = self.edit_win

        if self.search_win.valid:
            vim.command("%swincmd q" % self.search_win.number)

            if line:
                linenu = self.tags.get(line)
                if linenu:
                    pyvim.log.info("i got : %s %s", line, linenu)
                    vim.current.window.cursor = (linenu, 0)


@pyvim.cmd()
def TagFilter():
    if tag_filter.INSTANCE:
        return

    tag_filter()


if __name__ == "__main__":
    pass

