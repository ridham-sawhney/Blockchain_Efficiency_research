import csv
import random
from math import remainder
stakersArray = []
blockchain = []


#======================================================================================

def convertCSV(Dataset, csv_file, csv_columns):
    stakers_dict = Dataset
    csv_columns = ['staker', 'blocks', 'age', 'faults', 'time', 'priority', 'eligible']

    # csv_file = "BlockchainCSV_Equation1.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in stakers_dict:
                writer.writerow(data)
        response = {
            'message': 'File Saved to CSV'
        }
        return True
        # return jsonify(response), 200
    except IOError:
        response = {
            'message': 'I/O error'
        }
        return False
        # return jsonify(response), 404
        # print("I/O error")


#======================================================================================
def optimizeRows():
    rows = []
    for block in blockchain:
        for staker in block["stakers"]:
            rows.append(staker)
    return rows


#======================================================================================
def generateStakers(num):
    for num in range(num):

        newdetails = {
            'staker': "S" + str(num),
            'blocks': 0,
            'age': 0,
            'faults': 0,
            'time': 1,
            'priority': 0,
            'eligible': 0,

        }
        stakersArray.append(newdetails)
        newdetails = {}




#======================================================================================
def simulateValidation(block):

    stakerDetails = []

    for staker in stakersArray:
        equation = calculateEquation(staker)
        staker["priority"]=equation
        staker["age"] = staker["age"] + 1
        # print(staker["blocks"])
        if staker["blocks"] % 3 == 0:
          staker["faults"]=staker["blocks"]*0.30

        _eligible=1
        #print(staker["faults"])

        if staker['blocks'] < 20:
            _eligible=1

        if staker['blocks'] >=20 & staker['blocks']<=40:
            if staker['faults'] > 0.8 *staker['blocks']:
                _eligible=0

        if staker['blocks'] > 40:
            # if staker['faults'] > 0.3 * staker['blocks']:
            #     staker['time'] = staker['time'] + 0.5
            #     _eligible=1
            #print(0.25*staker["blocks"])
            if staker['faults'] >= staker["blocks"]*0.30:
                _eligible=0


        details = {
            "staker": staker["staker"],
            'blocks': staker["blocks"],
            'age': staker["age"],
            'faults': staker["blocks"]/2,
            'time': staker["time"],
            'priority': equation,
            'eligible': _eligible
        }
        stakerDetails.append(details)
        details = {}

    sorted_stakers = sorted(stakerDetails, key=lambda i: i["priority"],reverse=True)


    top8 = []

    for index in range(8):
        top8.append(sorted_stakers[index])

    print("Winner For Block " + str(block) + " is " + top8[0]["staker"] + " value was " + str(top8[0]["priority"]))



    updateWinnerStakerDetails(top8[0])


    return top8


#======================================================================================

def simulateBlocks(blocks):
    for b in range(blocks):
        newblock = {
            "Block": b,
            "stakers": simulateValidation(b)
        }
        blockchain.append(newblock)
        newblock = {}

#======================================================================================
def updateWinnerStakerDetails(winner):
    random.seed(3)
    for staker in stakersArray:
        if (staker["staker"] == winner["staker"]):
            staker["blocks"] = staker["blocks"] + 1
            staker["time"] = staker["time"] + random.random()
            staker["age"] = 0

        if (staker["staker"] != winner["staker"]):
            staker["age"] = staker["age"]+1;

#======================================================================================
def calculateEquation(staker):
    if staker["blocks"] == 0 or staker["time"] == 0:
        time_per_block = 0
    else:
        time_per_block = staker["blocks"] / staker["time"]


    equation = staker["age"] + ((staker["blocks"] / staker["time"]) / ((2 ** staker["faults"] )* 100))*100

    return equation
#======================================================================================


generateStakers(8)
#======================================================================================
simulateBlocks(15000)
#======================================================================================

convertCSV(optimizeRows(), "Blockchain_Testing_Dataset_1.csv", ['staker', 'blocks', 'age', 'faults', 'time', 'priority', 'eligible'])