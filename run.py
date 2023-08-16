import gspread
from google.oauth2.service_account import Credentials
import datetime
import random
from os import system

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

def game_over(reason, current_case):
    """
    Called when player choice leads to game over and passed an argument giving the reason why
    Final scene of the game played, including an explanation of the reason for game over
    """
    notebook_row = current_case.notebook_column
    notebook_entry = [f"GAME OVER: {reason}"]
    update_notebook(notebook_row, notebook_entry)
    if reason == "case_not_accepted":
        print("")
        print(f"'I'm not sure you are the sort of detective we need here at Case Closed {current_case.player_name}. We only employ the best here and the best do not turn down important cases that need solving'\n")
    elif reason == "false_search_warrant":
        print("")
        print(f"'Good day to you {current_case.player_name}'")
    else:
        print("You suddenly notice Detective Inspector Job Done walking towards you")
        if reason == "poor_detective":
            print(f"'It seems I have been mis-lead about your detective skills. A good detective evaluates all the evidence'")
            print("")
            print(f"'Good day to you {current_case.player_name}'")
        elif reason == "false_arrest":
            print(f"'What are you doing {current_case.player_name}! You have arrested the wrong person!'")
            print("")
            print(f"Detective Inspector Job Done turns to the suspect removing the hand-cuffs\n'I cannot apologise enough, {current_case.player_name} will not be allowed to cause such upset to the members of our community you can rest assured that their days as a detective are over!'")
            print("")
            print(f"Your services are no longer required {current_case.player_name} you are no detective please kindly leave this establishment at once!'")
    title = """
            ____  ____ ___ ___   ___       ___  __ __   ___ ____  
           /    |/    |   |   | /  _]     /   \|  |  | /  _]    \ 
          |   __|  o  | _   _ |/  [_     |     |  |  |/  [_|  D  )
          |  |  |     |  \_/  |    _]    |  O  |  |  |    _]    / 
          |  |_ |  _  |   |   |   [_     |     |  :  |   [_|    \ 
          |     |  |  |   |   |     |    |     |\   /|     |  .  \ 
          |___,_|__|__|___|___|_____|     \___/  \_/ |_____|__|\_|    
    """
    print(title)
    print("")
    print("The next day .....")
    print("")
    print(f"You pick up the newspaper to read:\nCase Closed has solved and closed another case in record time!\nDetective Inspector Job Done arrested {current_case.thief_details['Thief']} who had stolen the {current_case.case_details['item']} and hidden it at the {current_case.stash_location}. '{current_case.thief_details['Motive']}' Great job Detective Inspector Job Done!")
    new_game(current_case)

def clear():
    """
    Clears the terminal
    """
    system("clear")

def new_game(current_case):
    """
    Entices the player to play again. Asks if they would like to
    and handles the request.
    """
    print("")
    print("")
    print("Case Closed has a number of different cases, each with a number of potential thieves and if even when you work out who the thief is, you can never be sure where they stashed it!\n")
    while True:
            player_input = input("Would you like to play again? (y/n)")
            play_again = player_input.strip().lower()
            if play_again == "y":
                break
            elif play_again == "n":
                break
            else:
                print("Your input does not match requirements.\nYou need to either type 'y' or 'n' please try again")
                print("")
    if play_again == "y":
        notebook_row = current_case.notebook_column
        notebook_entry = ["Play again chosen"]
        update_notebook(notebook_row, notebook_entry)
        intro_and_setup()
    elif play_again == "n":
        notebook_row = current_case.notebook_column
        notebook_entry = ["Game exited"]
        update_notebook(notebook_row, notebook_entry)
        print("Oh well. If change your mind click run program to start the game again")

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
        print("")
        enter_agency = "You enter Case Closed Detective Agency"
        print(enter_agency)
        print("")
        brief_welcome = f"'You must be Junior Detective {self.player_name}. I have heard great things about your detective skills. I hope you are eager to get started, as we’ve just had a new case come through ......'\n"
        print(brief_welcome)
        introduce_case = f"'Someone has stolen {self.case_details['item']} {self.case_details['event']} at the {self.case_details['crime_scene']}'"
        print(introduce_case)
        print("")
        while True:
            accept_input = input("Do you wish to take on the case? (y/n)\n")
            accept_case = accept_input.strip().lower()
            if accept_case == "y":
                break
            elif accept_case == "n":
                break
            else:
                print("Your input does not match requirements.\nYou need to either type 'y' or 'n' please try again")
                print("")
        return accept_case

    def welcome(self):
        clear()
        print("")
        main_welcome = "'Fantastic! I do love an enthusiastic detective. Sorry I almost forgot:\n\nWelcome to Case Closed Detective Agency. My name is Detective Inspector Job Done\nand I will be keeping a close eye on your work during this case.\nWe pride ourselves here at Case Closed on being able to solve and close every\ncase we are given."
        print(main_welcome)
        print("")
        game_explanation = "Throughout the case you will access to:\n - a map of the area, which you can use to select a location you would like to visit and obtain a search warrant\n - a notebook containing all the clues you have discovered\n - a list of possible suspects, which you can use to question a suspect and arrest the thief."
        print(game_explanation)
        print("")
        warnings = "A quick word of warning. We don't tolerate false arrests here at Case Closed and we have never yet failed to locate a missing item. I'm sure though that you will be able to swiftly solve this case, maintaining our high reputation."
        print(warnings)
        print("")
        print("Where would you like to start?")

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
        work_location = self.thief_details['work_location']
        work_evidence = self.thief_details['Evidence at work']
        # build an instance of the Stash_location class and return
        current_location = Stash_location(location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness, thief, event_physcial_clue, item, work_location, work_evidence)
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
        work_location = self.thief_details['work_location']
        work_evidence = self.thief_details['Evidence at work']
        # build an instance of the Pre_crime_location class and return
        current_location = Pre_crime_location(location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness, pre_crime, physical_clue, work_location, work_evidence)
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
class Work_location:
    """
    This class is a mixin to be assessed by all locations (except) crime_scene
    When looking around
    """
    def check_if_work_location(self):
        """
        checks if the current_location is the thief's work location
        return True if work_location and False if not work_location
        """
        work_location = self.work_location
        current_location = self.location_name
        if current_location == work_location:
            is_work_location = True
            evidence_found = f"As you look around you notice {self.work_evidence}"
            print(evidence_found)
            notebook_clue = self.work_evidence
        else:
            is_work_location = False
            notebook_clue = "no clue"
        return [is_work_location, notebook_clue]

