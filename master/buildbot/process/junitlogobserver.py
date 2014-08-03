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

from buildbot.process.xmllogobserver import XMLLogObserver
from buildbot.status import results
from buildbot.status.testresult import TestResult


class JUnitLogObserver(XMLLogObserver):

    def __init__(self):
        XMLLogObserver.__init__(self)
        self.testsuite = None
        self.testcase = None
        self.results = None
        self.message = None
        self.logs = None
        self.text = None

    def addTestResult(self):
        test = tuple(filter(bool, [
            self.testsuite.get('name'),
            self.testcase.get('classname'),
            self.testcase.get('name')
        ]))
        testresult = TestResult(name, self.results, self.message, self.logs)
        self.step.build.build_status.addTestResult(testresult)

    def startElement(self, name, attrs):
        dispatch = {
            'testsuite': self.startTestsuite,
            'testcase': self.startTestcase,
            'system-out': self.startLog,
            'system-err': self.startLog,
            'failure': self.startStatus,
            'skipped': self.startStatus,
            'error': self.startStatus
        }
        if name in dispatch:
            dispatch[name](name, attrs)

    def endElement(self, name):
        dispatch = {
            'testsuite': self.endTestsuite,
            'testcase': self.endTestcase,
            'system-out': self.endLog,
            'system-err': self.endLog,
            'failure': self.endStatus,
            'skipped': self.endStatus,
            'error': self.endStatus
        }
        if name in dispatch:
            dispatch[name](name)

    def startTestsuite(name, attrs):
        self.testsuite = dict(attrs)

    def endTestsuite(name):
        self.testsuite = None

    def startTestcase(name, attrs):
        self.testcase = dict(attrs)
        self.results = results.SUCCESS
        self.message = ''
        self.logs = {}

    def endTestcase(name):
        self.addTestResult()
        self.testcase = None
        self.results = None
        self.message = None
        self.logs = None

    def startStatus(name, attrs):
        if name == 'failure':
            self.results = results.FAILURE
        elif name == 'skipped':
            self.results = results.SKIPPED
        else:
            raise ValueError('Unexpected test result tag')
        if 'message' in attrs:
            self.message = message
        self.startLog(name, attrs)

    def endStatus(name):
        self.endLog(name, attrs)

    def characters(content):
        if self.text:
            self.text.write(content)

    def startLog(self, name, attrs):
        self.text = StringIO()

    def endLog(self, name):
        if not isinstance(self.text, StringIO):
            raise ValueError('Broken XML?')
        if self.logs is None:
            # outside testcase
            pass
        else:
            self.logs[name] = self.text.getvalue()
        self.text = None
