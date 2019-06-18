const fs = require('fs');

module.exports = {
	tradePage: (req, res) => {
       // let query = "SELECT * FROM `players`"; // query database to get all the Rooms

        // execute query
       // db.query(query, [1, 2], (err, result) => {
        //    if (err) {
          //      res.redirect('/');
           // }
            res.render('trade.ejs', {
                
            });
        //});
    },
	//playerStats: (req, res) => {
	//	res.render('playerstats.ejs', {
      //          
        //    });
	//}
}