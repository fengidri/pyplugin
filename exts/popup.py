# -*- coding:utf-8 -*-

import vim
import pyvim
import popup
import vgit

import vgit.options


def filter_cb(ws, bw):
    o = []
    lines = open('/home/xuanzhuo.dxf/nvme/kernel/upstream-stable/net/ipv4/tcp.c').readlines()
    for line in lines:
        for w in ws:
            if line.find(w) == -1:
                break
        else:
            o.append(line)

    return o



def finish_cb(line_nu):
    vim.current.buffer[0] = str(line_nu)

@pyvim.cmd()
def PopupRun():
    p = popup.PopupRun("echo a >> a")

@pyvim.cmd()
def PopupDialog():
    p = popup.PopupDialog('hello')


@pyvim.cmd()
def PopupGit(line, target = None):
    vgit.options.commit_log_append(line, target = target)

@pyvim.cmd()
def GitLog(n = 10):
    popup.PopupRun('git log -%s' % n)


