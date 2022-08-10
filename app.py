####################################################################
# File: dwdata.py                                                  #
# Description: WSGI API Rest for a node deep web information.      #
#                                                                  #
#   Input: HTTP GET Request.                                       #
#   Params: N.D.                                                   #
#   Output: Return a set of JSON data form an HTTP GET request.    #
#                                                                  #
####################################################################

####################################################################
# HTTP Errors Codes                                                #
#                                                                  #
# Code  Meaning Description                                        #
# 200   OK  The requested action was successful.                   #
# 201   Created A new resource was created.                        #
# 202   Accepted    The request was received, but no modification  #
#        has been made yet.                                        #
# 204   No Content  The request was successful, but the response   #
#       has no content.                                            #
# 400   Bad Request The request was malformed.                     #
# 401   Unauthorized The client is not authorized to perform the   #
#       requested action.                                          #
# 404   Not Found   The requested resource was not found.          #
# 415   Unsupported Media Type  The request data format is not     #
#       supported by the server.                                   #
# 422   Unprocessable Entity    The request data was properly      #
#       formatted but contained                                    #
#       invalid or missing data.                                   #
# 500   Internal Server Error   The server threw an error when     #
#       processing the request.                                    #
####################################################################

# Library Import

from random import random
from flask import Flask, request, jsonify
import os, sys
import socket
import secrets

from stat import *

#App name

app = Flask(__name__)

with app.app_context():

    # Return code
    _dwret = 500

    #Global variables
    _srRefUrl = ""
    _berror = False
    _dwnodeinfo =  {"Error":"No Data","Description": "No Data Founds - see error code"}

    _MAX_ID_SIZE       = 64
    _MAX_RES_NAME_SIZE = 100
    _MAX_RES_TYPE_SIZE = 5
    _MAX_RES_DES_SIZE  = 100
    _MAX_RES_SIZE      = 9
   #not used (links builts offline!!)
    _MAX_RES_LINK_SIZE = 100

###################################################################
# Data structure for node informations to return.                 #
# resources - Resources list definition 
# resource_id - Resource id - lenght 64 bytes                     #
# resource_name - Resource name - length 100 bytes                 #
# resource_type - Resource type - length 5 bytes (W [web],        #
#                                            I[image], S [sound], #
#                                              C [code], X [xml], #
#                                                       T [text], #
#                                            V [video], O [iot])  #
# resource_description - Resource description - length 100 bytes  #
# resource_ref - Resource Url reference - length  200 bytes       #
# resource_size - Resource size on remote node - length 9 bytes   #
# resource_link - Resource links for web/xml/text/code remote     # 
#                                                     resource    #
####################################################################

# Get all node file system information and populate the
# dwnodeinfo cache.

####################################################################
#               README for Data structure to return                #
####################################################################
# data = {"lista":[                                                #
#   {                                                              #
#    "primo":str(uno),                                             #
#    "secondo":str(due),                                           #
#    "terzo":str(tre)                                              #
#   }                                                              #
# ],                                                               #
# "quarto":str(quattro),                                           #
# "quinto":str(cinque)                                             #
# }                                                                #
#                                                                  #            
# print(json.dumps(data))                                          #
# res = json.loads(json.dumps(data))                               #
# print (res)                                                      #
# print (res["lista"][0])                                          #
#                                                                  #
## Generalized Data structure                                      #
#  dwnodeinfo = "                                                  #
#  {"resources":[                                                  #
#    {                                                             #
#     "resource_name": str(srName),                                #
#     "resource_type": str(srType),                                #
#     "resource_description": str(srDescription),                  #
#     "resource_ref": str(srUrl),                                  #
#     "resource_size": str(srSize),                                #
#     "resource_links" : [                                         #
#       {                                                          #
#           "resource_link": str(srLink),                          #
#       }                                                          #
#      ]                                                           #
#    }                                                             #
#  ]                                                               #
#  }                                                               #
#  "                                                               #
####################################################################
# print(json.dumps(data))                                          #
# res = json.loads(json.dumps(data))                               #
# print (res)                                                      #
# print (res["lista"][0])                                          #
####################################################################
# line 152: Iterate on hyperlink for web content ::getResourceLinks
# (srName) for i::todo
# line 155: Comma separated on non latest link element
# line 159: Comma separated on non latest resource element

## Functions ##

# Links list from local node resource on file system
def getResourceLinks (sLocalResource):
   sRet = [""]
   return sRet

