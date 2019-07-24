const fs = require('fs');
module.exports = {

  addDropPage: (req, res) => {

    db.query("SELECT p.first_name, p.last_name, p.Player_ID, p.position, o.Team FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id", [1,2], (err, result) => {

      if (err) {
        res.redirect('/');
      }
      else{
        //console.log(result); // [{1: 1}]
        }
        res.render('add_drop.ejs', {
           players: result,
           message: ''      
        });
      });
      },

      addDrop: (req,res) => {
        let userPlayer1 = req.body.user1;
        let userPlayer2 = req.body.user2;
        let userPlayer3 = req.body.user3;
        let userPlayer4 = req.body.user4;
        let userPlayer5 = req.body.user5;
        let userPlayer6 = req.body.user6;
        let otherPlayer1 = req.body.FA1;
        let otherPlayer2 = req.body.FA2;
        let otherPlayer3 = req.body.FA3;
        let otherPlayer4 = req.body.FA4;
        let otherPlayer5 = req.body.FA5;
        let otherPlayer6 = req.body.FA6;
        // Use child_process.spawn method from  
        // child_process module and assign it 
        // to variable spawn 
        var spawn = require("child_process").spawn; 
          
        // Parameters passed in spawn - 
        // 1. type_of_script 
        // 2. list containing Path of the script 
        //    and arguments for the script  
          
        var process = spawn('python',["./BackEnd/Python/add_drop.py", 
                                userPlayer1,userPlayer2,userPlayer3,userPlayer4,userPlayer5,userPlayer6,
                                otherPlayer1, otherPlayer2,otherPlayer3,otherPlayer4,otherPlayer5,otherPlayer6 
                                ] ); 
        // Takes stdout data from script which executed 
        // with arguments and send this data to res object 
        //process.stdout.on('data', function(data) { res.send(data.toString()); } )
  
        db.query("SELECT p.first_name, p.last_name, p.Player_ID, p.position, o.Team FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id", [1,2], (err, result) => {

          if (err) {
            res.redirect('/');
          }
          else{
            // console.log(result); // [{1: 1}]
            }

            process.stdout.on('data', (data) => {

            if(userPlayer1 != ''){  
              res.render('add_drop.ejs', {
                players: result,
                message: data     
             });
            }
            else{
              res.render('add_drop.ejs', {
                players: result,
                message: 'No players selected'     
             });
            }
              // Do something with the data returned from python script
          });
            
          });
      },
}