class Location(Work_location):
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
        clear()
        title = """
                                            ________
                                    __     |   __   |
          ________________    _____|  |_   |  |__|  |  
          |   __   __     |  |    __    |  |   __   |    _____________
          |  |__| |__|    |  |   |__|   |__|  |__|  |   |   __   __   |
          |   __   __     |  |    __           __   |___|  |__| |__|  |
        __|  |__| |__|    |__|   |__|         |__|          __   __   |__
        |                                                  |__| |__|     |
        |________________________________________________________________| 
"""
        print(title)
        intro_location = f"You enter the {self.location_name} it is {self.description}"
        print(intro_location)

    def cctv_unconnected_location(self):
        """
        Prints storyline for checking the cctv at the current_location
        Generates and returns clues to be added to the notebook
        """
        clear()
        print("")
        intro_cctv_location = f"You review the cctv during the hours after the crime.\nYou notice the following suspects at the {self.location_name}:"
        print(intro_cctv_location)
        print("")
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
        clear()
        print("")
        intro_look_around = f"You quickly search the {self.location_name}, there is nothing of interest.\n\nIf you want to do a more thorough search you will need to obtain a search warrant."
        print(intro_look_around)
        clue_for_notebook = f"You find no clues when looking around.\n"
        return clue_for_notebook

    def talk_witness_unconnected_location(self):
        """
        Prints storyline for talking to the witness at the current location
        Generates and returns clues to be added to the notebook
        """
        clear()
        print("")
        question = f"You question the {self.work_witness}:"
        print(question)
        response = f"'I don't know that I can help you. {self.employee} works here. {self.regular_hobby_link} is often to be seen here. {self.character_connection} who is {self.employee}'s {self.connection} also pops in occasionally'"
        print(response)
        clue_for_notebook = f"{self.employee} works here. {self.regular_hobby_link} is often seen here and {self.character_connection} who is {self.employee}'s {self.connection} pops in occasionally.\n"
        return clue_for_notebook

class Stash:
    def __init__(self, thief, crime_physcial_clue, item, work_location, work_evidence):
        self.thief = thief
        self.crime_physcial_clue = crime_physcial_clue
        self.item = item
        self.work_location = work_location
        self.work_evidence = work_evidence

class Stash_location(Location, Stash, Work_location):
    def __init__(self, location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness, thief, crime_physcial_clue, item, work_location, work_evidence):
        Location.__init__(self, location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness)
        Stash.__init__(self, thief, crime_physcial_clue, item, work_location, work_evidence)

    def cctv_stash_location(self):
        """
        Prints storyline for checking the cctv at the stash location
        Generates and returns clues to be added to the notebook
        """
        clear()
        print("")
        intro_cctv_stash = f"You review the cctv during the hours after the {self.item} was stolen.\n\nYou notice the following suspects at the {self.location_name}:"
        print(intro_cctv_stash)
        suspects = f"{self.employee}, {self.regular} and {self.character_connection}"
        print(suspects)
        suspicion_raised = f"You are immediately suspicious when you notice the {self.thief} appear on the CCTV at an odd hour."
        print("")
        print(suspicion_raised)
        clue_for_notebook = f"{self.thief} appeared on the CCTV at an odd hour.\n"
        return clue_for_notebook

    def look_around_stash_location(self):
        """
        Prints storyline for looking around the current_location
        Generates and returns clues to be added to the notebook
        """
        clear()
        print("")
        is_work_location = self.check_if_work_location()
        if is_work_location[0]:
            clue_for_notebook = is_work_location[1]
        else:
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
        clear()
        print("")
        question = f"You question the {self.work_witness}:"
        print(question)
        response = f"'Well there was something odd. When I came in next morning I could have sworn that a couple of things seemed out of place. As though someone had been in after we had locked up.'"
        print(response)
        clue_for_notebook = f"The {self.work_witness} thought someone might have been in after they had locked up.\n"
        return clue_for_notebook

class Pre_crime:
    def __init__(self, pre_crime, physical_clue, work_location, work_evidence):
        self.pre_crime = pre_crime
        self.physical_clue = physical_clue
        self.work_location = work_location
        self.work_evidence = work_evidence

class Pre_crime_location(Location, Pre_crime):
    def __init__(self, location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness, pre_crime, physical_clue, work_location, work_evidence):
        Location.__init__(self, location_name, description, employee, regular, regular_hobby_link, character_connection, connection, work_witness)
        Pre_crime.__init__(self, pre_crime, physical_clue, work_location, work_evidence)

    def cctv_pre_crime(self):
        """
        Prints storyline for checking the cctv at the pre_crime location
        Generates and returns clues to be added to the notebook
        """
        clear()
        print("")
        intro_cctv_pre_crime = f"You review the cctv on the morning of the crime.\n\nYou notice the following suspects at the {self.location_name}:"
        print(intro_cctv_pre_crime)
        suspects = f"{self.employee}, {self.regular} and {self.character_connection}"
        print(suspects)
        print("")
        summary_cctv = "Nothing stands out as being suspicious."
        print(summary_cctv)
        clue_for_notebook = f"{suspects} were spotted on the morning of the crime.\n"
        return clue_for_notebook

    def talk_witness_pre_crime(self):
        """
        Prints storyline for talking to the witness at the pre_crime location
        Generates and returns clues to be added to the notebook
        """
        clear()
        print("")
        question = f"You question the {self.work_witness}"
        print(question)
        response = f"Well on that morning {self.employee} was here as normal and {self.regular} came in during the morning. {self.character_connection} also popped in...."
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
        clear()
        title = """
                                            ________
                                    __     |   __   |
          ________________    _____|  |_   |  |__|  |  
          |   __   __     |  |    __    |  |   __   |    _____________
          |  |__| |__|    |  |   |__|   |__|  |__|  |   |   __   __   |
          |   __   __     |  |    __           __   |___|  |__| |__|  |
        __|  |__| |__|    |__|   |__|         |__|          __   __   |__
        |                                                  |__| |__|     |
        |________________________________________________________________| 
"""
        print(title)
        intro_crime_scene = f"As you walk into {self.location_name} {self.employee} rushes over to meet you"
        print("")
        print(intro_crime_scene)
        greet_employee = f"'Are you Junior detective {self.player_name}? I had hoped for one of the senior detectives, but Detective Inspector Job Done has assured me that your detective skills are second to none. You must find {self.item}! {self.plea}'"
        print("")
        print(greet_employee)
        while True:
            print("")
            question_input = input(f"Ask the {self.employee} to explain what has happened (y/n)\n")
            question_employee = question_input.strip().lower()
            if question_employee == "y":
                break
            elif question_employee == "n":
                break
            else:
                print("Your input does not match requirements.\nYou need to either type 'y' or 'n' please try again")
                print("")
        return question_employee

    def event_timeline(self):
        print("")
        print("")
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
        clear()
        print("")
        intro_cctv_crime_scene = f"You review the cctv from the {self.event}"
        print(intro_cctv_crime_scene)
        print("")
        cctv_recording_crime_scene = f"You spot the following suspects at the {self.location_name}:\n{self.list_suspects}.\n\nIt’s impossible to tell from the CCTV who of these might have stolen the {self.item}"
        print(cctv_recording_crime_scene)
        clue_for_notebook = f"{self.list_suspects} were spotted at the crime scene.\n"
        return clue_for_notebook

    def look_around_crime_scene(self):
        """
        Prints storyline for looking around the crime_scene
        Generates and returns clues to be added to the notebook
        """
        clear()
        print("")
        intro_look_around = f"You quickly search the {self.location_name} if you want to do a more thorough search you will need to obtain a search warrant."
        print(intro_look_around)
        print("")
        notice_clue = f"As you look around you notice {self.pre_crime_physical_clue} {self.clue_detail}"
        print(notice_clue)
        clue_for_notebook = f"You find {self.pre_crime_physical_clue} in the vicinity of the crime.\n"
        return clue_for_notebook

    def talk_witness_crime_scene(self):
        """
        Prints storyline for talking to the witness at the crime_scene
        Generates and returns clues to be added to the notebook
        """
        clear()
        print("")
        question = f"You question the {self.witness}:"
        print(question)
        print("")
        response = f"'{self.witness_report} I couldn't tell who it was, but it was definitely a {self.description_clue}.'"
        print(response)
        clue_for_notebook = f"The thief is a {self.description_clue}.\n"
        return clue_for_notebook

