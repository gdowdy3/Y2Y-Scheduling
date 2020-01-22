# Y2Y-Scheduling
This code can be used to efficiently assign volunteers to shifts at Y2Y Homeless Shelter.
Questions should be directed to Garrett (gdowdy3@gmail.com)

## Pre-requisites
To run this code, you need the following three (free!) pieces of software:
1. Python 3.7
    - You can download it here: https://www.python.org/downloads/
    - Be careful not to install Python 3.8, because ortools (see below) is not currently compatible with Python 3.8.
    - When installing, be sure you check the box indicating that python should be added to the system path.
2. pandas
    - Assuming that you installed "pip" when installing Python, pandas is installed by simplying entering the following in the command line: `pip install pandas`
3. ortools
    - Similarly, assuming that you installed "pip" when installing Python, ortools is installed by simplying entering the following in the command line: `pip install ortools` 


## Using the Code for the First Time
1. Create a directory on your computer to contain the code and the input/output files.  In what follows this directory will be called the "Working Directory".
2. Download the files from this repository into the Working Directory.
    - Click the green "Clone or download" button in the top left of the screen.
    - Select "Download ZIP" in the drop-down menu.
    - Save the zipped file to your Working Directory.
2. Extract the zipped file to the Working Directory.  Doing so will create a sub-directory in your Working Directory called "Y2Y-Scheduling".
3. Open up the command line console.
    - You can do this by typing `cmd` + `Enter` in the "Type here to search" bar on Windows.
4. Once you are in the console, navigate to the Y2Y-Scheduling directory
    - You can do this by: 
        - Navigating to the Y2Y-Scheduling directory in Windows Explorer 
        - Copying the full path to the directory from the bar at the top of the screen
        - Typing `cd <paste the path here>` in the console (do not include the <> arrows)
        - Pressing `Enter`
5. Enter `python ScheduleShifts.py` in the console.  This will run the code.
6. The recommended schedule will be printed in the console, together with some summary statistics.
7. The results are also stored more permanently in the "Shift-Focused Schedule.csv" and "Volunteer-Focused Schedule.csv" files in the Y2Y-Scheduling directory.
   
## Using the Code with Your Own Input Data
To use the code with your own input data, you just need to provide your own "Individual Preferences.csv" and "Group Volunteers.csv" files.  To do so:
1. Using Excel, create your own "Individual Preferences.csv" and "Group Volunteers.csv" files, using the provided files as examples for the required format of the data.
   - These files must be named exactly "Individual Preferences.csv" and "Group Volunteeers.csv"!
   - Their formatting must be exactly the same as the provided sample files!
2. Follow steps 4 - 6 in the previous section.

