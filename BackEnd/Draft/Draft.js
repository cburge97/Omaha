const fs = require('fs');

module.exports = {
	draftPage: (req, res) => {
    db.query("SELECT * FROM `players`", [1,2], (err, result) => {

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