# Suspect class and associated classes
class Suspect:
    def __init__(self, suspect_name, occupation, work_location, hobby_location, character_connection, connection_location):
        self.suspect_name = suspect_name
        self.occupation = occupation
        self.work_location = work_location
        self.hobby_location = hobby_location
        self.character_connection = character_connection
        self.connection_location = connection_location

    def call_suspect_for_questioning(self):
        clear()
        call_for_questioning = f"You invite {self.suspect_name} in for questioning."
        print(call_for_questioning)

    def question_reason_at_crime_scene(self):
        clear()
        question = f"You ask {self.suspect_name} why they were at the crime scene"
        print(question)
        response = self.presence_reason
        print(response)
        clue_for_notebook = f"Reason for presence at crime scene: '{response}'"
        return clue_for_notebook

    def question_connections(self):
        clear()
        question = f"You ask {self.suspect_name} where they have been in the last two days"
        print(question)
        response = f"'Well, I work at the {self.work_location}, I often go the {self.hobby_location} and I popped into to see {self.character_connection} at the {self.connection_location}.'"
        print(response)
        clue_for_notebook = f"In the last two days visited: {self.work_location}, {self.hobby_location} and {self.connection_location}."
        return clue_for_notebook

    def question_item_recognition(self):
        clear()
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

class Present_at_scene_suspect(Suspect, Present_at_scene):
    def __init__(self, suspect_name, occupation, work_location, hobby_location, character_connection, connection_location, presence_reason, item_connection):
        Suspect.__init__(self, suspect_name, occupation, work_location, hobby_location, character_connection, connection_location)
        Present_at_scene.__init__(self, presence_reason, item_connection)

class Suspect_is_thief(Suspect, Thief):
    def __init__(self, suspect_name, occupation, work_location, hobby_location, character_connection, connection_location, presence_reason, motive, denile):
        Suspect.__init__(self, suspect_name, occupation, work_location, hobby_location, character_connection, connection_location)
        Thief.__init__(self, presence_reason, motive, denile)
        self.item_connection = self.denile

