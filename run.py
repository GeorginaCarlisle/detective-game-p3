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
    # check the number of entries to be added
    list_entries = list(entries[0])
    number_of_entries = len(list_entries)
    # Calculate the column range in letters where the new entries are to be added
    alphabet_list = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    start_column_letter = alphabet_list[next_free_column]
    end_column_number = next_free_column + number_of_entries
    end_column_letter = alphabet_list[end_column_number]
    # Add new entries to the notebook
    notebook.update(f'{start_column_letter}{notebook_row}:{end_column_letter}{notebook_row}', [list_entries])

# Classes

class Case:
    def __init__(self, player_name, notebook_column, case_details, thief_details, pre_crime_location, stash_location, all_locations, all_suspects):
        self.player_name = player_name
        self.notebook_column = notebook_column
        self.case_details = case_details
        self.thief_details = thief_details
        self.pre_crime_location = pre_crime_location
        self.stash_location = stash_location
        self.all_locations = all_locations
        self.all_suspects = all_suspects

    def introduce_case(self):
        enter_agency = "You enter Case Closed Detective Agency"
        print(enter_agency)
        brief_welcome = f"'You must be Junior Detective {self.player_name}. I have heard great things about your\ndetective skills. I hope you are eager to get started, as we’ve just had a new case\ncome through ......'\n"
        print(brief_welcome)
        introduce_case = f"'Someone has stolen the {self.case_details['item']} {self.case_details['event']} at the {self.case_details['crime_scene']}'"
        print(introduce_case)
        accept_case = input("'Do you wish to take on the case?' (y/n)\n")
        # input to be validated and input handled
        return accept_case

    def welcome(self):
        main_welcome = "'Fantastic! I do love an enthusiastic detective. Sorry I almost forgot:\n\nWelcome to Case Closed Detective Agency. My name is Detective Inspector Job Done\nand I will be keeping a close eye on your work during this case.\n\nWe pride ourselves here at Case Closed on being able to solve and close every\ncase we are given."
        print(main_welcome)
        print("")
        print("")
        game_explanation = "Throughout the case you will access to:\n - a map of the area, which you can use to select a location you would like\nto visit\n - a notebook containing all the clues you have discovered\ - a list of possible suspects, which you can use to question a suspect and arrest the thief\nA search warrant which you can use to thoroughly search one of the locations for the missing item.\n"
        print(game_explanation)
        print("")
        warnings = "A quick word of warning. We don't tolerate false arrests here at Case Closed and we have never yet failed to locate a missing item. I'm sure though that you will be able to swiftly solve this case, maintaining our high reputation"
        print(warnings)
        print("Where would you like to start?\n")

    def set_stash_location(self):
        """
        builds an instance of the Stash_location class specific to this game
        """
        # Locate the correct list in self.all_locations for the location chosen for stash 
        location_name = self.stash_location
        list_location_names = []
        for ind in range(0, 8):
            list_location_names.append(self.all_locations[ind][0])
        stash_list = list_location_names.index(location_name)
        # Pull the needed details from self.all_locations
        location_name = self.all_locations[stash_list][0]
        description = self.all_locations[stash_list][1]
        employee = self.all_locations[stash_list][2]
        regular = self.all_locations[stash_list][3]
        regular_hobby_link = self.all_locations[stash_list][4]
        character_connection = self.all_locations[stash_list][5]
        connection = self.all_locations[stash_list][6]
        work_witness = self.all_locations[stash_list][7]
        thief = self.thief_details["Thief"]
        event_physcial_clue = self.case_details['event_physcial_clue']
        item = self.case_details['item']
        # build an instance of the Stash_location class and return
        current_location = Stash_location(location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness, thief, event_physcial_clue, item)
        return current_location

    def set_pre_crime_location(self):
        """
        builds an instance of the Pre_crime_location class specific to this game
        """
        # Locate the correct list in self.all_locations for the location chosen for pre_crime
        location_name = self.pre_crime_location
        list_location_names = []
        for ind in range(0, 8):
            list_location_names.append(self.all_locations[ind][0])
        pre_crime_list = list_location_names.index(location_name)
        print(pre_crime_list)
        # Pull the needed details from self.all_locations
        location_name = self.all_locations[pre_crime_list][0]
        description = self.all_locations[pre_crime_list][1]
        employee = self.all_locations[pre_crime_list][2]
        regular = self.all_locations[pre_crime_list][3]
        regular_hobby_link = self.all_locations[pre_crime_list][4]
        character_connection = self.all_locations[pre_crime_list][5]
        connection = self.all_locations[pre_crime_list][6]
        work_witness = self.all_locations[pre_crime_list][7]
        physical_clue = self.all_locations[pre_crime_list][8]
        pre_crime = self.thief_details['Pre-crime evidence']
        # build an instance of the Pre_crime_location class and return
        current_location = Pre_crime_location(location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness, pre_crime, physical_clue)
        return current_location

    def set_crime_scene(self):
        """
        builds an instance of the Crime_scene class specific to this game
        """
        location_name = self.case_details["crime_scene"]
        list_suspects = f"{self.case_details['suspect_1']}, {self.case_details['suspect_2']}, {self.case_details['suspect_3']}, {self.case_details['suspect_4']} and {self.case_details['suspect_5']}"
        clue_detail = self.case_details["clue_detail"]
        witness = self.case_details["witness"]
        witness_report = self.case_details["witness_report"]
        item = self.case_details["item"]
        plea = self.case_details["plea"]
        timeline = self.case_details["timeline"]
        event = self.case_details["event"]
        player_name = self.player_name
        # Pull the physical_clue to be left at the crime_scene from the location chosen for pre_crime
        pre_crime_location_name = self.pre_crime_location
        locations = SHEET.worksheet("locations")
        location_name_column = locations.col_values(1)
        pre_crime_location_row = location_name_column.index(pre_crime_location_name) + 1
        pre_crime_physical_clue = locations.cell(pre_crime_location_row, 9).value
        # Pull the employee from the location chosen as the crime_scene
        locations = SHEET.worksheet("locations")
        location_name_column = locations.col_values(1)
        crime_scene_location_row = location_name_column.index(location_name) + 1
        employee = locations.cell(crime_scene_location_row, 3).value
        # Pull the description clue from thief details
        description_clue = self.thief_details["description_clue"]
        # build an instance of the Crime_scene class and return
        current_location = Crime_scene(location_name, list_suspects, clue_detail, witness, witness_report, pre_crime_physical_clue, item, plea, timeline, event, player_name, employee, description_clue)
        return current_location

