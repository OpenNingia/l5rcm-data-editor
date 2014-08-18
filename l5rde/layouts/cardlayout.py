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

class CardLayout(QtGui.QLayout):
    items = []
    def __init__(self, parent = None):

        #if isinstance(parent, type(QtGui.QWidget)):
        super(CardLayout, self).__init__(parent)
        #elif isinstance(parent, type(QtGui.QLayout)):
        #    super(CardLayout, self).__init__(parent)

        #self.items = []

    def __del__(self):
        for i in self.items: del i
        self.items = []

    def addItem(self, item):
        self.items.append(item)
        item.widget().installEventFilter(self)

    def sizeHint(self):
        s = QtCore.QSize(0,0)
        n = self.count();
        if n > 0:
            s = QtCore.QSize(100,70); # start with a nice default size

        for o in self.items:
            s = s.expandedTo(o.sizeHint())
        return s + n*QtCore.QSize(self.spacing(), self.spacing())

    def minimumSize(self):
        s = QtCore.QSize(0,0)
        n = self.count()
        for o in self.items:
            s = s.expandedTo(o.minimumSize())
        return s + n*QtCore.QSize(self.spacing(), self.spacing())

    def count(self):
        return len(self.items)

    def itemAt(self, idx):
        if idx > 0 and idx < self.count():
            return self.items[idx]
        return None

    def takeAt(self, idx):
        tmp = None
        if idx > 0 and idx < self.count():
            tmp = self.items[idx]
            self.items.remove(idx)
        return tmp

    def spacing(self):
        return (self.parent().height() * 0.08 + self.parent().width() * 0.08)/2

    def setGeometry(self, rect):
        super(CardLayout, self).setGeometry(rect)

        if self.count() == 0:
            return

        margins = self.contentsMargins()
        #w = rect.width () - (self.count()) * self.spacing() - margins.right() - margins.left()
        #h = rect.height() - (self.count()) * self.spacing() - margins.bottom() - margins.top()
        w = rect.width() - margins.right() - margins.left()
        h = rect.height() - margins.bottom() - margins.top() - self.count() * self.spacing()

        i   = 0

        while i < self.count():
            o    = self.items[i]
            if o.widget().property('hover') == True:
                #geom = QtCore.QRect(rect.x()+i*self.spacing(), rect.y() + (i-1) * self.spacing(), w, h)
                o.widget().setFocus()
                o.widget().raise_()

            geom = QtCore.QRect(
                #rect.x()+i*self.spacing() + margins.left(),
                rect.x() + margins.left(),
                rect.y() + i * self.spacing() + margins.top(),
                w,
                h)
            o.setGeometry(geom)
            i += 1

    def event(self, ev):
        if ev.type() == QtCore.QEvent.LayoutRequest:
            self.invalidate()
            return True
        return False

    def eventFilter(self, obj, ev):
        if ev.type() == QtCore.QEvent.Enter:
            obj.setProperty('hover', True)
            #self.invalidate()
        elif ev.type() == QtCore.QEvent.Leave:
            obj.setProperty('hover', False)
            #self.invalidate()

        if ev.type() == QtCore.QEvent.Enter:
            QtGui.QApplication.postEvent(self, QtCore.QEvent(QtCore.QEvent.LayoutRequest))

        return False

### test ###
import sys
def test():
    app = QtGui.QApplication(sys.argv)

    dlg = QtGui.QDialog()
    cbox = CardLayout(dlg)
    def big_bt(text):
        bt = QtGui.QPushButton(text)
        bt.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
        return bt

    #cbox.setSpacing(20)
    cbox.addWidget( big_bt("Card1") )
    cbox.addWidget( big_bt("Card2") )
    cbox.addWidget( big_bt("Card3") )
    cbox.addWidget( big_bt("Card4") )
    cbox.addWidget( big_bt("Card5") )
    cbox.setContentsMargins(12, 12, 12, 12)
    dlg.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    test()
