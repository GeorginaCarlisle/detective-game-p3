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

# Functions used throughout the running of the program

def update_notebook(notebook_row, *entries):
    """
    Takes the current game's notebook_column as a parameter along with
    and *args object containing the entries to be added into the notebook
    Locates the next free cell in the column for this game
    Updates the cell with the string
    """
    # Locate the number of the next free column in this game's row
    notebook = SHEET.worksheet("notebook")
    notebook_row_list = notebook.row_values(notebook_row)
    number_columns = len(notebook_row_list)
    next_free_column = number_columns
    print(next_free_column)
    # check the number of entries to be added
    list_entries = list(entries[0])
    print(list_entries)
    number_of_entries = len(list_entries)
    print(number_of_entries)
    # Calculate the column range in letters where the new entries are to be added
    alphabet_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    start_column_letter = alphabet_list[next_free_column]
    print(start_column_letter)
    end_column_number = next_free_column + number_of_entries
    end_column_letter = alphabet_list[end_column_number]
    print(end_column_letter)
    # Add new entries to the notebook
    notebook.update(f'{start_column_letter}{notebook_row}:{end_column_letter}{notebook_row}', [list_entries])

# Classes

class Case:
    def __init__(self, player_name, notebook_column, case_details, thief_details, pre_crime_location, stash_location):
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

    def welcome(self):
        main_welcome = "'Fantastic! I do love an enthusiastic detective. Sorry I almost forgot:\nWelcome to Case Closed Detective Agency. My name is ??? and\nI will be keeping a close eye on your work during this case.\nWe pride ourselves here at Case Closed on being able to solve and close every case we are given.\nThis is your chance to show us you deserve a place on the team."
        print(main_welcome)
        print("")
        print("")
        game_explanation = "Throughout the case you will access to:\na map of the area, which you can use to select a location you would like to visit,\na notebook containing all the clues you have discovered\nand a list of possible suspects, which you can use to question a suspect (a maximum of two), and arrest the thief (we don’t tolerate false arrests here at Case Closed)\nWhen you know where the thief hid the item obtain a search warrant to hunt for the missing item (we have never failed to find a missing item before).\nI’m sure you will keep our reputation high and resolve this case swiftly'\n"
        print(game_explanation)
        print("Where would you like to start?\n")

    def set_stash_location(self):
        location_name = self.stash_location["location_name"]
        description = self.stash_location["description"]
        employee = self.stash_location["employee"]
        regulars = self.stash_location["regulars"]
        character_connection = self.stash_location["character_connection"]
        work_witness = self.stash_location["work_witness"]
        thief = self.stash_location["thief"]
        crime_physcial_clue = self.stash_location["crime_physcial_clue"]
        item = self.stash_location["item"]
        current_location = Stash_location(location_name, description, employee, regulars, character_connection, work_witness, thief, crime_physcial_clue, item)
        return current_location

    def set_pre_crime_location(self):
        """
        builds an instance of the Pre_crime_location class specific to this game
        """
        # Locate the correct row for the location chosen for pre_crime
        location_name = self.pre_crime_location
        locations = SHEET.worksheet("locations")
        location_name_column = locations.col_values(1)
        pre_crime_location_row = location_name_column.index(location_name) + 1
        # Pull the needed details from the spreadsheet
        list_pre_crime_location_details = locations.get(f'B{pre_crime_location_row}:G{pre_crime_location_row}')
        description = list_pre_crime_location_detail[0][0]
        employee = list_pre_crime_location_detail[0][1]
        regulars = list_pre_crime_location_detail[0][2]
        character_connection = list_pre_crime_location_detail[0][3]
        work_witness = list_pre_crime_location_detail[0][4]
        physical_clue = locations.cell[0][5]
        pre_crime = self.thief_details['Pre-crime evidence']
        # build an instance of the Pre_crime_location class and return
        current_location = Pre_crime_location(location_name, description, employee, regulars, character_connection, work_witness, pre_crime, physical_clue)
        return current_location

    def set_crime_scene(self):
        """
        builds an instance of the Crime_scene class specific to this game
        """
        cases = SHEET.worksheet("cases")
        chosen_case_number = self.case_details["case_number"]
        location_name = self.case_details["crime_scene"]
        suspects_at_event = self.case_details["suspects_at_event"]
        clue_detail = self.case_details["clue_detail"]
        witness = self.case_details["witness"]
        witness_report = self.case_details["witness_report"]
        item = self.case_details["item"]
        plea = self.case_details["plea"]
        timeline = self.case_details["timeline"]
        event = self.case_details["event"]
        player_name = self.player_name
        # Pull the physical_clue to be left at the crime_scene from the location chosen for pre_crime
        location_name = self.pre_crime_location
        locations = SHEET.worksheet("locations")
        location_name_column = locations.col_values(1)
        pre_crime_location_row = location_name_column.index(location_name) + 1
        physical_clue = worksheet.cell(pre_crime_location_row, 7).value
        # build an instance of the Crime_scene class and return
        current_location = Crime_scene(location_name, suspects, clue_detail, witness, witness_report, physical_clue, item, plea, timeline, event, player_name)
        return current_location

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

    def location_actions(self):
        print("Would you like to:")
        choice = input("check the cctv (c), look around (l), or talk to a witness (t)\nAlternatively type (r) to return to the main options\n")
        return choice

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

