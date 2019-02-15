import sublime, sublime_plugin, time

# open new group and run python interpreter of cur file in it
class OpenFileInReplCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        #GROUP, where we push REPL output
        target_group=0

        wnd= self.view.window()
        cur_view=wnd.active_view()
        gr_i,v_i=wnd.get_view_index(cur_view) 
        # sel = self.view.sel()
        # for s in sel:
        #     self.view.replace(edit, s, time.ctime()) 
        
        # f=open('d:/test1.txt','w')
        # s=str(v_i)+str(gr_i)
        # f.write(s)
        # f.close()

        wnd.run_command("save")
        # GET LAYOUT
        layout_num=wnd.num_groups()
        
        # SET PROPER LAYOUT
        if layout_num==1:
            wnd.set_layout({
            "cols": [0, 1],
            "rows": [0, 0.75, 1],
            "cells": [[0, 1, 1, 2],[0,0,1,1]]})
            for _v in reversed(wnd.views_in_group(0)):
                wnd.set_view_index(_v, 1, 0)
            wnd.focus_view(cur_view)
            gr_i=1
        
        # CLOSE ALL PREVIOUS CONSOLES OUTPUT
        # ADD HERE CHECK OF PRC THAT WERE NOT FINISHED

        ## - HACK, HELPING CURRENTLY RUNNING PROGRAM TO CLOSE PROPERLY
        wnd.focus_group(target_group)
        wnd.focus_view(cur_view)
        ## -

        for _v in wnd.views_in_group(target_group):
            _, _v_i = wnd.get_view_index(_v)
            wnd.run_command("close_by_index", { "group": target_group, "index": _v_i})
        
        # A HACK TO SET TARGET WINDOW IN REPL
        SETTINGS_FILE = 'SublimeREPL.sublime-settings'
        REPLsettings = sublime.load_settings(SETTINGS_FILE)
        gr_trg_i = REPLsettings.get("open_repl_in_group")
        if gr_trg_i!=target_group:
            REPLsettings.set("open_repl_in_group",target_group)
        
        # LAUNCH REPL PRC
        PyDLER_SETTINGS_FILE = 'PyDLER.sublime-settings'
        PyDLER = sublime.load_settings(PyDLER_SETTINGS_FILE)
        pypath = PyDLER.get("pypath")
        arguments={
                    "type": "subprocess",
                    "encoding": "utf8",
                    "cmd": [pypath, "-u", "-i", "$file_basename"],
                    "cwd": "$file_path",
                    "syntax": "Packages/Python/Python.tmLanguage",
                    "external_id": "$file_basename "+str(time.strftime('%H_%M_%S')),
                    "extend_env": {"PYTHONIOENCODING": "utf-8"}
                  }
        wnd.run_command("repl_open", arguments)
        
        # FOCUS BACK
        wnd.focus_group(gr_i)

# create 3 groups and run python idle in group 1
class OpenIdleInReplCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        #GROUP, where we push IDLE REPL output
        target_idle_group=1

        wnd= self.view.window()
        cur_view=wnd.active_view()
        gr_i,v_i=wnd.get_view_index(cur_view) 

        # GET LAYOUT
        layout_num=wnd.num_groups()
        
        # SET PROPER LAYOUT
        if layout_num!=3:
            wnd.set_layout({
            "cols": [0, 0.5, 1],
            "rows": [0, 0.75, 1],
            "cells": [[1, 1, 2, 2],[1,0,2,1],[0, 0, 1, 2]]})
            for _v in reversed(wnd.views_in_group(layout_num-1)):
                wnd.set_view_index(_v, 2, 0)
            
            if len(wnd.views_in_group(0))==0:
                wnd.focus_group(0)
                file_path=sublime.packages_path()+r'\PyDLER\ascii.txt'
                ascii_v=wnd.open_file(file_path)

            wnd.focus_view(cur_view)


        # A HACK TO SET TARGET WINDOW IN REPL
        SETTINGS_FILE = 'SublimeREPL.sublime-settings'
        REPLsettings = sublime.load_settings(SETTINGS_FILE)
        gr_trg_i = REPLsettings.get("open_repl_in_group")
        if gr_trg_i!=target_idle_group:
            REPLsettings.set("open_repl_in_group",target_idle_group)

        # LAUNCH REPL IDLE PRC
        PyDLER_SETTINGS_FILE = 'PyDLER.sublime-settings'
        PyDLER = sublime.load_settings(PyDLER_SETTINGS_FILE)
        pypath = PyDLER.get("pypath")
        arguments={
                    "type": "subprocess",
                    "encoding": "utf8",
                    "cmd": [pypath, "-i", "-u"],
                    "cwd": "$file_path",
                    "syntax": "Packages/Python/Python.tmLanguage",
                    "external_id": "IDLE",
                    "extend_env": {"PYTHONIOENCODING": "utf-8"}
                  }
        wnd.run_command("repl_open", arguments)

        #wnd.focus_group(1)
        vw=wnd.views_in_group(1)[-1]
        vw.show(0)
        wnd.focus_view(vw)

