import pandas as pd
import sys
#installed pandas, openpyxl
#Names of files to use: testsheet, 202302CSV.xlsx

"""
make_df
Parameters: file_name, a string that contains the name of the excel file to read
Purpose: Sets up a dataframe (df) using only the columns N:P which should be:
    N: Days
    O: Time1
    P: BLDG_RM1

Returns df, a dataframe containing columns N, O, and P
"""
def make_df(file_name):
    #Read the excel file into a dataframe using the specific columns
    df = pd.read_excel(file_name, usecols="N:P")
    return df 


"""
format_df
Parameters: df, a dataframe
Purpose: takes the original dataframe (df) to do the following:
    1. Remove rows that have NaN
    2. Remove rooms that are not considered to be classrooms
    3. Reset the index of the dataframe after the above changes are made
Rooms considered not to be valid classrooms are assigned to the variable 'not_valid_rooms'

Returns df, a dataframe that contains only "valid" classrooms
"""
def format_df(df):
    #Remove rows that had NaN since they don't have a time
    df = df.dropna()
    
    #List of rooms that are not considered to be "valid" classrooms. 
    not_valid_rooms = ["Lang Perf Arts Ctr", "Matchbox", "Off Campus", "TBA", "Whittier", "Lang Music", 
        "Ware", "Fieldhouse", "Mullan Tennis", "Lodges", "Tarble GYM", "Wister Center"]
    
    #Get the df that contains the rooms not mentioned in not_valid_rooms
    df = df[~(df['BLDG_RM1'].str.contains('|'.join(not_valid_rooms)))]

    #Reset the table indices
    df = df.reset_index()
    
    #The following are print statements to see the dataframe and its contents, and the dimensions
    #print(df)
    #print(df.shape)
    return df


"""
make_room_dict
Parameters: df, a dataframe that contains valid classrooms along with their room #, and Day & Time
Purpose: creates a dictionary where:
    * The keys are the classroom numbers and 
    * The values are a list of tuples where:
        * The tuples are composed of (day, time)
Returns room_dict, a dictionary following the specification above
"""
def make_room_dict(df):
    #where 1 is the day, 2 is the time, 3 is the room

    room_dict = {}
    for i in range (df.shape[0]):
        #if room already in dict
        if df.iloc[i, 3] in room_dict:
            #get the value, append new item, update val in dic
            current_times = room_dict.get(df.iloc[i, 3])
            lst_of_times = sep_times((df.iloc[i, 1], df.iloc[i, 2]))
            current_times.extend(lst_of_times)
            room_dict.update({df.iloc[i, 3]: current_times})
        #else if room not in dict
        else:
            lst_of_times = sep_times((df.iloc[i, 1], df.iloc[i, 2]))
            room_dict[df.iloc[i, 3]] = lst_of_times
    #Print statements delete later
    """
    print("The loop worked?")
    for i in room_dict.get("Science Center 181"):
        print(i[0])
    """
    return room_dict


"""
sep_times
Parameters: tpl_time, a tuple made as a (day, time) pair
Purpose: seperate times that for which the day value contains mutiple days (MW, MWF, etc...)
into a set of tuples where each day value contains just one day (M, some time), (W, some time) etc.
In the case that the day value is already in a single day format, we add tpl_time to lst_of_times
Returns lst_of_times, a list of tuples with times seperated 
"""

def sep_times(tpl_time):
    lst_of_times = []
    #print("Day is: " + tpl_time[0])
    if "MWF" in tpl_time:
        lst_of_times.append(("M", tpl_time[1]))
        lst_of_times.append(("W", tpl_time[1]))
        lst_of_times.append(("F", tpl_time[1]))
    elif "MW" in tpl_time:
        lst_of_times.append(("M", tpl_time[1]))
        lst_of_times.append(("W", tpl_time[1]))
    elif "MF" in tpl_time:
        lst_of_times.append(("M", tpl_time[1]))
        lst_of_times.append(("F", tpl_time[1]))
    elif "TTH" in tpl_time:
        lst_of_times.append(("T", tpl_time[1]))
        lst_of_times.append(("TH",tpl_time[1]))
    elif "TWTHF" in tpl_time:
        lst_of_times.append(("T", tpl_time[1]))
        lst_of_times.append(("W", tpl_time[1]))
        lst_of_times.append(("TH",tpl_time[1]))
        lst_of_times.append(("F", tpl_time[1]))
    elif "UMTWTHF" in tpl_time:
        lst_of_times.append(("M", tpl_time[1]))
        lst_of_times.append(("T", tpl_time[1]))
        lst_of_times.append(("W", tpl_time[1]))
        lst_of_times.append(("TH",tpl_time[1]))
        lst_of_times.append(("F", tpl_time[1]))
    else:
         lst_of_times.append(tpl_time)
    return lst_of_times


"""
set_time
Parameters: room_dict, a dictionary whose keys are classrooms and values are a list of tuples
made as a (day, time) pair
Purpose: populate a set of dictionaries (mon, tues, weds, thurs, fri) where:
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
def set_time(room_dict):
    for room,times in room_dict.items():
        #given a tuple, a room and a list of tuples containing (day, time)
        for i in times:
            #given a tuple containing (day, time) MTWTHF
            if (i[0] == "M"):
                add_items(mon, (room, i[1]))
            elif (i[0] == "T"):
                add_items(tues, (room, i[1]))
            elif (i[0] == "W"):
                add_items(weds, (room, i[1]))
            elif (i[0] == "TH"):
                add_items(thurs, (room, i[1]))
            else:
                add_items(fri, (room, i[1]))
    """
    for i,j in fri.items():
        print(i,j)
    """
    return

"""
"""
def add_items(container, item):
    if item[0] in container:
        set_of_values = container.get(item[0])
        set_of_values.append(item[1])
        container.update({item[0]: set_of_values})
    else:
        container[item[0]] = [item[1]]





"""
save_times
Parameters: info_to_save, a tuple where [0] is the name for the Dictionary and [1] is the actual dictionary
Purpose: create a file containing the times in which the rooms are being used on a specific day
Return: nothing
"""
def save_times(info_to_save):
    try:
        f = open(info_to_save[0], "x")
    except:
        print("A file containing the times for: %s, already exists. Please delete it and try again" % info_to_save[0])
        exit()
    for x, y in info_to_save[1].items():
        f.write(x + ": " + str(y) + "\n")
    f.close()
    return


def main(argv):
    global mon, tues, weds, thurs, fri
    mon, tues, weds, thurs, fri = {}, {}, {}, {}, {}
    dictionary_pair = [
        ("Monday Times.txt", mon), 
        ("Tuesday Times.txt", tues), 
        ("Wednesday Times.txt", weds), 
        ("Thursday Times.txt", thurs), 
        ("Friday Times.txt", fri)
        ]
    #Read the excel file
    file_name = argv[0]
    #TODO: check if it has .xlsx tag at the end
    #print(file_name)

    df = make_df(file_name)
    
    df = format_df(df)

    room_dict = make_room_dict(df)
    

    ####Testing stuff delete later
    #rooms = room_dict.keys()
    #for i in rooms:
     #   print(i)
    ###


    #This should make the final df where the index are the rooms, and the col go M-F
    #final_df = pd.DataFrame(0, index = df['BLDG_RM1'].unique(), columns = list("MTWHF")) 
    final_df = pd.DataFrame.from_dict(room_dict, orient='index')
    #print(final_df)
    #save_times(room_dict)

    set_time(room_dict)
    for i in dictionary_pair:
        save_times(i)

    return

if __name__ == "__main__":
    main(sys.argv[1:])
