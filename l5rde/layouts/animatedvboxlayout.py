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

class QAnimatedLayoutItem(QtGui.QWidgetItem):
    trg_rect      = None
    cur_rect      = QtCore.QRect()
    anim          = None
    anim_duration = 400
    anim_curve    = QtCore.QEasingCurve.OutBack

    def __init__(self, widget):
        super(QAnimatedLayoutItem, self).__init__(widget)

    def setAnimationDuration(self, duration):
        self.anim_duration = duration

    def animationDuration(self):
        return self.anim_duration

    def setAnimationEasingCurve(self, curve):
        self.anim_curve = curve

    def animationEasingCurve(self):
        return self.anim_curve

    def setGeometry(self, rect):
        print('setGeometry', rect, self.widget().objectName())
        self.trg_rect = rect
        if ( self.anim is None ):
            self.anim = QtCore.QPropertyAnimation( self.widget(), "geometry" )
            self.anim.setStartValue (self.cur_rect)
            self.anim.setEndValue   (self.trg_rect)
            self.anim.setDuration   (self.anim_duration)
            self.anim.setEasingCurve(self.anim_curve)
            self.anim.finished.connect( self.on_anim_finished )
            self.anim.start()
        else:
            self.anim.setEndValue  (self.trg_rect)

    def on_anim_finished(self):
        self.anim.deleteLater()
        self.anim = None
        self.cur_rect = self.trg_rect
        super(QAnimatedLayoutItem, self).setGeometry(self.cur_rect)

class AnimatedVBoxLayout(QtGui.QVBoxLayout):

    anim_duration = 400
    anim_curve    = QtCore.QEasingCurve.OutBack
    proxy_list    = []

    def __init__(self, parent):
        super(AnimatedVBoxLayout, self).__init__(parent)

    def addWidget(self, widget):
        self.addChildWidget(widget)
        proxy_item = QAnimatedLayoutItem(widget)
        proxy_item.setAnimationDuration(self.anim_duration)
        proxy_item.setAnimationEasingCurve(self.anim_curve)
        super(AnimatedVBoxLayout, self).addItem(proxy_item)
        self.proxy_list.append(proxy_item)

    def setDefaultAnimationDuration(self, duration):
        self.anim_duration = duration
        for proxy_item in self.proxy_list:
            proxy_item.setAnimationDuration(self.anim_duration)

    def defaultAnimationDuration(self):
        return self.anim_duration

    def setDefaultAnimationEasingCurve(self, curve):
        self.anim_curve = curve
        for proxy_item in self.proxy_list:
            proxy_item.setAnimationEasingCurve(self.anim_curve)

    def defaultAnimationEasingCurve(self):
        return self.anim_curve

### test ###
import sys

def big_bt(text, parent):
    bt = QtGui.QPushButton(text, parent)
    bt.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
    bt.setObjectName(text)
    bt.clicked.connect( bt.deleteLater )
    return bt

class TestDLG(QtGui.QDialog):
    def __init__(self, parent = None):
        super(TestDLG, self).__init__(parent)
        cbox = AnimatedVBoxLayout(self)
        cbox.addWidget( big_bt("Card1", self) )
        cbox.addWidget( big_bt("Card2", self) )
        cbox.addWidget( big_bt("Card3", self) )
        cbox.addWidget( big_bt("Card4", self) )
        cbox.addWidget( big_bt("Card5", self) )
        cbox.addWidget( self.add_bt("ADD"  ) )

        cbox.setContentsMargins(12, 12, 12, 12)
        self.cbox = cbox

    def add_bt(self, text):
        bt = QtGui.QPushButton(text, self)
        bt.setSizePolicy( QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding )
        bt.setObjectName(text)
        bt.clicked.connect( self.on_add_bt )
        return bt

    def on_add_bt(self):
        bt = self.add_bt("Another ADD")
        self.cbox.addWidget(bt)
        print(self.cbox.count())

def test():
    app = QtGui.QApplication(sys.argv)

    dlg = TestDLG()
    dlg.show()
    dlg.on_add_bt()
    sys.exit(app.exec_())

if __name__ == '__main__':
    test()
