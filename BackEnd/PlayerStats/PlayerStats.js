const fs = require('fs');

module.exports = {
	playerStatsPage: (req, res) => {
       // let query = "SELECT * FROM `players`"; // query database to get all the Rooms

        // execute query
       // db.query(query, [1, 2], (err, result) => {
        //    if (err) {
          //      res.redirect('/');
           // }
            res.render('playerstats.ejs', {
                
            });
        //});
    },
	//playerStats: (req, res) => {
	//	res.render('playerstats.ejs', {
      //          
        //    });
	//}
}