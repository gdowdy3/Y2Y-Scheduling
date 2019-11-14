# Import the pandas library
import pandas as pd

# Import the OR-Tools library
from ortools.sat.python import cp_model

class Volunteer():
    # This class describes individual volunteers

    def __init__(self):
        self.ID_Number = 0
        self.FirstName = ''
        self.LastName = ''
        self.IsPreferredVolunteer = False
        self.ShiftPreferences = []

class VolunteerGroup():
    # This class describes volunteer groups

    def __init__(self):
        self.ID_Number = 0
        self.GroupName = ''
        self.AssignedShift = ''

class Shift():
    # This class describes volunteer groups

    def __init__(self):
        self.ShiftName = ''
        self.RequiredVolunteers = 0
        
def ReadInIndividualVolunteerData():
    # This function reads the preferences into a data frame

    # Specify the name of the csv file
    CSV_Name = 'Individual Preferences.csv'

    # Read in the data
    Data = pd.read_csv(CSV_Name)

    # Instantiate the list of volunteers
    Volunteers = []

    # Loop over the rows of data
    for (_, Row) in Data.iterrows():

        # Instantiate a new volunteer
        v = Volunteer()
    
        # Populate the volunteer's properties
        v.ID_Number = len(Volunteers)
        v.FirstName = Row['First Name']
        v.LastName = Row['Last Name']
        v.IsPreferredVolunteer = Row['Preferred Applicants']
        v.ShiftPreferences = [
            Row['1st Preference'],
            Row['2nd Preference'],
            Row['3rd Preference'],
            Row['4th Preference'],
            Row['5th Preference'],
        ]

        # Add this volunteer to the growing list
        Volunteers.append(v)

    # Return the list of volunteers
    return Volunteers

def ReadInGroupVolunteerData():
    # This function reads the preferences into a data frame

    # Specify the name of the csv file
    CSV_Name = 'Prefilled Shifts.csv'

    # Read in the data
    Data = pd.read_csv(CSV_Name)

    # Instantiate the list of volunteer groups
    VolunteerGroups = []

    # Loop over the rows of data
    for (_, Row) in Data.iterrows():
    
        # Instantiate a new volunteer group
        v = VolunteerGroup()

        # Populate the volunteer's properties
        v.ID_Number = len(VolunteerGroups) + 1
        v.GroupName = Row['Group']
        v.AssignedShift = Row['Shift']

        # Add this volunteer group to the growing list
        VolunteerGroups.append(v)

    # Return the list of volunteer groups
    return VolunteerGroups

def BuildShiftList():
    # This function builds a list of shift objects
    
    # Specify the days of the week
    Weekdays = [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday', 
        'Friday',
        'Saturday'
    ]

    # Specify the time periods
    Periods = [
        'Breakfast',
        'Dinner',
        'Evening',
        'Overnight'
    ]

    # Initialize the list of shifts
    Shifts = []
    for w in Weekdays:
        for p in Periods:

            # Construct the shift name corresponding to this weekday and period
            ShiftName = '%s %s' % (w, p)

            # Instantiate a new shift object
            s = Shift()

            # Add the shift's properties
            s.ShiftName = ShiftName
            s.RequiredVolunteers = 5

            # Add the shift to the growing list of shifts
            Shifts.append(s)

    # Return the list of shifts
    return Shifts

def BuildModel(IndividualVolunteers, Shifts):
    # This function builds the constraint programming model for the problem
    # Inputs:
    #   IndividualVolunteers = a list of volunteer objects.
    #   Shifts = a list of shift objects.
    # Outputs:
    #   model = a CP model object populated with decision variables, constraints, and an objective.

    # Instantiate the CP model
    model = cp_model.CpModel()

    # Create the model variables
    Assignment = {}
    for v in IndividualVolunteers:
        for s in Shifts:
            Assignment[(v,s)] = model.NewBoolVar('Volunteer %s assigned to %s shift' % (v.ID_Number,s.ShiftName))

    # Create the constraints
    ## Each shift has at most 5 volunteers assigned to it
    for s in Shifts:
        model.Add(
            sum(Assignment[(v,s)] for v in IndividualVolunteers) <= 5
        )

    ## Each volunteer is assigned to at most one shift
    for v in IndividualVolunteers:
        model.Add(
            sum(Assignment[(v,s)] for s in Shifts) <= 1
        )

    ## Each volunteer can only be assigned to the one of the shifts they indicated in their preference list
    for v in IndividualVolunteers:
        for s in Shifts:
            if not s.ShiftName in v.ShiftPreferences:
                model.Add(
                    Assignment[(v,s)] == 0
                )

    # Set the objective
    ## Maximize the number of covered shifts
    model.Maximize(
        sum(
            sum(
                Assignment[(v,s)] for v in IndividualVolunteers
            )
            for s in Shifts
        )
    )

    # Return the model
    return (model, Assignment)

def PrintShiftAssignments(solver, Assignment):
    # This function prints out a shift-centric view of the shift assignments
    # Inputs:
    #   solver = the CP solver object, which has already solved the model.
    #   Assignment = a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables
    
    # Loop over the shifts
    for s in Shifts:

        # Print the name of the shift
        print(s.ShiftName)

        for v in IndividualVolunteers:

            if solver.Value(Assignment[(v,s)]) == 1:

                # Print the volunteer's first and last name
                print('\t' + v.FirstName, v.LastName)

# Read in the individual volunteer data
IndividualVolunteers = ReadInIndividualVolunteerData()

# Read in the volunteer group data
GroupVolunteers = ReadInGroupVolunteerData()

# Build the list of shifts
Shifts = BuildShiftList()

# Build the constraint programming model
(model, Assignment) = BuildModel(IndividualVolunteers, Shifts)   # "Assignment" is a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables

# Create the solver and solve.
solver = cp_model.CpSolver()
solver.Solve(model)
    
# Print out the results
PrintShiftAssignments(solver, Assignment)