class Pre_crime:
    def __init__(self, pre_crime, physical_clue):
        self.pre_crime = pre_crime
        self.physical_clue = physical_clue

    def cctv_pre_crime(self):
        intro_cctv_pre_crime = f"You review the cctv the morning of the crime\nYou notice the following suspects at the {self.location_name}:"
        print(intro_cctv_pre_crime)
        list_suspects = "list of suspects"
        # need to look at how it will work to gain suspect list from spreadsheet and how to then print
        summary_cctv = f"Nothing stands out as being suspicious. Anyone of them could have ended up with the {self.physical_clue} in their pocket."
        print(summary_cctv)
        # run specific location choices and main action choices

    def talk_witness_pre_crime(self):
        question = f"You question the {self.work_witness}"
        print(question)
        response = f"Well on that morning {self.employee} was here as normal and {self.regulars} came in during the morning. {self.character_connection} also popped in"
        print(response)
        clue = f"Oh and come to think of it {self.pre_crime}"
        print(clue)
        # run specific location choices and main action choices

class Pre_crime_location(Location, Pre_crime):
    def __init__(self, location_name, description, employee, regulars, character_connection, work_witness, pre_crime, physical_clue):
        Location.__init__(self, location_name, description, employee, regulars, character_connection, work_witness)
        Pre_crime.__init__(self, pre_crime, physical_clue)

class Crime_scene:
    def __init__(self, location_name, suspects, clue_detail, witness, witness_report, pre_crime_physical_clue, item, plea, timeline, event, player_name):
        self.location_name = location_name
        self.suspects = suspects
        self.clue_detail = clue_detail
        self.witness = witness
        self.witness_report = witness_report
        self.pre_crime_physical_clue = pre_crime_physical_clue
        self.item = item
        self.plea = plea
        self.timeline = timeline
        self.event = event
        self.player_name

    def enter_crime_scene(self):
        intro_crime_scene = f"As you walk into {self.location_name} the {self.employee} rushes over to meet you"
        print(intro_crime_scene)
        greet_employee = f"'Are you Junior detective {self.player_name}? I had hoped for one of the senior detectives, but ?? has assured me that your detective skills are second to none. You must find the missing {self.item}! {self.plea}'"
        print(greet_employee)
        question_employee = input(f"Ask the {self.employee} to explain what has happened (y/n)\n")
        # input to be validated including handling of error
        # Below needs looking at
        event_timeline() if question_employee == "y" else game_over("poor_detective")

    def event_timeline(self):
        print(timeline)
        help_offer = f"'Is there anything I can do to help? I can show you where the {self.item} was stolen from'"
        # run specific location choices and main action choices
    
    def cctv_crime_scene(self):
        intro_cctv_crime_scene = f"You review the cctv from the {self.event}"
        print(intro_cctv_crime_scene)
        list_suspects = "list of suspects"
        # need to look at how it will work to gain suspect list from spreadsheet and how to then print
        cctv_recording_crime_scene = f"The following suspects have been spotted in the vicinity of the crime:\nList of suspects\nIt’s impossible to tell from the CCTV who of these might have stolen the {self.item}"
        # run specific location choices and main action choices

    def look_around_crime_scene(self):
        look_around_location(self)
        notice_clue = f"As you look around you notice {self.pre_crime_physical_clue} {self.clue_detail}"
        print(notice_clue)
        # run specific location choices and main action choices

    def talk_witness_crime_scene(self):
        question = f"You question the {self.witness}"
        print(question)
        response = f"{self.witness_report} I noticed the thief ..."
        # need to look at how to generate description clue
        print(response)
        # run specific location choices and main action choices

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
    notebook_row = new_notebook_entry(date)
    case_details = set_case(notebook_row)
    thief_details = set_thief(case_details, notebook_row)
    stash_and_pre_crime_locations = set_stash_and_precrime_locations(thief_details, case_details, notebook_row)
    pre_crime_location = stash_and_pre_crime_locations[1]
    stash_location = stash_and_pre_crime_locations[0]
    current_case = Case(player_name, notebook_row, case_details, thief_details, pre_crime_location, stash_location)
    #begin_game(current_case)

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
    first_column = notebook.col_values(1)
    number_rows = len(first_column)
    notebook_row = number_rows + 1
    date_entry = [date]
    update_notebook(notebook_row, date_entry)
    return notebook_row

