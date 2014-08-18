# -*- coding: utf-8 -*-
# Copyright (C) 2011 Daniele Simonetti
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

"""
{
    "id": "core",
    "display_name": "Core book",
    "language": "en_US",
    "authors": ["Daniele Simonetti"],
    "version": "3.9",
    "update-uri": "",
    "download-uri": "",
    "min-cm-version": "3.8"
}
"""

from PySide import QtCore, QtGui

class ManifestWidget(QtGui.QWidget):
    def __init__(self, model, parent = None):
        super(ManifestWidget, self).__init__(parent)

        self.fl = QtGui.QFormLayout(self)

        self.le_id      = QtGui.QLineEdit(self)
        self.le_name    = QtGui.QLineEdit(self)
        self.le_lang    = QtGui.QLineEdit(self)
        self.le_authors = QtGui.QLineEdit(self)
        self.le_version = QtGui.QLineEdit(self)
        self.le_min_ver = QtGui.QLineEdit(self)

        self.le_id     .setPlaceholderText("Unique identifier (e.g. my_data_pack)")
        self.le_name   .setPlaceholderText("Display name (e.g. My Data Pack)")
        self.le_lang   .setPlaceholderText("Target language (leave empty if not sure)")
        self.le_authors.setPlaceholderText("Comma separated authors")
        self.le_version.setPlaceholderText("Package version (e.g. 1.0)")
        self.le_min_ver.setPlaceholderText("Minimum CM version (e.g. 3.9)")

        self.le_id     .textEdited.connect( self.on_change )
        self.le_name   .textEdited.connect( self.on_change )
        self.le_lang   .textEdited.connect( self.on_change )
        self.le_authors.textEdited.connect( self.on_change )
        self.le_version.textEdited.connect( self.on_change )
        self.le_min_ver.textEdited.connect( self.on_change )


        self.fl.addRow(             "Id", self.le_id     )
        self.fl.addRow(           "Name", self.le_name   )
        self.fl.addRow(       "Language", self.le_lang   )
        self.fl.addRow(        "Authors", self.le_authors)
        self.fl.addRow(        "Version", self.le_version)
        self.fl.addRow("Min. CM Version", self.le_min_ver)

        self.fl.setContentsMargins(12,12,12,12)

        self.model = model

    def load(self):
        obj = self.model.object
        self.le_id     .setText( obj.id           or "" )
        self.le_name   .setText( obj.display_name or "" )
        self.le_lang   .setText( obj.language     or "" )
        self.le_authors.setText( ', '.join(obj.authors) )
        self.le_version.setText( obj.version      or "" )
        self.le_min_ver.setText( obj.min_cm_ver   or "" )

    def apply(self):
        # TODO. validation
        obj = self.model.object
        obj.id           = self.le_id  .text()
        obj.display_name = self.le_name.text()
        obj.language     = self.le_lang.text()
        obj.authors      = [x.strip() for x in self.le_authors.text().split(",")]
        obj.version      = self.le_version.text()
        obj.min_cm_ver   = self.le_min_ver.text()

    def on_change(self):
        self.model.dirty = True