# File type from local node resource on file system
def getFileType (sLocalResource):
    sRet = "n.d."
    #Check the extension
    try:
        if((len(sLocalResource) > 3) and (sLocalResource.count(".") == 1)):
            #extension
            sTemp = sLocalResource.split(".")
            if (len(sTemp) == 2):
                sRet = sTemp[1]
    except:
       print("getFileType::An error occurred")
     
    return sRet
   
######################################################
# File system data retrive and encoding  START:      #
# ####################################################

# CAUTION: If topdown==False ==> Anything in one step in files!!

def init_data():
    with app.app_context():
        _dwnodeinfo = {"Error":"No Data","Description": "No Data Founds - see error code"}
        _srRefUrl = ""
        _berror = False
        _dwret = 500
    return True
 
def set_data(buffer, obj):
    with app.app_context():
        _dwnodeinfo = buffer
        _srRefUrl = obj

def get_dwdata(srRefUrl):
    with app.app_context():
        l_count = 0
        _berror = False
        _srRefUrl = srRefUrl
        _dwnodeinfo = """
         {"resources":["
        """
        top = "/Users/marcopuccetti/Sites/Eo_Admin/"
        # Retrive all the node information, on WSGI application on '/var/www/the_app'

        for root, dirs, files in os.walk(top, topdown=False):
             #if(l_count >= 100): break
             l_count = 0
             t_count = len(files)
             #print("*******DEBUG**********")
             #print("Directory: "+root)
             #print("Total Resources: "+str(t_count))
             #print("Url: "+_srRefUrl)
             #print("Count: "+str(l_count))
             for name in files:
                 _berror = False
                 l_count+=1
                 #print("Risorsa: "+name)
                 srName= str(os.path.join(root, name))
                 #print("Resource absolute path: "+srName)
                 #Retrive the stat info for the file
                 try:
                   statinfo = os.stat(srName)
                 except (FileNotFoundError):
                     print("Warning error reading the resource: "+srName)
                     print("This resource will be skipped.")
                     _berror = True
                 stmode = statinfo.st_mode
                 if S_ISREG(stmode) and (_berror == False):
                        print("Regular file")
                    #Process only regular files!!
                        srID = str(secrets.token_hex()).ljust(_MAX_ID_SIZE)
                        srType = getFileType(srName).ljust(_MAX_RES_TYPE_SIZE)
                        srCreator = str(statinfo.st_uid)
                        srCtime = str(statinfo.st_ctime)
                        # (last metadata change for some Unix -- creation time for windows systems)
                        srDescription = str("File: "+srName+" created by: "+srCreator+", cTime: "+srCtime).ljust(_MAX_RES_DES_SIZE)
                        srUrl = _srRefUrl # Request url from flask http request
                        srSize =  str(statinfo.st_size).ljust(_MAX_RES_SIZE)
                        srLinks = getResourceLinks(srName)
                        i=0
                        _dwnodeinfo+="""
                        {
                        "resource_id": """+str(srID)+""",
                        "resource_name": """+str(srName)+""",
                        "resource_type": """+str(srType)+""",
                        "resource_description": """+str(srDescription)+""",
                        "resource_ref": """+str(srUrl)+""",
                        "resource_size": """+str(srSize)+""",
                        "resource_links" : [{"""
                        _dwnodeinfo+=""""resource_link": """+str(srLinks[i].ljust(_MAX_RES_LINK_SIZE))
                        _dwnodeinfo+="""
                           }
                        ]"""
                        #comma for only internal elements
                        if (l_count < t_count):
                            _dwnodeinfo+="""},"""
                        else:
                            _dwnodeinfo+="""}"""
                        
             print("**********************")
        _dwnodeinfo+="""
         ]
        }
        """
        _dwnodeinfo = _dwnodeinfo.replace("\n","")
        print ("get_dwdata::dwnodeinfo--> "+_dwnodeinfo)
        return _dwnodeinfo

######################################################
# File system data retrive and encoding: END         #
# ####################################################

# GET /dwdata definition

@app.route("/dwdata", methods=["GET"])
def dwdata():
    with app.app_context():   
       init_data()
       #Get Host name
       _srRefUrl = str(request.path)
       _srRefUrl.replace(" ","")
     
       if(_srRefUrl == "/"):
           _srRefUrl = socket.gethostname()
           
       print ("URL: "+_srRefUrl)
     
       _dwnodeinfo = ""
       set_data (_dwnodeinfo, _srRefUrl)
     
       _dwnodeinfo = get_dwdata(_srRefUrl)
    
       if (_berror == False):
           _dwret = 200
    
       return jsonify(_dwnodeinfo), _dwret