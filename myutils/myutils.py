#! /usr/bin/env python
#-*- coding:utf-8 -*-

def isiterable(obj):
    return hasattr(obj, "__iter__") \
            and callable(getattr(obj, "__iter__"))

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = self._GetchWindows()
        except ImportError:
            self.impl = self._GetchUnix()

    def __call__(self): return self.impl()


    class _GetchUnix:
        def __init__(self):
            import tty, sys, termios

        def __call__(self):
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                #tty.setraw(sys.stdin.fileno())
                tty.setcbreak(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                #termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                termios.tcsetattr(fd, termios.TCSANOW, old_settings)
            return ch


    class _GetchWindows:
        def __init__(self):
            import msvcrt

        def __call__(self):
            import msvcrt
            return msvcrt.getwchreak

class Drawer():
    """
    描画を管理するクラス

    draw_lineで1行ずつ描画してresetでクリア
    改行含む文字列の描画には非対応
    """
    def __init__(self, draw_chars = None, delete_space = ' ', is_draw = True):
        self.is_draw = is_draw
        self.rows = 0
        self.max_cols = []

        self.draw_chars = draw_chars
        self.delete_space = delete_space

    def _print_char(self, c):
        # int型なら描画記号リストから選択
        if self.draw_chars is not None and isinstance(c, int):
            print(self.draw_chars[c], end = '')
        else:
            print(c, end = '')
        
    def draw_line(self, line):
        if not self.is_draw:return

        line = str(line) if not isiterable(line) else line

        for c in line:
            # 色付け等用に以下のリストを想定
            # [[前処理],[文字など],[後処理]]
            #
            # 描画記号指定のリストの場合もあり
            # [[c1],[c2],[c3]...]
            if isinstance(c, list):
                for c_ in c:self._print_char(c_)
            else:
                self._print_char(c)

        if len(self.max_cols)-1 >= self.rows:
            print (self.delete_space * (self.max_cols[self.rows] - len(line)))
            self.max_cols[self.rows] = len(line)
        else:
            print()
            self.max_cols.append(len(line))
        
        self.rows += 1

    def reset(self):
        if not self.is_draw:return

        print("\033[{}A".format(self.rows),end="")
        self.rows = 0

