"""
eliminate-duplicates.py runs over an input directory comparing .txt and .mml files.
If a file is the same as an existing .txt file or an existing .mml file, it is removed.

Usage:
py -2.7 eliminate-duplicates.py inputDir outputDir
"""
import os
import sys
import getopt
import filecmp
#from subprocess import call, Popen
import shutil
import inspect
import string
from sets import Set

#sys.path.append(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())),
#"lib"))


# Main method to parse command-line args and set the tests going
def main():

    inputDir = "C:\\Dev\\MathData\\algebra\\books\\col10614_1.3_MathML"
    outputDir = "C:\\Dev\\MathData\\algebra\\books\\col10614_1.3_complete\\col10614_1.3_MathML_NoDuplicates"

    if len(sys.argv) > 2:   
        Usage()
        sys.exit(0)
    else:
        # parse command line options
        try:
            opts = (getopt.getopt(sys.argv[1:], "i:o", ["help", "indir=", "outdir="]))[0]
        except getopt.error, msg:
            print msg
            print "for help use --help"
            sys.exit(2)
                
        # process options
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                Usage()
                sys.exit(0)
            elif opt in ("-i", "--indir"):		
                inputDir = arg
                        
            elif opt in ("-o", "--outdir"):		
                outputDir = arg
    
    if not os.path.isdir(inputDir):
        print inputDir + ' does not exist.  Please enter the correct location of the input files to test.'
    
    if not os.path.isdir(outputDir):
        if not os.path.exists(outputDir):
           os.makedirs(outputDir)

    if IsWindows():
      CleanInput(inputDir.lower(), outputDir.lower())
    else: 
      CleanInput(inputDir, outputDir, addToName)
            
def Usage():
    print __doc__
    
def CleanInput(inputDir, outputDir):    
    inputDir = StripTrailingSlash(inputDir)
    outputDir = StripTrailingSlash(outputDir)
    inputDir = EscapePath(inputDir)
    outputDir = EscapePath(outputDir)
    
    fileStringSet = Set()
    nMMLDuplicates = 0
    nTXTDuplicates = 0
    
    nMMLOriginals = 0
    nTXTOriginals = 0
    
    # we run through all the files
    # foreach file, if it is NOT in the set, we add it and write it to the
    # outputdir
    if os.path.exists(inputDir):
        for infile in os.listdir(inputDir):
            # Read in the file
            with open(inputDir + '/' + infile, 'r') as file :
                infileData = file.read()
              
            if infileData in fileStringSet:
                if infile.endswith(".txt"):
                    nTXTDuplicates += 1
                else:
                    nMMLDuplicates += 1
            else:              
                if infile.endswith(".txt"):
                    nTXTOriginals += 1
                else:
                    nMMLOriginals += 1
                fileStringSet.add(infileData)
               
                # Write the new file/string
                with open(outputDir + '/' + infile, 'w') as file :
                    file.write(infileData)
                  
        print "Kept ", nMMLOriginals, "mml files  and ", nTXTOriginals, " txt files"
        print "Eliminated ", nMMLDuplicates, "mml duplicates and ", nTXTDuplicates, " txt duplicates"
    else:
        print "input directories must exist."

        
def StripTrailingSlash(path):
    if len(path) > 0:
        if path[len(path) - 1] == os.sep:
            return path[:len(path) - 1]
    return path

def EscapePath(path):
    if len(path) > 0:
        if IsCygwin():
            path = string.replace(path, "\\\\", "/") 
            path = string.replace(path, "\\", "/")
            path = AbsPath(path)
        elif IsMac():
            # mac uses the /
            path = string.replace(path, "\\\\", "/") 
            path = string.replace(path, "\\", "/")
            #escape any spaces
            #path = string.replace(path, " ", "\\ ")
        elif IsWindows():
            # switch any / to \
            path = string.replace(path, "/", "\\")
    return path

def IsWindows():
    return sys.platform == 'win32' or sys.platform == 'win64'

def IsMac():
    return sys.platform == 'darwin'

def IsCygwin():
    return sys.platform == 'cygwin'



if __name__ == "__main__":
    main()
