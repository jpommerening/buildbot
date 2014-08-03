# This file is part of Buildbot.  Buildbot is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright Buildbot Team Members

from cStringIO import StringIO

from buildbot.interfaces import ILogObserver
from zope.interface import implements
from twisted.python import log

try:
    from defusedxml.sax import make_parser
    from defusedxml.sax.handler import ContentHandler
except ImportError:
    log.msg("Could not import defusedxml, using (the vulnerable) xml module instead")
    from xml.sax import make_parser
    from xml.sax.handler import ContentHandler


class XMLLogObserver(ContentHandler):
    implements(ILogObserver)

    def __init__(self):
        self.parser = make_parser()
        self.parser.setContentHandler(self)

    def setStep(self, step):
        self.step = step

    def setLog(self, log):
        self.log = log

    def logChunk(self, build, step, log, channel, text):
        self.parser.feed(text)

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startElement(self, name, attrs):
        pass

    def endElement(self, name):
        pass
