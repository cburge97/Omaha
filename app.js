const express = require('express');
const fileUpload = require('express-fileupload');
const bodyParser = require('body-parser');
const mysql = require('mysql');
const path = require('path');
const app = express();

const {getHomePage} = require('./BackEnd/index');

//Playerstats
const {playerStatsPage, playerStats} = require('./BackEnd/PlayerStats/PlayerStats');

//Draft
const {draftPage, draft} = require('./BackEnd/Draft/Draft');

//Trade
const {tradePage, trade} = require('./BackEnd/Trade/trade');

//Add&Drop
const {addDropPage, addDrop} = require('./BackEnd/AddDrop/AddDrop');

//Team
const {teamPage, team} = require('./BackEnd/Team/Team');

const port = 5000;

// create connection to database
// the mysql.createConnection function takes in a configuration object which contains host, user, password and the database name.
const db = mysql.createConnection ({
    multipleStatements: true,
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'nfl player stats'
});

// connect to database
db.connect((err) => {
    if (err) {
        throw err;
    }
    console.log('Connected to database');
});
global.db = db;

//include css
app.use(express.static('css'));

// configure middleware
app.set('port', process.env.port || port); // set express to use this port
app.set('views', __dirname + '/views'); // set express to look in this folder to render our view
app.set('view engine', 'ejs'); // configure template engine
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json()); // parse form data client
app.use(express.static(path.join(__dirname, 'public'))); // configure express to use public folder
app.use(fileUpload()); // configure fileupload

// routes for the app
app.get('/', getHomePage);

// Draft
app.get('/Draft', draftPage);
//app.post('/Draft', draft);

// PlayerStats
app.get('/PlayerStats', playerStatsPage);
//app.post('/PlayerStats', playerStats);

// Trade
app.get('/trade', tradePage);
//app.post('/trade', trade);

// Add Drop
app.get('/add_drop', addDropPage);
//app.post('/add_drop', addDrop);

// Add Drop
app.get('/Team', teamPage);

// set the app to listen on the port
app.listen(port, () => {
    console.log(`Server running on port: ${port}`);
});