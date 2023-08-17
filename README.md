# Detective game

Developer: Georgina Carlisle

A detective game where the player must follows the clues to work out who stole the missing item and where they have hidden it.

This game is currently under development

## Contents
[Features](#features)

[Design](#design)
- [The Strategy Plane](#the-strategy-plane)
- [The Scope Plane](#the-scope-plane)
- [The Structure Plane](#the-structure-plane)

[Testing and Validation](#testing-and-validation)

[Bugs and Fixes](#bugs-and-fixes)

[Deployment](#deployment)

[Cloning this repository](#cloning)

[Forking a branch](#forking)

[Making additions and changes to the game](#making-additions-and-changes-to-the-game)

[Languages](#languages)

[Tools and technologies](#tools-and-technologies)

[Credits](#credits)

[Acknowledgements](#acknowledgements)

## Features

## Design

### The Strategy Plane

#### Users

The target audience enjoy solving ‘who dunnit’ mysteries. They enjoy finding clues and linking them together in order to solve a puzzle. They also enjoy the narrative of a story. In particular, the story lines and level of difficulty will make it suitable for children to play.

As a first-time user:
-	I would like to understand what sort of game this is and what it is about before I start playing.
-	I would like to know what happens to any information that I input into the game.
-	I would like the game controls, what I need to do and how I can win to be concisely explained and easy to understand.

As a user:
-	I would like a ‘who dunnit’ style mystery to solve.
-	I would like the story line of the game to both make sense and be enjoyable.
-	I would like to be able to move through the game easily, quickly navigating between different options.
-	I would like to be able to review any clues that I have picked up as and when I would like to.
-	I would like the game to provide challenge so that I have to link together multiple clues, but I would like the trail to be fairly obvious. 

As a returning user:
-	I would like the game to be different each time I play so that it is always a mystery. 
-	I would like the story that ends up unfolding as I play to be different each time.
-	I would like the game to be structured to minimise and avoid short cuts where possible. For example: once I find the thief I don’t want to automatically know where they have hid the item, because the item is always to be found in thief’s work location. 

#### Owner

The owner is looking to:
-	Provide a fun and enjoyable ‘who dunnit’ style mystery game that both children and adults can enjoy.

The owner requires:
-	The ability to quickly and easily add, update or change different elements to the game. These elements are to include the case present to the user, the suspects and the locations.
-	Readable code that allows for quick debugging.
-	Data to allow for further improving and refining of the game. Data showing how users are moving through the game, whether they are picking up on and following the clues and whether they are correct in their guesses as to the thief and the location of the stolen item. Data providing feedback from users.

[Return to contents list](#contents)

### The Scope Plane

The scope for this project explores the requirements of both user and owner, and how these could be met.

| Requirement | Feature |
| -- | -- |
| Explanation as to the style and theme of the game before first input required. | 1. Introduction to the game that displays right under the title. |
| Clear explanation of what happens to any information that the user inputs into the game. | 2.	As part of (1) a clear explanation given about input data. |
| Clear and concise explanation of the game aim, movement through the game and controls. | 3. Paragraph introducing the case and explaining the players actions. |
| | 4. Available player actions clearly stated at each point input is required. |
| | 5. Player given clear feedback should an error occur on input. |
| A ‘who dunnit’ style mystery that requires solving. | 6. Player set a case to solve. Each case will involve a stolen item and the player will need to work out who stole it and where it is hidden. |
| An enjoyable storyline to the game that makes sense. | 7.	During (3) the scene will be set. Who the player is, what their role is, the case etc. |
| | 8. Throughout the game player movements and clues will be given in a narrative fashion. |
| | 9. Each case (6) will involve a plausible event, a reason for characters being at the event and a motive for the thief (these will discovered at different points of the game) to steal the item. All characters will have a reason for being at any locations in which they are found. |
| Straight forward and easy to use navigation through the game. | 3, 4, 5 |
| | 10. Likely routes of movement through the game thought of and catered for. Available player actions will allow the player to quickly jump to areas of the game they may want to visit without overloading with options. Movement is logical at all points. |
| Option to review clues gained so far available throughout the game. | 11.	The player will have a notebook that they can access at all points during the game. This notebook will contain all the clues they have collected in the order they have collected them. Clues will be summarised clearly and concisely within the notebook. |
| User required to link together multiple clues in order to solve the mystery. | 12. Each clue come across will link the player to a further location where they might gain other clues or to the thief. The first couple of clues will allow the player to narrow the suspect list but they will have to move further into the game to confirm who the thief is and then locate the item. |
| Trail of clues to be fairly obvious. | 13. Each clue pointing to a location will clearly link to that location. As the player moves through the game the thief will begin to clearly stand out, as will the location of the item. |
| Multiple game scenarios. | 14. The game will include multiple stolen items and for each item there will be 3 different thieves and for each thief 2/3 different locations they might have hidden the item. All of these will be randomly chosen from a background spreadsheet. |
| Storyline variations. | 15. Each stolen item will have a different storyline detailing the event during which it was stolen. |
| | 16.	Each thief will have a motive and clue to be found that is specific to the case. |
| No/minimal short cuts for returning users. | 17. Potential shortcuts to be evaluated during the structure plane and the structure changed, if possible, in order to eliminate. |
| Game can be enjoyed by both children and adults | Each case (6) will be a stolen item rather than a murder. Clues will be fairly obvious (13) and the storyline (7, 8, 9, 15, 16) will be appropriate and make sense to children. |
| Game elements such as: the case present to the user, the suspects and the locations  can be easily and quickly added, update or changed. | 18. All details relevant to the case, the locations and the suspects will be stored in a background spreadsheet. Allowing for any of these to be changed, removed or added to without any alteration to the code. |
| Readable code that allows for quick debugging. | 19.	Readable code with clear comments that is easy to follow through. Also see (5) |
| Data showing how users are moving through the game, whether they are picking up on and following the clues and whether they are correct in their guesses as to the thief and the location of the stolen item. | 20. The spreadsheet will also include a notebook sheet where all the clues the player picks up in the order they have picked them up will be recorded. As well as linking to the virtual notebook (11) this will continue to be stored after the game is completed. The players name will not be stored. |
| Data providing feedback from users. | 21.	The user will be prompted to provide any feedback at the end of the game that will be stored within the notebook sheet. User to be made aware that their comments will be stored. |

All features to be implement during the 1st edition of this application. However only 3 cases and corresponding elements will be created initially.

[Return to contents list](#contents)

### The Structure Plane

Detective game is a terminal based game. The following flow diagram shows how the player will move through the game.
Available player actions will be clearly stated at each point input is required. Player input will then activate the chosen action.

![Flow diagram showing how the player will move through the game](documentation/game_flow.drawio.pdf)

The following diagram shows the clues that can be gained through visiting a location or questioning the suspect and how these lead the player to further linked locations and build a clear picture of who the thief is and where they have stashed the item. The green font shows all the information that is specific to the case and thief identity and the black shows background information that will always show regardless of the case or thief.

![Diagram showing how the clues will work](documentation/clues.drawio.pdf)

[Return to contents list](#contents)

## Testing and Validation

[Return to contents list](#contents)

## Bugs and fixes

| Bug | Action | Result |
| -- | -- | -- |
| Error and Warning from cloud.google that quota reached | Followed links in warning and researched api quotas. Made changes to code to reduce api calls, pulling and pushing information in larger chunks to reduce the number of calls | Resolved: no reacurrence of error or warning, situation to be monitored |
| gspread generated message printed to terminal when first api call goes through | Current research and asking for help has not led me to find a way to prevent or hide this message. In order to reduce the impact on users a message prior to first api call 'Please ignore the following message:' and messages to reassure as the settings are built 'Your game is now loading' 'Almost there ....' have been added | Unresolved: no impact on running of program and action taken to reduce impact on user |
| Suspect from whom the item is stolen, won't recognise it when questioned or react as they should during questioning | This is a current flaw in the underlining logic that was realised too late to be fixed | Unresolved: will only be noticed by user should they happen to question this individual |

All unresolved bugs will be handled during the next release of the game.

[Return to contents list](#contents)

## Deployment

This website has been deployed using Heroku.

Instructions to deploy using Heroku:

1 - While in Heroku, navigate to dashboard and then click on the new button in the top right corner choosing: create new app.

2 - Input a name for your app (this name will need to be unique) and choose the correct region for where you are located. Click create app.

3 - Your app has been created, now click on the settings tab.

4 - Click reveal config vars to add any keys the application will need. For this project I added the api credentials for my spreadsheet to a key of CREDS and a value of 8000 to a key of PORT.

5 - Click add buildpack to install any interdependecies needed. For this project I installed 'python' and 'nodejs'.

6 - Click on deploy tab. Select deploy method, in this case Git Hub. Confirm connection to git hub by searching for the correct repository and then connecting to it.

7 - To manually deploy project click 'Deploy Branch'. Once built a message will appear saying: Your app was successfully deployed. Click the view button to view the deployed page making a note of it's url.

[Return to contents list](#contents)

## Cloning this repository

In order to work on this repository you will first need to clone it.

**Instructions to clone the repository**:

1 - While in the GitHub repository, click on the green code button.

2 - Copy the link.

3 - In your IDE or local coding environment use the link to open the repository. 

For example: in VScode 
- clicking on 'Clone Git Repository...' will bring up a box in which to paste the link. 
- once vscode has the link, you will then be asked where you would like the repo saving.
- You should now be set up ready to work on the repository.

For example: in CodeAnywhere
- Click on 'Add new workspace'
- You will then be given the option to 'Create from your project repository' and a box in which to paste the link
- CodeAnywhere will now open a new workspace containing the repository.
- You should now be set up ready to work on the repository.

[Return to contents list](#contents)

## Forking a branch

In order to protect the main branch while you work on something new, essential when working as part of a team or when you want to experiment with a new feature, you will need to fork a branch.

**Instructions to fork the repository**:

1 - While in the GitHub repository, click on the branch symbol and text indicating the number of branches.

2 - This will load details on current branches. Click on the green 'New branch' button.

3 - Enter a name for the new branch and then click the green 'create new branch' button.

4 - Your new branch should now have appeared on the screen.

5 - Clicking on the new branch and then following the steps for cloning will allow you to open up and work on this branch.

[Return to contents list](#contents)

## Making additions and changes to the game

To add a new case, or make changes to the suspects, locations or current case no change to the code is needed. This can all be done through the background spreadsheets.


When editing the suspects, case or locations sheets, the following rules need to be followed:
- number of suspects/locations must remain as 8.
- all columns must be filled
- location names must exactly match their name as written elsewhere
- Suspect names must exactly match their names as written else where
- take time to preview changes in the game, to ensure that any wording works in context

[Return to contents list](#contents)

## Languages

Python with the following libraries:
- gspread
- datetime
- random
- os
- time

[Return to contents list](#contents)

## Tools and Technologies

- Codeanywhere: Used for writing, previewing and pushing the code to git hub
- VScode: Used for writing and pushing the code to git hub
- Git: Used for version control
- Git hub: Used to store the repository for this project
- Heroku: Used to deploy the website
- [CI Python Linter](https://pep8ci.herokuapp.com): Used to validate Python code
- [Text to ASCII Art Generator](http://patorjk.com/software/taag/#p=display&h=2&v=2&f=AMC%20Thin&t=Notebook): Used to generate the title art created (note the buildings art was created by myself).
- [draw.io](https://app.diagrams.net/): Used to create the flow charts used during planning

[Return to contents list](#contents)

## Credits

### Code

- This project was made using the following template [Code Institute p3-template](https://github.com/Code-Institute-Org/p3-template). This template provides all the supprting code which allows my python run.py to run within a console window within a web page.

- Activating API credentials, connecting to API and importing of gspread library were all completed following the Love Sandwiches walkthrough by Code Institute.

- The clear() function created to clear the screen when called, making the latest text easier to find and read, was copied from a project by Juan A. Boccia [PP3_Diego_Santacarmen
](https://github.com/jbocciadev/PP3_Diego_Santacarmen).

- The use of the sleep() method imported from time, was copied from a project by Juan A. Boccia [PP3_Diego_Santacarmen
](https://github.com/jbocciadev/PP3_Diego_Santacarmen).

### Title art

- The Case closed, Map, Suspects and congratulations title art were created by Ethan and Ray Carlisle using [Text to ASCII Art Generator](http://patorjk.com/software/taag/#p=display&h=2&v=2&f=AMC%20Thin&t=Notebook)

### Detective storyline

- The case of the stolen manuscript, Famous author's treehouse in the woods location and suspect Mr Ethan Carlisle were written in collaboration with Ethan Carlisle.

- The case of the stolen crown, the library location and suspect Mr Ray Carlisle were written in collaboration with Ray Carlisle.

[Return to contents list](#contents)

## Acknowledgements

My two young boys - For being the inspiration and the drive for this project. It is for them. They also helped with the detective storyline and the creation of the title art. They tested the game and gave feedback. They kept me going with their support and were completely understanding of the time I spent sat at my laptop during their summer holidays.

My husband - For his invaluable support and lots of user testing throughout the development of this project.

Juan A. Boccia - His project [PP3_Diego_Santacarmen
](https://github.com/jbocciadev/PP3_Diego_Santacarmen) provided me with the idea of creating a detective game for my third portfolio project.

My mentor Gurjot - For his reassurance and push to make sure there were no global variables.

Code Institue - The vast majority of the coding skills, knowledge and understanding showcased in this project have been learnt through the 'Diploma of Full stack software development' that I am completing with Code Institute.

### Websites, articles and tutorials

[Python Tutorial: Datetime Module](https://www.youtube.com/watch?v=eirjjyP2qcQ) - This tutorial helped me to understand how to get today's date.

[Gspread documentation](https://docs.gspread.org/en/v5.10.0/) - This document was invaluable in locating the methods I needed to be able to interact with my spreadsheet.

[Python List index() method](https://www.w3schools.com/python/ref_list_index.asp) - This article helped me to understand how to search for the location of the thief name within the list generated from the first column of the suspects sheet.

[Python *args](https://www.youtube.com/watch?v=MNLy8atLI3k) - This tutorial aided my understanding of *args and how to handle them.

[Stack Overflow: Access item in a list of lists](https://stackoverflow.com/questions/18449360/access-item-in-a-list-of-lists) - This question and its responses helped me in retrieving a value from a list of lists.

[How to use google sheets with Python](https://www.youtube.com/watch?v=bu5wXjz2KvU) - This tutorial was invaluable in helping me understand how to use the get() gspread method. 

[Return to contents list](#contents)

