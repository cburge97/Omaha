const fs = require('fs');
module.exports = {

  addDropPage: (req, res) => {

    db.query("SELECT p.first_name, p.last_name, p.Player_ID FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id", [1,2], (err, result) => {

 

      if (err) {

        res.redirect('/');

      }

      else{

        //console.log(result); // [{1: 1}]

        }

        res.render('add_drop.ejs', {

           players: result      

        });

      });

      },

}