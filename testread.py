import pandas as pd
import sys
#installed pandas, openpyxl
#Names of files to use: testsheet, 202302CSV.xlsx

"""
makeDF
Parameters: filename, a string that contains the name of the excel file to read
Purpose: Sets up a dataframe (df) using only the columns N:P which should be:
    N: Days
    O: Time1
    P: BLDG_RM1

Returns df, a dataframe containing columns N, O, and P
"""
def makeDF(filename):
    #Read the excel file into a dataframe using the specific columns
    df = pd.read_excel(filename, usecols="N:P")
    return df 


"""
formatDF
Parameters: df, a dataframe
Purpose: takes the original dataframe (df) to do the following:
    1. Remove rows that have NaN
    2. Remove rooms that are not considered to be classrooms
    3. Reset the index of the dataframe after the above changes are made
Rooms considered not to be valid classrooms are assigned to the variable 'notValidRooms'

Returns df, a dataframe that contains only "valid" classrooms
"""
def formatDF(df):
    #Remove rows that had NaN since they don't have a time
    df = df.dropna()
    
    #List of rooms that are not considered to be "valid" classrooms. 
    notValidRooms = ["Lang Perf Arts Ctr", "Matchbox", "Off Campus", "TBA", "Whittier", "Lang Music", 
        "Ware", "Fieldhouse", "Mullan Tennis", "Lodges", "Tarble GYM", "Wister Center"]
    
    #Get the df that contains the rooms not mentioned in notValidRooms
    df = df[~(df['BLDG_RM1'].str.contains('|'.join(notValidRooms)))]

    #Reset the table indices
    df = df.reset_index()
    
    #The following are print statements to see the dataframe and its contents, and the dimensions
    #print(df)
    #print(df.shape)
    return df


"""
makeRoomDict
Parameters: df, a dataframe that contains valid classrooms along with their room #, and Day & Time
Purpose: creates a dictionary where:
    * The keys are the classroom numbers and 
    * The values are a list of tuples where:
        * The tuples are composed of (day, time)
Returns roomDict, a dictionary following the specification above
"""
def makeRoomDict(df):
    #where 1 is the day, 2 is the time, 3 is the room

    roomDict = {}
    for i in range (df.shape[0]):
        #if room already in dict
        if df.iloc[i, 3] in roomDict:
            #get the value, append new item, update val in dic
            currentTimes = roomDict.get(df.iloc[i, 3])
            lstOfTimes = sepTimes((df.iloc[i, 1], df.iloc[i, 2]))
            currentTimes.extend(lstOfTimes)
            roomDict.update({df.iloc[i, 3]: currentTimes})
        #else if room not in dict
        else:
            lstOfTimes = sepTimes((df.iloc[i, 1], df.iloc[i, 2]))
            roomDict[df.iloc[i, 3]] = lstOfTimes
    #Print statements delete later
    print("The loop worked?")
    for i in roomDict.get("Science Center 181"):
        print(i[0])
    
    return roomDict


"""
sepTimes
Parameters: tplTime, a tuple made as a (day, time) pair
Purpose: seperate times that for which the day value contains mutiple days (MW, MWF, etc...)
into a set of tuples where each day value contains just one day (M, some time), (W, some time) etc.
In the case that the day value is already in a single day format, we add tplTime to lstOfTimes
Returns lstOfTimes, a list of tuples with times seperated 
"""

def sepTimes(tplTime):
    lstOfTimes = []
    #print("Day is: " + tplTime[0])
    if "MWF" in tplTime:
        lstOfTimes.append(("M", tplTime[1]))
        lstOfTimes.append(("W", tplTime[1]))
        lstOfTimes.append(("F", tplTime[1]))
    elif "MW" in tplTime:
        lstOfTimes.append(("M", tplTime[1]))
        lstOfTimes.append(("W", tplTime[1]))
    elif "MF" in tplTime:
        lstOfTimes.append(("M", tplTime[1]))
        lstOfTimes.append(("F", tplTime[1]))
    elif "TTH" in tplTime:
        lstOfTimes.append(("T", tplTime[1]))
        lstOfTimes.append(("TH",tplTime[1]))
    elif "TWTHF" in tplTime:
        lstOfTimes.append(("T", tplTime[1]))
        lstOfTimes.append(("W", tplTime[1]))
        lstOfTimes.append(("TH",tplTime[1]))
        lstOfTimes.append(("F", tplTime[1]))
    elif "UMTWTHF" in tplTime:
        lstOfTimes.append(("M", tplTime[1]))
        lstOfTimes.append(("T", tplTime[1]))
        lstOfTimes.append(("W", tplTime[1]))
        lstOfTimes.append(("TH",tplTime[1]))
        lstOfTimes.append(("F", tplTime[1]))
    else:
         lstOfTimes.append(tplTime)
    return lstOfTimes


"""
setTime
Parameters: roomDict, a dictionary whose keys are classrooms and values are a list of tuples
made as a (day, time) pair
Purpose: populate a set of dictionaries (Mon, Tues, Weds, Thurs, Fri) where:
    * The keys are the classrooms
    * The values are the times in which the rooms are in use

Additional notes 
keep a container for free times
Range for free time is from 8:00AM to 10:00PM
For each room:
    Find the tuples
    Look at tuple m[0]
    Locate the proper dict to add the room, time 

End
"""
def setTime(roomDict):
    for room,times in roomDict.items():
        #given a tuple, a room and a list of tuples containing (day, time)
        for i in times:
            #given a tuple containing (day, time) MTWTHF
            #if (i[0] = "M"):
            print(i)
            #else:
    return



"""
saveTimes
Parameters: none
Purpose: create a file containing the times in which the rooms are being used
Return: nothing, 
"""
def saveTimes(roomDict):
    safe = 1
    while (safe != 0):
        filename = input("Enter a name for the file: ")
        try:
            f = open(filename, "x")
            safe = 0
        except:
            print("That filename already exists")
            response = input("Enter another name: ")
    for x, y in roomDict.items():
        f.write(x + ": " + str(y) + "\n")
    f.close()
    return


def main(argv):
    global Mon, Tues, Weds, Thurs, Fri
    Mon, Tues, Weds, Thurs, Fri = {}, {}, {}, {}, {}
    #Read the excel file
    filename = argv[0]
    #TODO: check if it has .xlsx tag at the end
    print(filename)

    df = makeDF(filename)
    
    df = formatDF(df)

    roomDict = makeRoomDict(df)
    

    ####Testing stuff delete later
    #rooms = roomDict.keys()
    #for i in rooms:
     #   print(i)
    ###


    #This should make the final df where the index are the rooms, and the col go M-F
    #finaldf = pd.DataFrame(0, index = df['BLDG_RM1'].unique(), columns = list("MTWHF")) 
    finaldf = pd.DataFrame.from_dict(roomDict, orient='index')
    #print(finaldf)
    #saveTimes(roomDict)

    setTime(roomDict)
    return

if __name__ == "__main__":
    main(sys.argv[1:])
