import os
from pysys.constants import SKIPPED
from pysys.writer.outcomes import JUnitXMLResultsWriter
from pysys.utils.logutils import stripANSIEscapeCodes
from xml.dom.minidom import getDOMImplementation


class GitLabTestsWriter(JUnitXMLResultsWriter):
    outputDir = None

    def processResult(self, testObj, **kwargs):
        if "cycle" in kwargs:
            if self.cycle != kwargs["cycle"]:
                self.cycle = kwargs["cycle"]

        impl = getDOMImplementation()
        document = impl.createDocument(None, 'testsuite', None)
        rootElement = document.documentElement
        attr1 = document.createAttribute('name')
        attr1.value = testObj.descriptor.id
        attr2 = document.createAttribute('tests')
        attr2.value='1'
        attr3 = document.createAttribute('failures')
        attr3.value = '%d'%(int)(testObj.getOutcome().isFailure())
        attr4 = document.createAttribute('skipped')
        attr4.value = '%d'%(int)(testObj.getOutcome() == SKIPPED)
        attr5 = document.createAttribute('time')
        attr5.value = '%s'%kwargs['testTime']
        rootElement.setAttributeNode(attr1)
        rootElement.setAttributeNode(attr2)
        rootElement.setAttributeNode(attr3)
        rootElement.setAttributeNode(attr4)
        rootElement.setAttributeNode(attr5)

        # add the testcase information
        testcase = document.createElement('testcase')
        attr1 = document.createAttribute('classname')
        attr1.value = testObj.descriptor.classname
        attr2 = document.createAttribute('name')
        attr2.value = testObj.descriptor.id
        attr3 = document.createAttribute('time')
        attr3.value = '%s'%kwargs['testTime']
        testcase.setAttributeNode(attr1)
        testcase.setAttributeNode(attr2)
        testcase.setAttributeNode(attr3)

        # add in failure information if the test has failed
        if testObj.getOutcome().isFailure():
            failure = document.createElement('failure')
            attr1 = document.createAttribute('message')
            attr1.value = str(testObj.getOutcome())
            failure.setAttributeNode(attr1)
            failure.appendChild(document.createTextNode( testObj.getOutcomeReason() ))

            stdout = document.createElement('system-out')
            runLogOutput = stripANSIEscapeCodes(kwargs.get('runLogOutput',''))
            stdout.appendChild(document.createTextNode(runLogOutput.replace('\r','').replace('\n', os.linesep)))

            testcase.appendChild(failure)
            testcase.appendChild(stdout)
        rootElement.appendChild(testcase)

        # write out the test result
        self._writeXMLDocument(document, testObj, **kwargs)