def set_case(notebook_row):
    """
    Calculates number of available cases and randomly chooses one
    Takes all case information, expect the thief specific values from the cases sheet
    Uses them to create and a return a dictionary
    """
    # Randomly choose a case
    cases = SHEET.worksheet("cases")
    column_one = cases.col_values(1)
    number_rows = len(column_one)
    number_cases = number_rows - 1
    chosen_case_number = random.randrange(number_cases) + 2
    # Pull all case information, expect the thief specific values from the cases sheet
    list_case_details = cases.get(f'A{chosen_case_number}:K{chosen_case_number}')
    case_name = list_case_details[0][0]
    item = list_case_details[0][1]
    event = list_case_details[0][2]
    crime_scene = list_case_details[0][3]
    timeline = list_case_details[0][4]
    plea = list_case_details[0][5]
    suspects_at_event = list_case_details[0][6]
    clue_detail = list_case_details[0][7]
    witness = list_case_details[0][8]
    witness_report = list_case_details[0][9]
    event_physical_clue = list_case_details[0][10]
    # Call the update_notebook function and pass it the notebook_column 
    # and a list of the entries to be added
    notebook_entries = [case_name, item, event, crime_scene]
    update_notebook(notebook_row, notebook_entries)
    # Create a dictionary of all the case details and return
    case_details = {
        "case_number": chosen_case_number,
        "case_name": case_name,
        "item": item,
        "event": event,
        "crime_scene": crime_scene,
        "timeline": timeline,
        "plea": plea,
        "suspects_at_event": suspects_at_event,
        "clue_detail": clue_detail,
        "witness": witness,
        "witness_report": witness_report,
        "event_physcial_clue": event_physical_clue
    }
    return case_details

def set_thief(case_details, notebook_row):
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
    update_notebook(notebook_row, [thief_dictionary['Thief']])
    return thief_dictionary

def set_stash_and_precrime_locations(thief_details, case_details, notebook_row):
    """
    Retrieves the selected case's crime_scene
    Using the thief_name retrieves the thief's work, hobby and connection locations
    Randomly assignes two of the locations not being used as the crime scene as the stash and pre_crime locations
    """
    # Get all the details needed
    thief_name = thief_details['Thief']
    suspects = SHEET.worksheet("suspects")
    suspect_name_column = suspects.col_values(1)
    thief_row = suspect_name_column.index(thief_name) + 1
    work_location = suspects.cell(thief_row, 4).value
    hobby_location = suspects.cell(thief_row, 7).value
    connection_location = suspects.cell(thief_row, 9).value
    crime_scene = case_details['crime_scene']
    # Generate a random number
    choose_locations_number = random.randrange(2)
    # Using random number choose stash and pre_crime locations
    if work_location == crime_scene:
        if choose_locations_number == 0:
            stash_location = hobby_location
            pre_crime_location = connection_location
        elif choose_locations_number == 1:
            stash_location = connection_location
            pre_crime_location = hobby_location
        else:
            print("ERROR!!")
    elif hobby_location == crime_scene:
        if choose_locations_number == 0:
            stash_location = work_location
            pre_crime_location = connection_location
        elif choose_locations_number == 1:
            stash_location = connection_location
            pre_crime_location = work_location
        else:
            print("ERROR!!")
    elif connection_location == crime_scene:
        if choose_locations_number == 0:
            stash_location = work_location
            pre_crime_location = hobby_location
        elif choose_locations_number == 1:
            stash_location = hobby_location
            pre_crime_location = work_location
        else:
            print("ERROR!!")
    else:
        if choose_locations_number == 0:
            stash_location = work_location
            pre_crime_location = hobby_location
        elif choose_locations_number == 1:
            stash_location = connection_location
            pre_crime_location = work_location
        else:
            print("ERROR!!")
    # update notebook with choices and return them
    update_notebook(notebook_row, [stash_location, pre_crime_location])
    return [stash_location, pre_crime_location]

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