# Location class and associated classes
class Location:
    def __init__(self, location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness):
        self.location_name = location_name
        self.description = description
        self.employee = employee
        self.regular = regular
        self.regular_hobby_link = regular_hobby_link
        self.character_connection = character_connection
        self.connection = connection
        self.work_witness = work_witness

    def enter_location(self):
        intro_location = f"You enter the {self.location_name} it is {self.description}"
        print(intro_location)

    def cctv_unconnected_location(self):
        """
        Prints storyline for checking the cctv at the current_location
        Generates and returns clues to be added to the notebook
        """
        intro_cctv_location = f"You review the cctv during the hours after the crime.\nYou notice the following suspects at the {self.location_name}:"
        print(intro_cctv_location)
        suspects = f"{self.employee}, {self.regular} and {self.character_connection}"
        print(suspects)
        summary_cctv_location = f"Nothing stands out as being suspicious."
        print(summary_cctv_location)
        clue_for_notebook = f"{suspects} were spotted during the hours after the crime.\n"
        return clue_for_notebook

    def look_around_unconnected_location(self):
        """
        Prints storyline for looking around the current_location
        Generates and returns clues to be added to the notebook
        """
        intro_look_around = f"You quickly search the {self.location_name} there is nothing of intrest\nIf you want to do a more thorough search you will need to obtain a search warrant."
        print(intro_look_around)
        clue_for_notebook = f"You find no clues when looking around.\n"
        return clue_for_notebook

    def talk_witness_unconnected_location(self):
        """
        Prints storyline for talking to the witness at the current location
        Generates and returns clues to be added to the notebook
        """
        question = f"You question the {self.work_witness}"
        print(question)
        response = f"I don't know that I can help you. {self.employee} works here {self.regular_hobby_link} is often to be seen here. {self.character_connection} who is {self.employee}'s {self.connection} also pops in occasionally"
        print(response)
        clue_for_notebook = f"{self.employee} works here. {self.regular_hobby_link} is often seen here and {self.character_connection} who is {self.employee}'s {self.connection} pops in occasionally.\n"
        return clue_for_notebook

class Stash:
    def __init__(self, thief, crime_physcial_clue, item):
        self.thief = thief
        self.crime_physcial_clue = crime_physcial_clue
        self.item = item

class Stash_location(Location, Stash):
    def __init__(self, location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness, thief, crime_physcial_clue, item):
        Location.__init__(self, location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness)
        Stash.__init__(self, thief, crime_physcial_clue, item)

    def cctv_stash_location(self):
        """
        Prints storyline for checking the cctv at the stash location
        Generates and returns clues to be added to the notebook
        """
        intro_cctv_stash = f"You review the cctv during the hours after the {self.item} was stolen.\nYou notice the following suspects at the {self.location_name}:"
        print(intro_cctv_stash)
        suspects = f"{self.employee}, {self.regular} and {self.character_connection}"
        print(suspects)
        suspicion_raised = f"You are immediately suspicious when you notice the {self.thief} appear on the CCTV at an odd hour"
        print(suspicion_raised)
        clue_for_notebook = f"{self.thief} appeared on the CCTV at an odd hour.\n"
        return clue_for_notebook

    def look_around_stash_location(self):
        """
        Prints storyline for looking around the current_location
        Generates and returns clues to be added to the notebook
        """
        intro_look_around = f"You quickly search the {self.location_name} if you want to do a more thorough search you will need to obtain a search warrant."
        print(intro_look_around)
        notice_clue = f"As you look around you notice {self.crime_physcial_clue}. Now how did that end up here?"
        print(notice_clue)
        clue_for_notebook = f"When looking around you notice {self.crime_physcial_clue}.\n"
        return clue_for_notebook

    def talk_witness_stash_location(self):
        """
        Prints storyline for talking to the witness at the stash location
        Generates and returns clues to be added to the notebook
        """
        question = f"You question the {self.work_witness}"
        print(question)
        response = f"Well there was something odd.\nWhen I came in next morning I could have sworn that a couple of things seemed out of place.\nAs though someone had been in after we had locked up."
        print(response)
        clue_for_notebook = f"The {self.work_witness} thought someone might have been in after they had locked up.\n"
        return clue_for_notebook

