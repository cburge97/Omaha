# Omaha 
## Description
### What?

Omaha  is a web application that will help users. It will allow users to see different statistics about different players. It will also give them strategies and helpful advice to build a Fantasy Football Team.
### Why?

With Omaha , we aim to assist people who have had trouble building a Fantasy Football team in the past. This app could be used for daily fantasy football player, weekly, or league fantasy football. If our program works correctly, it would give them an advantage over their competition and the potential to win their league. There are other apps that do similar things to ours but most of them are not extremely accurate at predicting the stats for all the players.
### How?

Omaha  will purely be a software product that runs on a web application. The app will be able to store data from the past seasons then recover the data efficiently. Our team will implement a full-stack application model, with front end and back end. The framework and tools we expect to use are:

Front End
* HTML, CSS
* JavaScript

Back end
* NodeJS
* Python
* SQL

Tools
*Anaconda (Jupyter Notebooks) Visual Studio Code, Git/GitHub
*Google Drive
*Kaggle.com
*Trello

Miscellaneous

## Deliverables

1.	Web app
  * View Player Stats
       * User can view different player stats. There will be a link the user clicks on and a pop up will showing the player stats
  * Import Current Team
       * User can import their current Fantasy Team and the app will show the user stats of their players and give them feedback
  * Offense Focused
       * For now we will stick with offense Focused Fantasy Leagues. The site will contain posistions: QB, RB,WR, TE, K, D
  * Rate Trades
       * User will be able to put in a player they have and input a player they are trading for. The app will give them feedback on the trade, show them the risks, and grade the trade on a letter grade
  * Rate Add/Drop
       * User will be able to put a player that they are either dropping from their team, a player they wish to add, or both. The app will give them feedback based on what action they do. (Similar to Rate Trades)
  * Suggested Lineup
       * The app will give advice on what players the user should start that week
2.	Documentation 
  * Project Proposal
  * Pitch Presentation
  * Project Plan Dcument
  * Desgin Document 
  * Weekly Updates
  * Poster
3.  Testing 
  * Test View Player Stats
       * Test to see if we can view player stats with the link
  * Test Import Current Team
       * See if the database can take the users players and pull the data for the players
  * Test Rate Trades
       * Test to see if our Machine Learning code gives accurate results
  * Rate Add/Drop
       * Test to see if our Machine Learning code gives accurate results
  * Suggested Lineup
       * Test to see if our Machine Learning code gives feedback
  * Test Database Connection
       * Test to see if database connects to web app
  * Test Web App
       Test to see if app can be viewed on different browsers
4. Optional Features
  * Rank Player vs. Opponent Team
       * User will be able to see how one of their NFL players stacks up against the NFL Team they are facing. 
  * League with Defenseive players
       * Some Fantasy Leagues use individual defensive players. Hope to expand to where users who use either a offensive league or an offensive + defensive league can use webb app
  * Random Facts
       * Simple page where people can view random facts
  * Rookie Page
       * Page that predicts stats for this years rookies

## Getting Started

### Install
* XAMPP
* Python 2.7
* body-parser@1.19.0
* bootstrap@4.3.1
* child_process@1.0.2
* ejs@2.6.2
* express@4.17.1
* express-fileupload@1.1.5
* UNMET PEER DEPENDENCY jquery@1.9.1 - 3
* mysql@2.17.1
* UNMET PEER DEPENDENCY popper.js@^1.14.7
* python-shell@1.0.7
* req-flash@0.0.3
* requirejs@2.3.6 extraneous

### Run
1. Start-up Database
   * Run XAMPP Control Panel
   * Start Apache 
   * Start MySQL
2. Open Command prompt
   * Go to the directory where the project is located
   * Run node app.js command
3. Website
   * Open a browser
   * Type http://localhost:5000/ as the url
  
### Features
1. Player Stats Page:
   * User navigates to through Player Stats page
   * Can view different stats from of different players
   * Can use search filter bar to find specific players by first or last name
   * User clicks on player row to view stats from 2016, 2017, and overall stats
  
2. Add drop Page:
   * User navigates through add drop page
   * user selects how many people they want to drop from their team
   * user selects how many people they want to add to their team
   * user input player names into the text boxes
   * user clicks on submit button and gets a rating on their transaction and gets feedback on if the transaction is worth it
  
3. Trade Page:
   * User navigates through add drop page
   * user selects how many people they want to trade away from their team
   * user selects how many people they will recieve from the other team
   * user input player names into the text boxes
   * user clicks on submit button and gets a rating on their transaction and gets feedback on if the transaction is worth it
  
4. Draft Page:
   * User navigates through draft page
   * User inputs how many people are in their draft and what draft pick they have
   * User can scroll and view stats of each player by clicking the player name once
   * User selects a player by double clicking the player name in the table
   * As draft goes on, user clicks on the players on the players that have been taken so those players are added to the taken list
   * When it's users time to pick a player, they double click and the player is added to the taken list and the user's team list
   * When draft is finished, user clicks submit and gets  feedback on how each player they chose will do this year and the overall grade on how they drafted
   
### Demo Video

https://www.youtube.com/watch?v=MF-7dYxFUzQ

## Team members

* Christopher Burgess, Backend Developer, Tester, Team Lead
* Dheric Seney, Frontend Developer, Database Developr

