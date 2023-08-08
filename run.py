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

user_name = ""
notebook_column = 0
current_case = []
thief_dictionary = {}
stash_location = ""
pre_crime_location = ""

# Functions used throughout the running of the program

def update_notebook(entry):
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
    def __init__(self, case_name, item, event, crime_scene):
        self.case_name = case_name
        self.item = item
        self.event = event
        self.crime_scene = crime_scene
    
    def introduce(self):
       return f"Someone has stolen the {item} {event} at the {crime_scene}"        

# Initial sequence and introduction to game and case
def intro_and_setup():
    """
    Runs all the functions that happen prior to the main game beginning
    """
    initial_sequence()
    set_game()
    introduce_case()
    # welcome()

def initial_sequence():
    """
    Prints initial info to be seen when the user first loads the website
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
    global user_name
    print(developer)
    print(question_user)
    print(game_introduction)
    user_name = input("Please input your name to begin your new career as a detective:\n")
    # input to be validated including request for confirmation of name if
    # len(user_name) <3 or >20, or user_name.isaplpha()is False

def set_game():
    """
    Runs all the functions required to set-up a new game
    """
    date = str(get_date())
    new_notebook_entry(date)
    chosen_case_number = set_case()
    thief_name = set_thief(chosen_case_number)
    set_stash_and_precrime_locations(thief_name)

def get_date():
    """
    Gets and returns the current date
    """
    date = datetime.date.today()
    return date

def new_notebook_entry(date):
    """
    Locate the number of the next empty column within the notebook
    Update the global variable notebook_column with this number
    Call the update_notebook function passing it the argument date
    """
    global notebook_column
    notebook = SHEET.worksheet("notebook")
    top_row = notebook.row_values(1)
    number_columns = len(top_row)
    notebook_column = number_columns + 1
    update_notebook(date)

def set_case():
    """
    Calculates number of available cases and randomly chooses one
    Takes the: case_name, item, event, crime_scene for the chosen case from the cases sheet
    Adding to the global list variable current_case
    """
    cases = SHEET.worksheet("cases")
    column_one = cases.col_values(1)
    number_rows = len(column_one)
    number_cases = number_rows -1
    chosen_case_number = random.randrange(number_cases) +2
    global current_case
    for ind in range(1, 5):
        new_list_item = cases.cell(chosen_case_number, ind).value
        update_notebook(new_list_item)
        current_case.append(new_list_item)
    return chosen_case_number

def set_thief(chosen_case_number):
    """
    Randomly selects one of the three potential thieves for the chosen case
    update_notebook with the chosen_thief_number
    Creates a dictionary for the thief using the headings and values related to that thief
    from the cases sheet
    """
    cases = SHEET.worksheet("cases")
    case_row = cases.row_values(chosen_case_number)
    chosen_thief_number = random.randrange(3) +1
    update_notebook(chosen_thief_number)
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
    thief_details = []
    for ind in range(start_range, end_range):
        thief_detail = cases.cell(chosen_case_number, ind).value
        thief_details.append(thief_detail)
    headings = []
    for ind in range(start_range, end_range):
        heading = cases.cell(1, ind).value
        headings.append(heading)
    global thief_dictionary
    thief_dictionary = {headings[i]: thief_details[i] for i in range(len(headings))}
    return thief_dictionary['Thief']

def set_stash_and_precrime_locations(thief_name):
    """
    Retrieves the selected case's crime_scene
    Using the thief_name retrieves the thief's work, hobby and connection locations
    Randomly assignes two of the locations not being used as the crime scene as the stash and pre_crime locations
    """
    suspects = SHEET.worksheet("suspects")
    suspect_name_column = suspects.col_values(1)
    thief_row = suspect_name_column.index(thief_name) + 1
    work_location = suspects.cell(thief_row, 4).value
    hobby_location = suspects.cell(thief_row, 7).value
    connection_location = suspects.cell(thief_row, 9).value
    crime_scene = current_case[3]
    choose_locations_number = random.randrange(3)
    global stash_location
    global pre_crime_location
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
    update_notebook(stash_location)
    update_notebook(pre_crime_location)

def introduce_case():
    brief_welcome = f"You enter ??\n'You must be Junior detective {user_name}.\nI have heard great things about your detective skills.\nI hope you are eager to get started, as we’ve just had a new case come through …\n'"
    print(brief_welcome)
    #introduce case using a class of case
    accept_case = input("Do you wish to take on the case?” (y/n)\n")
    # input to be validated and input handled


intro_and_setup()
# Write your code to expect a terminal of 80 characters wide and 24 rows high
