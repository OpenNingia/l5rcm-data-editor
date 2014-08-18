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
import os

from widgets.manifest import ManifestWidget
from widgets.datalist import DataListWidget

class L5RCMTabbedEditor(QtGui.QWidget):
    def __init__(self, model, parent = None):
        super(L5RCMTabbedEditor, self).__init__(parent)

        self.vbox = QtGui.QVBoxLayout(self)

        self.tabs    = QtGui.QTabBar(self)
        self.widgets = QtGui.QStackedWidget(self)

        self.package_data = None

        self.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )

        # TABS
        self.tabs.setDocumentMode(False)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setUsesScrollButtons(True)
        self.tabs.setExpanding(False)

        # WIDGETS
        palette = self.widgets.palette()
        palette.setColor( QtGui.QPalette.Window, QtGui.QColor("#fff")  )
        self.widgets.setPalette(palette)
        self.widgets.setAutoFillBackground(True)


        # LAYOUT
        self.vbox.addWidget(self.tabs   )
        self.vbox.addWidget(self.widgets)

        self.tabs.currentChanged.connect   (self.widgets.setCurrentIndex)
        self.tabs.tabCloseRequested.connect(self.on_tab_close_requested )

        model.doc_added        .connect( self.on_doc_added          )
        model.doc_removed      .connect( self.on_doc_removed        )
        model.doc_status_change.connect( self.on_doc_status_changed )

        self.model = model

    def on_doc_added(self, doc):
        index = self.find_tab(doc)
        if index < 0:
            widget = self.widget_for_document(doc)
    	    index  = self.add_tab(widget, doc.name, hash(doc))
        #else:
        self.set_current(index)

    def on_doc_status_changed(self, doc):
        tab_title = doc.name + "*" if doc.dirty else doc.name
        tab_color = QtCore.Qt.red if doc.dirty else QtCore.Qt.black
        print( 'status changed', tab_title, doc.status, doc.dirty )
        index     = self.find_tab(doc)
        if index >= 0:
            self.tabs.setTabText(index, tab_title)
            self.tabs.setTabTextColor(index, tab_color)

    def on_doc_removed(self, doc):
        print( repr(doc) )

    def on_tab_close_requested(self, index):
        #TODO check document status and ask to save
        doc_hash = self.tabs.tabData(index)
        self.tabs.removeTab   (index)
        w = self.widgets.widget(index)
        self.widgets.removeWidget(w)

        self.model.remove_doc_hash(doc_hash)

    def add_tab(self, widget, text, data = None):
        index = self.tabs.addTab(text)
        self.tabs.setTabData(index, data)
        self.widgets.insertWidget(index, widget)

        if hasattr(widget, 'load'):
            widget.load()
        return index

    def find_tab(self, doc):
        print('search', doc)
        for i in range(0, self.tabs.count()):
            print(i, self.tabs.tabData(i), hash(doc))
            if self.tabs.tabData(i) == hash(doc):
                print('found at', i)
                return i
        return -1

    def activate_document(self, doc):
        index = self.find_tab( doc )
        if index >= 0:
            self.set_current(index)

    def set_current(self, index):
        print('set current', index)
        self.tabs.setCurrentIndex(index)

    def widget_for_document(self, doc):
        if os.path.basename(doc.path) == 'manifest':
            return ManifestWidget(doc, self)
        else:
            dw = DataListWidget(doc, self)
            dw.set_full_data( self.package_data )
            return dw
        #return QtGui.QLabel(doc.path, self)