class Pre_crime:
    def __init__(self, pre_crime, physical_clue):
        self.pre_crime = pre_crime
        self.physical_clue = physical_clue

class Pre_crime_location(Location, Pre_crime):
    def __init__(self, location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness, pre_crime, physical_clue):
        Location.__init__(self, location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness)
        Pre_crime.__init__(self, pre_crime, physical_clue)

    def cctv_pre_crime(self):
        """
        Prints storyline for checking the cctv at the pre_crime location
        Generates and returns clues to be added to the notebook
        """
        intro_cctv_pre_crime = f"You review the cctv on the morning of the crime\nYou notice the following suspects at the {self.location_name}:"
        print(intro_cctv_pre_crime)
        suspects = f"{self.employee}, {self.regular} and {self.character_connection}"
        print(suspects)
        summary_cctv = "Nothing stands out as being suspicious."
        print(summary_cctv)
        clue_for_notebook = f"{suspects} were spotted on the morning of the crime.\n"
        return clue_for_notebook

    def talk_witness_pre_crime(self):
        """
        Prints storyline for talking to the witness at the pre_crime location
        Generates and returns clues to be added to the notebook
        """
        question = f"You question the {self.work_witness}"
        print(question)
        response = f"Well on that morning {self.employee} was here as normal and {self.regular} came in during the morning. {self.character_connection} also popped in"
        print(response)
        clue = f"Oh and come to think of it {self.pre_crime}"
        print(clue)
        clue_for_notebook = f"The {self.work_witness} mentioned '{self.pre_crime}'\n"
        return clue_for_notebook

class Crime_scene:
    def __init__(self, location_name, list_suspects, clue_detail, witness, witness_report, pre_crime_physical_clue, item, plea, timeline, event, player_name, employee, description_clue):
        self.location_name = location_name
        self.list_suspects = list_suspects
        self.clue_detail = clue_detail
        self.witness = witness
        self.witness_report = witness_report
        self.pre_crime_physical_clue = pre_crime_physical_clue
        self.item = item
        self.plea = plea
        self.timeline = timeline
        self.event = event
        self.player_name = player_name
        self.employee = employee
        self.description_clue = description_clue

    def enter_crime_scene(self):
        intro_crime_scene = f"As you walk into {self.location_name} {self.employee} rushes over to meet you"
        print(intro_crime_scene)
        greet_employee = f"'Are you Junior detective {self.player_name}? I had hoped for one of the senior detectives, but Detective Inspector Job Done has assured me that your detective skills are second to none. You must find the missing {self.item}! {self.plea}'"
        print(greet_employee)
        question_employee = input(f"Ask the {self.employee} to explain what has happened (y/n)\n")
        # input to be validated including handling of error
        # Below needs looking at
        Crime_scene.event_timeline(self) if question_employee == "y" else game_over("poor_detective", self)

    def event_timeline(self):
        print(self.timeline)

    def location_actions(self):
        print("Would you like to:")
        choice = input("check the cctv (c), look around (l), or talk to a witness (t)\nAlternatively type (r) to return to the main options\n")
        return choice

    def cctv_crime_scene(self):
        """
        Prints storyline for checking the cctv at the crime_scene
        Generates and returns clues to be added to the notebook
        """
        intro_cctv_crime_scene = f"You review the cctv from the {self.event}"
        print(intro_cctv_crime_scene)
        cctv_recording_crime_scene = f"You spot the following suspects at the {self.location_name}:\n{self.list_suspects}\nIt’s impossible to tell from the CCTV who of these might have stolen the {self.item}"
        print(cctv_recording_crime_scene)
        clue_for_notebook = f"{self.list_suspects} were spotted at the crime scene.\n"
        return clue_for_notebook

    def look_around_crime_scene(self):
        """
        Prints storyline for looking around the crime_scene
        Generates and returns clues to be added to the notebook
        """
        intro_look_around = f"You quickly search the {self.location_name} if you want to do a more thorough search you will need to obtain a search warrant."
        print(intro_look_around)
        notice_clue = f"As you look around you notice {self.pre_crime_physical_clue} {self.clue_detail}."
        print(notice_clue)
        clue_for_notebook = f"You find {self.pre_crime_physical_clue} in the vicinity of the crime.\n"
        return clue_for_notebook

    def talk_witness_crime_scene(self):
        """
        Prints storyline for talking to the witness at the crime_scene
        Generates and returns clues to be added to the notebook
        """
        question = f"You question the {self.witness}"
        print(question)
        response = f"'{self.witness_report} I couldn't tell who it was, but it was definitely a {self.description_clue}.'"
        print(response)
        clue_for_notebook = f"The thief is a {self.description_clue}.\n"
        return clue_for_notebook

