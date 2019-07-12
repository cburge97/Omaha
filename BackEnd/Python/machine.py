
import sys 
sys.path.append("NumPy_path")
sys.path.append("Pandas_path")
sys.path.append("mysql.connector_path")
import mysql.connector as sql
import pandas as pd
import numpy as np

#merge tables to one table
def createTable(players,stats):
    players['Player_ID'] = players['Player_ID'].astype(int)
    stats['Player_ID'] = stats['Player_ID'].astype(int)
    player_stats = pd.merge(players, stats.drop_duplicates(), on=['Player_ID'])
    player_stats.reset_index(drop=True)

    #create age column
    player_stats['age'] = (player_stats['Year']).astype('int64') - player_stats['birth_year']

    #drop unesessary columns
    stats = player_stats.drop([u'height', u'weight', u'college', u'round_drafted',u'draft_pick',u'draft_year', u'current_salary'], axis=1)
    return stats

# # def getStatsByPosition(x):
def getQBStats(stats):
    QB = pd.DataFrame(stats[stats['position'] == "QB"])
    QB = QB.drop([u'Team',                 u'game_won',
              u'player_team_score',           u'opponent_score',
                       u'passing_rating',
                  u'passing_sacks', u'passing_sacks_yards_lost',
               u'receiving_targets',
           u'receiving_receptions',          u'receiving_yards',
           u'receiving_touchdowns',     u'kick_return_attempts',
              u'kick_return_yards',   u'kick_return_touchdowns',
           u'point_after_attempts',        u'point_after_makes',
            u'field_goal_attempts',         u'field_goal_makes'], axis =1)
    return QB

def getRBStats(stats):
    RB = pd.DataFrame(stats[stats['position'] == "RB"])
    RB = RB.drop([u'Team',                 u'game_won',
              u'player_team_score',           u'opponent_score',
               u'passing_attempts',      u'passing_completions',
                  u'passing_yards',           u'passing_rating',
             u'passing_touchdowns',    u'passing_interceptions',
                  u'passing_sacks', u'passing_sacks_yards_lost',
                u'kick_return_attempts',
              u'kick_return_yards',   u'kick_return_touchdowns',
           u'point_after_attempts',        u'point_after_makes',
            u'field_goal_attempts',         u'field_goal_makes'], axis = 1)
    return RB

def getWRStats(stats):
    WR = pd.DataFrame(stats[stats['position'] == "WR"])
    WR = WR.drop([u'Team',                 u'game_won',
              u'player_team_score',           u'opponent_score',
               u'passing_attempts',      u'passing_completions',
                  u'passing_yards',           u'passing_rating',
             u'passing_touchdowns',    u'passing_interceptions',
                  u'passing_sacks', u'passing_sacks_yards_lost',
         u'kick_return_attempts',
              u'kick_return_yards',   u'kick_return_touchdowns',
           u'point_after_attempts',        u'point_after_makes',
            u'field_goal_attempts',         u'field_goal_makes'], axis = 1)
    return WR

def getTEStats(stats):
    TE = pd.DataFrame(stats[stats['position'] == "TE"])
    TE = TE.drop([u'Team',                 u'game_won',
              u'player_team_score',           u'opponent_score',
               u'passing_attempts',      u'passing_completions',
                  u'passing_yards',           u'passing_rating',
             u'passing_touchdowns',    u'passing_interceptions',
                  u'passing_sacks', u'passing_sacks_yards_lost',
               u'rushing_attempts',            u'rushing_yards',
             u'rushing_touchdowns',      u'kick_return_attempts',
              u'kick_return_yards',   u'kick_return_touchdowns',
           u'point_after_attempts',        u'point_after_makes',
            u'field_goal_attempts',         u'field_goal_makes'], axis = 1)
    return TE

def getKStats(stats):
    K = pd.DataFrame(stats[stats['position'] == "K"])
    K = K.drop([u'Team',                 u'game_won',
              u'player_team_score',           u'opponent_score',
               u'passing_attempts',      u'passing_completions',
                  u'passing_yards',           u'passing_rating',
             u'passing_touchdowns',    u'passing_interceptions',
                  u'passing_sacks', u'passing_sacks_yards_lost',
               u'rushing_attempts',            u'rushing_yards',
             u'rushing_touchdowns',        u'receiving_targets',
           u'receiving_receptions',          u'receiving_yards',
           u'receiving_touchdowns',     u'kick_return_attempts',
              u'kick_return_yards',   u'kick_return_touchdowns'], axis = 1)
    return K    

