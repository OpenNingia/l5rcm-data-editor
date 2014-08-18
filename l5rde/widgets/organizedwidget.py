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

'''
  <Merit type="material" id="gaijin_gear" name="Gaijin Gear">
    <Rank id="1" value="5">
      <Exception tag="mantis" value="4"/>
      <Exception tag="unicorn" value="4"/>
    </Rank>
  </Merit>
'''


class OrganizedWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(OrganizedWidget, self).__init__(parent)
        self.itm_map     = {}
        self.rev_itm_map = {}

    def wrap_widget(self, widget, cb, name = ""):
        ex = ExpanderWidget(self)
        ex.setExpanded(False)
        ex.addPage(widget)
        if name:
            ex.setExpanderTitle( name )

        ex.itemDeletion.connect( cb )
        self.itm_map[ex] = widget
        self.rev_itm_map[widget] = ex
        return ex

    def update_items(self, key):
        print( 'update_items', key, self.itm_map )
        if key in self.itm_map:
            self.update_item(self.itm_map[key], key)
        elif key in self.rev_itm_map:
            self.update_item(key, self.rev_itm_map[key])

    def update_item(self, w, ex):
        ex.setExpanderTitle( w.get_title() )

    def remove_from_map(self, key):
        if key in self.itm_map:
            w = self.itm_map.pop(key, None)
            w.deleteLater()
        elif key in self.rev_itm_map:
            w = self.rev_itm_map.pop(key, None)
            w.deleteLater()                        
        key.deleteLater()