class Unconnected_suspect(Suspect):
    def __init__(self, suspect_name, occupation, work_location, hobby_location, character_connection, connection_location):
        Suspect.__init__(self, suspect_name, occupation, work_location, hobby_location, character_connection, connection_location)
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
    print("")
    print("Please ignore the following message:")
    print("")
    date = str(get_date())
    notebook_row = new_notebook_entry(date)
    print("")
    case_details = set_case(notebook_row)
    print("Your game is now loading")
    thief_details = set_thief(case_details, notebook_row)
    print("")
    all_suspects = set_all_suspects()
    print("Almost there ....")
    stash_pre_crime_and_description = set_stash_and_precrime_locations(thief_details, case_details, notebook_row, all_suspects)
    pre_crime_location = stash_pre_crime_and_description[1]
    stash_location = stash_pre_crime_and_description[0]
    thief_details['description_clue'] = stash_pre_crime_and_description[2]
    thief_details['work_location'] = stash_pre_crime_and_description[3]
    print("")
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
      __________________________________________________________________
            __                                                          
          /    )                              /                        /
      ---/---------__---__----__--------__---/----__---__----__----__-/-
        /        /   ) (_ ` /___)     /   ' /   /   ) (_ ` /___) /   /  
      _(____/___(___(_(__)_(___ _____(___ _/___(___/_(__)_(___ _(___/___
                                                                  
"""
    print(title)
    developer = "Created by Georgina Carlisle 2023\n"
    question_user = "Would you make a good detective? Have you got the skills to follow the clues, arrest the correct suspect and\nlocate the stolen item? \n"
    game_introduction = "In Case Closed you will choose which locations to visit, who to\ninterview, who to arrest and where to search for the stolen item.\nYour game data will be saved and used for development purposes, but no personal data will be kept and used outside of your game.\n"
    print(developer)
    print(question_user)
    print(game_introduction)
    while True:
        input_name = input("Please enter your name to begin your new career as a detective:\n")
        player_name = input_name.strip()
        if len(player_name) < 80:
            break
        else:
            print("")
            print("Your name is far too long! It needs to be less than 80 characters long. This is the length of one row. Please try again.")
            print("")
    if player_name == "":
        player_name = "No Name"
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
    return [stash_location, pre_crime_location, thief_description, work_location]

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
    clear()
    accept_case = current_case.introduce_case()
    if accept_case == "y":
        current_case.welcome()
        main_action_options(current_case)
    elif accept_case == "n":
        clear()
        game_over("case_not_accepted", current_case)
    else:
        print("Error!! Please contact developer")

def main_action_options(current_case):
    """
    Prints the main actions the player can choose from: map, notebook, suspect list or search warrant
    Handles player input and calls the associated functions
    """
    while True:
        action = input("view map (m), view notebook (n) or view suspect list (s)\n")
        confirmed_action = action.strip().lower()
        if confirmed_action in ("m", "n", "s"):
            break
        else:
            print("Your input does not match requirements.\nYou need to either type 'm' or 'n' or 's'  please try again")
            print("")
    if confirmed_action == "m":
        view_map(current_case)
    elif confirmed_action == "n":
        view_notebook(current_case)
    elif confirmed_action == "s":
        view_suspect_list(current_case)
    else:
        print("ERROR! Please contact developer")

def view_map(current_case):
    """
    Prints the map title, intro and a list of all the locations
    Requests that user choose one of the locations or chooses to return to the main options
    Handles user input and either calls the main options or calls check_location_type
    passing the chosen location number adjusted to represent the location's row number in the sheet
    """
    clear()
    title = """
                           ___ ___  ____ ____     
                          |   |   |/    |    \ 
                          | _   _ |  o  |  o  )
                          |  \_/  |     |   _/ 
                          |   |   |  _  |  |   
                          |   |   |  |  |  |   
                          |___|___|__|__|__|   

"""
    print(title)
    print("A map of the area shows the following notable locations:")
    # loop to print location names
    for ind in range(0, 8):
        location = current_case.all_locations[ind][0]
        print(f"{ind + 1} - {location}")
    # Player choice requested and handled
    print("")
    confirmed_choice = ""
    while True:
        choice = input("To visit a location (v) or to obtain a search warrant (w). Alternatively type (r) to return to the main options\n")
        confirmed_choice = choice.strip().lower()
        if confirmed_choice in ("v", "w", "r"):
            break
        else:
            print("Your input does not match requirements.\nYou need to either type 'v', 'w' or 'r' please try again")
            print("")
    if confirmed_choice == "v":
        while True:
            action = input("Please type in the number of the location you would like to visit.\n")
            confirmed_action = action.strip()
            if confirmed_action in ("1", "2", "3", "4", "5", "6", "7", "8"):
                break
            else:
                print("Your input does not match requirements.\nYou need to enter a number between 1 and 8, please try again")
                print("")
        location_number = int(confirmed_action) - 1
        check_location_type(location_number, current_case)
    elif confirmed_choice == "w":
        while True:
            action = input("Please type in the number of the location you would like thoroughly search.\n")
            confirmed_action = action.strip()
            if confirmed_action in ("1", "2", "3", "4", "5", "6", "7", "8"):
                break
            else:
                print("Your input does not match requirements.\nYou need to enter a number between 1 and 8, please try again")
                print("")
        location_number = int(confirmed_action) - 1
        confirm_warrant_request(location_number, current_case)
    elif confirmed_choice == "r":
        main_action_options(current_case)
    else:
        print("ERROR!!!")

def view_notebook(current_case):
    """
    Prints the notebook title, intro and a record of all the clues the player has gained
    """
    clear()
    title = """
                   __      _       _                 _    
                /\ \ \___ | |_ ___| |__   ___   ___ | | __
               /  \/ / _ \| __/ _ \ '_ \ / _ \ / _ \| |/ /
              / /\  / (_) | ||  __/ |_) | (_) | (_) |   < 
              \_\ \/ \___/ \__\___|_.__/ \___/ \___/|_|\_\ 

"""
    print(title)
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
    clear()
    title = """
            _______ __  _________   ___    __ ______  _____
           / ___/  |  |/ ___/    \ /  _]  /  ]      |/ ___/
          (   \_|  |  (   \_|  o  )  [_  /  /|      (   \_ 
           \__  |  |  |\__  |   _/    _]/  / |_|  |_|\__  |
           /  \ |  :  |/  \ |  | |   [_/   \_  |  |  /  \ |
           \    |     |\    |  | |     \     | |  |  \    |
            \___|\__,_| \___|__| |_____|\____| |__|   \___|

"""
    print(title)
    print("One of these characters is the thief. Can you work out who?")
    # loop to print suspect names and occupations
    for ind in range(0, 8):
        suspect = current_case.all_suspects[ind][0]
        occupation = current_case.all_suspects[ind][1]
        print(f"{ind + 1} - {suspect} the {occupation}")
    # Player choice requested and handled
    print("")
    confirmed_choice = ""
    while True:
        choice = input("To question a suspect type (q) or to arrest a suspect type (a). Alternatively type (r) to return to the main options\n")
        confirmed_choice = choice.strip().lower()
        if confirmed_choice in ("q", "a", "r"):
            break
        else:
            print("Your input does not match requirements.\nYou need to either type 'q', 'a' or 'r' please try again")
            print("")
    if confirmed_choice == "q":
        confirmed_action = ""
        while True:
            action = input("Please type in the number of the suspect you would like to question\n")
            confirmed_action = action.strip()
            if confirmed_action in ("1", "2", "3", "4", "5", "6", "7", "8"):
                break
            else:
                print("Your input does not match requirements.\nYou need to enter a number between 1 and 8, please try again")
                print("")
        suspect_number = int(confirmed_action) - 1
        check_suspect_type(suspect_number, current_case)
    elif confirmed_choice == "a":
        confirmed_action = ""
        while True:
            action = input("Please type in the number of the suspect you would like to arrest\n")
            confirmed_action = action.strip()
            if confirmed_action in ("1", "2", "3", "4", "5", "6", "7", "8"):
                break
            else:
                print("Your input does not match requirements.\nYou need to enter a number between 1 and 8, please try again")
                print("")
        suspect_number = int(confirmed_action) - 1
        arrest_confirm(suspect_number, current_case)
    elif action == "r":
        main_action_options(current_case)
    else:
        print("ERROR!!!")

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
        # checks number of actions available and requests and confirms appropriate input
        confirmed_action = ""
        # No actions yet completed
        if len(actions_available) == 3:
            while True:
                action = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                print(confirmed_action)
                if confirmed_action in ("c", "s", "t", "r"):
                    break
                else:
                    print("")
                    print("Your input does not match requirements.\nYou need to either type 'c', 's', 't' or 'r'  please try again")
                    print("")
        # One action completed
        elif len(actions_available) == 2:
            # Work out which actions are left
            choice_1 = ""
            if actions_available[0] == "check the cctv (c)":
                choice_1 = "c"
            elif actions_available[0] == "look around (s)":
                choice_1 = "s"
            elif actions_available[0] == "talk to a witness(t)":
                choice_1 = "t"
            else:
                print("ERROR!! Please contact developer")
            choice_2 = ""
            if actions_available[1] == "check the cctv (c)":
                choice_2 = "c"
            elif actions_available[1] == "look around (s)":
                choice_2 = "s"
            elif actions_available[1] == "talk to a witness(t)":
                choice_2 = "t"
            else:
                print("ERROR!! Please contact developer")
            # Request input and error handle
            while True:
                action = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, choice_2, "r"):
                    break
                else:
                    print("")
                    print(f"Your input does not match requirements.\nYou need to either type '{choice_1}', '{choice_2}' or 'r'. Please try again")
                    print("")
        # Two actions completed
        elif len(actions_available) == 1:
            # Work out which actions is left
            choice_1 = ""
            if actions_available[0] == "check the cctv (c)":
                choice_1 = "c"
            elif actions_available[0] == "look around (s)":
                choice_1 = "s"
            elif actions_available[0] == "talk to a witness(t)":
                choice_1 = "t"
            else:
                print("ERROR!! Please contact developer")
            while True:
                action = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, "r"):
                    break
                else:
                    print("")
                    print(f"Your input does not match requirements.\nYou need to either type '{choice_1}' or 'r' please try again")
                    print("")
        else:    
            print("ERROR!!")
        if confirmed_action == "c":
            position_of_choice = actions_available.index("check the cctv (c)")
            actions_available.pop(position_of_choice)
            print("")
            cctv_clue = current_location.cctv_unconnected_location()
            clues_for_notebook = clues_for_notebook + cctv_clue
        elif confirmed_action == "s":
            position_of_choice = actions_available.index("look around (s)")
            actions_available.pop(position_of_choice)
            print("")
            look_around_clue = current_location.look_around_unconnected_location()
            clues_for_notebook = clues_for_notebook + look_around_clue
        elif confirmed_action == "t":
            position_of_choice = actions_available.index("talk to a witness(t)")
            actions_available.pop(position_of_choice)
            print("")
            witness_clue = current_location.talk_witness_unconnected_location()
            clues_for_notebook = clues_for_notebook + witness_clue
        elif confirmed_action == "r":
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
        # checks number of actions available and requests and confirms appropriate input
        confirmed_action = ""
        # No actions yet completed
        if len(actions_available) == 3:
            while True:
                action = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                print(confirmed_action)
                if confirmed_action in ("c", "s", "t", "r"):
                    break
                else:
                    print("")
                    print("Your input does not match requirements.\nYou need to either type 'c', 's', 't' or 'r'  please try again")
                    print("")
        # One action completed
        elif len(actions_available) == 2:
            # Work out which actions are left
            choice_1 = ""
            if actions_available[0] == "check the cctv (c)":
                choice_1 = "c"
            elif actions_available[0] == "look around (s)":
                choice_1 = "s"
            elif actions_available[0] == "talk to a witness(t)":
                choice_1 = "t"
            else:
                print("ERROR!! Please contact developer")
            choice_2 = ""
            if actions_available[1] == "check the cctv (c)":
                choice_2 = "c"
            elif actions_available[1] == "look around (s)":
                choice_2 = "s"
            elif actions_available[1] == "talk to a witness(t)":
                choice_2 = "t"
            else:
                print("ERROR!! Please contact developer")
            # Request input and error handle
            while True:
                action = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, choice_2, "r"):
                    break
                else:
                    print("")
                    print(f"Your input does not match requirements.\nYou need to either type '{choice_1}', '{choice_2}' or 'r'. Please try again")
                    print("")
        # Two actions completed
        elif len(actions_available) == 1:
            # Work out which actions is left
            choice_1 = ""
            if actions_available[0] == "check the cctv (c)":
                choice_1 = "c"
            elif actions_available[0] == "look around (s)":
                choice_1 = "s"
            elif actions_available[0] == "talk to a witness(t)":
                choice_1 = "t"
            else:
                print("ERROR!! Please contact developer")
            while True:
                action = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, "r"):
                    break
                else:
                    print("")
                    print(f"Your input does not match requirements.\nYou need to either type '{choice_1}' or 'r' please try again")
                    print("")
        else:    
            print("ERROR!!")
        if confirmed_action == "c":
            position_of_choice = actions_available.index("check the cctv (c)")
            actions_available.pop(position_of_choice)
            print("")
            cctv_clue = current_location.cctv_unconnected_location()
            clues_for_notebook = clues_for_notebook + cctv_clue
        elif confirmed_action == "s":
            position_of_choice = actions_available.index("look around (s)")
            actions_available.pop(position_of_choice)
            print("")
            look_around_clue = current_location.look_around_unconnected_location()
            clues_for_notebook = clues_for_notebook + look_around_clue
        elif confirmed_action == "t":
            position_of_choice = actions_available.index("talk to a witness(t)")
            actions_available.pop(position_of_choice)
            print("")
            witness_clue = current_location.talk_witness_unconnected_location()
            clues_for_notebook = clues_for_notebook + witness_clue
        elif confirmed_action == "r":
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
        # checks number of actions available and requests and confirms appropriate input
        confirmed_action = ""
        # No actions yet completed
        if len(actions_available) == 3:
            while True:
                action = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                print(confirmed_action)
                if confirmed_action in ("c", "s", "t", "r"):
                    break
                else:
                    print("")
                    print("Your input does not match requirements.\nYou need to either type 'c', 's', 't' or 'r'  please try again")
                    print("")
        # One action completed
        elif len(actions_available) == 2:
            # Work out which actions are left
            choice_1 = ""
            if actions_available[0] == "check the cctv (c)":
                choice_1 = "c"
            elif actions_available[0] == "look around (s)":
                choice_1 = "s"
            elif actions_available[0] == "talk to a witness(t)":
                choice_1 = "t"
            else:
                print("ERROR!! Please contact developer")
            choice_2 = ""
            if actions_available[1] == "check the cctv (c)":
                choice_2 = "c"
            elif actions_available[1] == "look around (s)":
                choice_2 = "s"
            elif actions_available[1] == "talk to a witness(t)":
                choice_2 = "t"
            else:
                print("ERROR!! Please contact developer")
            # Request input and error handle
            while True:
                action = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, choice_2, "r"):
                    break
                else:
                    print("")
                    print(f"Your input does not match requirements.\nYou need to either type '{choice_1}', '{choice_2}' or 'r'. Please try again")
                    print("")
        # Two actions completed
        elif len(actions_available) == 1:
            # Work out which actions is left
            choice_1 = ""
            if actions_available[0] == "check the cctv (c)":
                choice_1 = "c"
            elif actions_available[0] == "look around (s)":
                choice_1 = "s"
            elif actions_available[0] == "talk to a witness(t)":
                choice_1 = "t"
            else:
                print("ERROR!! Please contact developer")
            while True:
                action = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, "r"):
                    break
                else:
                    print("")
                    print(f"Your input does not match requirements.\nYou need to either type '{choice_1}' or 'r' please try again")
                    print("")
        else:    
            print("ERROR!!")
        if confirmed_action == "c":
            position_of_choice = actions_available.index("check the cctv (c)")
            actions_available.pop(position_of_choice)
            print("")
            cctv_clue = current_location.cctv_unconnected_location()
            clues_for_notebook = clues_for_notebook + cctv_clue
        elif confirmed_action == "s":
            position_of_choice = actions_available.index("look around (s)")
            actions_available.pop(position_of_choice)
            print("")
            look_around_clue = current_location.look_around_unconnected_location()
            clues_for_notebook = clues_for_notebook + look_around_clue
        elif confirmed_action == "t":
            position_of_choice = actions_available.index("talk to a witness(t)")
            actions_available.pop(position_of_choice)
            print("")
            witness_clue = current_location.talk_witness_unconnected_location()
            clues_for_notebook = clues_for_notebook + witness_clue
        elif confirmed_action == "r":
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
    Runs enter_crime_scene and calls event_timeline and explore_crime_scene
    If player makes the correct choice, if not game_over called
    """
    current_location = current_case.set_crime_scene()
    question_employee = current_location.enter_crime_scene()
    if question_employee == "y":
        current_location.event_timeline()
        explore_crime_scene(current_case, current_location)
    else:
        game_over("poor_detective", current_case)

def explore_crime_scene(current_case, current_location):
    """
    Requests player to choose their actions while visiting the crime scene and handles their choice
    Returns to main_action_choices at players request or when all location actions completed
    """
    clues_for_notebook = f"{current_location.location_name}:\n"
    # Loop requesting and handling choice from player
    # User will only be present with options they haven't already chosen plus return option
    # Loop will run until all options chosen or player inputs return option
    actions_available = ["check the cctv (c)", "look around (s)", "talk to a witness(t)"]
    while actions_available:
        print("")
        print("Would you like to:")
        # checks number of actions available and requests and confirms appropriate input
        confirmed_action = ""
        # No actions yet completed
        if len(actions_available) == 3:
            while True:
                action = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                print(confirmed_action)
                if confirmed_action in ("c", "s", "t", "r"):
                    break
                else:
                    print("")
                    print("Your input does not match requirements.\nYou need to either type 'c', 's', 't' or 'r'  please try again")
                    print("")
        # One action completed
        elif len(actions_available) == 2:
            # Work out which actions are left
            choice_1 = ""
            if actions_available[0] == "check the cctv (c)":
                choice_1 = "c"
            elif actions_available[0] == "look around (s)":
                choice_1 = "s"
            elif actions_available[0] == "talk to a witness(t)":
                choice_1 = "t"
            else:
                print("ERROR!! Please contact developer")
            choice_2 = ""
            if actions_available[1] == "check the cctv (c)":
                choice_2 = "c"
            elif actions_available[1] == "look around (s)":
                choice_2 = "s"
            elif actions_available[1] == "talk to a witness(t)":
                choice_2 = "t"
            else:
                print("ERROR!! Please contact developer")
            # Request input and error handle
            while True:
                action = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, choice_2, "r"):
                    break
                else:
                    print("")
                    print(f"Your input does not match requirements.\nYou need to either type '{choice_1}', '{choice_2}' or 'r'. Please try again")
                    print("")
        # Two actions completed
        elif len(actions_available) == 1:
            # Work out which actions is left
            choice_1 = ""
            if actions_available[0] == "check the cctv (c)":
                choice_1 = "c"
            elif actions_available[0] == "look around (s)":
                choice_1 = "s"
            elif actions_available[0] == "talk to a witness(t)":
                choice_1 = "t"
            else:
                print("ERROR!! Please contact developer")
            while True:
                action = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, "r"):
                    break
                else:
                    print("")
                    print(f"Your input does not match requirements.\nYou need to either type '{choice_1}' or 'r' please try again")
                    print("")
        else:    
            print("ERROR!!")
        # Carries out chosen action
        if confirmed_action == "c":
            position_of_choice = actions_available.index("check the cctv (c)")
            actions_available.pop(position_of_choice)
            print("")
            cctv_clue = current_location.cctv_crime_scene()
            clues_for_notebook = clues_for_notebook + cctv_clue
        elif confirmed_action == "s":
            position_of_choice = actions_available.index("look around (s)")
            actions_available.pop(position_of_choice)
            print("")
            look_around_clue = current_location.look_around_crime_scene()
            clues_for_notebook = clues_for_notebook + look_around_clue
        elif confirmed_action == "t":
            position_of_choice = actions_available.index("talk to a witness(t)")
            actions_available.pop(position_of_choice)
            print("")
            witness_clue = current_location.talk_witness_crime_scene()
            clues_for_notebook = clues_for_notebook + witness_clue
        elif confirmed_action == "r":
            break
        else:
            print("ERROR!!")
    # Once all actions completed and loop exited or user chooses to return to main_actions
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
    work_location = suspect_details[3]
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
    current_suspect = Suspect_is_thief(suspect_name, occupation, work_location, hobby_location, character_connection, connection_location, presence_reason, motive, denile)
    return current_suspect

def set_present_at_scene_suspect(suspect_number, current_case):
    """
    builds an instance of the Present_at_scene_suspect class specific to this game
    """
    # Find variables needed from all_suspects list of lists
    suspect_details = current_case.all_suspects[suspect_number]
    suspect_name = suspect_details[0]
    occupation = suspect_details[1]
    work_location = suspect_details[3]
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
    current_suspect = Present_at_scene_suspect(suspect_name, occupation, work_location, hobby_location, character_connection, connection_location, presence_reason, item_connection)
    return current_suspect

def set_suspect(suspect_number, current_case):
    """
    builds an instance of the Unconnected_suspect class specific to this game
    """
    # Find variables needed from all_suspects list of lists
    suspect_details = current_case.all_suspects[suspect_number]
    suspect_name = suspect_details[0]
    occupation = suspect_details[1]
    work_location = suspect_details[3]
    hobby_location = suspect_details[4]
    connection_location = suspect_details[5]
    character_connection = suspect_details[6]
    # build an instance of the Unconnected_suspect class and return
    current_suspect = Unconnected_suspect(suspect_name, occupation, work_location, hobby_location, character_connection, connection_location)
    return current_suspect

def question_suspect(current_suspect, current_case):
    """
    Runs call_suspect_for_questioning, requests player to choose next action and handles their choice
    Returns to main_action_choices at players request or when all location actions completed
    """
    clear()
    clues_for_notebook = f"{current_suspect.suspect_name}:\n"
    current_suspect.call_suspect_for_questioning()
    # Loop requesting and handling choice from player
    # User will only be present with options they haven't already chosen plus return option
    # Loop will run until all options chosen or player inputs return option
    actions_available = ["why they were present at the crime scene (p)", "about there movements over the last two days (m)", "if they recognise the stolen item (i)"]
    while actions_available:
        print("")
        print("Would you like to ask the suspect:")
        # checks number of actions available and requests and confirms appropriate input
        confirmed_action = ""
        # No actions yet completed
        if len(actions_available) == 3:
            while True:
                action = input(f"{actions_available[0]}, {actions_available[1]} or {actions_available[2]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in ("p", "m", "i", "r"):
                    break
                else:
                    print("Your input does not match requirements.\nYou need to either type 'p', 'm', 'i' or 'r'  please try again")
                    print("")
        # One action completed
        elif len(actions_available) == 2:
            # Work out which actions are left
            choice_1 = ""
            if actions_available[0] == "why they were present at the crime scene (p)":
                choice_1 = "p"
            elif actions_available[0] == "about there movements over the last two days (m)":
                choice_1 = "m"
            elif actions_available[0] == "if they recognise the stolen item (i)":
                choice_1 = "i"
            else:
                print("ERROR!! Please contact developer")
            choice_2 = ""
            if actions_available[1] == "why they were present at the crime scene (p)":
                choice_2 = "p"
            elif actions_available[1] == "about there movements over the last two days (m)":
                choice_2 = "m"
            elif actions_available[1] == "if they recognise the stolen item (i)":
                choice_2 = "i"
            else:
                print("ERROR!! Please contact developer")
            # Request input and error handle
            while True:
                action = input(f"{actions_available[0]} or {actions_available[1]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, choice_2, "r"):
                    break
                else:
                    print(f"Your input does not match requirements.\nYou need to either type {choice_1}, {choice_2} or 'r'. Please try again")
                    print("")
        # Two actions completed
        elif len(actions_available) == 1:
            # Work out which action is left
            choice_1 = ""
            if actions_available[0] == "why they were present at the crime scene (p)":
                choice_1 = "p"
            elif actions_available[0] == "about there movements over the last two days (m)":
                choice_1 = "m"
            elif actions_available[0] == "if they recognise the stolen item (i)":
                choice_1 = "i"
            else:
                print("ERROR!! Please contact developer")
            while True:
                action = input(f"{actions_available[0]}\nAlternatively type (r) to return to the main options\n")
                confirmed_action = action.strip().lower()
                if confirmed_action in (choice_1, "r"):
                    break
                else:
                    print(f"Your input does not match requirements.\nYou need to either type {choice_1} or 'r' please try again")
                    print("")
        else:
            print("ERROR!!")
        # Carries out chosen action
        if confirmed_action == "p":
            position_of_choice = actions_available.index("why they were present at the crime scene (p)")
            actions_available.pop(position_of_choice)
            print("")
            presence_clue = current_suspect.question_reason_at_crime_scene()
            clues_for_notebook = clues_for_notebook + presence_clue
        elif confirmed_action == "m":
            position_of_choice = actions_available.index("about there movements over the last two days (m)")
            actions_available.pop(position_of_choice)
            print("")
            location_connection_clue = current_suspect.question_connections()
            clues_for_notebook = clues_for_notebook + location_connection_clue
        elif confirmed_action == "i":
            position_of_choice = actions_available.index("if they recognise the stolen item (i)")
            actions_available.pop(position_of_choice)
            print("")
            item_recognition_clue = current_suspect.question_item_recognition()
            clues_for_notebook = clues_for_notebook + item_recognition_clue
        elif confirmed_action == "r":
            break
        else:
            print("ERROR!!")
    # Once loop completed or user chooses to return
    print("")
    update_notebook(current_case.notebook_column, [clues_for_notebook])
    print("Exiting location. You will now be taken back to the main options")
    print("")
    main_action_options(current_case)

# Game win specific functions

def arrest_confirm(suspect_number, current_case):
    """
    Confirms that the player definitely wants to arrest the suspect they have chosen
    """
    suspect_name = current_case.all_suspects[suspect_number][0]
    question_arrest = f"Are you sure {suspect_name} is the thief? Remember here at Case Closed we don’t tolerate false arrests!"
    print(question_arrest)
    while True:
        arrest_input = input("y/n\n")
        arrest_confirm = arrest_input.strip().lower()
        if arrest_confirm == "y":
            break
        elif arrest_confirm == "n":
            break
        else:
            print("Your input does not match requirements.\nYou need to either type 'y' or 'n' please try again")
            print("")
    if arrest_confirm == "y":
        arrest_suspect(suspect_name, current_case)
    elif arrest_confirm == "n":
        print("Returning you to the main options")
        main_action_options(current_case)
    else:
        print("ERROR!!!")

def arrest_suspect(suspect_name, current_case):
    """
    Check if the chosen suspect is the theif and print corrosponding story line
    """
    clear()
    if suspect_name == current_case.thief_details["Thief"]:
        title = """
       ___                            _         _       _   _                 
      / __\___  _ __   __ _ _ __ __ _| |_ _   _| | __ _| |_(_) ___  _ __  ___ 
     / /  / _ \| '_ \ / _` | '__/ _` | __| | | | |/ _` | __| |/ _ \| '_ \/ __|
    / /__| (_) | | | | (_| | | | (_| | |_| |_| | | (_| | |_| | (_) | | | \__ \
    \____/\___/|_| |_|\__, |_|  \__,_|\__|\__,_|_|\__,_|\__|_|\___/|_| |_|___/
                      |___/  
"""
        print(title)
        correct_arrest_statement = f"You have arrested the correct suspect.\nYou read {suspect_name} their rights and they hang their head in shame."
        print(correct_arrest_statement)
        print("")
        crime_motive = f"You ask {suspect_name} why they stole the {current_case.case_details['item']}\n'{current_case.thief_details['Motive']}'"
        print(crime_motive)
        notebook_clue_one = "Correct arrest!"
        notebook_clue_two = f"{suspect_name} stole the {current_case.case_details['item']}"
        notebook_entries = [notebook_clue_one, notebook_clue_two]
        notebook_row = current_case.notebook_column
        update_notebook(notebook_row, notebook_entries)
        check_for_win(current_case)
    else:
        game_over("false_arrest", current_case)

def confirm_warrant_request(location_number, current_case):
    """
    Confirms that the player definitely wants to obtain a search warrant for the chosen location
    """
    location_name = current_case.all_locations[location_number][0]
    question_warrant = f"Are you sure the thief hid the {current_case.case_details['item']} at the {location_name}? This is your one chance to find it!"
    print(question_warrant)
    while True:
        confirm_input = input("y/n\n")
        warrant_confirm = confirm_input.strip().lower()
        if warrant_confirm == "y":
            break
        elif warrant_confirm == "n":
            break
        else:
            print("Your input does not match requirements.\nYou need to either type 'y' or 'n' please try again")
            print("")
    if warrant_confirm == "y":
        search_location(location_number, current_case)
    elif warrant_confirm == "n":
        print("Returning you to the main options")
        main_action_options(current_case)
    else:
        print("ERROR!!!")

def search_location(location_number, current_case):
    """
    Check if the chosen location is the stash_location and print corrosponding story line
    """
    clear()
    # retrieve all variables required
    location_name = current_case.all_locations[location_number][0]
    employee = current_case.all_locations[location_number][2]
    item = current_case.case_details['item']
    crime_scene = current_case.case_details['crime_scene']
    locations = SHEET.worksheet("locations")
    location_name_column = locations.col_values(1)
    crime_scene_location_row = location_name_column.index(crime_scene) + 1
    item_owner = locations.cell(crime_scene_location_row, 3).value
    # Present search warrant
    present_search_warrant = f"You present the search warrant to {employee} at the {location_name}. They look thoroughly confused but you ignore them and enter the building."
    print(present_search_warrant)
    print("")
    # check if the chosen location is the stash_location and print corrosponding story line
    if location_name == current_case.stash_location:
        clear()
        title = """
     ___                            _         _       _   _                 
    / __\___  _ __   __ _ _ __ __ _| |_ _   _| | __ _| |_(_) ___  _ __  ___ 
   / /  / _ \| '_ \ / _` | '__/ _` | __| | | | |/ _` | __| |/ _ \| '_ \/ __|
  / /__| (_) | | | | (_| | | | (_| | |_| |_| | | (_| | |_| | (_) | | | \__ \
  \____/\___/|_| |_|\__, |_|  \__,_|\__|\__,_|_|\__,_|\__|_|\___/|_| |_|___/
                    |___/
"""
        print(title)
        search = f"While searching the {location_name} you find {item}"
        print(search)
        print("")
        # Print return item story line
        return_item = f"You head straight to the {crime_scene} And give the {item} back to {item_owner}"
        print(return_item)
        print("")
        # Print thank you story line
        print(f"{item_owner} beams with delight as you hand them back the {item}")
        print(f"How can I ever thank you Junior detective {current_case.player_name}!!!")
        # Update the notebook
        notebook_clue_one = "Item found!"
        notebook_clue_two = f"The {item} was hidden at the {location_name}"
        notebook_entries = [notebook_clue_one, notebook_clue_two]
        notebook_row = current_case.notebook_column
        update_notebook(notebook_row, notebook_entries)
        check_for_win(current_case)
    else:
        long_search = f"Six hours later you have thoroughly searched the {location_name} but {item} is nowhere to be found. You resign yourself to the fact that it is not here."
        print(long_search)
        agitated_employee = f"Throughout your search {employee} has become more and more agitated as you have torn apart the {location_name} looking for the {item} and is now in a state of great upset."
        print(agitated_employee)
        print("")
        boss_appears = f"Detective Inspector Job Done appears.\n'What are you doing {current_case.player_name}? It is clear the {item} is not here!'"
        print(boss_appears)
        print("")
        reassure_employee = f"Detective Inspector Job Done turns to {employee} 'I cannot apologise enough {employee}, rest assured {current_case.player_name} will not be allowed to leave until the {location_name} is spotless and back to it’s normal state!'"
        print(reassure_employee)
        print("")
        tidy_location = f"Finally the {location_name} is tidy.\nDetective Inspector Job Done inspects your work.\n'Hmm that will do. Maybe you should find yourself a cleaning job as you are clearly no detective!'"
        print(tidy_location)
        game_over("false_search_warrant", current_case)

def check_for_win(current_case):
    """
    Checks to see if the player has achieved both the arrest and the item location
    """
    notebook_row = current_case.notebook_column
    notebook = SHEET.worksheet("notebook")
    notebook_row_list = notebook.row_values(notebook_row)
    found_item = ""
    thief_arrested = ""
    try:
        found_item = notebook_row_list.index("Item found!")
    except ValueError:
        print("")
        print("Now you just need to retrieve the stolen item. Remember you can obtain a search warrant from the map in order to thoroughly search a location")
    try:
        thief_arrested = notebook_row_list.index("Correct arrest!")
    except ValueError:
        print("")
        print("Now you just need to arrest the thief")
    if found_item and thief_arrested:
        win(current_case)
    else:
        print("Returning you to the main options")
        main_action_options(current_case)

def win(current_case):
    """
    Prints win storyline
    """
    clear()
    print("Detective Inspector Job appears")
    print("")
    congratulations = f"Absolutely amazing work Junior detective {current_case.player_name} you have correctly arrested {current_case.thief_details['Thief']} and located the {current_case.case_details['item']}. You have preserved the reputation of the Case Closed Detective Agency and we would be delighted for you to continue working as part of our team.”"
    print(congratulations)
    notebook_row = current_case.notebook_column
    update_notebook(notebook_row, "Win achieved")
    title = """
      __________________________________________________________________
            __                                                          
          /    )                              /                        /
      ---/---------__---__----__--------__---/----__---__----__----__-/-
        /        /   ) (_ ` /___)     /   ' /   /   ) (_ ` /___) /   /  
      _(____/___(___(_(__)_(___ _____(___ _/___(___/_(__)_(___ _(___/___

"""
    print(title)
    new_game(current_case)

intro_and_setup()
# Write your code to expect a terminal of 80 characters wide and 24 rows high