# Suspect class and associated classes
class Suspect:
    def __init__(self, suspect_name, occupation, hobby_location, character_connection, connection_location):
        self.suspect_name = suspect_name
        self.occupation = occupation
        self.hobby_location = hobby_location
        self.character_connection = character_connection
        self.connection_location = connection_location

    def call_suspect_for_questioning(self):
        call_for_questioning = f"You invite {self.suspect_name} in for questioning."
        print(call_for_questioning)

    def question_reason_at_crime_scene(self):
        question = f"You ask {self.suspect_name} why they were at the crime scene"
        print(question)
        response = self.presence_reason
        print(response)
        clue_for_notebook = f"Reason for presence at crime scene: '{response}'"
        return clue_for_notebook

    def question_connections(self):
        question = f"You ask {self.suspect_name} if they have a connection with any of the other suspects"
        print(question)
        response = f"'{self.character_connection}'"
        print(response)
        clue_for_notebook = f"Connection to other characters: '{response}'"
        return clue_for_notebook

    def question_item_recognition(self):
        question = f"You ask {self.suspect_name} if they recognise the stolen item"
        print(question)
        response = f"'{self.item_connection}'"
        print(response)
        clue_for_notebook = f"Recognition of item: '{response}'"
        return clue_for_notebook

class Present_at_scene:
    def __init__(self, presence_reason, item_connection):
        self.presence_reason = presence_reason
        self.item_connection = item_connection

class Thief:
    def __init__(self, presence_reason, motive, denile):
        self.presence_reason = presence_reason
        self.motive = motive
        self.denile = denile

class Present_at_scene_suspect(Suspect):
    def __init__(self, suspect_name, occupation, hobby_location, character_connection, connection_location, presence_reason, item_connection):
        Suspect.__init__(self, suspect_name, occupation, hobby_location, character_connection, connection_location)
        Present_at_scene.__init__(self, presence_reason, item_connection)

class Suspect_is_thief(Suspect):
    def __init__(self, suspect_name, occupation, hobby_location, character_connection, connection_location, presence_reason, motive, denile):
        Suspect.__init__(self, suspect_name, occupation, hobby_location, character_connection, connection_location)
        Thief.__init__(self, presence_reason, motive, denile)
        self.item_connection = self.denile

class Unconnected_suspect(Suspect):
    def __init__(self, suspect_name, occupation, hobby_location, character_connection, connection_location):
        Suspect.__init__(self, suspect_name, occupation, hobby_location, character_connection, connection_location)
        self.presence_reason = "I think you must be mistaken I was nowhere near the crime scene when the item was stolen"
        self.item_connection = "I have never seen it before. What is it?"

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
    all_suspects = set_all_suspects()
    stash_pre_crime_and_description = set_stash_and_precrime_locations(thief_details, case_details, notebook_row, all_suspects)
    pre_crime_location = stash_pre_crime_and_description[1]
    stash_location = stash_pre_crime_and_description[0]
    thief_details['description_clue'] = stash_pre_crime_and_description[2]
    all_locations = set_all_locations()
    current_case = Case(player_name, notebook_row, case_details, thief_details, pre_crime_location, stash_location, all_locations, all_suspects)
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
    question_user = "Would you make a good detective?\nHave you got the skills to follow the clues, arrest the correct suspect and\nlocate the stolen item? \n"
    game_introduction = "In Case Closed you will choose which locations to visit, who to\ninterview, who to arrest and where to search for the stolen item.\nYour game data will be saved and used for development purposes, but no personal data will be kept and used outside of your game.\n"
    print(developer)
    print(question_user)
    print(game_introduction)
    player_name = input("Please enter your name to begin your new career as a detective:\n")
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
    list_case_details = cases.get(f'A{chosen_case_number}:Y{chosen_case_number}')
    case_name = list_case_details[0][0]
    item = list_case_details[0][1]
    event = list_case_details[0][2]
    crime_scene = list_case_details[0][3]
    timeline = list_case_details[0][4]
    plea = list_case_details[0][5]
    clue_detail = list_case_details[0][6]
    witness = list_case_details[0][7]
    witness_report = list_case_details[0][8]
    event_physical_clue = list_case_details[0][9]
    suspect_1 = list_case_details[0][10]
    presence_reason_1 = list_case_details[0][11]
    item_connection_1 = list_case_details[0][12]
    suspect_2 = list_case_details[0][13]
    presence_reason_2 = list_case_details[0][14]
    item_connection_2 = list_case_details[0][15]
    suspect_3 = list_case_details[0][16]
    presence_reason_3 = list_case_details[0][17]
    item_connection_3 = list_case_details[0][18]
    suspect_4 = list_case_details[0][19]
    presence_reason_4 = list_case_details[0][20]
    item_connection_4 = list_case_details[0][21]
    suspect_5 = list_case_details[0][22]
    presence_reason_5 = list_case_details[0][23]
    item_connection_5 = list_case_details[0][24]
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
        "clue_detail": clue_detail,
        "witness": witness,
        "witness_report": witness_report,
        "event_physcial_clue": event_physical_clue,
        "suspect_1": suspect_1,
        "presence_reason_1": presence_reason_1,
        "item_connection_1": item_connection_1,
        "suspect_2": suspect_2,
        "presence_reason_2": presence_reason_2,
        "item_connection_2": item_connection_2,
        "suspect_3": suspect_3,
        "presence_reason_3": presence_reason_3,
        "item_connection_3": item_connection_3,
        "suspect_4": suspect_4,
        "presence_reason_4": presence_reason_4,
        "item_connection_4": item_connection_4,
        "suspect_5": suspect_5,
        "presence_reason_5": presence_reason_5,
        "item_connection_5": item_connection_5,
    }
    return case_details

