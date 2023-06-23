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
            currentTimes.append((df.iloc[i, 1], df.iloc[i, 2]))
            roomDict.update({df.iloc[i, 3]: currentTimes})
        #else if room not in dict
        else:
            #add room to dict with list of times
            roomDict[df.iloc[i, 3]] = [(df.iloc[i, 1], df.iloc[i, 2])]

    #Print statements delete later
    print("The loop worked?")
    for i in roomDict.get("Science Center 181"):
        print(i)
    
    return roomDict


def main(argv):
    #Read the excel file
    filename = argv[0]
    #TODO: check if it has .xlsx tag at the end
    print(filename)

    df = makeDF(filename)
    
    df = formatDF(df)

    roomDict = makeRoomDict(df)
    
    finaldf = pd.DataFrame(0, index = df['BLDG_RM1'].unique(), columns = list("MTWHF")) 
    #print(finaldf)

    return

if __name__ == "__main__":
    main(sys.argv[1:])
