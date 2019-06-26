const fs = require('fs');

module.exports = {
	draftPage: (req, res) => {
    db.query("SELECT b.Player_ID, b.first_name, b.last_name, b.position, b.college, a.Team, SUM(a.rushing_yards) FROM `offense_stats` a, `players` b WHERE a.Year = 2017 AND b.Player_ID = a.Player_ID GROUP BY b.Player_ID", [1,2], (err, result) => {

      if (err) {
        res.redirect('/');
      }
      else{
        //console.log(result); // [{1: 1}]
        }
        res.render('Draft.ejs', {
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