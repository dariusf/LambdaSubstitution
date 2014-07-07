#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import re

LAMBDA = 'λ'
BACKSLASH = '\\'

def saves_lambda_characters():
    settings = sublime.load_settings("Preferences.sublime-settings")
    return bool(settings.get("save_lambda_characters", True))

def set_saves_lambda_characters(enabled):
    settings = sublime.load_settings("Preferences.sublime-settings")
    settings.set("save_lambda_characters", enabled)

class LambdaSubstitutionCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        selection = view.sel()
        new_cursor_positions = [];
        for s in selection:
            if s.empty():
                # Insert a lambda character if the previous character
                # wasn't a lambda character, else insert a backslash.
                character_before = sublime.Region(s.a-1, s.a)
                if view.substr(character_before) == LAMBDA:
                    view.replace(edit, character_before, BACKSLASH)
                else:
                    view.insert(edit, s.a, LAMBDA)
            else:
                # We need to deal with overwriting a selected region here.
                # Save future cursor position so we don't mutate selection
                # while iterating and write over it.
                new_cursor_positions.append(sublime.Region(s.begin()+1))
                view.replace(edit, s, LAMBDA)

        # Move cursors to new positions if a selection was overwritten
        if len(new_cursor_positions) > 0:
            selection.clear()
            for r in new_cursor_positions:
                selection.add(r)

class ReplaceLambdasCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        all_text = sublime.Region(0, self.view.size())
        self.view.replace(edit, all_text, re.sub(LAMBDA, BACKSLASH, self.view.substr(all_text)))

class LambdaReplace(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        if not saves_lambda_characters():
            view.run_command("replace_lambdas")
