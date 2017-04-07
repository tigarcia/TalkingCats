"""
copy-if-different.py runs over two specified input directories comparing .txt files.
If the files differ, a new file is created in the first directory with the name <filename>_<part>.txt,
where <part> is the third command line arg

Note: any <bookmark> is deleted from the file in the second dir before comparision.

Usage:
python copy-if-different.py dir1 dir2 addToName
"""
import os
import sys
import getopt
import filecmp
#from subprocess import call, Popen
import shutil
import inspect
import string

#sys.path.append(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), "lib"))


# Main method to parse command-line args and set the tests going
def main():

    inputDir1 = "C:\\Dev\\MathData\\20170322.04\\SPEECH\\col10614_1.3_MathML_NoDuplicates"
    inputDir2 = "C:\\Dev\\MathData\\algebra\\books\\col10614_1.3_MathML"
    addToName = "simple-ld"

    if len(sys.argv) > 4:   #FIX ME -- should be != 
        Usage()
        sys.exit(0)
    else:
        # parse command line options
        try:
            opts = (getopt.getopt(sys.argv[1:], "1:2:a", ["help", "dir1=", "dir2=", "append=",]))[0]
        except getopt.error, msg:
            print msg
            print "for help use --help"
            sys.exit(2)
                
        # process options
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                Usage()
                sys.exit(0)
            elif opt in ("-1", "--dir1"):		
                inputDir1 = arg
                        
            elif opt in ("-2", "--dir2"):		
                inputDir2 = arg
            elif opt in ("-a", "--append"):		
                addToName = arg
    
    if len(inputDir1) == 0 or len(inputDir2) == 0:
        print 'You are missing some required options.'
        Usage()
        sys.exit(0)

    if not os.path.isdir(inputDir1):
        print inputDir1 + ' does not exist.  Please enter the correct location of the input files to test.'
    elif not os.path.isdir(inputDir2):
        print inputDir2 + ' does not exist.  Please enter the correct location of the input files to test.'
    else:
        if IsWindows():
            CompareOutput(inputDir1.lower(), inputDir2.lower(), addToName)
        else: 
            CompareOutput(inputDir1, inputDir2, outputDir, addToName)
            
def Usage():
    print __doc__
    
def CompareOutput(inputDir1, inputDir2, addToName):
    global g_inputTypesToExtensionMap
    
    inputDir1 = StripTrailingSlash(inputDir1)
    inputDir2 = StripTrailingSlash(inputDir2)
    inputDir1 = EscapePath(inputDir1)
    inputDir2 = EscapePath(inputDir2)
    
    # gather all of the input files
    # was inputDir1
    if os.path.exists(inputDir1):
       for file1 in os.listdir(inputDir1):
         file1 = inputDir1 + '/' +  file1
         if file1.endswith(".txt"):
            file2 = file1.replace(inputDir1, inputDir2)
            #remove <bookmark>
            # Read in the file
            with open(file1, 'r') as file :
              file1Data = file.read()
            with open(file2, 'r') as file :
              file2Data = file.read()

            # Replace the target string
            file1Data = file1Data.replace("<bookmark mark='0'/> ", '')
            if (file1Data!=file2Data):
               # Write the file out again
               with open(file2[0:-4]+'_'+addToName+'.txt', 'w') as file:
                  file.write(file1Data)
    else:
        print "Both input directories must exist."

        
def StripTrailingSlash(path):
    if len(path) > 0:
        if path[len(path)-1] == os.sep:
            return path[:len(path)-1]
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