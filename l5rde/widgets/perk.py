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
from organizedwidget import OrganizedWidget

'''
  <Merit type="material" id="gaijin_gear" name="Gaijin Gear">
    <Rank id="1" value="5">
      <Exception tag="mantis" value="4"/>
      <Exception tag="unicorn" value="4"/>
    </Rank>
  </Merit>
'''


class PerkExceptionWidget(QtGui.QWidget):
    def __init__(self, model, parent = None):
        super(PerkExceptionWidget, self).__init__(parent)

        self.fl = QtGui.QFormLayout(self)

        self.le_tag   = QtGui.QLineEdit(self)
        self.le_value = QtGui.QLineEdit(self)

        self.le_tag   .setPlaceholderText("Exception tag (e.g. mantis)")
        self.le_value .setPlaceholderText("XP Value")

        self.le_tag   .textEdited.connect( self.on_change )
        self.le_value .textEdited.connect( self.on_change )

        self.fl.addRow(             "Tag", self.le_tag   )
        self.fl.addRow(           "Value", self.le_value )
        self.fl.setContentsMargins(12,12,12,12)

        self.model = model

    def setup(self, data):
        pass

    def load(self):
        obj = self.model
        self.le_tag   .setText( obj.tag        or "" )
        self.le_value .setText( str(obj.value) or "" )

    def apply(self):
        # TODO. validation
        obj = self.model
        obj.tag    = self.le_tag   .text()
        obj.value  = self.le_value .text()

    def get_title(self):
        if self.model.tag:
            return "Exception: {}".format(self.model.tag)
        return "Exception: <new>"

    def on_change(self):
        print('on_change PerkExceptionWidget')
        self.apply()
        self.changed.emit()

    changed = QtCore.Signal()

class PerkRankWidget(OrganizedWidget):
    def __init__(self, model, parent = None):
        super(PerkRankWidget, self).__init__(parent)

        self.fl = QtGui.QFormLayout(self)

        self.le_id      = QtGui.QLineEdit(self)
        self.le_value   = QtGui.QLineEdit(self)
        self.exceptions = [ PerkExceptionWidget( x, self ) for x in model.exceptions ]

        self.le_id    .textEdited.connect( self.on_change )
        self.le_value .textEdited.connect( self.on_change )

        self.le_id      .setPlaceholderText("Rank ( positive integer > 0 )")
        self.le_value   .setPlaceholderText("XP Value ( positive integer )")

        fr_excp_head = QtGui.QFrame(self)
        hb = QtGui.QHBoxLayout(fr_excp_head)
        hb.setContentsMargins(0,0,0,0)
        lb_head = QtGui.QLabel("Exceptions")
        bt_add  = QtGui.QToolButton()
        bt_add.setIcon( QtGui.QIcon(":/icons/add.png") )
        bt_add.setAutoRaise(True)
        bt_add.clicked.connect( self.on_add_exception )
        hb.addWidget( lb_head )
        hb.addWidget( bt_add  )

        fr_exceptions = QtGui.QFrame(self)
        vb = QtGui.QVBoxLayout(fr_exceptions)
        vb.setContentsMargins(0,0,0,0)
        vb.addSpacing(20)
        for e in self.exceptions:
            vb.addWidget( self.wrap_widget( e, self.on_delete, e.get_title() ) )
            e.changed.connect( self.on_change )

        self.exceptions_vb = vb

        self.fl.addRow(            "Rank", self.le_id          )
        self.fl.addRow(           "Value", self.le_value       )
        self.fl.addRow(fr_excp_head      , fr_exceptions )
        self.fl.setContentsMargins(12,12,12,12)

        self.model = model

    def load(self):
        obj = self.model
        self.le_id    .setText( str(obj.id)    or "" )
        self.le_value .setText( str(obj.value) or "" )

        for ex in self.exceptions:
            ex.load()

    def apply(self):
        # TODO. validation
        obj = self.model
        obj.id     = self.le_id    .text()
        obj.value  = self.le_value .text()

        for ex in self.exceptions:
            ex.apply()

    def on_change(self):
        print('on_change PerkRankWidget')

        self.update_items( self.sender() )
        self.apply()
        self.changed.emit()

    def remove_from_model(self, itm):
        obj = self.model
        obj.exceptions.remove ( itm )

    def get_title(self):
        if self.model.id:
            return "Rank: {}".format( self.model.id )
        return "Rank: <new>"

    def on_add_exception(self):
        from dal.perk import PerkException
        x = PerkException()
        w = PerkExceptionWidget( x, self )
        w.changed.connect( self.on_change )

        self.exceptions_vb.insertWidget( 0, self.wrap_widget( w, self.on_delete, w.get_title() ) )
        self.model.exceptions.append( x )

        self.on_change()

    def on_delete(self, w):

        self.remove_from_model( w.model )
        self.remove_from_map  ( self.sender() )

        self.on_change()

    changed = QtCore.Signal()

