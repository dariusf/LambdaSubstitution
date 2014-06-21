# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import re

LAMBDA = 'λ'

def is_enabled():
    settings = sublime.load_settings("Preferences.sublime-settings")
    return bool(settings.get("enabled_by_default", True))

def set_enabled(enabled):
    settings = sublime.load_settings("Preferences.sublime-settings")
    settings.set("enabled_by_default", enabled)

def replace_lambdas(view):
    edit = view.begin_edit()
    all_text = sublime.Region(0, view.size())
    view.replace(edit, all_text, re.sub(LAMBDA, u"\\\\", view.substr(all_text)))
    view.end_edit(edit)

def replace_backslashes(view):
    edit = view.begin_edit()
    all_text = sublime.Region(0, view.size())
    view.replace(edit, all_text, re.sub(r'\\(?=(?:[^"]*"[^"]*")*[^"]*$)', LAMBDA, view.substr(all_text)))
    view.end_edit(edit)

class LambdaSubstitutionOnCommand(sublime_plugin.WindowCommand):
    def run(self):
        set_enabled(True)
        replace_backslashes(self.window.active_view())

class LambdaSubstitutionOffCommand(sublime_plugin.WindowCommand):
    def run(self):
        set_enabled(False)
        view = self.window.active_view()
        dirty = view.is_dirty()
        if (not dirty or (dirty and sublime.ok_cancel_dialog("This will revert the current file."))):
            view.run_command("revert")

class LambdaSubstitutionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selection = self.view.sel()
        new_cursor_positions = [];
        for s in selection:
            if s.empty():
                # insert a lambda character if the previous character
                # wasn't a lambda character, else insert a backslash
                character_before = sublime.Region(s.a-1, s.a)
                if self.view.substr(character_before) == LAMBDA:
                    self.view.replace(edit, character_before, "\\")
                else:
                    self.view.insert(edit, s.a, LAMBDA if is_enabled() else "\\")
            else:
                # we need to deal with overwriting a selected region here.
                # save future cursor position (so we don't mutate selection
                # while iterating) and write over it
                new_cursor_positions.append(sublime.Region(s.begin()+1))
                self.view.replace(edit, s, LAMBDA if is_enabled() else "\\")

        # move cursors to new positions if a selection was overwritten
        if len(new_cursor_positions) > 0:
            selection.clear()
            for r in new_cursor_positions:
                selection.add(r)

class LambdaReplace(sublime_plugin.EventListener):

    # previous_text = ""

    def on_load(self, view):
        if is_enabled():
            replace_backslashes(view)

    def on_pre_save(self, view):
        # all_text = sublime.Region(0, view.size())
        # self.previous_text view.substr(all_text)
        if is_enabled():
            replace_lambdas(view)

    def on_post_save(self, view):
        # possibly set the previous text rather than do a replace
        if is_enabled():
            replace_backslashes(view)
