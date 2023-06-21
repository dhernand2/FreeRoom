import pandas as pd
import sys
#installed pandas, openpyxl
#Names of files to use: testsheet, 202302CSV.xlsx
def main(argv):
    #Read the excel file
    filename = argv[0]
    #TODO: check if it has .xlsx tag at the end
    print(filename)

    #Read the excel file into a dataframe using the specific columns
    df = pd.read_excel(filename, usecols="N:P")

    #Remove rows that had NaN since they don't have a time
    df = df.dropna()

    #Kohlberg
    #df[df['A'].str.contains("hello")]

    keepstr = ["Kohlberg"]
    #df1 = df[~(df['Courses'] == "PySpark")].index 
    #df1 = df[~(df['BLDG_RM1'] == 'Matchbox FITNESS')].index Keeps all rows that have the str given

    #This line keeps all rows that contain 'Kohlberg' in its 'BLDG_RM1' col 
    notValidRooms = ["Lang Perf Arts Ctr", "Matchbox", "Off Campus", "TBA", "Whittier", "Lang Music", 
        "Ware", "Fieldhouse", "Mullan Tennis", "Lodges", "Tarble GYM", "Wister Center"]
    df = df[~(df['BLDG_RM1'].str.contains('|'.join(notValidRooms)))]
    #Reset the table indices
    df = df.reset_index()
    #print(df)
    print(df.shape)


    #where 1 is the day, 2 is the time, 3 is the room
    #rowz = df.iloc[0, 1]
    #print(rowz)
    
    roomDict = {}
    #dfSize = df.shape
    #print(dfSize[0])
    #print(df.iloc[0, 3])
    count = 0
    for i in range (df.shape[0]):
        #if room already in dic
        if df.iloc[i, 3] in roomDict:
            #get the list, append new item, update val in dic
            #print("a")
            currentTimes = roomDict.get(df.iloc[i, 3])
            currentTimes.append((df.iloc[i, 1], df.iloc[i, 2]))
            roomDict.update({df.iloc[i, 3]: currentTimes})
            count += 1
        #else if room not in dict
        else:
            #add room to dic with list of times
            #print("b")
            roomDict[df.iloc[i, 3]] = [(df.iloc[i, 1], df.iloc[i, 2])]
            count += 1


    print("The loop worked?")
    print("count is %d" % (count))
    #print(roomDict.keys())
    #for i in roomDict.keys():
     #   print(i)
    
    for i in roomDict.get("Science Center 181"):
        print(i)
    
    finaldf = pd.DataFrame(0, index = df['BLDG_RM1'].unique(), columns = list("MTWHF")) 
    #print(finaldf)


    return

if __name__ == "__main__":
    main(sys.argv[1:])
