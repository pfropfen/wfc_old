import pandas as pd
import requests
from flask import Flask, request, render_template, redirect
#import logging

app = Flask(__name__)

#logging.basicConfig(level=logging.DEBUG)

#numberOfTiles = (0,0)

# MANAGER


# READ RULES
data = pd.read_excel("rules.xlsx", usecols="B")

numberOfTiles = (int(data.values[0][0]),int(data.values[1][0]))
numberOfParts = int(data.values[2][0])
entropyTolerance = int(data.values[3][0])
numberOfWorkers = int(data.values[4][0])

#logging.logger.debug("numberOfTiles: "+str(numberOfTiles))
#logging.logger.debug("numberOfParts: "+str(numberOfParts))
#logging.logger.debug("entropyTolerance: "+str(entropyTolerance))
#logging.logger.debug("numberOfWorkers: "+str(numberOfWorkers))
print("numberOfTiles: ", numberOfTiles)
print("numberOfParts: ", numberOfParts)
print("entropyTolerance: ", entropyTolerance)
print("numberOfWorkers: ", numberOfWorkers)



#@app.route("/")
#def showRules():
    #return Flask.jsonify({"numberOfTiles: ": numberOfTiles, "numberOfParts: ": numberOfParts, "entropyTolerance: ": entropyTolerance, "numberOfWorkers: ": numberOfWorkers})

@app.route('/', methods=['GET', 'POST'])
def showHome():
    if request.method == 'POST':
        # aktualisierten Werte verarbeiten
        numberOfTiles = request.form.get('var1')
        numberOfParts = request.form.get('var2')
        entropyTolerance = request.form.get('var3')
        numberOfWorkers = request.form.get('var4')
        # Werte speichern oder weiterverarbeiten
        return render_template('template/manager.html', var1=numberOfTiles, var2=numberOfParts, var3=entropyTolerance, var4=numberOfWorkers)

    return render_template('template/manager.html', var1=numberOfTiles, var2=numberOfParts, var3=entropyTolerance, var4=numberOfWorkers)


@app.route("/numberOfTiles")
def getNumberOfTiles():
    return Flask.jsonify(numberOfTiles)
    
@app.route("/numberOfParts")
def getNumberOfParts():
    return Flask.jsonify(numberOfParts)

@app.route("/entropyTolerance")
def getEntropyTolerance():
    return Flask.jsonify(entropyTolerance)
    
@app.route("/numberOfWorkers")
def getNumberOfWorkers():
    return Flask.jsonify(numberOfWorkers)
    
@app.route("/restrictions")
def getRestrictions():
    return Flask.jsonify((tileCompatibilityList,tileCompatibilityLookUpTable,binaryLookUpTable))



# WAVE FUNCTION TILE LOOKUP TABLE
data = pd.read_excel("restrictions.xlsx", usecols="AI")

tileCompatibilityList = []
tileCompatibilityLookUpTable = {}

ind = 0

for tile in data.values:
    tileCompatibilityList.append(int(tile[0],2))
    tileCompatibilityLookUpTable[2**ind] = int(tile[0],2)
    ind += 1


                                
binaryLookUpTable = {"grass":0b000000001,
                     "wald":0b000000010,
                     "kuh":0b000000100,
                     "strand":0b000001000,
                     "wasser":0b000010000,
                     "fisch":0b000100000,
                     "berg":0b001000000,
                     "bergschnee":0b010000000,
                     "schneemann":0b100000000}
                     
                     
                     
