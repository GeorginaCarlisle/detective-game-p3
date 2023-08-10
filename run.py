import gspread
from google.oauth2.service_account import Credentials
import datetime
import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('detective_game')

# Global variables
stash_location = ""
pre_crime_location = ""

# Functions used throughout the running of the program

def update_notebook(notebook_column, entry):
    """
    Takes the string to be entered into the notebook as a parameter
    Locates the next free cell in the column for this game
    Updates the cell with the string
    """
    notebook = SHEET.worksheet("notebook")
    current_column = notebook.col_values(notebook_column)
    number_rows = len(current_column)
    next_free_row = number_rows + 1
    notebook.update_cell(next_free_row, notebook_column, entry)

# Classes

class Case:
    def __init__(self, player_name, notebook_column, case_details, thief_details, crime_scene, pre_crime_location, stash_location):
        self.player_name = player_name
        self.notebook_column = notebook_column
        self.case_details = case_details
        self.thief_details = thief_details
        self.crime_scene = crime_scene
        self.pre_crime_location = pre_crime_location
        self.stash_location = stash_location

    def introduce_case(self):
        brief_welcome = f"You enter Case Closed Detective Agency\n'You must be Junior detective {self.player_name}.\nI have heard great things about your detective skills.\nI hope you are eager to get started, as we’ve just had a new case come through …'\n"
        print(brief_welcome)
        introduce_case = f"Someone has stolen the {self.case_details['item']} {self.case_details['event']} at the {self.case_details['crime_scene']}"
        print(introduce_case)
        accept_case = input("Do you wish to take on the case?” (y/n)\n")
        # input to be validated and input handled
        return accept_case

# Location class and associated classes
class Location:
    def __init__(self, location_name, description, employee, regulars, character_connection, work_witness):
        self.location_name = location_name
        self.description = description
        self.employee = employee
        self.regulars = regulars
        self.character_connection = character_connection
        self.work_witness = work_witness

    def enter_location(self):
        intro_location = f"You enter the {self.location_name} it is {self.description}"
        print(intro_location)

    def cctv_unconnected_location(self):
        intro_cctv_location = f"You review the cctv during the hours after the {self.item} was stolen.\nYou notice the following suspects at the {location_name}:"
        print (intro_cctv_stash)
        list_suspects = "list of suspects"
        # need to look at how it will work to gain suspect list from spreadsheet and how to then print
        summary_cctv_location = f"Nothing stands out as being suspicious."

    def look_around_location(self):
        intro_look_around = f"You quickly search the {self.location_name} if you want to do a more thorough search you will need to obtain a search warrant."
        print(intro_look_around)

    def look_around_unconnected_location(self):
        look_around_location(self)
        notice_nothing = f"As you look around you notice nothing that might connect with the crime "
        print(notice_nothing)

    def talk_witness_unconnected_location(self):
        question = f"You question the {self.work_witness}"
        print(question)
        response = f"I don't know that I can help you. {self.employee} works here {self.regulars} are often to be seen here. {character_connection} also pops in occasionally"
        print(response)

class Stash:
    def __init__(self, thief, crime_physcial_clue, item):
        self.thief = thief
        self.crime_physcial_clue = crime_physcial_clue
        self.item = item

    def cctv_stash_location(self):
        intro_cctv_stash = f"You review the cctv during the hours after the {self.item} was stolen.\nYou notice the following suspects at the {self.location_name}:"
        print (intro_cctv_stash)
        list_suspects = "list of suspects"
        # need to look at how it will work to gain suspect list from spreadsheet and how to then print
        suspicion_raised = f"You are immediately suspicious when the notice {self.thief} appear on the CCTV at an odd hour"
        print(suspicion_raised)

    def look_around_stash_location(self):
        look_around_location(self)
        notice_clue = f"As you look around you notice {self.crime_physcial_clue}. Now how did that end up here?"
        print(notice_clue)

    def talk_witness_stash_location(self):
        question = f"You question the {self.work_witness}"
        print(question)
        response = f"Well there was something odd.\nWhen I came in next morning I could have sworn that a couple of things seemed out of place.\nAs though someone had been in after we had locked up."
        print(response)