#gives player value a class value
def set_class(x):
    cl = []
    
    class1 = x.iloc[:,1].mean() / 2
    class3 = x.iloc[:,1].mean() + class1

    for i in x.iloc[:,1]:
        if( i < class1):
            cl.append(1)
        elif((i >= class1) and (i < class3)):
            cl.append(2)
        else:
            cl.append(3)
    classes = pd.Series(cl)
    x = x.assign(classes = classes.values)
    return x

#probability of each class. 
def class_probability(x):
    total = len(x)
    c1 = 0.0
    c2 = 0.0
    c3 = 0.0
    #get cl
    for i in x.iloc[:,2]:
        if( i == 1):
            c1 = c1 + 1.0
        elif(i == 2):
            c2 = c2 + 1.0
        else:
            c3 = c3 + 1.0
    pc1 = c1/total
    pc2 = c2/total
    pc3 = c3/total
    
    return [c1,c2,c3, pc1, pc2, pc3]

#Get the probability's for each class by age
def age_prob(x):
    c1,c2,c3, pc1, pc2, pc3  = class_probability(x)
    ages = []
    
    cl1 = x[x['classes'] == 1]
    cl2 = x[x['classes'] == 2]
    cl3 = x[x['classes'] == 3]
    
    one = []
    two = []
    three = []
    p1 = []
    p2 = []
    p3 = []
    
    for i in x.iloc[:,0]:
        ages.append(i)
    ages = np.unique(ages)
    
    for j in ages:
        for i in cl1['age']:
            if (j == i):
                one.append(j)  
                
    for j in ages:
        for i in cl2['age']:
            if (j == i):
                two.append(j) 
                
    for j in ages:
        for i in cl3['age']:
            if (j == i):
                three.append(j)
                
    for i in ages:
        if c1 == 0:
            p1.append(0)
        else:
            p1.append((pc1 * (one.count(i) / c1)))
    for i in ages:
        if c2 == 0:
            p2.append(0)
        else:    
            p2.append(pc2 * (two.count(i) / c2))
    for i in ages:
        if c3 == 0:
            p3.append(0)
        else:    
            p3.append(pc3 * (three.count(i) / c3))
        
        
        
    l = {'Age': ages, 'Probability of Class 1': p1, 'Probability of Class 2': p2, 'Probability of Class 3': p3}
    class_prob = pd.DataFrame(l)    
    
    return class_prob

#match age with winning class
def ageToClass(x):
    probl = []
    age = []
    c1 = 1
    c2 = 2
    c3 = 3
    
    for i in range(len(x)):
        age.append(x.iloc[i,0])
        if(x.iloc[i,1] > x.iloc[i,2]):
            if(x.iloc[i,1] > x.iloc[i,3]):
                probl.append(c1)
            else:
                 probl.append(c3)
        elif(x.iloc[i,2] > x.iloc[i,1]):
            if(x.iloc[i,2] > x.iloc[i,3]):
                probl.append(c2)
            else:
                 probl.append(c3)
        else:
            probl.append(c2)
    
    l = { 'Age': age, 'Class' : probl}
    
    return pd.DataFrame(l)

#Classifying each age by what class they are

def QBProbability(QB):
    QBpassing = pd.DataFrame(QB.filter(['age','passing_yards'],axis=1))
    QBpassing['passing_yards'] = QBpassing['passing_yards'].astype(float)
    QBpassing = QBpassing[QBpassing['passing_yards'] > 1000]
    QBpassing = set_class(QBpassing)
    pPassing = age_prob(QBpassing)
    p_py = ageToClass(pPassing)


    QBTD = pd.DataFrame(QB.filter(['age','passing_touchdowns']))
    QBTD['passing_touchdowns'] = QBTD['passing_touchdowns'].astype(float)
    QBTD = QBTD[QBTD['passing_touchdowns'] > 10]
    QBTD = set_class(QBTD) 
    pTD = age_prob(QBTD)
    p_TD = ageToClass(pTD)


    QBInt = pd.DataFrame(QB.filter(['age', 'passing_interceptions']))
    QBInt['passing_interceptions'] = QBInt['passing_interceptions'].astype(float)
    QBTD = QBInt[QBInt['passing_interceptions'] > 0]
    QBInt = set_class(QBInt)
    pINT = age_prob(QBInt)
    p_INT = ageToClass(pINT)

    l = {"Age" : p_py.iloc[:,0], "QB Passing" : p_py.iloc[:,1], "QB Touchdowns" : p_TD.iloc[:,1], "QB Interceptions" : p_INT.iloc[:,1]}
    QB_Probability = pd.DataFrame(l)
    return QB_Probability

