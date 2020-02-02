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

                # Check if this is a preferred volunteer
                if self.IsPreferredVolunteer == True: 

                    # Increase the points
                    self.ShiftPreferencePoints[s] = self.ShiftPreferencePoints[s] * 2  # This ensures preferential treatment for preferred volunteers

class VolunteerGroup():
    # This class describes volunteer groups

    def __init__(self):
        self.ID_Number = 0
        self.GroupName = ''
        self.AssignedShift = ''
        self.Volunteers = 0

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
            Row['6th Preference']
        ]

        # Add this volunteer to the growing list
        Volunteers.append(v)

    # Return the list of volunteers
    return Volunteers

def ReadInGroupVolunteerData():
    # This function reads the preferences into a data frame

    # Specify the name of the csv file
    CSV_Name = 'Group Volunteers.csv'

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
        v.Volunteers = Row['Volunteers']

        # Add this volunteer group to the growing list
        VolunteerGroups.append(v)

    # Return the list of volunteer groups
    return VolunteerGroups

def DisaggregateVolunteerGroups(GroupVolunteers, IndividualVolunteers):
    # Inputs:
    #   GroupVolunteers = a list of VolunteerGroup objects
    #   IndividualVolunteers = a list of individual volunteer objects
    # Outputs:
    #   Creates a number of individual volunteers for each VolunteerGroup and adds these individuals to the list of individual volunteers

    # Loop over the volunteer groups
    for g in GroupVolunteers:

        # Cap the number of volunteers in this group at the number required by their preferred shift
        g.Volunteers = min(g.Volunteers, Shifts[g.AssignedShift].RequiredVolunteers)

        # Create an individual volunteer object for each volunteer in this group
        for VolunteerIndex in range(g.Volunteers):

            # Instantiate a new individual volunteer
            v = Volunteer()

            # Assign an ID Number to the volunteer
            v.ID_Number = len(IndividualVolunteers)

            # Create a placeholder for the name of the volunteer
            v.FirstName = g.GroupName
            v.LastName = 'Volunteer %d' % (VolunteerIndex + 1)

            # Specify them as a preferred volunteer
            v.IsPreferredVolunteer = True

            # Specify their first preference for a shift as the group's preference
            v.PreferredShifts = [ g.AssignedShift ]

            # Specify their other preferences as empty
            for _ in range(4):
                v.PreferredShifts.append('')

            # Add this individual to the list of volunteers
            IndividualVolunteers.append(v)

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
        Period(Name='Breakfast', RequiredVolunteers=8),
        Period(Name='Dinner', RequiredVolunteers=6),
        Period(Name='Evening', RequiredVolunteers=5),
        Period(Name='Overnight', RequiredVolunteers=4),
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
    ## Primary decision variables
    Assignment = {}
    for v in IndividualVolunteers:
        for s in Shifts:
            Assignment[(v,s)] = model.NewBoolVar('Volunteer %s assigned to %s shift' % (v.ID_Number,s))

    # Create the constraints
    ## Each shift has a maximum number of volunteers assigned to it
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
        'Maximize the shift coverage' : 10,
        'Respect the volunteer preferences' : 1,
    }

    ## Calculate the scalar required to make everything integer
    Scalar = CalcObjectiveScalar(Shifts)  # This is multiplied in because the CP solver insists on the data being integer.

    ## Define the objective
    model.Maximize(

        # Maximize the number of covered shifts
        Weight['Maximize the shift coverage'] *
        sum(
            int(Scalar / Shifts[s].RequiredVolunteers) *
            sum(
                Assignment[(v,s)] 
                for v in IndividualVolunteers
            )
            for s in Shifts
        )

        +

        # Maximize the number of realized shift preference points
        Weight['Respect the volunteer preferences'] *
        Scalar *
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

def CalcObjectiveScalar(Shifts):

    # Get the list of unique "Required Volunteer" numbers
    UniqueList = GetUniqueListElements(
        [Shifts[s].RequiredVolunteers for s in Shifts]
    )

    # Calculate the product of this list
    p = ListProd(UniqueList)

    # Round the product to an integer
    Scalar = int(p)

    # Return the scalar
    return Scalar

def ListProd(List):

    # Initialize the product
    p = 1

    # Loop over the elements of the list
    for e in List:

        p = p * e

    return p

def GetUniqueListElements(List):

    # Initialize the list of unique elements
    UniqueList = []

    # Loop over the list
    for e in List:

        # Check if it's in the Unique list
        if not e in UniqueList: # it's not there

            # Add it
            UniqueList.append(e)
    
    # Return the unique list
    return UniqueList

def PrintShiftAssignments(solver, Assignment, Shifts):
    # This function prints out a shift-centric view of the shift assignments
    # Inputs:
    #   solver = the CP solver object, which has already solved the model.
    #   Assignment = a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables
    #   Shifts = a dictionary of Shift objects
    
    # Loop over the shifts
    for s in Shifts:

        # Print the name of the shift
        print(s)

        for v in IndividualVolunteers:

            if solver.Value(Assignment[(v,s)]) == 1:

                # Print the volunteer's first and last name
                print('\t' + v.FirstName, v.LastName)

def PrintSummaryStatistics(solver, Assignment, Shifts):
    # This function prints out several statistics summarizing the quality of the shift assignment found by the optimizer
    # Inputs:
    #   solver = the CP solver object, which has already solved the model.
    #   Assignment = a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables
    #   Shifts = a dictionary of Shift objects

    # Calculate the fraction of the staffing requirements that have been fulfilled
    ## Initialize the count of desired assignments
    AssignmentsRequired = 0

    ## Initialize the count of assignments realized
    AssignmentsRealized = 0

    ## Initialize the count of preferred assignments realized
    PreferredAssignmentsRealized = 0

    ## Count the number of preferred volunteers
    PreferredVolunteers = 0
    for v in IndividualVolunteers:

        # Check if this is a preferred volunteer
        if v.IsPreferredVolunteer == True:

            # Increment the count of preferred volunteers
            PreferredVolunteers += 1

    ## Initialize the count of under-staffed shifts
    UnderStaffedShifts = 0

    ## Loop over the shifts
    for s in Shifts:

        # Increment the staffing requirements
        AssignmentsRequired += Shifts[s].RequiredVolunteers

        # Initialize the count of volunteers assigned to this shift
        AssignmentsForShift = 0

        # Loop over each of the volunteers
        for v in IndividualVolunteers:

            # Check if they were assigned to the current shift
            if solver.Value(Assignment[(v,s)]) == 1:  # They were assigned to the current shfit

                # Increment the count of assignments realized
                AssignmentsRealized += 1

                # Increment the count of assignments for this particular shift
                AssignmentsForShift += 1

                # Check if this is a preferred volunteer
                if v.IsPreferredVolunteer == True:

                    # Increment the count of preferred assignments realized
                    PreferredAssignmentsRealized += 1

        # Check if this shift is under-staffed
        if AssignmentsForShift < Shifts[s].RequiredVolunteers: # this shift is under-staffed

            # Increment the count of under-staffed shifts
            UnderStaffedShifts += 1

    ## Calculate the fraction of required assignments that were realized
    FractionOfRequirementsRealized = AssignmentsRealized / AssignmentsRequired

    ## Calculate the fraction of under-staffed shifts
    FractionOfUnderStaffedShifts = UnderStaffedShifts / len(Shifts)

    ## Calculate the fraction of volunteers assigned
    FractionOfVolunteersAssigned = AssignmentsRealized / len(IndividualVolunteers)

    ## Calculate the fraction of preferred volunteers assigned
    FractionOfPreferredVolunteersAssigned = PreferredAssignmentsRealized / PreferredVolunteers

    ## Print the results
    print('\nStaffing requirements covered: %1.1f%%.' % (FractionOfRequirementsRealized * 100))

    print('Shifts fully covered: %1.1f%%.' % ((1- FractionOfUnderStaffedShifts) * 100))

    print('Volunteers assigned to a shift: %1.1f%%.' % (FractionOfVolunteersAssigned * 100))

    print('Preferred volunteers assigned to a shift: %1.1f%%.' % (FractionOfPreferredVolunteersAssigned * 100))

def ExportVolunteerFocusedSchedule(solver, Assignment, Shifts):
    # This function exports a shift-centric CSV of the shift assignments
    # Inputs:
    #   solver = the CP solver object, which has already solved the model.
    #   Assignment = a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables
    #   Shifts = a dictionary of Shift objects

    # Import the necessary libraries
    import csv
    import sys

    # Specify the name of the file to be exported
    FileName = 'Volunteer-Focused Schedule.csv'

    # Create the file
    with open(FileName, mode='w') as f:

        # Instantiate the csv writer
        if 'win' in sys.platform:  # Check for windows
            Writer = csv.writer(f, delimiter=',', lineterminator = '\n')
        else:
            Writer = csv.writer(f, delimiter=',')

        # Add the header line
        ## Intialize the header line
        HeaderLine = ['Volunteer', 'Assignment']

        ## Write the header line to the csv
        Writer.writerow(HeaderLine)

        # Add the line for each volunteer
        for v in IndividualVolunteers:

            # Initialize the line with the volunteer's first and last name
            Line = [ '%s %s' % (v.FirstName, v.LastName) ]

            # Initialize the flag indicating whether or not an assignment has been found
            AssignmentFound = False

            # Loop over each shift
            for s in Shifts:

                # Check if the volunteer was assigned to the current shift
                if solver.Value(Assignment[(v,s)]) == 1:  # They were assigned to the current shfit

                    # Print the shift's name
                    Line.append( '%s' % s )

                    # Raise the flag indicating that an assignment has been found
                    AssignmentFound = True

            # Check if an assignment was found
            if AssignmentFound == False:

                # Print a message indicating that no assignement was found
                Line.append( 'Unassigned' )

            # Write out the line for the current volunteer
            Writer.writerow(Line)

def ExportShiftFocusedSchedule(solver, Assignment, Shifts):
    # This function exports a shift-centric CSV of the shift assignments
    # Inputs:
    #   solver = the CP solver object, which has already solved the model.
    #   Assignment = a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables
    #   Shifts = a dictionary of Shift objects

    # Import the necessary libraries
    import csv
    import sys

    # Specify the name of the file to be exported
    FileName = 'Shift-Focused Schedule.csv'

    # Create the file
    with open(FileName, mode='w') as f:

        # Instantiate the csv writer
        if 'win' in sys.platform:  # Check for windows
            Writer = csv.writer(f, delimiter=',', lineterminator = '\n')
        else:
            Writer = csv.writer(f, delimiter=',')

        # Construct the header line
        ## Intialize the header line
        HeaderLine = ['Shift']

        ## Calculate the maximum number of volunteers required in any given shift
        MaxVolunteersPerShift = max( [s.RequiredVolunteers for s in Shifts.values()] )
 
        ## Add a column for each possible volunteer
        for v in range(1, MaxVolunteersPerShift + 1):

            # Add the header for the vth volunteer
            HeaderLine.append( 'Volunteer %s' % str(v) )

        ## Add a column for notes
        HeaderLine.append( 'Notes' )

        ## Write the header line to the csv
        Writer.writerow(HeaderLine)

        # Add the line for each shift
        for s in Shifts:

            # Initialize the line with the name of the shift
            Line = [s]

            # Initialize the count of volunteers assigned to this shift
            VolunteersAssigned = 0

            # Loop over the volunteers
            for v in IndividualVolunteers:

                # Check if they were assigned to the current shift
                if solver.Value(Assignment[(v,s)]) == 1:  # They were assigned to the current shfit

                    # Print the volunteer's first and last name
                    Line.append( '%s %s' % (v.FirstName, v.LastName) )

                    # Increment the count of volunteers assigned
                    VolunteersAssigned += 1

            # Check for under-staffing
            if VolunteersAssigned < Shifts[s].RequiredVolunteers: # this is an under-staffed shift

                # Add the appropriate number of empty strings
                for _ in range(MaxVolunteersPerShift - VolunteersAssigned):
                    Line.append(' ')

                # Add the warning about under-staffing
                Line.append('Warning: this shift is under-staffed.')

            # Write out the line for the current shift
            Writer.writerow(Line)

# Build the list of shifts
Shifts = BuildShiftDictionary()

# Read in the individual volunteer data
IndividualVolunteers = ReadInIndividualVolunteerData()

# Read in the volunteer group data
GroupVolunteers = ReadInGroupVolunteerData()

# Break the volunteer groups down into individuals
DisaggregateVolunteerGroups(GroupVolunteers, IndividualVolunteers)

# Calculate the number of preference points each volunteer associates with each shift
for v in IndividualVolunteers:
    v.CalculateShiftPreferencePoints(Shifts)

# Build the constraint programming model
(model, Assignment) = BuildModel(IndividualVolunteers, Shifts)   # "Assignment" is a dictionary mapping (volunteer, shift) tuples to binary assignment decision variables

# Create the solver and solve.
solver = cp_model.CpSolver()
solver.Solve(model)
    
# Print out the results
PrintShiftAssignments(solver, Assignment, Shifts)
PrintSummaryStatistics(solver, Assignment, Shifts)

# Write the results to a CSV file
ExportShiftFocusedSchedule(solver, Assignment, Shifts)
ExportVolunteerFocusedSchedule(solver, Assignment, Shifts)