class Stash_location(Location, Stash):
    def __init__(self, location_name, description, employee, regulars, character_connection, work_witness, thief, crime_physcial_clue, item):
        Location.__init__(self, location_name, description, employee, regulars, character_connection, work_witness)
        Stash.__init__(self, thief, crime_physcial_clue, item)

# Initial sequence and introduction to game and case
def intro_and_setup():
    """
    Runs all the functions which provide an initial introduction to the game and set up a new case 
    The player's name is gained 
    A case, thief, stash location and pre_crime location are randomly chosen
    All game specific information is added to a new instance of the Case class
    The begin_game function is then called passing on the new instance
    """
    player_name = initial_sequence()
    date = str(get_date())
    notebook_column = new_notebook_entry(date)
    case_details = set_case(notebook_column)
    thief_details = set_thief(case_details, notebook_column)
    crime_scene_details = build_crime_scene_info(case_details)
    extra_locations = set_stash_and_precrime_locations(thief_details, case_details, notebook_column)
    pre_crime_location_details = build_pre_crime_location_info(extra_locations, thief_details, crime_scene_details)
    stash_location_details = build_stash_location_info(extra_locations, case_details, thief_details)
    current_case = Case(player_name, notebook_column, case_details, thief_details, crime_scene_details, pre_crime_location, stash_location)
    begin_game(current_case)

def initial_sequence():
    """
    Prints initial info to be seen when the user first loads the website:
    the game title image, developer info, a brief explanation of the game
    and an input request from the user to input their name to start the game.
    """
    title = """
Title name and art to be created
"""
    print(title)
    developer = "Created by Georgina Carlisle 2023\n"
    question_user = "Would you make a good detective?\nHave you got the skills to follow the clues, arrest the correct suspect and locate the stolen item? \n"
    game_introduction = "In ??? detective agency you will choose which locations to visit, who to interview, who to arrest and where to search for the stolen item.\nYour game data will be saved and used for development purposes, but no personal data will be kept and used outside of your game.\n"
    print(developer)
    print(question_user)
    print(game_introduction)
    player_name = input("Please input your name to begin your new career as a detective:\n")
    return player_name
    # input to be validated including request for confirmation of name if
    # len(user_name) <3 or >20, or user_name.isaplpha()is False

def get_date():
    """
    Gets and returns the current date
    """
    date = datetime.date.today()
    return date

def new_notebook_entry(date):
    """
    Locate the number of the next empty column within the notebook
    Call the update_notebook function passing it the arguments notebook_column and date
    Return the notebook_column number
    """
    notebook = SHEET.worksheet("notebook")
    top_row = notebook.row_values(1)
    number_columns = len(top_row)
    notebook_column = number_columns + 1
    update_notebook(notebook_column, date)
    return notebook_column

def set_case(notebook_column):
    """
    Calculates number of available cases and randomly chooses one
    Takes the: case_name, item, event and crime_scene for the chosen case from the cases sheet
    Adds these values to the notebook and
    Uses them to create and a return a dictionary
    """
    cases = SHEET.worksheet("cases")
    column_one = cases.col_values(1)
    number_rows = len(column_one)
    number_cases = number_rows - 1
    chosen_case_number = random.randrange(number_cases) + 2
    case_name = cases.cell(chosen_case_number, 1).value
    update_notebook(notebook_column, case_name)
    item = cases.cell(chosen_case_number, 2).value
    update_notebook(notebook_column, item)
    event = cases.cell(chosen_case_number, 3).value
    update_notebook(notebook_column, event)
    crime_scene = cases.cell(chosen_case_number, 4).value
    update_notebook(notebook_column, crime_scene)
    crime_physcial_clue = cases.cell(chosen_case_number, 11).value
    case_details = {
        "case_number": chosen_case_number,
        "case_name": case_name,
        "item": item,
        "event": event,
        "crime_scene": crime_scene,
        "crime_physcial_clue": crime_physcial_clue
    }
    return case_details

