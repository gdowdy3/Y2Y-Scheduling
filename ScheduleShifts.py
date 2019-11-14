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
        self.PreferredShifts = []
        self.ShiftPreferencePoints = {}

    def CalculateShiftPreferencePoints(self, Shifts):

        # Instantiate the dictionary of shift preference points
        self.ShiftPreferencePoints = {}

        # Initialize a point value of zero for each shift
        for s in Shifts:
            self.ShiftPreferencePoints[s] = 0

        # Assign preference points for each of the volunteer's preferred shifts
        for s in Shifts:
            
            # Check if the current shift is in the volunteer's list of preferred shifts
            if not s in self.PreferredShifts:  # then it's not there

                # Assign 0 preference points to this shift for this volunteer
                self.ShiftPreferencePoints[s] = 0

            else: # the shift *is* in the volunteer's list of preferred shifts

                # Find the position of the shift in the list
                Index = self.PreferredShifts.index(s)

                # Find the length of the list
                ListLength = len(self.PreferredShifts)

                # Calculate the number of points corresponding to this index
                self.ShiftPreferencePoints[s] = ListLength - Index  # Index = 0 ==> max points,  Index = Max Index ==> 1 point

class VolunteerGroup():
    # This class describes volunteer groups

    def __init__(self):
        self.ID_Number = 0
        self.GroupName = ''
        self.AssignedShift = ''

class Shift():
    # This class describes shifts

    def __init__(self):
        self.ShiftName = ''
        self.RequiredVolunteers = 0

class Period():
    # This class describes periods

    def __init__(self, Name, RequiredVolunteers):
        self.Name = Name
        self.RequiredVolunteers = RequiredVolunteers
        
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
    
        # Assign an ID Number to the volunteer
        v.ID_Number = len(Volunteers)
        
        # Read in most of the volunteer's properties
        v.FirstName = Row['First Name']
        v.LastName = Row['Last Name']
        v.IsPreferredVolunteer = Row['Preferred Applicants']
        v.PreferredShifts = [
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

def BuildShiftDictionary():
    # This function builds a dictionary of shift objects, where the dictionary keys are the shift names
    
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

    # Create the list of periods
    Periods = [
        Period(Name='Breakfast', RequiredVolunteers=4),
        Period(Name='Dinner', RequiredVolunteers=3),
        Period(Name='Evening', RequiredVolunteers=5),
        Period(Name='Overnight', RequiredVolunteers=2),
    ]

    # Initialize the dictionary of shifts
    Shifts = {}
    for w in Weekdays:
        for p in Periods:

            # Construct the shift name corresponding to this weekday and period
            ShiftName = '%s %s' % (w, p.Name)

            # Instantiate a new shift object
            s = Shift()

            # Add the shift's properties
            s.ShiftName = ShiftName
            s.RequiredVolunteers = p.RequiredVolunteers

            # Add the shift to the growing dictionary of shifts
            Shifts[ShiftName] = s

    # Return the list of shifts
    return Shifts

def BuildModel(IndividualVolunteers, Shifts):
    # This function builds the constraint programming model for the problem
    # Inputs:
    #   IndividualVolunteers = a list of volunteer objects.
    #   Shifts = a dictionary of shift objects, indexed by shift names
    # Outputs:
    #   model = a CP model object populated with decision variables, constraints, and an objective.

    # Instantiate the CP model
    model = cp_model.CpModel()

    # Create the model variables
    Assignment = {}
    for v in IndividualVolunteers:
        for s in Shifts:
            Assignment[(v,s)] = model.NewBoolVar('Volunteer %s assigned to %s shift' % (v.ID_Number,s))

    # Create the constraints
    ## Each shift has at most 5 volunteers assigned to it
    for s in Shifts:
        model.Add(
            sum(Assignment[(v,s)] for v in IndividualVolunteers) <= Shifts[s].RequiredVolunteers
        )

    ## Each volunteer is assigned to at most one shift
    for v in IndividualVolunteers:
        model.Add(
            sum(Assignment[(v,s)] for s in Shifts) <= 1
        )

    ## Each volunteer can only be assigned to the one of the shifts they indicated in their preference list
    for v in IndividualVolunteers:
        for s in Shifts:
            if not s in v.PreferredShifts:
                model.Add(
                    Assignment[(v,s)] == 0
                )

    # Set the objective
    ## Define the weights of the various objectives
    Weight = {
        'Maximize the number of covered shifts' : 1,
        'Respect the volunteer preferences' : 1,
    }

    ## Define the objective
    model.Maximize(

        # Maximize the number of covered shifts
        Weight['Maximize the number of covered shifts'] *
        sum(
            sum(
                Assignment[(v,s)] for v in IndividualVolunteers
            )
            for s in Shifts
        )

        +

        # Maximize the number of realized shift preference points
        Weight['Respect the volunteer preferences'] *
        sum(
            sum(
                Assignment[(v,s)] * v.ShiftPreferencePoints[s]
                for v in IndividualVolunteers
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
        print(s)

        for v in IndividualVolunteers:

            if solver.Value(Assignment[(v,s)]) == 1:

                # Print the volunteer's first and last name
                print('\t' + v.FirstName, v.LastName)

# Build the list of shifts
Shifts = BuildShiftDictionary()

# Read in the individual volunteer data
IndividualVolunteers = ReadInIndividualVolunteerData()

# Read in the volunteer group data
GroupVolunteers = ReadInGroupVolunteerData()

# Calculate the number of preference points each volunteer associates with each shift
for v in IndividualVolunteers:
    v.CalculateShiftPreferencePoints(Shifts)

# Build the constraint programming model
(model, Assignment) = BuildModel(IndividualVolunteers, Shifts)   # "Assignment" is a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables

# Create the solver and solve.
solver = cp_model.CpSolver()
solver.Solve(model)
    
# Print out the results
PrintShiftAssignments(solver, Assignment)






