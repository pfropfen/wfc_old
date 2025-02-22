import pandas as pd
import requests
import json


# WAVE FUNCTION TILE LOOKUP TABLE

#managerurl = "192.168.178.56:31000"
managerurl = "http://192.168.178.56:31000"


tileCompatibilityList = []
tileCompatibilityLookUpTable = {}
binaryLookUpTable = {}

def requestRestrictions():
    global tileCompatibilityList
    global tileCompatibilityLookUpTable
    global binaryLookUpTable
    
    response = requests.get(managerurl+"/restrictions").json()
    
    temp = response[1]
    for i in temp.items():
        tileCompatibilityLookUpTable[int(i[0])] = i[1]
    tileCompatibilityList = response[0]
    #tileCompatibilityLookUpTable = response[1]
    binaryLookUpTable = response[2]