def set_thief(case_details, notebook_column):
    """
    Randomly selects one of the three potential thieves for the chosen case
    Creates a dictionary for the thief using the headings and values related to that thief from the cases sheet
    Updates the notebook with the thief's name
    Returns the thief dictionary
    """
    cases = SHEET.worksheet("cases")
    chosen_thief_number = random.randrange(3) + 1
    if chosen_thief_number == 1:
        start_range = 12
        end_range = 17
    elif chosen_thief_number == 2:
        start_range = 17
        end_range = 22
    elif chosen_thief_number == 3:
        start_range = 22
        end_range = 27
    else:
        print("ERROR!!")
    chosen_case_number = case_details['case_number']
    thief_details = []
    for ind in range(start_range, end_range):
        thief_detail = cases.cell(chosen_case_number, ind).value
        thief_details.append(thief_detail)
    headings = []
    for ind in range(start_range, end_range):
        heading = cases.cell(1, ind).value
        headings.append(heading)
    thief_dictionary = {headings[i]: thief_details[i] for i in range(len(headings))}
    update_notebook(notebook_column, thief_dictionary['Thief'])
    return thief_dictionary

def build_crime_scene_info(case_details):
    """
    Creates a dictionary of information linked to the crime_scene and returns
    """
    cases = SHEET.worksheet("cases")
    chosen_case_number = case_details["case_number"]
    location_name = case_details["crime_scene"]
    suspects = cases.cell(chosen_case_number, 7).value
    clue_detail = cases.cell(chosen_case_number, 8).value
    witness = cases.cell(chosen_case_number, 9).value
    witness_report = cases.cell(chosen_case_number, 10).value
    item = case_details["item"]
    plea = cases.cell(chosen_case_number, 6).value
    timeline = cases.cell(chosen_case_number, 5).value
    event = case_details["event"]
    crime_scene_details = {
       "location_name": location_name,
       "suspects": suspects,
       "clue_detail": clue_detail,
       "witness": witness,
       "witness_report": witness_report,
       "item": item,
       "plea": plea,
       "timeline": timeline,
       "event": event 
    }
    return crime_scene_details

def set_stash_and_precrime_locations(thief_details, case_details, notebook_column):
    """
    Retrieves the selected case's crime_scene
    Using the thief_name retrieves the thief's work, hobby and connection locations
    Randomly assignes two of the locations not being used as the crime scene as the stash and pre_crime locations
    """
    thief_name = thief_details['Thief']
    suspects = SHEET.worksheet("suspects")
    suspect_name_column = suspects.col_values(1)
    thief_row = suspect_name_column.index(thief_name) + 1
    work_location = suspects.cell(thief_row, 4).value
    hobby_location = suspects.cell(thief_row, 7).value
    connection_location = suspects.cell(thief_row, 9).value
    crime_scene = case_details['crime_scene']
    choose_locations_number = random.randrange(3)
    if choose_locations_number == 0:
        if work_location != crime_scene:
            stash_location = work_location
            pre_crime_location = hobby_location
        else:
            stash_location = hobby_location
            pre_crime_location = connection_location
    if choose_locations_number == 1:
        if hobby_location != crime_scene:
            stash_location = hobby_location
            pre_crime_location = connection_location
        else:
            stash_location = connection_location
            pre_crime_location = work_location
    if choose_locations_number == 2:
        if connection_location != crime_scene:
            stash_location = connection_location
            pre_crime_location = work_location
        else:
            stash_location = work_location
            pre_crime_location = hobby_location
    update_notebook(notebook_column, stash_location)
    update_notebook(notebook_column, pre_crime_location)
    return [stash_location, pre_crime_location]

