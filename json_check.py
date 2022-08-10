####################################################################
# File: json_check.py                                              #
# Description: JSON output file format and coehrence check.        #
#                                                                  #
#   Input: Json output file\s                                      #
#   Params: N.D.                                                   #
#   Output: Return the test result (with checked datas)            #
#                                                                  #
####################################################################
from fileinput import close
import json
import string
import sys

class json_check:
    #Global variables
    global _filename
    global _file
    global _data
    global _bOk
    #constructor
    def __init__(self, sFilePathname):
        self._filename = ""
        self._file     = ""
        self._data     = ""
        self._bOk      = False
       
        if (len(sFilePathname) > 0):
            self._filename = sFilePathname
            self._bOk = True
        else: self._bOk = False
        
        if (self._bOk):
            self._bOk = False
            try:
                self._file = open(self._filename,"r")
                self._file.close()
                self._bOk = True
            except(FileNotFoundError):
                print("json_check::__init__ An error occurred!")
    
    #load data from file
    def load_json_from_file():
        
        bRet = False
        buffer = ""
        _bOk = bRet

        try:
             _file = open(_filename,"r")
        except(FileNotFoundError):
            print("json_check::load_json_from_file (open) - An error occurred!")

        try:
            buffer = _file.read()
        except(Exception):
            print("json_check::load_json_from_file (read) - An error occurred!")
        
        #Build the dictionary
        try:
            if (buffer.len() > 0):
                _data = json.loads(buffer)
                if(len(_data) > 0):
                    _file.close()
                    print("load_json_from_file::Dictionary: "+_data)
                    bRet = True
        except (Exception):
            print("json_check::load_json_from_file - (json.loads) - An error occurred!")
            bRet = False #Unusual!!
        
        #Unusual!!
        bRet = True
        _bOk = bRet

        return bRet

    #Check dictionary consistency
    def chk_data_values():
        bRet = False
        try:
            if (len(_data) > 0):
                pass
        except (Exception):
            print("json_check::chk_data_values (--) - An error occurred!")

        return bRet
######################
# End of class 
#####################

######################
# start Main 
#####################
# 

try:
    args = str(sys.argv[1])
    print("Param: "+args)
    print ("sys.argv: "+str(sys.argv[1]))
except(Exception): 
    print("json_check::main ('arg = sys.argv[1:]') an error has occurred")

#Load and Check using the json_check utility class
pChk = json_check(args)

bRet = False
bRet = pChk.load_json_from_file()

if (bRet):
    bRet = pChk.chk_data_values()

print("json_check::__main__:: "+bRet)