def set_all_suspects():
    """
    Takes all suspect information, expect the headings from the locations sheet
    returns this list of lists
    """
    suspects = SHEET.worksheet("suspects")
    all_suspects = suspects.get("A2:G9")
    return all_suspects

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
        start_range = 26
        end_range = 31
    elif chosen_thief_number == 2:
        start_range = 31
        end_range = 36
    elif chosen_thief_number == 3:
        start_range = 36
        end_range = 41
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

def set_stash_and_precrime_locations(thief_details, case_details, notebook_row, all_suspects):
    """
    Using the thief_name retrieves the thief's work, hobby and connection locations
    Randomly assignes two of the locations not being used as the crime scene as the stash and pre_crime locations
    """
    # Locate the correct list for the thief in the all_suspects list of lists
    thief_name = thief_details['Thief']
    list_suspect_names = []
    for ind in range(0, 8):
        list_suspect_names.append(all_suspects[ind][0])
    thief_list_ind = list_suspect_names.index(thief_name)
    thief_description = all_suspects[thief_list_ind][2]
    work_location = all_suspects[thief_list_ind][3]
    hobby_location = all_suspects[thief_list_ind][4]
    connection_location = all_suspects[thief_list_ind][5]
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
    return [stash_location, pre_crime_location, thief_description]

def set_all_locations():
    """
    Takes all location information, expect the headings from the locations sheet
    returns this list of lists
    """
    locations = SHEET.worksheet("locations")
    all_locations = locations.get("A2:I9")
    return all_locations

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
    print("")
    if reason == "case_not_accepted":
        print(f"'I'm not sure you are the sort of detective we need here at Case Closed {current_case.player_name}. We only employ the best here and the best do not turn down important cases that need solving'\n")
    else:
        print("You suddenly notice Detective Inspector Job Done walking towards you")
        if reason == "poor_detective":
            print(f"'It seems I have been mis-lead about your detective skills. A good detective evaluates all the evidence'")    
    print(f"'Good day to you {current_case.player_name}'")
    print("GAME OVER")
    print("")
    print("Click run program to play again")

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
        view_notebook(current_case)
    elif action == "s":
        view_suspect_list(current_case)
    elif action == "w":
        obtain_search_warrant(current_case)
    else:
        print("ERROR!!")

def view_map(current_case):
    """
    Prints the map title, intro and a list of all the locations
    Requests that user choose one of the locations or chooses to return to the main options
    Handles user input and either calls the main options or calls check_location_type 
    passing the chosen location number adjusted to represent the location's row number in the sheet
    """
    print("Map title to be created")
    print("A map of the area shows the following notable locations:")
    # loop to print location names
    for ind in range(0, 8):
        location = current_case.all_locations[ind][0]
        print(f"{ind + 1} - {location}")
    # Player choice requested and handled
    action = input("Please type in the number of the location you would like to visit.\n Alternatively type (r) to return to the main options\n")
    # input to be validated
    if action in ("1","2","3","4","5","6","7","8"):
        location_number = int(action) - 1
        check_location_type(location_number, current_case)
    elif action == "r":
        main_action_options(current_case)
    else:
        print("ERROR!!!")

def view_notebook(current_case):
    """
    Prints the notebook title, intro and a record of all the clues the player has gained
    """
    print("Notebook title to be created")
    notebook = SHEET.worksheet("notebook")
    list_clues = notebook.row_values(current_case.notebook_column)
    number_clues = len(list_clues)
    # Prints the basic case information
    basic_case_info = f"{list_clues[1]}:\n{list_clues[2].capitalize()} has been stolen {list_clues[3]} at the {list_clues[4]}."
    print(basic_case_info)
    # Prints the clues the player has gained
    for ind in range(8, number_clues):
        print("")
        print(list_clues[ind])
    main_action_options(current_case)

def view_suspect_list(current_case):
    """
    Prints the Suspects title, intro and a list of all the suspects
    Requests that user choose one of the suspects or chooses to return to the main options
    Handles user input and either calls the main options or calls check_suspect 
    """
    print("Suspects title to be created")
    print("One of these characters is the thief. Can you work out who?")
    # loop to print suspect names and occupations
    for ind in range(0, 8):
        suspect = current_case.all_suspects[ind][0]
        occupation = current_case.all_suspects[ind][1]
        print(f"{ind + 1} - {suspect} the {occupation}")
    # Player choice requested and handled
    print("")
    action = input("To question a suspect type (q) or to arrest a suspect type (a)\n Alternatively type (r) to return to the main options\n")
    # input to be validated
    if action == "q":
        suspect_choice = input("Please type in the number of the suspect you would like to question\n")
        suspect_number = int(suspect_choice) - 1
        check_suspect_type(suspect_number, current_case)
    elif action == "a":
        suspect_choice = input("Please type in the number of the suspect you would like to arrest\n")
        suspect_number = int(suspect_choice) - 1
        arrest_confirm(suspect_number, current_case)
    elif action == "r":
        main_action_options(current_case)
    else:
        print("ERROR!!!")

