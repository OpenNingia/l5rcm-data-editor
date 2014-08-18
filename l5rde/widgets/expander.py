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

class ExpanderWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(ExpanderWidget, self).__init__(parent)

        self.expanded = True

        self._button = QtGui.QPushButton(self)
        self._button.setObjectName("__qt__passive_button")
        self._button.setText("Expander")
        self._button.setIcon( QtGui.QIcon(":/icons/arrow-expanded.png") )
        self._button.setFlat(True)
        self._button.setStyleSheet("text-align: left; font-weight: bold; border: none;");
        self._button.clicked.connect(self.buttonPressed)

        self._del_bt = QtGui.QToolButton(self)
        self._del_bt.setObjectName("__qt__passive_button")
        self._del_bt.setText("")
        self._del_bt.setIcon( QtGui.QIcon(":/icons/trash-bin.png") )
        self._del_bt.setAutoRaise(True)
        self._del_bt.clicked.connect(self.deletePressed)

        self._stackWidget    = QtGui.QStackedWidget(self)

        hb = QtGui.QHBoxLayout()
        hb.addWidget( self._button )
        hb.addWidget( self._del_bt )

        self._layout         = QtGui.QVBoxLayout   (self)
        #self._layout.addWidget(self._button, 0, QtCore.Qt.AlignTop)
        #self._layout.addWidget(self._del_bt, 1, QtCore.Qt.AlignTop)
        self._layout.addItem  (hb)
        self._layout.addWidget(self._stackWidget)

    def getExpanderTitle(self):
        return self._button.text()
    def setExpanderTitle(self, val):
        self._button.setText(val);

    def getExpanded(self):
        return self.expanded
    def setExpanded(self, val):
        if val != self.expanded:
            self.buttonPressed()
        else:
            self.expanded = val;

    def sizeHint(self):
        return QtCore.QSize(200, 20)

    def count(self):
        return self._stackWidget.count()

    def currentIndex(self):
        return self._stackWidget.currentIndex()

    def widget(self, index):
        return self._stackWidget.widget(index)

    def buttonPressed(self):
        if self.expanded:

            self.expanded = False;
            self._button.setIcon( QtGui.QIcon(":/icons/arrow.png") )
            size = self._layout.sizeHint()
            w = size.width ()
            h = size.height()
            self.setSizePolicy( QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred )
            self._stackWidget.hide()
            self.resize(w, 20)
            self.updateGeometry()
        else:

            self.expanded = True;
            self._button.setIcon( QtGui.QIcon(":/icons/arrow-expanded.png") )
            self.setSizePolicy( QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding )
            self._stackWidget.show()
            self.updateGeometry()

        self.expanderChanged.emit(self.expanded)

    def deletePressed(self):
        w = self.widget( self.currentIndex() )
        if w:
            self.itemDeletion.emit(w)

    def addPage(self, page):
        self.insertPage(self.count(), page);

    def insertPage(self, index, page):
        page.setParent(self._stackWidget)
        self._stackWidget.insertWidget(index, page);

    def removePage(self, index):
        pass

    def setCurrentIndex(self, index):
        if index != self.currentIndex():
            self._stackWidget.setCurrentIndex(index)
            self.currentIndexChanged.emit(index)

    expanderTitle = QtCore.Property(str , getExpanderTitle, setExpanderTitle)
    isExpanded    = QtCore.Property(bool, getExpanded     , setExpanded     )

    currentIndexChanged = QtCore.Signal(int)
    expanderChanged     = QtCore.Signal(bool)
    itemDeletion        = QtCore.Signal(QtGui.QWidget)