# Main game

def begin_game(current_case):
    """
    Runs functions to indroduce the case and welcome the user
    this includes explaining how the game works
    If the user doesn't accept the case, the game_over function is called
    """
    accept_case = current_case.introduce_case()
    if accept_case == "y":
        current_case.welcome()
        main_action_options(current_case)
    elif accept_case == "n":
        game_over("case_not_accepted", current_case)
    else:
        print("Error!!")

def game_over(reason, current_case):
    """
    Called when player choice leads to game over and passed an argument giving the reason why
    Final scene of the game played, including an explanation of the reason for game over
    """
    if reason == "case_not_accepted":
        print(f"'I'm afraid {current_case.player_name} that your time at Case Closed must end before it has even begun. I did warn you that we only accept the best here and the best do not turn down important cases that need solving'\n")
    print(f"'Good day to you {current_case.player_name}'")
    print("GAME OVER")

def main_action_options(current_case):
    """
    Prints the main actions the player can choose from: map, notebook, suspect list or search warrant
    Handles player input and calls the associated functions
    """
    action = input("view map (m), view notebook (n), view suspect list (s) or obtain a search warrant (w)\n")
    # input to be validated
    if action == "m":
        view_map(current_case)
    elif action == "n":
        view_notebook()
    elif action == "s":
        view_suspect_list()
    elif action == "w":
        obtain_search_warrant()
    else:
        print("ERROR!!")

def view_map(current_case):
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
        location_number = int(action) + 1
        check_location_type(location_number, current_case)
    elif action == "r":
        main_action_options(current_case)
    else:
        print("ERROR!!!")

def view_notebook():
    print("notebook reached")

def view_suspect_list():
    print("suspect_list reached")

def obtain_search_warrant():
    print("search warrant reached")

def check_location_type(location_number, current_case):
    """
    Checks the location chosen to see how it needs handling and calls one of the following functions
    visit_stash_location, visit_pre_crime_location, visit_crime_scene_location
    """
    locations = SHEET.worksheet("locations")
    location_name = locations.cell(location_number, 1).value
    update_notebook(current_case.notebook_column, f"You visted {location_name}")
    if location_name == current_case.stash_location["location_name"]:
        visit_stash_location(current_case)
    elif location_name == current_case.pre_crime_location["location_name"]:
        visit_pre_crime_location(current_case)
    elif location_name == current_case.crime_scene["location_name"]:
        visit_crime_scene_location(current_case)
    else:
        print("visit unconnected location")
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

def visit_stash_location(current_case):
    """
    Sets the current_location as an instance of Stash_location. 
    Runs enter_location, requests player to choose next action and handles choice
    """
    current_location = current_case.set_stash_location()
    current_location.enter_location()
    choice = current_location.location_actions()
    if choice == "c":
        current_location.cctv_stash_location()
    elif choice == "l":
        current_location.look_around_stash_location()
    elif choice == "t":
        current_location.talk_witness_crime_scene()
    elif choice == "r":
        main_action_options(current_case)
    else:
        print("ERROR!!")

def visit_pre_crime_location(current_case):
    """
    Sets the current_location as an instance of pre_crime_location. 
    Runs enter_location, requests player to choose next action and handles choice
    """
    current_location = current_case.set_pre_crime_location()
    current_location.enter_location()
    choice = current_location.location_actions()
    if choice == "c":
        current_location.cctv_pre_crime()
    elif choice == "l":
        current_location.look_around_location()
    elif choice == "t":
        current_location.talk_witness_pre_crime()
    elif choice == "r":
        main_action_options(current_case)
    else:
        print("ERROR!!")

def visit_crime_scene_location(current_case):
    """
    Sets the current_location as an instance of Crime_scene. 
    Runs enter_location, requests player to choose next action and handles choice
    """
    current_location = current_case.set_crime_scene()
    current_location.enter_crime_scene()
    choice = current_location.location_actions()
    if choice == "c":
        current_location.cctv_crime_scene()
    elif choice == "l":
        current_location.look_around_crime_scene()
    elif choice == "t":
        current_location.talk_witness_stash_location()
    elif choice == "r":
        main_action_options(current_case)
    else:
        print("ERROR!!")

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
