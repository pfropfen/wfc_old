import wave
import math
import requests
from flask import Flask, request, render_template, redirect
import uuid
import json
import time
from datetime import datetime
#import logging


app = Flask(__name__)

#logging.basicConfig(level=logging.DEBUG)

huburl = "http://wfchub:5002"
managerurl = "http://wfcmanager:5000"
timekeeperurl = "http://wfctimekeeper:6002"

@app.route("/")
def showHome():
    return "SERVICE FOR DISTRIBUTING MAPS"
    
@app.route("/mapGenerator",methods=["GET","POST"])
def mapGenerator():
    if request.method == 'POST':
        mapuuid = generateMap()
        return render_template('distributor.html')+"\n<H1>"+ mapuuid +"</H1>"
    elif request.method == 'GET':
        return render_template('distributor.html')
    

def getRules():
    # GET RULES
    #logging.debug("-> getting numberOfTiles..")
    print("-> getting numberOfTiles..")
    numberOfTilesResponse = requests.get(managerurl+"/numberOfTiles").json()
    numberOfTiles = (numberOfTilesResponse[0],numberOfTilesResponse[1])
    #logging.debug("numberOfTiles: "+str(numberOfTiles))
    print("numberOfTiles: ", numberOfTiles)
    #logging.debug("-> getting numberOfParts..")
    print("-> getting numberOfParts..")
    numberOfPartsResponse = requests.get(managerurl+"/numberOfParts").json()
    numberOfParts = numberOfPartsResponse
    #logging.debug("numberOfParts: "+str(numberOfParts))
    print("numberOfParts: ", numberOfParts)
    #logging.debug("-> getting entropyTolerance..")
    print("-> getting entropyTolerance..")
    entropyToleranceResponse = requests.get(managerurl+"/entropyTolerance").json()
    entropyTolerance = entropyToleranceResponse
    #logging.debug("entropyTolerance: "+str(entropyTolerance))
    print("entropyTolerance: ", entropyTolerance)
    #logging.debug("-> getting numberOfWorkers..")
    print("-> getting numberOfWorkers..")
    numberOfWorkersResponse = requests.get(managerurl+"/numberOfWorkers").json()
    numberOfWorkers = numberOfWorkersResponse
    #logging.debug("numberOfWorkers: "+str(numberOfWorkers))
    print("numberOfWorkers: ", numberOfWorkers)

    return {"numberOfTiles":numberOfTiles, "numberOfParts":numberOfParts, "entropyTolerance":entropyTolerance, "numberOfWorkers":numberOfWorkers}


def setMap(t):
    # SET MAP
    fullMap = [[0b111111111 for x in range(0,t[0])] for y in range(0,t[1])]
    return fullMap




    


def distributeMap(map, numberOfParts):
    divisions = int(math.sqrt(numberOfParts))
    mapChunks = []
    for i in range (0,divisions):
        mapChunks.append([])
        for j in range (0,divisions):
            mapChunks[i].append([])
            for k in range (0,int(len(map)/divisions)):
                mapChunks[i][j].append([])
                for l in range (0,int(len(map[0])/divisions)):
                    mapChunks[i][j][k].append(0)
        
        
    if (len(map) % divisions != 0) or (len(map[0]) % divisions != 0):
        print("MAP SIZE NOT DISTRIBUTABLE")
        return 0
        
    for y in range (0,len(map)):
        for i in range (1, int(divisions)):
            x = int(len(map[0])/(divisions))*i-1
            map[y][x] = wave.collapseTile(map[y][x])
            wave.updateMap([(x,y,map[y][x])])
            map[y][x+1] = wave.collapseTile(map[y][x+1])
            wave.updateMap([(x+1,y,map[y][x+1])])
    for x in range (0,len(map[0])):
        for i in range (1, int(divisions)):
            y = int(len(map)/(divisions))*i-1
            map[y][x] = wave.collapseTile(map[y][x])
            wave.updateMap([(x,y,map[y][x])])
            map[y+1][x] = wave.collapseTile(map[y+1][x])
            wave.updateMap([(x,y+1,map[y+1][x])])
              

    for x in range (0,len(map[0])):
        for y in range (0,len(map)):
            mapChunks[int(y/(len(map)/divisions))][int(x/(len(map[0])/divisions))][y%int(len(map)/divisions)][x%int(len(map[0])/divisions)] = map[y][x]
    #wave.prettyPrintMap(mapChunks[0][0])
    #print("MAPCHUNKS: ",mapChunks)
    return mapChunks    



def generateMap():
    while True:
        try:
        #logging.debug("getting rules")
            print("getting rules")
            rules = getRules()
            print("rules: ", rules)
            print("")
            break
        except:
            print("Connection Failed")
            time.sleep(60)
    #logging.debug("connection success")
    print("connection success")
    wave.numberOfTiles = rules["numberOfTiles"]
    wave.entropyTolerance = rules["entropyTolerance"]
    fullMap = setMap(rules["numberOfTiles"])
    wave.map = fullMap
    mapChunks = distributeMap(fullMap, rules["numberOfParts"])
    
    # SEND PARTS TO HUB
    data = []
    mapID = str(uuid.uuid4())

    for x in range(0,len(mapChunks[0])):
        for y in range(0,len(mapChunks)):
            data.append({"mapID":mapID,"chunkID":str(uuid.uuid4()),"locX":x,"locY":y,"entropyTolerance":rules["entropyTolerance"],"content":mapChunks[y][x]})
    obj = json.dumps(data)
    print("OBJECT CONTENT: ", obj)
    result = requests.post(huburl+"/saveChunks", json=obj)
    
    #SEND DATA TO TIME KEEPER
    print("getting startTime..")
    startTime = datetime.now()
    startTime = startTime.isoformat()
    print("getting map info..")
    tdata = {"mapID":mapID,"mapSize":rules["numberOfTiles"],"chunkCount":rules["numberOfParts"],"numberOfWorkers":rules["numberOfWorkers"],"startTime":startTime,"endTime":None,"totalDuration":None}       
    tobj = json.dumps(tdata)
    print("TIME OBJECT CONTENT: ", tobj)
    print("sending data to timekeeper..")
    result = requests.post(timekeeperurl+"/saveMapTime", json=tobj)
    print("done.")
    print("")
    return mapID
        
        
        
        


