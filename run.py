import gspread
from google.oauth2.service_account import Credentials
import datetime

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

# Initial sequence and introduction to game and case
def intro_and_setup():
    """
    Runs all the functions that happen prior to the main game beginning
    """
    initial_sequence()
    set_game()
    # introduce_case()
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
    # choose case, thief and stash location and set variables/classes for these

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

intro_and_setup()
# Write your code to expect a terminal of 80 characters wide and 24 rows high
