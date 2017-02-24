import os.path
import shutil
import numpy as np
import pandas as pd
#---Variables----#

#where the master file resides
#Enter file path in srcFile variable.
srcFile = '.....'

#userHome is the local path of who ever is executing the script
userHome = os.path.expanduser('~')

#Full user path can be entered below
masterFileEmployee = os.path.join(userHome+'/Desktop/...')


#directory is the address of the parsed file and the copied master file: 'MasterFile.dat'
directory = userHome + '/Desktop/...'

#The local version of 'rbnusr.dat' is set to the users local path
newSrc = directory + 'MasterFile.dat'

#A new file name is created. The parsed data will be put into this file 
fullNameOfFile = os.path.join(directory, 'formattedData'+'.csv')

#Master file is copied to user's desktop to avoid overwriting masterfile.

def making_directory(address, file):
    os.mkdir(directory)
    file = shutil.copy(address, file)
    return file
	
def add_mananger_row():
    fN= os.path.join(directory+'formattedData.csv')
    employee = pd.read_csv(fN, usecols=range(32), header=None, sep=",",engine='python') # read in the data
    original_rows = employee.shape[0] # original number of rows
    managers = pd.read_excel(masterFileEmployee)
    managers= managers[['Cost Center','Profit Center','User ID', 'Description','Email address','Person Responsible']]
    # remove the first digit and make a new column
    managers['key'] = managers['Profit Center'].apply(lambda x: x[1:])
    # Convert the data in column 15 to strings so that it is matchable with the
    # manager data
    employee.loc[:, 'key'] = employee[15].apply(lambda x: str(int(x)) if not pd.isnull(x) else np.nan)
    # Left join so that the rows that do not match are not dropped from employee
    # data
    merged_df = pd.merge(employee, managers, on='key', how='left')
    #merging phone number columns. If Phone num. on clmn 28 fill empty rows in clm 27. 
    #Inplace means it is in numerical order
    merged_df[27].fillna(merged_df[28], inplace=True)
    #email columns are merged. Empty rows are filled with emails.
    merged_df[29].fillna(merged_df[30], inplace = True)
    #Dropping columns that do not contain relevant data. Along the X-axis. Inplace means that they are in numberical order.
    merged_df.drop(merged_df.columns[[0,4, 6, 8, 13, 14, 20, 24, 28,30, 31,33]], axis=1, inplace=True)
    # Number of rows should be unchanged
    # This should print out True
    print(merged_df.shape[0] == original_rows)
    return merged_df.to_csv(directory+'merged_data.csv', index=False, encoding='utf-8') # Save
	
def sorting_logic(MasterFile):
    with open(newSrc, 'r') as f: 
    #The file 'formattedData.csv' is created. 'w' stands for writable. 
    #The file is only able to be writable to.
    #Link to docs if alteration needs to be made: 
    #https://docs.python.org/3/library/functions.html#open
	
        out = open(fullNameOfFile,'w+') 
    #for loop to check each row of the .dat file
	
        for line in f:
        #Each line is checked
        #finds the identifier for Irish users
		
            if ':IE ' in line:
            # every chacter.contains(pattern 7)
            #parsing logic.
            #Delimitters are swamped. Whitespace is scrubbed.
			
                line = line.replace(' ', '')
                line = line.replace(':', ',')
				
            #'a' stands for appends. Data will be stacked under each other.
            #The name of the file is passed in as an argument.
			
                out = open(fullNameOfFile,'a+') 
				
            #data is being written to formattedData.csv. 
			
                out = out.write(line)
				
making_directory(srcFile, directory)
sorting_logic(newSrc)
add_mananger_row()