def build_pre_crime_location_info(extra_locations, thief_details, crime_scene_details):
    """
    Retrieves pre_crime location_name from extra_locations list
    Accesses the location spreadsheet and thief_details to locate all associated info
    Adds pre_crime_physical_clue info to crime_scene_details
    Builds a dictionary of information for the pre_crime_location
    Returns dictionary
    """
    location_name = extra_locations[1]
    locations = SHEET.worksheet("locations")
    location_name_column = locations.col_values(1)
    pre_crime_location_row = location_name_column.index(location_name) + 1
    description = locations.cell(pre_crime_location_row, 2).value
    employee = locations.cell(pre_crime_location_row, 3).value
    regulars = locations.cell(pre_crime_location_row, 4).value
    character_connection = locations.cell(pre_crime_location_row, 5).value
    work_witness = locations.cell(pre_crime_location_row, 6).value
    pre_crime = thief_details['Pre-crime evidence']
    pre_crime_physical_clue = locations.cell(pre_crime_location_row, 7).value
    crime_scene_details['pre_crime_physical_clue'] = pre_crime_physical_clue
    pre_crime_location_details = {
        "location_name": location_name,
        "description": description,
        "employee": employee,
        "regulars": regulars,
        "character_connection": character_connection,
        "work_witness": work_witness,
        "pre_crime": pre_crime,
    }
    return pre_crime_location_details

def build_stash_location_info(extra_locations, case_details, thief_details):
    """
    Retrieves stash location_name from extra_locations list
    Accesses the location spreadsheet, thief_details and case_details to locate all associated info
    Builds a dictionary of information for the stash_location
    Returns dictionary
    """
    location_name = extra_locations[0]
    locations = SHEET.worksheet("locations")
    location_name_column = locations.col_values(1)
    stash_location_row = location_name_column.index(location_name) + 1
    description = locations.cell(stash_location_row, 2).value
    employee = locations.cell(stash_location_row, 3).value
    regulars = locations.cell(stash_location_row, 4).value
    character_connection = locations.cell(stash_location_row, 5).value
    work_witness = locations.cell(stash_location_row, 6).value
    thief = thief_details['Thief']
    crime_physcial_clue = case_details['crime_physcial_clue']
    item = case_details['item']
    stash_location_details = {
        "location_name": location_name,
        "description": description,
        "employee": employee,
        "regulars": regulars,
        "character_connection": character_connection,
        "work_witness": work_witness,
        "thief": thief,
        "crime_physcial_clue": crime_physcial_clue,
        "item": item
    }
    return stash_location_details

def begin_game(current_case):
    """
    Runs functions to indroduce the case and welcome the user
    this includes explaining how the game works
    If the user doesn't accept the case, the game_over function is called
    """
    accept_case = current_case.introduce_case()
    if accept_case == "y":
        welcome(current_case)
    elif accept_case == "n":
        game_over("case_not_accepted")
    else:
        print("Error!!")



def welcome(current_case):
    main_welcome = "'Fantastic! I do love an enthusiastic detective. Sorry I almost forgot:\nWelcome to the ??? detective agency. My name is ??? and\nI will be keeping a close eye on your work during this case.\nWe pride ourselves here at ? on having the best detectives in the area.\nThis is your chance to show us you deserve a place on the team."
    print(main_welcome)
    print("")
    print("")
    game_explanation = "Throughout the case you will access to:\na map of the area, which you can use to select a location you would like to visit,\na notebook containing all the clues you have discovered\nand a list of possible suspects, which you can use to question a suspect (a maximum of two), and arrest the thief (we don’t tolerate false arrests here at ??)\nWhen you know where the thief hid the item obtain a search warrant to hunt for the missing item (we have never failed to find a missing item before).\nI’m sure you will keep our reputation high and resolve this case swiftly'\n"
    print(game_explanation)
    print("Where would you like to start?/n")
    main_action_options()

# Main game functions

def main_action_options(current_case):
    """
    Prints the main actions the player can choose from: map, notebook, suspect list or search warrant
    Handles player input and calls the associated functions
    """
    action = input("view map (m), view notebook (n), view suspect list (s) or obtain a search warrant (w)\n")
    # input to be validated
    if action == "m":
        view_map()
    elif action == "n":
        view_notebook()
    elif action == "s":
        view_suspect_list()
    elif action == "w":
        obtain_search_warrant()
    else:
        print("ERROR!!")

