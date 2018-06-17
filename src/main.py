# main.py
#
# Copyright 2018 Romain F. T.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gi
# from gettext import gettext as _

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, Gio, GLib

from .window import DynamicWallpaperEditorWindow

class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.gnome.Dynamic-Wallpaper-Editor',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        GLib.set_application_name('Dynamic Wallpaper Editor')
        GLib.set_prgname('org.gnome.Dynamic-Wallpaper-Editor')

        self.register(None)
        menu = self.get_app_menu()
        self.set_app_menu(menu)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = DynamicWallpaperEditorWindow(application=self)
        win.present()

    def get_app_menu(self):
        builder = Gtk.Builder()
        builder.add_from_resource("/org/gnome/Dynamic-Wallpaper-Editor/Appmenu.ui")
        menu = builder.get_object("app-menu")

        new_window_action = Gio.SimpleAction.new("new_window", None)
        new_window_action.connect("activate", self.on_new_window_activate)
        self.add_action(new_window_action)

        # prefs_action = Gio.SimpleAction.new("settings", None)
        # prefs_action.connect("activate", self.on_prefs_activate)
        # self.add_action(prefs_action)

        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about_activate)
        self.add_action(about_action)

        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)

        return menu

    def on_about_activate(self, a, b):
        self.build_about_dialog()
        self.about_dialog.show()

    def on_quit(self, a, b):
        self.quit()

    def on_new_window_activate(self, a, b):
        win = DynamicWallpaperEditorWindow(application=self)
        win.present()

    def on_shortcuts_activate(self, a, b):
        self.build_shortcuts_dialog()
        self.shortcuts_dialog.show()

    # Possible pref (TODO):
    # the beginning day/hh/mm/ss
    # def on_prefs_activate(self, a, b):
        # self.prefs_window =
        # self.prefs_window.present()

    def build_about_dialog(self):
        self.about_dialog = Gtk.AboutDialog.new()
        self.about_dialog.set_comments(_("Create or edit dynamic wallpapers for GNOME."))
        self.about_dialog.set_authors(['Romain F. T.'])
        self.about_dialog.set_copyright('© 2018 Romain F. T.')
        self.about_dialog.set_license_type(Gtk.License.GPL_3_0)
        self.about_dialog.set_logo_icon_name('org.gnome.Dynamic-Wallpaper-Editor')
        self.about_dialog.set_version('beta-2018-06-17')
        self.about_dialog.set_website('https://github.com/maestroschan/dynamic-wallpaper-editor')
        self.about_dialog.set_website_label(_("Website"))

def main(version):
    app = Application()
    return app.run(sys.argv)