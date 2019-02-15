import sublime

def plugin_loaded():
    wnd=sublime.active_window()
    ng=wnd.num_groups()
    if ng>1:
        sublime.active_window().run_command("set_layout", {
            "cols": [0.0, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1]]
        })
