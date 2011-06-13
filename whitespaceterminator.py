# coding: utf8
# Copyright © 2011 Kozea
# Licensed under a 3-clause BSD license.

"""
Strip trailing whitespace before saving.

"""

from gi.repository import GObject, Gedit


EOLS = {
    Gedit.DocumentNewlineType.CR: "\r",
    Gedit.DocumentNewlineType.LF: "\n",
    Gedit.DocumentNewlineType.CR_LF: "\r\n"}


class WhiteSpaceTerminator(GObject.Object, Gedit.WindowActivatable):
    """Strip trailing whitespace before saving."""
    window = GObject.property(type=Gedit.Window)
    
    def do_activate(self):
        self.window.connect("tab-added", self.on_tab_added)

    def on_tab_added(self, window, tab, data=None):
        tab.get_document().connect("save", self.on_document_save)
    
    def on_document_save(self, document, location, encoding, compression,
                         flags, data=None):
        eol = EOLS[document.props.newline_type]
        document.props.text = eol.join(
            line.rstrip() for line in document.props.text.rstrip().split(eol))
