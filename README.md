# TablePlanner

**Event Seating Planning Tool for DNDGent**

TablePlanner is a tool that helps the organizers of [DNDGent](https://www.dndgent.be/) efficiently plan seating arrangements for their tabletop RPG events.

### Showcase

https://github.com/user-attachments/assets/9c78af46-ecf5-469d-9d71-f46ecf672ea8

## About the Project

Events at DNDGent typically consist of around 50 participants divided over approximately 8 tables, each led by a Dungeon Master (DM). Participants can submit preferences for who they'd like to sit with and which DM they'd like to guide their game. Balancing all of these preferences manually is time-consuming and error-prone — TablePlanner automates this process.

## Features

### Excel-Based Interface
The tool is designed to integrate into the organizers' existing workflow. Input data (participants, preferences, available DMs, and reserved tables) is read from Excel files that the organizers maintain. The generated seating plan is also exported as an Excel file.

### Sorting Algorithm
All the preferences, for both player groups and desired DMs, and the rules of planning are taken into account. The participants' preferences for their playmates are kept as "friendgroups".

Every player is part of either one friendgroup or none. The participants for a specific event that are of the same friendgroup are put together in clusters. Clusters are paired with the DM with the most "votes" (each respective player’s reported preferred DM). The biggest clusters are paired with the biggest tables.

Those that don't have a group, or who have no members of their group participating, are put at the tables of their preferred DM or distributed evenly between the remaining spots.
This is the main feature of this application see here:
[Table Planner](DNDProj/services/planner.py)

### Simple GUI
A straightforward interface displays all registrations alongside the suggested seating plan. Icons indicate which participants share a friend group and whether they've been matched with their preferred DM.

### Planning requirements list
1 Seats players with friends
2 Seats players with prefered DM's
3 Does not exceed a DM's prefered maximum number of players, but will if necessary to seat all players
4 Will never put less then 3 players at one table
5 Will distribute players evenly among tables if all above requirements are satisfied
6 Puts the biggest groups at the biggest tables