def view_map():
    """
    Prints the map title, intro and a list of all the locations
    Requests that user choose one of the locations or chooses to return to the main options
    Handles user input and either calls the main options or calls visit_location 
    passing the chosen location number adjusted to represent the location's row number in the sheet
    """
    print("Map title to be created")
    print("A map of the area shows the following notable locations:")
    locations = SHEET.worksheet("locations")
    for ind in range(1, 9):
        row = ind + 1
        location = locations.cell(row, 1).value
        print(f"{ind} - {location}")
    action = input("Please type in the number of the location you would like to visit.\n Alternatively type (r) to return to the main options\n")
    # input to be validated
    if action == "1" or "2" or "3" or "4" or "5" or "6" or "7" or "8":
        action = int(action) + 1
        check_location_type(action)
    elif action == "r":
        main_action_options()
    else:
        print("ERROR!!!")

def view_notebook():
    print("notebook reached")

def view_suspect_list():
    print("suspect_list reached")

def obtain_search_warrant():
    print("search warrant reached")

def check_location_type(location_number):
    """
    Checks the location chosen to see how it needs handling and calls one of the following functions
    visit_stash_location, visit_pre_crime_location, visit_crime_scene_location
    """
    locations = SHEET.worksheet("locations")
    location_name = locations.cell(location_number, 1).value
    update_notebook(f"You visted {location_name}")
    if location_name == stash_location:
        visit_stash_location(location_number)
    elif location_name == pre_crime_location:
        visit_pre_crime_location(location_number)
    elif location_name == current_case.crime_scene:
        visit_crime_scene_location(location_number)
    else:
        visit_location(location_number)
    # need to look at what's going to happen with the work location

def visit_location(location_number):
    """
    Takes the chosen location_number as an argument and uses to create an instance of Location
    Uses the methods of the Location class to allow the user to explore the location
    """
    # Find values and create a new instance of Location
    locations = SHEET.worksheet("locations")
    location_name = locations.cell(location_number, 1).value
    description = locations.cell(location_number, 2).value
    employee = locations.cell(location_number, 3).value
    regulars = locations.cell(location_number, 4).value
    character_connection = locations.cell(location_number, 5).value
    work_witness = locations.cell(location_number, 6).value
    current_location = Location(location_name, description, employee, regulars, character_connection, work_witness)
    # Instance created actions follow below
    current_location.enter_location()

def visit_stash_location(location_number):
    """
    Takes the chosen location_number as an argument and uses to create an instance of Stash_location
    Uses the methods of the Location and Stash classes to allow the user to explore the location
    """
    # Find values and create a new instance of Stash_location
    locations = SHEET.worksheet("locations")
    location_name = locations.cell(location_number, 1).value
    description = locations.cell(location_number, 2).value
    employee = locations.cell(location_number, 3).value
    regulars = locations.cell(location_number, 4).value
    character_connection = locations.cell(location_number, 5).value
    work_witness = locations.cell(location_number, 6).value
    thief = thief_dictionary['Thief']
    # Need to figure through a way to location crime_physical_clue detail
    crime_physcial_clue = "need to locate"
    item = current_case.item
    current_location = Stash_location(location_name, description, employee, regulars, character_connection, work_witness, thief, crime_physcial_clue, item)
    # Instance created actions follow below
    current_location.enter_location()
    first_action = location_action_options()
    if first_action == "c":
        current_location.cctv_stash_location()
    elif first_action == "l":
        current_location.look_around_stash_location()
    elif first_action == "t":
        current_location.talk_witness_stash_location()
    else:
        print("ERROR!!")

def visit_pre_crime_location(location_number):
    print("This is the pre_crime location")

def visit_crime_scene_location(location_number):
    print("This is the crime_scene")

def location_action_options():
    print("Would you like to:")
    choice = input("check the cctv (c), look around (l), talk to a witness (t)\nAlternatively type (r) to return to the main options\n")
    # input to be validated
    if choice == "r":
        main_action_options()
    else:
        return choice

intro_and_setup()
# Write your code to expect a terminal of 80 characters wide and 24 rows high
