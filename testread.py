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
        "Ware", "Fieldhouse", "Mullan Tennis"]
    df = df[~(df['BLDG_RM1'].str.contains('|'.join(notValidRooms)))]
    #Reset the table indices
    df = df.reset_index()
    print(df)
    print(df.shape)
    return

if __name__ == "__main__":
    main(sys.argv[1:])