def obtain_search_warrant():
    print("search warrant reached")

# Location specific functions

def check_location_type(location_number, current_case):
    """
    Checks the location chosen to see how it needs handling and calls one of the following functions
    visit_stash_location, visit_pre_crime_location, visit_crime_scene_location
    """
    location_name = current_case.all_locations[location_number][0]
    if location_name == current_case.stash_location:
        visit_stash_location(current_case)
    elif location_name == current_case.pre_crime_location:
        visit_pre_crime_location(current_case)
    elif location_name == current_case.case_details['crime_scene']:
        visit_crime_scene_location(current_case)
    else:
        visit_unconnected_location(location_number, current_case)
    # need to look at what's going to happen with the work location

def visit_unconnected_location(location_number, current_case):
    """
    Takes the chosen location_number as an argument and uses to create an instance of Location
    Uses the methods of the Location class to allow the user to explore the location
    """
    # get details for chosen location
    location_name = current_case.all_locations[location_number][0]
    description = current_case.all_locations[location_number][1]
    employee = current_case.all_locations[location_number][2]
    regular = current_case.all_locations[location_number][3]
    regular_hobby_link = current_case.all_locations[location_number][4]
    character_connection = current_case.all_locations[location_number][5]
    connection = current_case.all_locations[location_number][6]
    work_witness = current_case.all_locations[location_number][7]
    # create an instance of Location for chosen location
    current_location = Location(location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness)
    clues_for_notebook = f"{current_location.location_name}:\n"
    current_location.enter_location()
    # Loop requesting and handling choice from player
    # User will only be present with options they haven't already chosen plus return option
    # Loop will run until all options chosen or player inputs return option
    actions_available = ["check the cctv (c)", "look around (s)", "talk to a witness(t)"]
    while actions_available:
        print("")
        print("Would you like to:")
        if len(actions_available) == 3:
            choice = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 2:
            choice = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 1:
            choice = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
        else:
            print("ERROR!!")
        if choice == "c":
            position_of_choice = actions_available.index("check the cctv (c)")
            actions_available.pop(position_of_choice)
            print("")
            cctv_clue = current_location.cctv_unconnected_location()
            clues_for_notebook = clues_for_notebook + cctv_clue
        elif choice == "s":
            position_of_choice = actions_available.index("look around (s)")
            actions_available.pop(position_of_choice)
            print("")
            look_around_clue = current_location.look_around_unconnected_location()
            clues_for_notebook = clues_for_notebook + look_around_clue
        elif choice == "t":
            position_of_choice = actions_available.index("talk to a witness(t)")
            actions_available.pop(position_of_choice)
            print("")
            witness_clue = current_location.talk_witness_unconnected_location()
            clues_for_notebook = clues_for_notebook + witness_clue
        elif choice == "r":
            break
        else:
            print("ERROR!!")
    # Once loop completed or user chooses to return
    print("")
    update_notebook(current_case.notebook_column, [clues_for_notebook])
    print("Exiting location. You will now be taken back to the main options")
    print("")
    main_action_options(current_case)
    
def visit_stash_location(current_case):
    """
    Sets the current_location as an instance of Stash_location. 
    Runs enter_location, requests player to choose next action and handles their choice
    Returns to main_action_choices at players request or when all location actions completed
    """
    current_location = current_case.set_stash_location()
    clues_for_notebook = f"{current_location.location_name}:\n"
    current_location.enter_location()
    # Loop requesting and handling choice from player
    # User will only be present with options they haven't already chosen plus return option
    # Loop will run until all options chosen or player inputs return option
    actions_available = ["check the cctv (c)", "look around (s)", "talk to a witness(t)"]
    while actions_available:
        print("")
        print("Would you like to:")
        if len(actions_available) == 3:
            choice = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 2:
            choice = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 1:
            choice = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
        else:
            print("ERROR!!")
        if choice == "c":
            position_of_choice = actions_available.index("check the cctv (c)")
            actions_available.pop(position_of_choice)
            print("")
            cctv_clue = current_location.cctv_stash_location()
            clues_for_notebook = clues_for_notebook + cctv_clue
        elif choice == "s":
            position_of_choice = actions_available.index("look around (s)")
            actions_available.pop(position_of_choice)
            print("")
            look_around_clue = current_location.look_around_stash_location()
            clues_for_notebook = clues_for_notebook + look_around_clue
        elif choice == "t":
            position_of_choice = actions_available.index("talk to a witness(t)")
            actions_available.pop(position_of_choice)
            print("")
            witness_clue = current_location.talk_witness_stash_location()
            clues_for_notebook = clues_for_notebook + witness_clue
        elif choice == "r":
            break
        else:
            print("ERROR!!")
    # Once loop completed or user chooses to return
    print("")
    update_notebook(current_case.notebook_column, [clues_for_notebook])
    print("Exiting location. You will now be taken back to the main options")
    print("")
    main_action_options(current_case)

