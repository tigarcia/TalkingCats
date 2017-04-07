"""
CleanMathML.py runs over an input or file and "cleans" a .mml files so they are all structured the same
A new file with the a .cml suffix is written

Usage:
python CleanMathML.py inputdir outputdir

The dirs can be a single file
"""

#import xml.dom.minidom as ET
import xml.etree.ElementTree as ET

import os
import sys
import getopt


def Usage():
    print(__doc__)

def main():
    if len(sys.argv) > 3:   
        Usage()
        sys.exit(0)

    # parse command line options
    inputdir = sys.argv[1]
    if len(sys.argv)==3:
        outputdir = sys.argv[2]

    if os.path.isfile(inputdir):
        cleanFile(inputdir, OutFileNameFromInputFileName(inputdir))
        return

    if not os.path.isdir(inputdir):
        print(inputdir + ' does not exist.  Please enter the correct location of the input files to test.')
    
    if os.path.isfile(outputdir):
        print(outputdir + ' is not a directory.  Please enter the correct location of the output files to write.')
    cleanDir(inputdir,outputdir)

def cleanDir(inputdir,outputdir):
    if not os.path.exists(outputdir):
        os.makedirs(outputdir) 

    for infile in os.listdir(inputdir):
        infileFullPath = inputdir + '/' + infile
        outfileFullPath = outputdir + '/' + infile
        if os.path.isdir(infileFullPath):
            cleanDir(infileFullPath, outfileFullPath)

        if infile.endswith(".mml"):
            cleanFile(infileFullPath, OutFileNameFromInputFileName(outfileFullPath))

def cleanFile(fullInputFileName, fullOutputFileName):
    with open(fullInputFileName, 'r',encoding='utf-8') as file :
        fileData = file.read()

    # strip any namespace prefixes
    fileData = stripNameSpacePrefix(fileData)

    # throw out content MathML
    if '<apply>' in fileData or '<cn>' in fileData:
        return 

    fileData = fileData.replace('&nbsp;', '&#160;')
    root = ET.fromstring(fileData)
    newElements = cleanElement(root, 'mrow')
    if len(newElements)>1:
        wrappedResult = ET.Element('mrow')
        wrappedResult.extend(newElements)
        newElements = [wrappedResult]
        
    if len(newElements) == 1:
        ET.ElementTree(newElements[0]).write(fullOutputFileName, encoding='utf-8')
    else:
        print("Empty tree! Initial input is: ", fileData)
    
def cleanElement(element, parentName):
    tagName = element.tag
    children=[]

    # if this tag goes away, it doesn't act as the parent name
    virtualParentName = tagName
    if tagName=='mstyle' or tagName=='semantics' or tagName=='math':
        virtualParentName = parentName
    for child in element:
        children.extend(cleanElement(child, virtualParentName))

    # throw out some tags
    if tagName=='mstyle' or tagName=='semantics' or tagName=='annotation' or tagName=='annotation-xml' or tagName=='math' or tagName=='mspace':
        return children

    # throw out mrows with just one child
    if tagName=='mrow' and len(children)==1:
        return children

    # throw out nested mrows
    if tagName=='mrow' and parentName=='mrow':
        return children

    newElement = ET.Element(tagName)
    if len(children)==0:
        newElement.text = element.text
    else:
        newElement.extend(children)
    return [newElement]

def RemoveAllAttrs(element):
#    while (element.attributes.length > 0):
#        element.removeAttributeNode(element.attributes.item(0))
     element.attrib = None
        
def stripNameSpacePrefix(str):
    if not ':' in str:
        return str

    iOpenBracket = str.find('<')
    iColon = str.find(':', iOpenBracket)
    prefix = str[iOpenBracket+1: iColon+1]  # e.g, 'm:'
    
    # although it is probably safe to just replace 'm:', we are more careful and only do it
    # at the start of begin and end tags
    return str.replace('<'+prefix, '<').replace('</'+prefix,'</')
    
def OutFileNameFromInputFileName(fileName):
    # assumes file name ends with .xxx
    return fileName[0:-4] + '.xml'
    


if __name__ == "__main__":
    main()