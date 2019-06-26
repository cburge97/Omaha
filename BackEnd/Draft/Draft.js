const fs = require('fs');

module.exports = {
	draftPage: (req, res) => {
     // let query = "SELECT * FROM `players`"; // query database to get all the Rooms
     db.query("SELECT p.first_name, p.last_name, p.Player_ID, p.position, p.college, o.Team FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id;SELECT a.first_name, a.last_name, SUM(b.passing_yards)*2 AS 'PassingYds', SUM(b.passing_touchdowns)*2 AS 'PassingTD', SUM(b.rushing_yards)*2 AS 'RushingYds', SUM(b.rushing_touchdowns)*2 AS 'RushingTD', SUM(b.receiving_yards)*2 AS 'ReceivingYDS',SUM(b.receiving_touchdowns)*2 AS 'ReceivingTD', SUM(b.point_after_makes)*2 AS 'PAT', SUM(b.field_goal_makes)*2 AS 'FG' FROM (SELECT p.first_name, p.last_name, p.Player_ID FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id) a LEFT JOIN (SELECT * FROM offense_stats WHERE Year = 2016 GROUP By Player_ID) b ON (a.Player_ID = b.Player_ID) GROUP BY a.Player_ID;SELECT a.first_name, a.last_name, SUM(b.passing_yards)*2 AS 'PassingYds', SUM(b.passing_touchdowns)*2 AS 'PassingTD', SUM(b.rushing_yards)*2 AS 'RushingYds', SUM(b.rushing_touchdowns)*2 AS 'RushingTD', SUM(b.receiving_yards)*2 AS 'ReceivingYDS',SUM(b.receiving_touchdowns)*2 AS 'ReceivingTD', SUM(b.point_after_makes)*2 AS 'PAT', SUM(b.field_goal_makes)*2 AS 'FG' FROM (SELECT p.first_name, p.last_name, p.Player_ID FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id) a LEFT JOIN (SELECT * FROM offense_stats WHERE Year = 2017 GROUP By Player_ID) b ON (a.Player_ID = b.Player_ID) GROUP BY a.Player_ID;SELECT a.first_name, a.last_name, SUM(b.pass_yds)*2 AS 'PassingYds', SUM(b.pass_td)*2 AS 'PassingTD', SUM(b.rush_yds)*2 AS 'RushingYds', SUM(b.rush_td)*2 AS 'RushingTD', SUM(b.receive_yds)*2 AS 'ReceivingYDS',SUM(b.receive_td)*2 AS 'ReceivingTD', SUM(b.pat)*2 AS 'PAT', SUM(b.fieldgoal)*2 AS 'FG' FROM (SELECT p.first_name, p.last_name, p.Player_ID FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id) a LEFT JOIN (SELECT * FROM career_total GROUP By Player_ID) b ON (a.Player_ID = b.Player_ID) GROUP BY a.Player_ID", [1,2], (err, result) => {

      if (err) {
        res.redirect('/');
      }
      else{
        //console.log(result); // [{1: 1}]
        }
        res.render('Draft.ejs', {
           player: result[0],
           stats: result[1],
           stats17: result[2],
           statsCareer: result[3]       
        });
      });
      },
}