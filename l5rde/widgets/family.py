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

class FamilyWidget(QtGui.QWidget):
    def __init__(self, model, parent = None):
        super(FamilyWidget, self).__init__(parent)

        self.fl = QtGui.QFormLayout(self)

        self.le_id      = QtGui.QLineEdit(self)
        self.le_name    = QtGui.QLineEdit(self)
        self.le_clan_id = QtGui.QLineEdit(self)
        self.le_trait   = QtGui.QLineEdit(self)

        self.le_id      .setPlaceholderText("Unique identifier (e.g. crab_hida)")
        self.le_name    .setPlaceholderText("Display name (e.g. Hida)")
        self.le_clan_id .setPlaceholderText("Clan identifier (e.g. crab)")
        self.le_trait   .setPlaceholderText("Bonus trait (e.g. agility)")

        self.le_id      .textEdited.connect( self.on_change )
        self.le_name    .textEdited.connect( self.on_change )
        self.le_clan_id .textEdited.connect( self.on_change )
        self.le_trait   .textEdited.connect( self.on_change )

        self.fl.addRow(             "Id", self.le_id      )
        self.fl.addRow(           "Name", self.le_name    )
        self.fl.addRow(          "Trait", self.le_trait   )
        self.fl.addRow(        "Clan ID", self.le_clan_id )
        self.fl.setContentsMargins(12,12,12,12)

        self.model = model

    def setup(self, full_data):

        clan_list = [ x.id for x in full_data.clans  ]
        traits    = [ x.id for x in full_data.traits ]

        q1 = QtGui.QCompleter( clan_list )
        q2 = QtGui.QCompleter( traits )

        qs = [ q1, q2 ]

        for q in qs:
            q.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
            q.setCompletionMode (QtGui.QCompleter.InlineCompletion)

        self.le_clan_id .setCompleter(q1)
        self.le_trait   .setCompleter(q2)

    def sizeHint(self):
        return QtCore.QSize(200, 20)

    def get_title(self):
        if self.model.name:
            return "Family: {}".format( self.model.name )
        return "Family: <new>"

    def load(self):
        obj = self.model
        self.le_id      .setText( obj.id     or "" )
        self.le_name    .setText( obj.name   or "" )
        self.le_clan_id .setText( obj.clanid or "" )
        self.le_trait   .setText( obj.trait  or "" )

    def apply(self):
        # TODO. validation
        obj = self.model
        obj.id     = self.le_id      .text()
        obj.name   = self.le_name    .text()
        obj.clanid = self.le_clan_id .text()

    def on_change(self):
        self.apply()
        self.changed.emit()

    changed = QtCore.Signal()
