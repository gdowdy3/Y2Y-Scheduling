# Y2Y-Scheduling
This code can be used to efficiently assign volunteers to shifts at Y2Y Homeless Shelter.

## Pre-requisites
1. Python
2. pandas
3. ortools


## Using the Code for the First Time
1. Download the files from this repository.
5. Test run the code
    - Click on the **Y2Y-Scheduling** folder.
    - Click on the **Y2Y Shift Assignment.ipnyb** file.  It should open in a new tab in your browser.
    - Follow the instructions there.
    - If you see a "Dead Kernel" error message, do the following:
        - Navigate back to the **Dashboard**.
        - Click on the **Packages** button.
        - Click on the **Yours** tab.
        - Click the yellow **Reset** button.
        - Return to the browser tab containing the code.
        - Click on **Kernel** in the options bar at the top of the screen.
        - In the drop-down menu, click **Restart Kernel & Clear All**.
        - Try again to run the code.
6. Inspect the output.
    - If the code ran successfully, it should have produced two files in the Y2Y-Scheduling Folder:
      - "Shift Focused Output.csv"
      - "Volunteer Focused Output.csv"
    - Save these files to your computer.
      - Check the box next to the first file.
      - Click the **Download** button that appears above when you do so.
      - Save it to a convenient location.
      - Repeat for the second file.
   - Open the files using Excel and manipulate them as you see fit (e.g., resizing and renaming columns).
   
   
## Using the Code with Your Own Input Data
To use the code with your own input data, you just need to provide your own "Individual Preferences.csv" and "Prefilled  Shifts.csv" files.  To do so:
1. Using Excel, create your own "Individual Preferences.csv" and "Group Volunteers.csv" files, using the provided files as examples for the required format of the data.
   - These files must be named exactly "Individual Preferences.csv" and "Group Volunteeers.csv"!
   - Their formatting must be exactly the same as the provided sample files!
2. Open up the command line console.
    - You can do this by typing `cmd` + `Enter` in the "Type here to search" bar on Windows.
3. In the console, navigate to the directory containing the .csv input files and the "ScheduleShifts.py" script.
    - You can do this by navigating to the directory in Windows explorer, copying the path from the bar at the top of the screen, and then entering `cd <paste the path here>` in the console.
4. Enter `python ScheduleShifts.py` in the console.  This will run the code.

