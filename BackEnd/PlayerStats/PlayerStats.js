const fs = require('fs');

module.exports = {
	playerStatsPage: (req, res) => {
      // let query = "SELECT * FROM `players`"; // query database to get all the Rooms
       db.query("SELECT p.first_name, p.last_name, p.Player_ID, p.position, p.college, o.Team FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id;SELECT a.first_name, a.last_name, SUM(b.passing_yards) AS 'PassingYds', SUM(b.passing_touchdowns) AS 'PassingTD', SUM(b.rushing_yards) AS 'RushingYds', SUM(b.rushing_touchdowns) AS 'RushingTD', SUM(b.receiving_yards) AS 'ReceivingYDS',SUM(b.receiving_touchdowns) AS 'ReceivingTD', SUM(b.point_after_makes) AS 'PAT', SUM(b.field_goal_makes) AS 'FG' FROM (SELECT p.first_name, p.last_name, p.Player_ID FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id) a LEFT JOIN (SELECT * FROM offense_stats WHERE Year = 2016 GROUP By Player_ID) b ON (a.Player_ID = b.Player_ID) GROUP BY a.Player_ID;SELECT a.first_name, a.last_name, SUM(b.passing_yards) AS 'PassingYds', SUM(b.passing_touchdowns) AS 'PassingTD', SUM(b.rushing_yards) AS 'RushingYds', SUM(b.rushing_touchdowns) AS 'RushingTD', SUM(b.receiving_yards) AS 'ReceivingYDS',SUM(b.receiving_touchdowns) AS 'ReceivingTD', SUM(b.point_after_makes) AS 'PAT', SUM(b.field_goal_makes) AS 'FG' FROM (SELECT p.first_name, p.last_name, p.Player_ID FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id) a LEFT JOIN (SELECT * FROM offense_stats WHERE Year = 2017 GROUP By Player_ID) b ON (a.Player_ID = b.Player_ID) GROUP BY a.Player_ID;SELECT a.first_name, a.last_name, SUM(b.pass_yds) AS 'PassingYds', SUM(b.pass_td) AS 'PassingTD', SUM(b.rush_yds) AS 'RushingYds', SUM(b.rush_td) AS 'RushingTD', SUM(b.receive_yds) AS 'ReceivingYDS',SUM(b.receive_td) AS 'ReceivingTD', SUM(b.pat) AS 'PAT', SUM(b.fieldgoal) AS 'FG' FROM (SELECT p.first_name, p.last_name, p.Player_ID FROM offense_stats o, players p WHERE o.Player_ID = p.player_id and o.Year = 2017 GROUP BY p.player_id) a LEFT JOIN (SELECT * FROM career_total GROUP By Player_ID) b ON (a.Player_ID = b.Player_ID) GROUP BY a.Player_ID", [1,2], (err, result) => {

      if (err) {
        res.redirect('/');
      }
      else{
        //console.log(result); // [{1: 1}]
        }
        res.render('playerstats.ejs', {
           player: result[0],
           stats: result[1],
           stats17: result[2],
           statsCareer: result[3]       
        });
      });
      },
}