def visit_pre_crime_location(current_case):
    """
    Sets the current_location as an instance of pre_crime_location.  
    Runs enter_location, requests player to choose next action and handles their choice
    Returns to main_action_choices at players request or when all location actions completed
    """
    current_location = current_case.set_pre_crime_location()
    clues_for_notebook = f"{current_location.location_name}:\n"
    current_location.enter_location()
    # Loop requesting and handling choice from player
    # User will only be present with options they haven't already chosen plus return option
    # Loop will run until all options chosen or player inputs return option
    actions_available = ["check the cctv (c)", "look around (s)", "talk to a witness(t)"]
    while actions_available:
        print("")
        print("Would you like to:")
        if len(actions_available) == 3:
            choice = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 2:
            choice = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 1:
            choice = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
        else:
            print("ERROR!!")
        if choice == "c":
            position_of_choice = actions_available.index("check the cctv (c)")
            actions_available.pop(position_of_choice)
            print("")
            cctv_clue = current_location.cctv_pre_crime()
            clues_for_notebook = clues_for_notebook + cctv_clue
        elif choice == "s":
            position_of_choice = actions_available.index("look around (s)")
            actions_available.pop(position_of_choice)
            print("")
            look_around_clue = current_location.look_around_unconnected_location()
            clues_for_notebook = clues_for_notebook + look_around_clue
        elif choice == "t":
            position_of_choice = actions_available.index("talk to a witness(t)")
            actions_available.pop(position_of_choice)
            print("")
            witness_clue = current_location.talk_witness_pre_crime()
            clues_for_notebook = clues_for_notebook + witness_clue
        elif choice == "r":
            break
        else:
            print("ERROR!!")
    # Once loop completed or user chooses to return
    print("")
    update_notebook(current_case.notebook_column, [clues_for_notebook])
    print("Exiting location. You will now be taken back to the main options")
    print("")
    main_action_options(current_case)

def visit_crime_scene_location(current_case):
    """
    Sets the current_location as an instance of Crime_scene. 
    Runs enter_crime_scene, requests player to choose next action and handles their choice
    Returns to main_action_choices at players request or when all location actions completed
    """
    current_location = current_case.set_crime_scene()
    clues_for_notebook = f"{current_location.location_name}:\n"
    current_location.enter_crime_scene()
    # Loop requesting and handling choice from player
    # User will only be present with options they haven't already chosen plus return option
    # Loop will run until all options chosen or player inputs return option
    actions_available = ["check the cctv (c)", "look around (s)", "talk to a witness(t)"]
    while actions_available:
        print("")
        print("Would you like to:")
        if len(actions_available) == 3:
            choice = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 2:
            choice = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 1:
            choice = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
        else:
            print("ERROR!!")
        if choice == "c":
            position_of_choice = actions_available.index("check the cctv (c)")
            actions_available.pop(position_of_choice)
            print("")
            cctv_clue = current_location.cctv_crime_scene()
            clues_for_notebook = clues_for_notebook + cctv_clue
        elif choice == "s":
            position_of_choice = actions_available.index("look around (s)")
            actions_available.pop(position_of_choice)
            print("")
            look_around_clue = current_location.look_around_crime_scene()
            clues_for_notebook = clues_for_notebook + look_around_clue
        elif choice == "t":
            position_of_choice = actions_available.index("talk to a witness(t)")
            actions_available.pop(position_of_choice)
            print("")
            witness_clue = current_location.talk_witness_crime_scene()
            clues_for_notebook = clues_for_notebook + witness_clue
        elif choice == "r":
            break
        else:
            print("ERROR!!")
    # Once loop completed or user chooses to return
    print("")
    update_notebook(current_case.notebook_column, [clues_for_notebook])
    print("Exiting location. You will now be taken back to the main options")
    print("")
    main_action_options(current_case)

# Suspect specific functions

def check_suspect_type(suspect_number, current_case):
    """
    Checks the suspect chosen to see how it needs handling and calls one of the following functions
    set_thief_suspect, set_suspect, set_unconnected_suspect
    """
    suspect_name = current_case.all_suspects[suspect_number][0]
    thief = current_case.thief_details["Thief"]
    list_suspects = [current_case.case_details['suspect_1'], current_case.case_details['suspect_2'], current_case.case_details['suspect_3'], current_case.case_details['suspect_4'], current_case.case_details['suspect_5']]
    if suspect_name == thief:
        current_suspect = set_thief_suspect(suspect_number, current_case)
    elif suspect_name in list_suspects:
        current_suspect = set_present_at_scene_suspect(suspect_number, current_case)
    else:
        current_suspect = set_suspect(suspect_number, current_case)
    question_suspect(current_suspect, current_case)