# swap between single/idle modes
class ChangeViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):

        wnd = self.view.window()
        cur_view=wnd.active_view()
        gr_i,v_i=wnd.get_view_index(cur_view)

        # GET LAYOUT
        layout_num=wnd.num_groups()
        
        # SET PROPER LAYOUT
        if layout_num==3:
            # CLOSE ALL PREVIOUS CONSOLES OUTPUT
            # ADD HERE CHECK OF PRC THAT WERE NOT FINISHED
            for _v in wnd.views_in_group(0):
                _, _v_i = wnd.get_view_index(_v)
                wnd.run_command("close_by_index", { "group": 0, "index": _v_i})
            for _v in wnd.views_in_group(1):
                _, _v_i = wnd.get_view_index(_v)
                wnd.run_command("close_by_index", { "group": 1, "index": _v_i})

            wnd.set_layout({
            "cols": [0, 1],
            "rows": [0, 1],
            "cells": [[0, 0, 1, 1]]})

        elif layout_num==2:
            num_views=len(wnd.views_in_group(layout_num-1))
            if num_views>0:
                wnd.run_command("open_idle_in_repl")
            else:
                # CLOSE ALL PREVIOUS CONSOLES OUTPUT
                # ADD HERE CHECK OF PRC THAT WERE NOT FINISHED
                for _v in wnd.views_in_group(0):
                    _, _v_i = wnd.get_view_index(_v)
                    wnd.run_command("close_by_index", { "group": 0, "index": _v_i})
                
                wnd.run_command("set_layout", {
                    "cols": [0.0, 1.0],
                    "rows": [0.0, 1.0],
                    "cells": [[0, 0, 1, 1]]
                })
                # LAUNCH REPL IDLE PRC
                PyDLER_SETTINGS_FILE = 'PyDLER.sublime-settings'
                PyDLER = sublime.load_settings(PyDLER_SETTINGS_FILE)
                pypath = PyDLER.get("pypath")
                arguments={
                            "type": "subprocess",
                            "encoding": "utf8",
                            "cmd": [pypath, "-i", "-u"],
                            "cwd": "$file_path",
                            "syntax": "Packages/Python/Python.tmLanguage",
                            "external_id": "IDLE",
                            "extend_env": {"PYTHONIOENCODING": "utf-8"}
                          }
                wnd.run_command("repl_open", arguments)

        elif layout_num==1:
            num_views=len(wnd.views_in_group(0))
            if num_views>0:
                wnd.run_command("open_idle_in_repl")
            else:
                # LAUNCH REPL IDLE PRC
                PyDLER_SETTINGS_FILE = 'PyDLER.sublime-settings'
                PyDLER = sublime.load_settings(PyDLER_SETTINGS_FILE)
                pypath = PyDLER.get("pypath")
                arguments={
                            "type": "subprocess",
                            "encoding": "utf8",
                            "cmd": [pypath, "-i", "-u"],
                            "cwd": "$file_path",
                            "syntax": "Packages/Python/Python.tmLanguage",
                            "external_id": "IDLE",
                            "extend_env": {"PYTHONIOENCODING": "utf-8"}
                          }
                wnd.run_command("repl_open", arguments)

# run exit command and return to default view on start
class ExitSublimeNowCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        wnd= self.view.window()
        cur_view=wnd.active_view()
        wnd.run_command("set_layout", {
            "cols": [0.0, 1.0],
            "rows": [0.0, 1.0],
            "cells": [[0, 0, 1, 1]]
        })
        wnd.run_command("exit")
