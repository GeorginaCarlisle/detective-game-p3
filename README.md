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

[Return to contents list](#contents)

## Deployment

[Return to contents list](#contents)

## Cloning this repository

[Return to contents list](#contents)

## Forking a branch

[Return to contents list](#contents)

## Making additions and changes to the game

[Return to contents list](#contents)

## Languages

[Return to contents list](#contents)

## Tools and Technologies

[Return to contents list](#contents)

## Credits

[Return to contents list](#contents)

## Acknowledgements

[Return to contents list](#contents)

