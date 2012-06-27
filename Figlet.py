import os, re
import sublime, sublime_plugin
from pyfiglet import Figlet

class CreateFigletCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.edit = self.view.begin_edit('Create Figlet')
        self.fonts_dir = os.path.join(sublime.packages_path(), 'sublime-figlet', 'pyfiglet', 'fonts')
        self.fonts = [os.path.splitext(f)[0] for f in os.listdir(self.fonts_dir) if os.path.splitext(f)[1] == '.flf']
        self.view.window().show_quick_panel(self.fonts, self.on_done)

    def on_done(self, index):
        if index == -1:
            return
        figlet = Figlet(font=self.fonts[index], dir=self.fonts_dir)
        for region in self.view.sel():
            self.render(self.edit, region, figlet)
        self.view.end_edit(self.edit)

    def render(self, edit, region, figlet):
        output = figlet.renderText(self.view.substr(region))
        output = self.normalize_line_endings('Unix', output)
        output = self.prepend_leading_text(region, output)
        output = self.normalize_line_endings(self.view.line_endings(), output)
        self.view.replace(edit, region, output)

    def prepend_leading_text(self, region, string):
        lead = self.view.substr(sublime.Region(self.view.line(region.begin()).begin(), region.begin()))
        lines = re.split(r'\n', string)
        string = lines[0] + '\n'
        string += '\n'.join([lead + line for line in lines[1:]])
        return string

    def normalize_line_endings(self, line_endings, string):
        string = string.replace('\r\n', '\n').replace('\r', '\n')
        if line_endings == 'Windows':
            string = string.replace('\n', '\r\n')
        elif line_endings == 'CR':
            string = string.replace('\n', '\r')
        return string
