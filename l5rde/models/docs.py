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

import os
from PySide import QtCore

DOC_STATUS_CLEAN = 0
DOC_STATUS_DIRTY = 1

class DocumentItem(QtCore.QObject):

    doc_status_change = QtCore.Signal(int)

    _obj    = None
    _path   = None
    _name   = None
    _status = DOC_STATUS_CLEAN

    def __init__(self, path, obj, parent = None):
        super(DocumentItem, self).__init__(parent)

        self._path = path
        self._obj  = obj

        h, t = os.path.split(path)
        self._name = t

    @property
    def object(self):
        return self._obj

    @property
    def path(self):
        return self._path

    @property
    def name(self):
        return self._name

    @property
    def dirty(self):
        return self._status == DOC_STATUS_DIRTY

    @property
    def status(self):
        return self._status

    @dirty.setter
    def dirty(self, value):
        st = DOC_STATUS_DIRTY if value else DOC_STATUS_CLEAN
        if st != self._status:
            print('got dirty')
            self._status = st
            self.doc_status_change.emit(st)

    def __eq__(self, obj):
        return hash(self) == hash(obj)

    def __hash__(self):
        return hash(self._path)

class OpenedDocuments(QtCore.QObject):

    doc_added         = QtCore.Signal(object     )
    doc_removed       = QtCore.Signal(object     )
    doc_status_change = QtCore.Signal(object, int)

    items = []

    def __init__(self, parent = None):
        super(OpenedDocuments, self).__init__(parent)

    def is_document_open(self, doc_path):
        di = DocumentItem(doc_path, None, self)
        return di in self.items

    def get_document(self, doc_path):
        di = DocumentItem(doc_path, None, self)
        if di in self.items:
            return di
        return None

    def add_document(self, doc_path, doc_obj):
        di = DocumentItem(doc_path, doc_obj, self)
        if di not in self.items:
            self.items.append(di)
            di.doc_status_change.connect( self.on_document_status_change )
            self.doc_added.emit(di)
            return di
        return None

    def rem_document(self, doc_item):
        if doc_item in self.items:
            self.items.remove(doc_item)
            self.doc_removed.emit(doc_item)
            return True
        return False

    def remove_doc_hash(self, doc_hash):
        for d in self.items:
            print(hash(d), doc_hash)
            if hash(d) == doc_hash:
                self.rem_document(d)
                return
        raise Exception("Document not found!")

    def on_document_status_change(self, st):
        self.doc_status_change.emit(self.sender(), st)
