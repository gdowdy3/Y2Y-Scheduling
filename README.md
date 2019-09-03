# Y2Y-Scheduling
This code can be used to efficiently assign volunteers to shifts at Y2Y Homeless Shelter.

## Using the Code for the First Time
1.  Go to www.juliabox.com.  Everything that follows in the instructions below will be done there. Use GitHub (this website) only to consult these instructions.
2.  Sign in via LinkedIn, GitHub, or Google.
3.  Click the big blue **Launch** button.
4.  Clone this repository from GitHub.
    - In the top right corner of the screen, click the **New** button.  From the dropdown menu, click **Terminal**.  Doing so will open a new tab in your browser showing a black terminal screen.
    - Enter the following three commands in the terminal (Tip: You can paste into the terminal by right-clicking and selecting *Paste*):
        - `cd /home/jrun` This ensures that you are in the right directory in the terminal for cloning.
        - `git clone https://github.com/gdowdy3/Y2Y-Scheduling.git` This clones the GitHub respository to JuliaBox.
        - `cp -R /home/jrun/Y2Y-Scheduling /mnt/juliabox` This copies the cloned repository to another directory.
    - Close the browser tab containing the terminal.
    - Return to the **JuliaBox** tab.
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
1. Using Excel, create your own "Individual Preferences.csv" and "Prefilled  Shifts.csv" files, using the provided files as examples for the required format of the data.
   - These files must be named exactly "Individual Preferences.csv" and "Prefilled  Shifts.csv"!
   - Their formatting must be exactly the same as the provided sample files!
2. In JuliaBox, navigate to the Y2Y-Scheduling folder.
3. Click the **Upload** button in the top right corner of the screen.
4. In the pop-up window, find and select the first file you want to upload, and click the **Open** button.
5. Repeat steps 3. and 4. for the second file.
6. Click the blue **Upload** buttons next to each file.
7. Overwrite any pre-existing files of the same.
8. Run the code, as in step 4. of the previous section.