class PerkWidget(OrganizedWidget):
    def __init__(self, ty, model, parent = None):
        super(PerkWidget, self).__init__(parent)

        self.ty = ty

        self.fl = QtGui.QFormLayout(self)

        self.le_id      = QtGui.QLineEdit(self)
        self.le_name    = QtGui.QLineEdit(self)
        self.le_type    = QtGui.QLineEdit(self)
        self.le_rule    = QtGui.QLineEdit(self)
        self.le_desc    = QtGui.QLineEdit(self)

        self.ranks = [ PerkRankWidget( x, self ) for x in model.ranks ]

        self.le_id      .setPlaceholderText("Unique identifier (e.g. ascetic)")
        self.le_name    .setPlaceholderText("Display name (e.g. Ascetic)")
        self.le_type    .setPlaceholderText("Type (e.g. mental)")
        self.le_rule    .setPlaceholderText("Rule (if unsure leave empty)")
        self.le_desc    .setPlaceholderText("Brief description")

        self.le_id      .textEdited.connect( self.on_change )
        self.le_name    .textEdited.connect( self.on_change )
        self.le_type    .textEdited.connect( self.on_change )
        self.le_rule    .textEdited.connect( self.on_change )
        self.le_desc    .textEdited.connect( self.on_change )

        fr_rank_head = QtGui.QFrame(self)
        hb = QtGui.QHBoxLayout(fr_rank_head)
        hb.setContentsMargins(0,0,0,0)
        lb_head = QtGui.QLabel("Ranks")
        bt_add  = QtGui.QToolButton()
        bt_add.setIcon( QtGui.QIcon(":/icons/add.png") )
        bt_add.setAutoRaise(True)
        bt_add.clicked.connect( self.on_add_rank )
        hb.addWidget( lb_head )
        hb.addWidget( bt_add  )

        fr_ranks = QtGui.QFrame(self)
        vb = QtGui.QVBoxLayout(fr_ranks)
        vb.setContentsMargins(0,0,0,0)
        for r in self.ranks:
            vb.addWidget( self.wrap_widget(r, self.on_delete, r.get_title()) )
            r.changed.connect( self.on_change )
        self.ranks_vb = vb

        self.fl.addRow(             "Id", self.le_id      )
        self.fl.addRow(           "Name", self.le_name    )
        self.fl.addRow(           "Type", self.le_type    )
        self.fl.addRow(           "Rule", self.le_rule    )
        self.fl.addRow(           "Desc", self.le_desc    )
        self.fl.addRow(fr_rank_head     , fr_ranks        )
        self.fl.setContentsMargins(12,12,12,12)

        self.model = model

    def setup(self, full_data):
        pass

    def sizeHint(self):
        return QtCore.QSize(200, 20)

    def get_title(self):
        t = 'Advantage' if self.ty == 'merit' else 'Disadvantage'

        if self.model.name:
            return "{}: {}".format( t, self.model.name )
        return "{}: <new>".format(t)

    def load(self):
        obj = self.model
        self.le_id   .setText( str(obj.id) or "" )
        self.le_name .setText( obj.name    or "" )
        self.le_type .setText( obj.type    or "" )
        self.le_rule .setText( obj.rule    or "" )
        self.le_desc .setText( obj.desc    or "" )

        for rk in self.ranks:
            rk.load()

    def apply(self):
        # TODO. validation
        obj = self.model
        obj.id     = self.le_id   .text()
        obj.name   = self.le_name .text()
        obj.type   = self.le_type .text()
        obj.rule   = self.le_rule .text()
        obj.desc   = self.le_desc .text()

        for rk in self.ranks:
            rk.apply()

    def remove_from_model(self, itm):
        obj = self.model
        obj.ranks.remove ( itm )

    def on_change(self):
        print('on_change PerkWidget')

        self.update_items( self.sender() )
        self.apply()
        self.changed.emit()

    def on_add_rank(self):
        from dal.perk import PerkRank
        x = PerkRank()
        w = PerkRankWidget( x, self )
        w.changed.connect( self.on_change )

        self.ranks_vb.insertWidget( 0, self.wrap_widget( w, self.on_delete, w.get_title() ) )
        self.model.ranks.append( x )

        self.on_change()

    def on_delete(self, w):

        self.remove_from_model( w.model )
        self.remove_from_map  ( self.sender() )

        self.on_change()

    changed = QtCore.Signal()