def RBProbability(RB):
    RByards = pd.DataFrame(RB.filter(['age','rushing_yards'],axis=1))
    RByards['rushing_yards'] = RByards['rushing_yards'].astype(float)
    RByards = RByards[RByards['rushing_yards'] > 150]
    RByards = set_class(RByards)
    pyards = age_prob(RByards)
    p_yards = ageToClass(pyards)

    RBTD = pd.DataFrame(RB.filter(['age','rushing_touchdowns']))
    RBTD['rushing_touchdowns'] = RBTD['rushing_touchdowns'].astype(float)
    RBTD = RBTD[RBTD['rushing_touchdowns'] > 1]
    RBTD = set_class(RBTD)
    pTD = age_prob(RBTD)
    p_TD = ageToClass(pTD)

    l = {"Age" : p_TD.iloc[:,0], "RB Rushing Yards" : p_yards.iloc[:,1], "RB Touchdowns" : p_TD.iloc[:,1]}
    RB_Probability = pd.DataFrame(l)
    return RB_Probability

def WRProbability(WR):
    WRyards = pd.DataFrame(WR.filter(['age','receiving_yards'],axis=1))
    WRyards['receiving_yards'] = WRyards['receiving_yards'].astype(float)
    WRyards = WRyards[WRyards['receiving_yards'] > 150]
    WRyards = set_class(WRyards)
    pyards = age_prob(WRyards)
    p_yards = ageToClass(pyards)

    WRTD = pd.DataFrame(WR.filter(['age','receiving_touchdowns'],axis=1))
    WRTD['receiving_touchdowns'] = WRTD['receiving_touchdowns'].astype(float)
    WRTD = WRTD[WRTD['receiving_touchdowns'] > 1]
    WRTD = set_class(WRTD)
    pTD = age_prob(WRTD)
    p_TD = ageToClass(pTD)

    l = {"Age" : p_TD.iloc[:,0], "WR Receiving Yards" : p_yards.iloc[:,1], "WR Touchdowns" : p_TD.iloc[:,1]}
    WR_Probability = pd.DataFrame(l)
    return WR_Probability

def TEProbability(TE):
    TEyards = pd.DataFrame(TE.filter(['age','receiving_yards'],axis=1))
    TEyards['receiving_yards'] = TEyards['receiving_yards'].astype(float)
    TEyards = TEyards[TEyards['receiving_yards'] > 150]
    TEyards = set_class(TEyards)
    pYards = age_prob(TEyards)
    p_yards = ageToClass(pYards)

    TETD = pd.DataFrame(TE.filter(['age','receiving_touchdowns'],axis=1))
    TETD['receiving_touchdowns'] =TETD['receiving_touchdowns'].astype(float)
    TETD = TETD[TETD['receiving_touchdowns'] > 1]
    TETD = set_class(TETD)
    pTD = age_prob(TETD)
    p_TD = ageToClass(pTD)

    l = {"Age" : p_TD.iloc[:,0], "TE Receiving Yards" : p_yards.iloc[:,1], "TE Touchdowns" : p_TD.iloc[:,1]}
    TE_Probability = pd.DataFrame(l)
    return TE_Probability

