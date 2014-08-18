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

from PySide import QtCore, QtGui

class ClanWidget(QtGui.QWidget):
    def __init__(self, model, parent = None):
        super(ClanWidget, self).__init__(parent)

        self.fl = QtGui.QFormLayout(self)

        self.le_id   = QtGui.QLineEdit(self)
        self.le_name = QtGui.QLineEdit(self)

        self.le_id     .setPlaceholderText("Unique identifier (e.g. crab)")
        self.le_name   .setPlaceholderText("Display name (e.g. Crab)")

        self.le_id     .textEdited.connect( self.on_change )
        self.le_name   .textEdited.connect( self.on_change )

        self.fl.addRow(             "Id", self.le_id     )
        self.fl.addRow(           "Name", self.le_name   )
        self.fl.setContentsMargins(12,12,12,12)

        self.model = model

    def sizeHint(self):
        return QtCore.QSize(200, 20)

    def get_title(self):
        if self.model.name:
            return "Clan: {}".format( self.model.name )
        return "Clan: <new>"

    def load(self):
        obj = self.model
        self.le_id     .setText( obj.id   or "" )
        self.le_name   .setText( obj.name or "" )

    def apply(self):
        # TODO. validation
        obj = self.model
        obj.id   = self.le_id  .text()
        obj.name = self.le_name.text()

    def on_change(self):
        self.apply()
        self.changed.emit()

    changed = QtCore.Signal()
