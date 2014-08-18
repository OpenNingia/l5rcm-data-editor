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

from expander import ExpanderWidget
from clan     import ClanWidget
from family   import FamilyWidget
from perk     import PerkWidget

class DataListWidget(QtGui.QWidget):
    def __init__(self, model, parent = None):
        super(DataListWidget, self).__init__(parent)

        self.sa        = QtGui.QScrollArea()
        self.container = QtGui.QFrame()
        self.vb        = QtGui.QVBoxLayout(self.container)

        self.add_menu = QtGui.QMenu()
        self.add_menu.addAction( QtGui.QIcon(":/icons/ball.png"), "Clan"  , self.add_clan   )
        self.add_menu.addAction( QtGui.QIcon(":/icons/ball.png"), "Family", self.add_family )
        self.add_menu.addAction( QtGui.QIcon(":/icons/ball.png"), "School", self.add_school )
        self.add_menu.addAction( QtGui.QIcon(":/icons/ball.png"), "Merit" , self.add_merit  )
        self.add_menu.addAction( QtGui.QIcon(":/icons/ball.png"), "Flaw"  , self.add_flaw   )
        self.add_menu.addAction( QtGui.QIcon(":/icons/ball.png"), "Armor" , self.add_armor  )

        self.add_button = QtGui.QToolButton()
        self.add_button.setText("Add ")
        self.add_button.setIcon( QtGui.QIcon(":/icons/add.png") )
        self.add_button.setMenu(self.add_menu)
        self.add_button.setPopupMode( QtGui.QToolButton.InstantPopup )

        self.toolbar = QtGui.QToolBar("data", self)
        self.toolbar.addAction( QtGui.QIcon(":/icons/save.png"), "Save", self.apply )
        self.toolbar.addWidget( self.add_button )

        self.v = QtGui.QVBoxLayout(self)
        self.v.addWidget(self.toolbar)
        self.v.addWidget(self.sa)
        self.v.setContentsMargins(0,0,0,0)

        self.model     = model
        self.full_data = None

        self.setStyleSheet( "QFrame QLabel { color: #21007F; }" )

        self.__itm_map = {}

    def load(self):
        obj = self.model.object

        # clans
        for e in obj.clans:
            self.add_clan( e )
        for e in obj.families:
            self.add_family( e )
        for e in obj.merits:
            self.add_perk( 'merit', e )
        for e in obj.flaws:
            self.add_perk( 'flaw', e )

        self.sa.setWidget( self.container )
        self.sa.setWidgetResizable( True )
        self.container.show()

    def set_full_data(self, data):
        self.full_data = data

    def apply(self):
        self.model.object.save()
        self.model.dirty = False

    def add_clan(self, e = None):
        from dal.clan import Clan
        prepend = False
        if not e:
            prepend = True
            e = Clan()
            self.model.object.clans.append( e )

        w = ClanWidget(e, self)
        w.changed.connect( self.on_change )
        w.load()

        if prepend:
            self.prepend_item( w )
        else:
            self.append_item( w )

    def add_family(self, e = None):
        from dal.family import Family
        prepend = False
        if not e:
            prepend = True
            e = Family()
            self.model.object.families.append( e )

        w = FamilyWidget(e, self)
        w.changed.connect( self.on_change )
        w.setup(self.full_data)
        w.load()

        if prepend:
            self.prepend_item( w )
        else:
            self.append_item( w )

    def add_merit(self, e = None):
        return self.add_perk('merit', e)

    def add_flaw(self, e = None):
        return self.add_perk('flaw', e)

    def add_perk(self, ty, e = None):
        from dal.perk import Perk
        prepend = False
        if not e:
            prepend = True
            e = Perk()
            if ty == 'merit':
                self.model.object.merits.append( e )
            else:
                self.model.object.flaws.append( e )

        w = PerkWidget(ty, e, self)
        w.changed.connect( self.on_change )
        w.setup(self.full_data)
        w.load()

        if prepend:
            self.prepend_item( w )
        else:
            self.append_item( w )

    def add_school(self):
        pass

    def add_armor(self):
        pass

    def append_item(self, w, name = None):
        self.vb.addWidget( self.build_item(w, w.get_title()) )

    def prepend_item(self, w, name = None):
        self.vb.insertWidget( 0, self.build_item(w, w.get_title()) )

    def build_item(self, w, name):
        ex = ExpanderWidget(self)
        ex.setExpanded(False)
        ex.addPage(w)
        if name:
            ex.setExpanderTitle( name )

        ex.itemDeletion.connect( self.on_delete )

        self.__itm_map[ w ] = ex

        return ex

    def update_item(self, ex, itm):
        ex.setExpanderTitle( itm.get_title() )

    def remove_from_model( self, itm ):

        obj = self.model.object
        if itm in obj.clans:
            obj.clans.remove(itm)

        if itm in obj.families:
            obj.families.remove(itm)

        if itm in obj.schools:
            obj.schools.remove(itm)

        if itm in obj.spells:
            obj.spells.remove(itm)

        if itm in obj.skills:
            obj.skills.remove(itm)

        if itm in obj.merits:
            obj.merits.remove(itm)

        if itm in obj.flaws:
            obj.flaws.remove(itm)

        if itm in obj.katas:
            obj.katas.remove(itm)

        if itm in obj.kihos:
            obj.kihos.remove(itm)

        if itm in obj.weapons:
            obj.weapons.remove(itm)

        if itm in obj.weapons:
            obj.weapons.remove(itm)

        if itm in obj.skcategs:
            obj.skcategs.remove(itm)

        if itm in obj.perktypes:
            obj.perktypes.remove(itm)

        if itm in obj.weapon_effects:
            obj.weapon_effects.remove(itm)

        if itm in obj.rings:
            obj.rings.remove(itm)

        if itm in obj.traits:
            obj.traits.remove(itm)

    def on_change(self):
        snd = self.sender()
        if snd in self.__itm_map:
            self.update_item(self.__itm_map[snd], snd)
        self.model.dirty = True

    def on_delete(self, w):
        snd = self.sender()

        self.remove_from_model( w.model )

        if w in self.__itm_map:
            self.__itm_map.pop(w, None)

        w.deleteLater()
        snd.deleteLater()

        self.model.dirty = True
