const fs = require('fs');

module.exports = {
	playerStatsPage: (req, res) => {
      // let query = "SELECT * FROM `players`"; // query database to get all the Rooms
       db.query("SELECT * FROM `players`", [1,2], (err, result) => {

      if (err) {
        res.redirect('/');
      }
      else{
        //console.log(result); // [{1: 1}]
        }
        res.render('playerstats.ejs', {
           player: result       
        });
      });
      },
	//playerStats: (req, res) => {
	//	res.render('playerstats.ejs', {
      //          
        //    });
	//}
}