def KProbability(K):
    KPAT= pd.DataFrame(K.filter(['age','point_after_makes'],axis=1))
    KPAT['point_after_makes'] = KPAT['point_after_makes'].astype(float)
    KPAT = KPAT[KPAT['point_after_makes'] > 1]
    KPAT = set_class(KPAT)
    pPAT = age_prob(KPAT)
    p_PAT = ageToClass(pPAT)

    KFG = pd.DataFrame(K.filter(['age','field_goal_makes'],axis=1))
    KFG['field_goal_makes'] = KFG['field_goal_makes'].astype(float)
    KFG = KFG[KFG['field_goal_makes'] > 1]
    KFG = set_class(KFG)
    pKG = age_prob(KFG)
    p_KG = ageToClass(pKG)

    l = {"Age" : p_PAT.iloc[:,0], "K PAT" : p_PAT.iloc[:,1], "K Field Goals" : p_KG.iloc[:,1]}
    K_Probability = pd.DataFrame(l)
    return K_Probability

def fantasyPoints(position, statRanges):
    passingyrds = 1.0/25.0
    passsingTD = 4.0
    interception = -2
    rushingyrds = 1.0/10
    rushingTD = 6
    recievingyrds = 1.0/10
    recievingTD = 6
    pat = 1
    fg = 3       
    
    if position == 'QB':
        INT = tuple([round((interception * i),2) for i in statRanges[0]])
        PS = tuple([round((passingyrds * i),2) for i in statRanges[1]])
        TD = tuple([round((passsingTD * i),2) for i in  statRanges[2]])
        
        row = {"Interceptions" : statRanges[0], "Passing Yards" : statRanges[1], "Passing Touchdowns" : statRanges[2], "Fantasy Points": tuple(map(lambda x, y,z: x + y + z, INT, PS, TD))}
        return row
    elif position == 'RB':
        return
    elif (position == 'WR') | (position == 'TE'):
        return 
    else:
        return 

def getRange(x, cl):
    x= x[x > 0]
    a = float(x.min())         
    b = float((x.mean()  / 2))   
    c = float(x.mean() + b)
    d = float(x.max() )
    
    if cl == 1:
        return (a,b)
    elif cl == 2:
        return (b,c)
    else: 
        return (c,d)

def main():

    cnx = sql.connect(user='root', password='', host='127.0.0.1', database='nfl player stats')

    cursor = cnx.cursor()

    player = ("SELECT * FROM players")
    past = ("SELECT * FROM offense_stats")
    # current = ("SELECT * FROM current_stats")

    players_df = pd.read_sql(player, cnx)
    past_df = pd.read_sql(past, cnx)
    # current_df = pd.read_sql(current, cnx)

    players_df = pd.DataFrame(players_df)
    train_df = pd.DataFrame(past_df)
    # test_df = pd.DataFrame(current_df)

    cnx.close()

    train = createTable(players_df,train_df)
    train17 = train[train['Year'] != '2017']
    train16 = train[train['Year'] != '2016']
    train15 = train[train['Year'] != '2015']
    test17 = train[train['Year'] == '2017']
    test16 = train[train['Year'] == '2016']
    test15 = train[train['Year'] == '2015']

    #Main
    #Add
    add = sys.argv[1]
    #Drop
    drop = "Drew Brees"

    split = add.split(" ")
    add_player = train[(train["first_name"] == split[0]) & (train["last_name"] == split[1])]
    position = add_player['position'].iloc[0]
    age = add_player['age'].max()

    l = []
    
    if position == 'QB':
        QB =getQBStats(train17)
        table = QBProbability(QB)
        count = 0
        for i in table.iloc[:,0]:
            if age == i:
                index = count
            else:    
                count = count + 1
        if  age == table.iloc[index, 0]:
            l = (table.iloc[index,1:]).tolist()
            ranges = [getRange(pd.to_numeric(QB['passing_interceptions']),l[0]), getRange(pd.to_numeric(QB['passing_yards']),l[1]), getRange(pd.to_numeric(QB['passing_touchdowns']),l[2])]
            answer = fantasyPoints(position,ranges)    
            print(answer)
            sys.stdout.flush()
        else:
            print("The age does not match an age in probability table")
            sys.stdout.flush()
  

if __name__ == "__main__":
    main()

# Takes first name and last name via command  
# line arguments and then display them 
#print("Output from Python") 
#print("First name: " + sys.argv[1]) 
#print("Last name: " + sys.argv[2]) 
#sys.argv[1]
#outP = sys.argv[1] 


#print is the return 
#print(outP + " stuff")
#sys.stdout.flush()
  
# save the script as hello.py 