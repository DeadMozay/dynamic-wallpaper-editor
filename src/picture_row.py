# picture_row.py
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

from gi.repository import Gtk, Gio, GdkPixbuf, Pango, GLib
from .gi_composites import GtkTemplate
import math
import xml.etree.ElementTree as xml_parser

# This is a row with the thumbnail and the path of the picture, and control
# buttons (up/down, delete) for this picture. It also contains "spinbuttons" if
# the user needs them.
# TODO make rows draggable ?
class PictureRow(Gtk.ListBoxRow):
    __gtype_name__ = 'PictureRow'

    def __init__(self, pic_struct, window):
        super().__init__()
        self.set_selectable(False)
        self.filename = pic_struct.filename
        self.window = window

        builder = Gtk.Builder()
        builder.add_from_resource("/com/github/maoschanz/DynamicWallpaperEditor/picture_row.ui")
        row_box = builder.get_object("row_box")
        self.time_box = builder.get_object("time_box")

        label = builder.get_object("row_label")
        label.set_label(self.filename)
        label.set_ellipsize(Pango.EllipsizeMode.START)

        delete_btn = builder.get_object("delete_btn")
        delete_btn.connect('clicked', self.destroy_row)

        up_btn = builder.get_object("up_btn")
        down_btn = builder.get_object("down_btn")
        up_btn.connect('clicked', self.on_up)
        down_btn.connect('clicked', self.on_down)

        self.static_time_btn = builder.get_object("static_btn")
        self.trans_time_btn = builder.get_object("transition_btn")
        self.static_time_btn.connect('value-changed', self.window.update_status)
        self.trans_time_btn.connect('value-changed', self.window.update_status)
        self.static_time_btn.set_value(float(pic_struct.static_time))
        self.trans_time_btn.set_value(float(pic_struct.trans_time))

        image = builder.get_object("row_thumbnail")
        try:
            # This size is totally arbitrary.
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(self.filename, 114, 64, True)
            image.set_from_pixbuf(pixbuf)
        except Exception:
            image.set_from_icon_name('dialog-error-symbolic', Gtk.IconSize.BUTTON)
            self.set_tooltip_text(_("This picture doesn't exist"))
            self.time_box.set_sensitive(False)
            up_btn.set_sensitive(False)
            down_btn.set_sensitive(False)

        self.add(row_box)
        self.show_all()
        self.time_box.set_visible(not self.window.time_switch.get_active())

    def generate_static(self, st_time):
        if st_time is None:
            time_str = str(self.static_time_btn.get_value())
        else:
            time_str = str(st_time)
        raw_string = (
"""
	<static>
		<file>{fn}</file>
		<duration>{dur}</duration>
	</static>
""").format(fn=self.filename, dur=time_str)
        return str(raw_string)

    def generate_transition(self, tr_time, next_fn):
        if tr_time is None:
            time_str = str(self.trans_time_btn.get_value())
        else:
            time_str = str(tr_time)
        if time_str == '0.0':
            raw_string = ''
        else:
            raw_string = (
"""
	<transition type="overlay">
		<duration>{dur}</duration>
		<from>{fn}</from>
		<to>{nfn}</to>
	</transition>
""").format(dur=time_str, fn=self.filename, nfn=next_fn)
        return str(raw_string)

    def on_up(self, b):
        index = self.get_index()
        self.window.update_durations()
        self.window.pic_list.remove(self.window.pic_list[index])
        self.window.pic_list.insert(index-1, PictureStruct(self.filename, \
            self.static_time_btn.get_value(), self.trans_time_btn.get_value()))
        self.window.add_pictures_to_list([])

    def on_down(self, b):
        index = self.get_index()
        self.window.update_durations()
        self.window.pic_list.remove(self.window.pic_list[index])
        self.window.pic_list.insert(index+1, PictureStruct(self.filename, \
            self.static_time_btn.get_value(), self.trans_time_btn.get_value()))
        self.window.add_pictures_to_list([])

    def destroy_row(self, b):
        index = self.get_index()
        self.window.update_durations()
        self.window.pic_list.remove(self.window.pic_list[index])
        self.window.add_pictures_to_list([])
        self.destroy()


# This structure keep track of a picture's path and times. While rows are
# destroyed during the edition, these structures are not.
# FIXME utiliser une structure normale
class PictureStruct():
    __gtype_name__ = 'PictureStruct'

    filename = ''
    static_time = 10
    trans_time = 0

    def __init__(self, filename, static_time, trans_time):
        self.filename = filename
        self.static_time = static_time
        self.trans_time = trans_time