def set_thief_suspect(suspect_number, current_case):
    """
    builds an instance of the Suspect_is_thief class specific to this game
    """
    # Find variables needed from all_suspects list of lists
    suspect_details = current_case.all_suspects[suspect_number]
    suspect_name = suspect_details[0]
    occupation = suspect_details[1]
    hobby_location = suspect_details[4]
    connection_location = suspect_details[5]
    character_connection = suspect_details[6]
    # Find variable needed from case_details dictionary
    suspects_at_scene = [current_case.case_details['suspect_1'], current_case.case_details['suspect_2'], current_case.case_details['suspect_3'], current_case.case_details['suspect_4'], current_case.case_details['suspect_5']]
    find_suspect = suspects_at_scene.index(suspect_name) + 1
    specific_presence_reason = f"presence_reason_{find_suspect}"
    presence_reason = current_case.case_details[specific_presence_reason]
    # Find variable needed from thief_details dictionary
    motive = current_case.thief_details['Motive']
    denile = current_case.thief_details['Denile']
    # build an instance of the Suspect_is_thief class and return
    current_suspect = Suspect_is_thief(suspect_name, occupation, hobby_location, character_connection, connection_location, presence_reason, motive, denile)
    return current_suspect

def set_present_at_scene_suspect(suspect_number, current_case):
    """
    builds an instance of the Present_at_scene_suspect class specific to this game
    """
    # Find variables needed from all_suspects list of lists
    suspect_details = current_case.all_suspects[suspect_number]
    suspect_name = suspect_details[0]
    occupation = suspect_details[1]
    hobby_location = suspect_details[4]
    connection_location = suspect_details[5]
    character_connection = suspect_details[6]
    # Find variable needed from case_details dictionary
    suspects_at_scene = [current_case.case_details['suspect_1'], current_case.case_details['suspect_2'], current_case.case_details['suspect_3'], current_case.case_details['suspect_4'], current_case.case_details['suspect_5']]
    find_suspect = suspects_at_scene.index(suspect_name) + 1
    specific_presence_reason = f"presence_reason_{find_suspect}"
    presence_reason = current_case.case_details[specific_presence_reason]
    specific_item_connection = f"item_connection_{find_suspect}"
    item_connection = current_case.case_details[specific_item_connection]
    # build an instance of the Present_at_scene_suspect class and return
    current_suspect = Present_at_scene_suspect(suspect_name, occupation, hobby_location, character_connection, connection_location, presence_reason, item_connection)
    return current_suspect

def set_suspect(suspect_number, current_case):
    """
    builds an instance of the Unconnected_suspect class specific to this game
    """
    # Find variables needed from all_suspects list of lists
    suspect_details = current_case.all_suspects[suspect_number]
    suspect_name = suspect_details[0]
    occupation = suspect_details[1]
    hobby_location = suspect_details[4]
    connection_location = suspect_details[5]
    character_connection = suspect_details[6]
    # build an instance of the Unconnected_suspect class and return
    current_suspect = Unconnected_suspect(suspect_name, occupation, hobby_location, character_connection, connection_location)
    return current_suspect

def question_suspect(current_suspect, current_case):
    """
    Runs call_suspect_for_questioning, requests player to choose next action and handles their choice
    Returns to main_action_choices at players request or when all location actions completed
    """
    clues_for_notebook = f"{current_suspect.suspect_name}:\n"
    current_suspect.call_suspect_for_questioning()
    # Loop requesting and handling choice from player
    # User will only be present with options they haven't already chosen plus return option
    # Loop will run until all options chosen or player inputs return option
    actions_available = ["why they were present at the crime scene (p)", "if they have a connection with any of the other suspects (c)", "if they recognise the stolen item (i)"]
    while actions_available:
        print("")
        print("Would you like to ask the suspect:")
        if len(actions_available) == 3:
            choice = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 2:
            choice = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
        elif len(actions_available) == 1:
            choice = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
        else:
            print("ERROR!!")
        if choice == "p":
            position_of_choice = actions_available.index("why they were present at the crime scene (p)")
            actions_available.pop(position_of_choice)
            print("")
            presence_clue = current_suspect.question_reason_at_crime_scene()
            clues_for_notebook = clues_for_notebook + presence_clue
        elif choice == "c":
            position_of_choice = actions_available.index("if they have a connection with any of the other suspects (c)")
            actions_available.pop(position_of_choice)
            print("")
            character_connection_clue = current_suspect.question_connections()
            clues_for_notebook = clues_for_notebook + character_connection_clue
        elif choice == "i":
            position_of_choice = actions_available.index("if they recognise the stolen item (i)")
            actions_available.pop(position_of_choice)
            print("")
            item_recognition_clue = current_suspect.question_item_recognition()
            clues_for_notebook = clues_for_notebook + item_recognition_clue
        elif choice == "r":
            break
        else:
            print("ERROR!!")
    # Once loop completed or user chooses to return
    print("")
    update_notebook(current_case.notebook_column, [clues_for_notebook])
    print("Exiting location. You will now be taken back to the main options")
    print("")
    main_action_options(current_case)

def arrest_confirm(suspect_number, current_case):
    print("confirming arrest")

intro_and_setup()
# Write your code to expect a terminal of 80 characters wide and 24 rows high
