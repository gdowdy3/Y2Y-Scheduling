# Y2Y-Scheduling
This code can be used to efficiently assign volunteers to shifts at Y2Y Homeless Shelter.

## Pre-requisites
1. Python 3.7
    - You can download it here: https://www.python.org/downloads/
    - Be careful not to install Python 3.8, because ortools (see below) is not currently compatible with Python 3.8.
2. pandas
    - Assuming that you installed "pip" when installing Python, pandas is installed by simplying entering the following in the command line: `pip install pandas`
3. ortools
    - Similarly, assuming that you installed "pip" when installing Python, ortools is installed by simplying entering the following in the command line: `pip install ortools` 


## Using the Code for the First Time
1. Download the files from this repository.
2. Work in progress
   
   
## Using the Code with Your Own Input Data
To use the code with your own input data, you just need to provide your own "Individual Preferences.csv" and "Group Volunteers.csv" files.  To do so:
1. Using Excel, create your own "Individual Preferences.csv" and "Group Volunteers.csv" files, using the provided files as examples for the required format of the data.
   - These files must be named exactly "Individual Preferences.csv" and "Group Volunteeers.csv"!
   - Their formatting must be exactly the same as the provided sample files!
2. Save these files in the same directory as the "ScheduleShifts.py" script.  In what follows, this directory will be referred to as the "Working Directory". 
3. Open up the command line console.
    - You can do this by typing `cmd` + `Enter` in the "Type here to search" bar on Windows.
4. Once you are in the console, navigate to the Working Directory
    - You can do this by: 
        - Navigating to the directory in Windows Explorer 
        - Copying the path from the bar at the top of the screen
        - Typing `cd <paste the path here>` in the console (do not include the <> arrows)
        - Pressing `Enter`
4. Enter `python ScheduleShifts.py` in the console.  This will run the code.

