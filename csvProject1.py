

import os.path
import shutil
import numpy as np
import pandas as pd
import csv
import sys
#---Global Variables----#
#where the master file resides
srcFile = #--SERVER LOCATION--#

#userHome is the local path of who ever is executing the script
userHome = os.path.expanduser('~')

#directory is the address of the parsed file and the copied master file: 'rbnusr25.dat'
directory = userHome + ##Put a desktop location here##

#The local version of 'rbnusr.dat' is set to the users local path
newSrc = directory + '/rbnusr25.dat'

globalName = '';
fullFileName = os.path.join(directory, globalName+ #Name of the file#
#A new file name is created. The parsed data will be put into this file    



#mergeData;
#Master file is copied to user's desktop to avoid overwriting masterfile.
def making_directory(address, file):
    
    try:
        os.mkdir(directory)
        file = shutil.copy(address, file)
        return file

    except: FileExistsError 
    sys.stdout.write("The folder has already been created. The proceed to formatting the data.");
    
def check_countries():

    Var = "";
    
    enteredInput= input("\nEnter the name of a country: ");
    

 #List of countries to choose from
    options= {
    'Ireland': ':IE ',  'Germany': ':DE ', 'Mexico': ':MX ', 'Korea': ':KR ', 'France': ':FR ', 'China' : ':CN ',
    'Signapore': ':SG ', 'Russia': ':RU ', 'Australia': ':AU ', 'United States' : ':US ', 'Austria': ':AT', 
    'India': ':IN ', 'Brazil': ':BR ', 'Turkey': ':TR ', 'Hungary': ':HU ', 'Colombia': ':CO ',
    'Belgium': ':BE ',  'Japan' : ':JP ', 'Czech Republic': ':CZ ', 'Malaysia:': ':MY ', 
    'Romania': ':RO ', 'Korea': ':KO ', 'Finland': ':FI ', 'Netherlands': ':NL ', 'Taiwan': ':TW ',
    'Portugal': ':PT ', 'Israel' : ':IL ', 'Bulgaria': ':BG ', 'United Kingdom' : ':GB ', 'Great Britain': ':GB ',
    'South Africa': ':ZA ', 'Egypt': ':EG ', 'Italy' : ':IT ', 'New Zealand' : ':NZ ', 'Thailand' : ':TH ',
    'Spain': ':ES ', 'Hong Kong': ':HK ', 'Sweden': ':SE '}

    for key, elem in options.items():
        if enteredInput == key:
         globalName ==  key;
         Var = elem;
    return Var;
def sorting_logic(rbnusr25, passedVariable):

    value = passedVariable;
  
    with open(rbnusr25, 'r') as f: 
    #The file 'formattedData.csv' is created. 'w' stands for writable. 
    #The file is only able to be writable to.
    #Link to docs if alteration needs to be made: 
    #https://docs.python.org/3/library/functions.html#open
    
       # if os.path.isfile(fullNameOfFile) != True:
        out = open(fullFileName,'w') 
       
    #for loop to check each row of the .dat file
        for line in f:
        #Each line is checked
        #finds the identifier for Irish users
            if value in line:
            # every chacter.contains(pattern 7)
            
            #parsing logic.
            #Delimitters are swamped. Whitespace is scrubbed.
          
                line = line.replace(' ', '')
               
                line = line.replace(':', ';')
                line = line.replace(',', ';')
           
            #'a' stands for appends. Data will be stacked under each other.
            #The name of the file is passed in as an argument.
            
                out = open(fullFileName,'a') 
          
            #data is being written to formattedData.csv. 
                out = out.write(line)
        
def add_mananger_row():

    employee = pd.read_csv(directory+ '/formattedData.csv', usecols=range(32), header=None, sep=";",engine='python') # read in the data
    original_rows = employee.shape[0] # original number of rows


    costCenter = directory + '/Cost_Centre_Final.XLSX';
    if os.path.exists(costCenter)!= True:
        #change to output to command line
        sys.stdout.write("You need to have Cost Center File in the folder")
        exit()

    
    managers = pd.read_excel(costCenter)
  
    managers= managers[['Cost Center','Profit Center','User ID', 'Description','Email address','Person Responsible']]
    #remove the first digit and make a new column
    managers['key'] = managers['Profit Center'].apply(lambda x: x[1:])

    # Convert the data in column 14 to strings so that it is matchable with the
    # manager data
    try:
        employee.loc[:, 'key'] = employee[15].apply(lambda x: str(int(x)) if not pd.isnull(x) else np.nan)
    except ValueError:
        pass  
        employee.loc[:, 'key'] = employee[15].apply(lambda x: str(str(x)) if not pd.isnull(x) else np.nan)
    except UnboundLocalError:
        employee.loc[:, 'key'] = employee[15].apply(lambda x: int(str(x)) if not pd.isnull(x) else np.nan)
    # Left join so that the rows that do not match are not dropped from employee
    # data
    merged_df = pd.merge(employee, managers, on='key', how='left')

    # Number of rows should be unchanged
    # This should print out True
 
#    print(pd.read_csv('merged_data.csv').head())
    merged_df = pd.merge(employee, managers, on='key', how='left')
    #merging phone number columns. If Phone num on clmn 28 fill empty rows in clm 27. 
    #Inplace means it is in numerical order
    merged_df[27].fillna(merged_df[28], inplace=True)
    #email columns are merged. Empty rows are filled with emails.
    merged_df[29].fillna(merged_df[30], inplace = True)
    
    #Dropping columns that do not contain relevant data. Along the X-axis. Inplace means that they are in numberical order.
    merged_df.drop(merged_df.columns[[1,4, 6, 8, 13, 14, 20, 24, 28,30, 31,33]], axis=1, inplace=True)    

    print(merged_df.shape[0] == original_rows)
    try:
        return merged_df.to_csv(directory+'merged_data.csv', index=False,sep=";", encoding='utf-8') 
    except PermissionError:
        return merged_df.to_csv(directory+'merged_data(1).csv', index=False, sep=";",encoding='utf-8') # Save

def redo():
     finishedFile = directory + 'merged_data.csv'
     finished = pd.read_csv(directory+ '/merged_data.csv',  header=None, sep=";",engine='python')
     return finished.to_csv(directory+'final_finished_data.csv', index=False, encoding='utf-8') 
 
making_directory(srcFile, directory)
passedVariable = check_countries()
sorting_logic(newSrc, passedVariable)
add_mananger_row()
