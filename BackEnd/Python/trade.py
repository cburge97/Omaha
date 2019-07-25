import sys 
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
#x represents dataframe of players stats
def set_class(x):
    cl = []
    maximum = x.iloc[:,1].max()
    minimum = x.iloc[:,1].min()
    interval = ((maximum / 6) + 1).round(2)

    bin1 = minimum + interval
    bin2 = bin1 + interval
    bin3 = bin2 + interval
    bin4 = bin3 + interval

    for i in x.iloc[:,1]:
        if( i < bin1):
            cl.append(1)
        elif((i >= bin1) and (i < bin2)):
            cl.append(2)
        elif((i >=bin2) and (i < bin3)):
            cl.append(3)
        elif((i >=bin3) and (i < bin4)):
            cl.append(4)    
        else:
            cl.append(5)
    classes = pd.Series(cl)
    x = x.assign(classes = classes.values)
    return x

#probability of each class. 
#probability of each class. 
def class_probability(x):
    total = len(x)
    c1 = 0.0
    c2 = 0.0
    c3 = 0.0
    c4 = 0.0
    c5 = 0.0
    #get cl
    for i in x.iloc[:,2]:
        if( i == 1):
            c1 = c1 + 1.0
        elif(i == 2):
            c2 = c2 + 1.0
        elif(i == 3):
            c3 = c3 + 1.0
        elif(i == 4):
            c4 = c4 + 1.0    
        else:
            c5 = c5 + 1.0
    pc1 = c1/total
    pc2 = c2/total
    pc3 = c3/total
    pc4 = c4/total
    pc5 = c5/total
    return [c1,c2,c3,c4,c5, pc1, pc2, pc3,pc4,pc5]

#Get the probability's for each class by age
def age_prob(x):
    c1,c2,c3,c4,c5, pc1, pc2, pc3, pc4, pc5  = class_probability(x)
    ages = []
    
    cl1 = x[x['classes'] == 1]
    cl2 = x[x['classes'] == 2]
    cl3 = x[x['classes'] == 3]
    cl4 = x[x['classes'] == 4]
    cl5 = x[x['classes'] == 5]
    
    one = []
    two = []
    three = []
    four = []
    five = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []
    p5 = []
    
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
                
    for j in ages:
        for i in cl4['age']:
            if (j == i):
                four.append(j)
             
    for j in ages:
        for i in cl5['age']:
            if (j == i):
                five.append(j)        
            
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
    for i in ages:
        if c4 == 0:
            p4.append(0)
        else:    
            p4.append(pc4 * (four.count(i) / c4))
    for i in ages:
        if c5 == 0:
            p5.append(0)
        else:    
            p5.append(pc5 * (five.count(i) / c5))        
        
        
        
    l = {'Age': ages, 'Probability of Class 1': p1, 'Probability of Class 2': p2, 'Probability of Class 3': p3, 'Probability of Class 4': p4, 'Probability of Class 5': p5,}
    class_prob = pd.DataFrame(l)    
    
    return class_prob

#match age with winning class
def ageToClass(x):
    probl = []
    age = []
    l = [1,2,3,4,5]
    for i in range(len(x)):
         # age | 1 | 2 | 3 | 4 | 5 
        age.append(x.iloc[i,0])
        greatest = x.iloc[i,1]
        c = l[0]
        for j in range(1,5):
            if(greatest < x.iloc[i,j+ 1]):
                greatest = x.iloc[i,j+ 1]
                c = l[j]     
        probl.append(c)
    
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
    for cl in  range(len(p_INT.iloc[:,1])):
        if p_INT.iloc[cl,1] == 1:
            p_INT.iloc[cl,1] = 5
        elif p_INT.iloc[cl,1] == 2:
            p_INT.iloc[cl,1] = 4
        elif p_INT.iloc[cl,1] == 3:
            p_INT.iloc[cl,1] = 3    
        elif p_INT.iloc[cl,1] == 4:
            p_INT.iloc[cl,1] =2
        else:
            p_INT.iloc[cl,1] = 1
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
        RY = tuple([round((rushingyrds * i),2) for i in statRanges[0]])
        RT = tuple([round((rushingTD * i),2) for i in statRanges[1]])
        row = {"Rushing Yards" : statRanges[0], "Rushing Touchdowns" : statRanges[1], "Fantasy Points": tuple(map(lambda x, y: x + y, RY, RT))}    
        return row
    elif(position == 'WR') | (position == 'TE'):
        CY = tuple([round((recievingyrds * i),2) for i in statRanges[0]])
        CT = tuple([round((recievingTD * i),2) for i in statRanges[1]])
        row = {"Recieving Yards" : statRanges[0], "Recieving Touchdowns" : statRanges[1], "Fantasy Points": tuple(map(lambda x, y: x + y, CY, CT))}    
        return row
    else:
        P = tuple([round((pat * i),2) for i in statRanges[0]])
        F = tuple([round((fg * i),2) for i in statRanges[1]])
        row = {"Point After Touchdown" : statRanges[0], "Field Goals" : statRanges[1], "Fantasy Points": tuple(map(lambda x, y: x + y, P, F))}    
        return row  

def getRange(x, cl):
    maximum = x.max()
    minimum = 0
    interval = ((maximum / 6) + 1).round(2)

    bin1 = minimum + interval
    bin2 = bin1 + interval
    bin3 = bin2 + interval
    bin4 = bin3 + interval
    
    if cl == 1:
        return (minimum,bin1)
    elif cl == 2:
        return (bin1 + 1, bin2)
    elif cl == 3:
        return (bin2 + 1, bin3)
    elif cl == 4:
        return (bin3 + 1, bin4)
    else: 
        return (bin4 + 1, maximum)

def getrating(x):
    if( x < 1):
            return "Bad"
    elif((x >= 1) and (x < 2)):
            return "Below Average"
    elif((x >=2) and (x < 3)):
            return "Average"
    elif((x > 3) and (x < 4)):
            return "Above Average"
    else:
            return "Fantastic"

def getPosStats(p,test18,train):
    split = p.split(" ")
    add_player = test18[(test18["first_name"] == split[1]) & (test18["last_name"] == split[2])]
    position = add_player['position'].iloc[0]
    age = add_player['age'].max()
    l = []
    index1 = 0
    index2 = 0
    index3 = 0
    if position == 'QB':
        QB =getQBStats(train)
        table = QBProbability(QB)
        count = 0
        if age > table.iloc[:,0].max():
            one = table.iloc[:,0].max()
            two = one - 1
            three = two - 1 
            for i in table.iloc[:,0]:
                if one == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)
            ranges = [getRange(pd.to_numeric(QB['passing_interceptions']),l[0]), getRange(pd.to_numeric(QB['passing_yards']),l[1]), getRange(pd.to_numeric(QB['passing_touchdowns']),l[2])]
            answer = fantasyPoints(position,ranges)
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Passing Touchdowns between:  ", answer['Passing Touchdowns'][0], " and ", answer['Passing Touchdowns'][1],'\n',\
#                     "Interceptions between:  ", answer['Interceptions'][0], " and ", answer['Interceptions'][1],'\n',\
#                     "Passing Yards between:  ", answer['Passing Yards'][0], " and ", answer['Passing Yards'][1],'\n'            
            
        elif age < table.iloc[:,0].min():
            one = table.iloc[:,0].min()
            two = one + 1
            three = two + 1 
            for i in table.iloc[:,0]:
                if one == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)
            ranges = [getRange(pd.to_numeric(QB['passing_interceptions']),l[0]), getRange(pd.to_numeric(QB['passing_yards']),l[1]), getRange(pd.to_numeric(QB['passing_touchdowns']),l[2])]
            answer = fantasyPoints(position,ranges)
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Passing Touchdowns between:  ", answer['Passing Touchdowns'][0], " and ", answer['Passing Touchdowns'][1],'\n',\
#                     "Interceptions between:  ", answer['Interceptions'][0], " and ", answer['Interceptions'][1],'\n',\
#                     "Passing Yards between:  ", answer['Passing Yards'][0], " and ", answer['Passing Yards'][1],'\n'            
        else:    
            index = 0
            for i in table.iloc[:,0]:
                if age == i:
                    index = count
                else:    
                    count = count + 1
            if  age == table.iloc[index, 0]:
                l = (table.iloc[index,1:]).tolist()
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(QB['passing_interceptions']),l[0]), getRange(pd.to_numeric(QB['passing_yards']),l[1]), getRange(pd.to_numeric(QB['passing_touchdowns']),l[2])]
                answer = fantasyPoints(position,ranges)
 #             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Passing Touchdowns between:  ", answer['Passing Touchdowns'][0], " and ", answer['Passing Touchdowns'][1],'\n',\
#                     "Interceptions between:  ", answer['Interceptions'][0], " and ", answer['Interceptions'][1],'\n',\
#                     "Passing Yards between:  ", answer['Passing Yards'][0], " and ", answer['Passing Yards'][1],'\n'               
            else:
                one = age
                two = one + 1
                three = one - 1 
                index1 = 0
                index2 = 0
                index3 = 0
                count = 0
                for i in table.iloc[:,0]:
                    if two == i:
                        index2 = count
                        count = count + 1
                    elif three == i:
                        index3 = count
                        count = count + 1
                    else:    
                        count = count + 1
                l2 = (table.iloc[index2,1:]).tolist()
                l3 = (table.iloc[index3,1:]).tolist()
                for i in range(len(l2)):
                    l.append(np.mean([l2[i],l3[i]]).round(0))
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(QB['passing_interceptions']),l[0]), getRange(pd.to_numeric(QB['passing_yards']),l[1]), getRange(pd.to_numeric(QB['passing_touchdowns']),l[2])]
                answer = fantasyPoints(position,ranges)
#                print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Passing Touchdowns between:  ", answer['Passing Touchdowns'][0], " and ", answer['Passing Touchdowns'][1],'\n',\
#                     "Interceptions between:  ", answer['Interceptions'][0], " and ", answer['Interceptions'][1],'\n',\
#                     "Passing Yards between:  ", answer['Passing Yards'][0], " and ", answer['Passing Yards'][1],'\n'
        
    elif position == 'RB':
        RB =getRBStats(test18)
        table = RBProbability(RB)
        count = 0
        if age > table.iloc[:,0].max():
            one = table.iloc[:,0].max()
            two = one - 1
            three = two - 1 
            for i in table.iloc[:,0]:
                if one == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)
            ranges = [getRange(pd.to_numeric(RB['rushing_yards']),l[0]), getRange(pd.to_numeric(RB['rushing_touchdowns']),l[1])]
            answer = fantasyPoints(position,ranges)
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Rushing Yards between:  ", answer['Rushing Yards'][0], " and ", answer['Rushing Yards'][1],'\n',\
#                     "Rushing Touchdowns between:  ", answer['Rushing Touchdowns'][0], " and ", answer['Rushing Touchdowns'][1],'\n'         
        elif age < table.iloc[:,0].min():
            one = table.iloc[:,0].min()
            two = one + 1
            three = two + 1 
            for i in table.iloc[:,0]:
                if one == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)
            ranges = [getRange(pd.to_numeric(RB['rushing_yards']),l[0]), getRange(pd.to_numeric(RB['rushing_touchdowns']),l[1])]
            answer = fantasyPoints(position,ranges)
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Rushing Yards between:  ", answer['Rushing Yards'][0], " and ", answer['Rushing Yards'][1],'\n',\
#                     "Rushing Touchdowns between:  ", answer['Rushing Touchdowns'][0], " and ", answer['Rushing Touchdowns'][1],'\n'
        else:
            index = 0
            for i in table.iloc[:,0]:
                if age == i:
                    index = count
                else:    
                    count = count + 1
            if  age == table.iloc[index, 0]:        
                l = (table.iloc[index,1:]).tolist()
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(RB['rushing_yards']),l[0]), getRange(pd.to_numeric(RB['rushing_touchdowns']),l[1])]
                answer = fantasyPoints(position,ranges)
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Rushing Yards between:  ", answer['Rushing Yards'][0], " and ", answer['Rushing Yards'][1],'\n',\
#                     "Rushing Touchdowns between:  ", answer['Rushing Touchdowns'][0], " and ", answer['Rushing Touchdowns'][1],'\n'
            else:
                one = age
                two = one + 1
                three = one - 1 
                index1 = 0
                index2 = 0
                index3 = 0
                count = 0
                for i in table.iloc[:,0]:
                    if two == i:
                        index2 = count
                        count = count + 1
                    elif three == i:
                        index3 = count
                        count = count + 1
                    else:    
                        count = count + 1
                l2 = (table.iloc[index2,1:]).tolist()
                l3 = (table.iloc[index3,1:]).tolist()
                for i in range(len(l2)):
                    l.append(np.mean([l2[i],l3[i]]).round(0))
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(RB['rushing_yards']),l[0]), getRange(pd.to_numeric(RB['rushing_touchdowns']),l[1])]
                answer = fantasyPoints(position,ranges)
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Rushing Yards between:  ", answer['Rushing Yards'][0], " and ", answer['Rushing Yards'][1],'\n',\
#                     "Rushing Touchdowns between:  ", answer['Rushing Touchdowns'][0], " and ", answer['Rushing Touchdowns'][1],'\n'
    elif position == 'WR':
        WR =getWRStats(test18)
        table = WRProbability(WR)
        count = 0
        if age > table.iloc[:,0].max():
            one = table.iloc[:,0].max()
            two = one - 1
            three = two - 1 
            for i in table.iloc[:,0]:
                if one == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)
            ranges = [getRange(pd.to_numeric(WR['receiving_yards']),l[0]), getRange(pd.to_numeric(WR['receiving_touchdowns']),l[1])]
            answer = fantasyPoints(position,ranges)    
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Recieving Yards between:  ", answer['Recieving Yards'][0], " and ", answer['Recieving Yards'][1],'\n',\
#                     "Recieving Touchdowns between:  ", answer['Recieving Touchdowns'][0], " and ", answer['Recieving Touchdowns'][1],'\n'
        elif age < table.iloc[:,0].min():
            one = table.iloc[:,0].min()
            two = one + 1
            three = two + 1 
            for i in table.iloc[:,0]:
                if one == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)  
            ranges = [getRange(pd.to_numeric(WR['receiving_yards']),l[0]), getRange(pd.to_numeric(WR['receiving_touchdowns']),l[1])]
            answer = fantasyPoints(position,ranges) 
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Recieving Yards between:  ", answer['Recieving Yards'][0], " and ", answer['Recieving Yards'][1],'\n',\
#                     "Recieving Touchdowns between:  ", answer['Recieving Touchdowns'][0], " and ", answer['Recieving Touchdowns'][1],'\n'
        else:
            index = 0
            for i in table.iloc[:,0]:
                if age == i:
                    index = count
                else:    
                    count = count + 1
            if  age == table.iloc[index, 0]:       
                l = (table.iloc[index,1:]).tolist()
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(WR['receiving_yards']),l[0]), getRange(pd.to_numeric(WR['receiving_touchdowns']),l[1])]
                answer = fantasyPoints(position,ranges)     
 #             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Recieving Yards between:  ", answer['Recieving Yards'][0], " and ", answer['Recieving Yards'][1],'\n',\
#                     "Recieving Touchdowns between:  ", answer['Recieving Touchdowns'][0], " and ", answer['Recieving Touchdowns'][1],'\n'
            else:
                one = age
                two = one + 1
                three = one - 1 
                index1 = 0
                index2 = 0
                index3 = 0
                count = 0
                for i in table.iloc[:,0]:
                    if two == i:
                        index2 = count
                        count = count + 1
                    elif three == i:
                        index3 = count
                        count = count + 1
                    else:    
                        count = count + 1
                l2 = (table.iloc[index2,1:]).tolist()
                l3 = (table.iloc[index3,1:]).tolist()
                for i in range(len(l2)):
                    l.append(np.mean([l2[i],l3[i]]).round(0))
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(WR['receiving_yards']),l[0]), getRange(pd.to_numeric(WR['receiving_touchdowns']),l[1])]
                answer = fantasyPoints(position,ranges)       
 #             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Recieving Yards between:  ", answer['Recieving Yards'][0], " and ", answer['Recieving Yards'][1],'\n',\
#                     "Recieving Touchdowns between:  ", answer['Recieving Touchdowns'][0], " and ", answer['Recieving Touchdowns'][1],'\n'                            
    elif position == 'TE':
        TE =getTEStats(test18)
        table = TEProbability(TE)
        count = 0
        if age > table.iloc[:,0].max():
            one = table.iloc[:,0].max()
            two = one - 1
            three = two - 1 
            for i in table.iloc[:,0]:
                if one == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)
            ranges = [getRange(pd.to_numeric(TE['receiving_yards']),l[0]), getRange(pd.to_numeric(TE['receiving_touchdowns']),l[1])]
            answer = fantasyPoints(position,ranges)    
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Recieving Yards between:  ", answer['Recieving Yards'][0], " and ", answer['Recieving Yards'][1],'\n',\
#                     "Recieving Touchdowns between:  ", answer['Recieving Touchdowns'][0], " and ", answer['Recieving Touchdowns'][1],'\n'
        elif age < table.iloc[:,0].min():
            one = table.iloc[:,0].min()
            two = one + 1
            three = two + 1 
            for i in table.iloc[:,0]:
                if one == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)
            ranges = [getRange(pd.to_numeric(TE['receiving_yards']),l[0]), getRange(pd.to_numeric(TE['receiving_touchdowns']),l[1])]
            answer = fantasyPoints(position,ranges)
 #             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Recieving Yards between:  ", answer['Recieving Yards'][0], " and ", answer['Recieving Yards'][1],'\n',\
#                     "Recieving Touchdowns between:  ", answer['Recieving Touchdowns'][0], " and ", answer['Recieving Touchdowns'][1],'\n'
        else:
            index = 0
            for i in table.iloc[:,0]:
                if age == i:
                    index = count
                else:    
                    count = count + 1
            if  age == table.iloc[index, 0]:
                l = (table.iloc[index,1:]).tolist()
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(TE['receiving_yards']),l[0]), getRange(pd.to_numeric(TE['receiving_touchdowns']),l[1])]
                answer = fantasyPoints(position,ranges) 
 #             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Recieving Yards between:  ", answer['Recieving Yards'][0], " and ", answer['Recieving Yards'][1],'\n',\
#                     "Recieving Touchdowns between:  ", answer['Recieving Touchdowns'][0], " and ", answer['Recieving Touchdowns'][1],'\n'
            else:
                one = age
                two = one + 1
                three = one - 1 
                index1 = 0
                index2 = 0
                index3 = 0
                count = 0
                for i in table.iloc[:,0]:
                    if two == i:
                        index2 = count
                        count = count + 1
                    elif three == i:
                        index3 = count
                        count = count + 1
                    else:    
                        count = count + 1
                l2 = (table.iloc[index2,1:]).tolist()
                l3 = (table.iloc[index3,1:]).tolist()
                for i in range(len(l2)):
                    l.append(np.mean([l2[i],l3[i]]).round(0))
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(TE['receiving_yards']),l[0]), getRange(pd.to_numeric(TE['receiving_touchdowns']),l[1])]
                answer = fantasyPoints(position,ranges) 
 #             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Recieving Yards between:  ", answer['Recieving Yards'][0], " and ", answer['Recieving Yards'][1],'\n',\
#                     "Recieving Touchdowns between:  ", answer['Recieving Touchdowns'][0], " and ", answer['Recieving Touchdowns'][1],'\n'      
    else:
        K =getKStats(test18)
        table = KProbability(K)
        count = 0
        if age > table.iloc[:,0].max():
            one = table.iloc[:,0].max()
            two = one - 1
            three = two - 1 
            for i in table.iloc[:,0]:
                if one == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)
            ranges = [getRange(pd.to_numeric(K['point_after_makes']),l[0]), getRange(pd.to_numeric(K['field_goal_makes']),l[1])]
            answer = fantasyPoints(position,ranges)    
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Points After Touchdown between:  ", answer['Point After Touchdown'][0], " and ", answer['Point After Touchdown'][1],'\n',\
#                     "Field Goals between:  ", answer['Field Goals'][0], " and ", answer['Field Goals'][1],'\n'
        elif age < table.iloc[:,0].min():
            one = table.iloc[:,0].min()
            two = one + 1
            three = two + 1 
            for i in table.iloc[:,0]:
                if two == i:
                    index1 = count
                    count = count + 1
                elif two == i:
                    index2 = count
                    count = count + 1
                elif three == i:
                    index3 = count
                    count = count + 1
                else:    
                    count = count + 1
            l1 = (table.iloc[index1,1:]).tolist()
            l2 = (table.iloc[index2,1:]).tolist()
            l3 = (table.iloc[index3,1:]).tolist()
            for i in range(len(l1)):
                l.append(np.mean([l1[i],l2[i],l3[i]]).round(0))
            score = np.mean(l).round(2)
            rating = getrating(score)
            ranges = [getRange(pd.to_numeric(K['point_after_makes']),l[0]), getRange(pd.to_numeric(K['field_goal_makes']),l[1])]
            answer = fantasyPoints(position,ranges)
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Points After Touchdown between:  ", answer['Point After Touchdown'][0], " and ", answer['Point After Touchdown'][1],'\n',\
#                     "Field Goals between:  ", answer['Field Goals'][0], " and ", answer['Field Goals'][1],'\n'
        else:
            index = 0
            for i in table.iloc[:,0]:
                if age == i:
                    index = count
                else:    
                    count = count + 1
            if  age == table.iloc[index, 0]:   
                l = (table.iloc[index,1:]).tolist()
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(K['point_after_makes']),l[0]), getRange(pd.to_numeric(K['field_goal_makes']),l[1])]
                answer = fantasyPoints(position,ranges)
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Points After Touchdown between:  ", answer['Point After Touchdown'][0], " and ", answer['Point After Touchdown'][1],'\n',\
#                     "Field Goals between:  ", answer['Field Goals'][0], " and ", answer['Field Goals'][1],'\n'
            else:
                one = age
                two = one + 1
                three = one - 1 
                index1 = 0
                index2 = 0
                index3 = 0
                count = 0
                for i in table.iloc[:,0]:
                    if two == i:
                        index2 = count
                        count = count + 1
                    elif three == i:
                        index3 = count
                        count = count + 1
                    else:    
                        count = count + 1
                l2 = (table.iloc[index2,1:]).tolist()
                l3 = (table.iloc[index3,1:]).tolist()
                for i in range(len(l2)):
                    l.append(np.mean([l2[i],l3[i]]).round(0))
                score = np.mean(l).round(2)
                rating = getrating(score)
                ranges = [getRange(pd.to_numeric(K['point_after_makes']),l[0]), getRange(pd.to_numeric(K['field_goal_makes']),l[1])]
                answer = fantasyPoints(position,ranges) 
#             print p, "will do ", rating, " this season! \n",\
#                     "Folowing stats: \n",\
#                     "Fantasy Points", answer['Fantasy Points'][0], " and ", answer['Fantasy Points'][1], "points \n",\
#                     "Points After Touchdown between:  ", answer['Point After Touchdown'][0], " and ", answer['Point After Touchdown'][1],'\n',\
#                     "Field Goals between:  ", answer['Field Goals'][0], " and ", answer['Field Goals'][1],'\n'
    return score

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
    test17 = train[train['Year'] == '2017']
    age2018 = test17['age'] + 1
    test18 = test17
    # print test18
    test18.iloc[:,-1] = age2018

    #Add
    players = []
    amount = len(sys.argv)
    for i in range(1,amount):
        players.append(sys.argv[i])
    drop = players[0:6]
    add = players[6:]
    add_overall_score = []
    drop_overall_score = []
    a = []
    d = []
    for p in add:
        if p !="":
            a.append(p)
            score = getPosStats(p,test18,train)
            add_overall_score.append(score)
    if add == []:
        add_score = 0
    else:
        add_score = np.mean(add_overall_score).round(2)
    print "The players", str(a),  "you want to receive from the other team has an average overall score of ", add_score, "out of 5 stars! \n"

    for p in drop:
        if p != "":
            d.append(p)
            score = getPosStats(p,test18,train)
            drop_overall_score.append(score)
    if drop == []:
        drop_score = 0
    else:
        drop_score = np.mean(drop_overall_score).round(2)
    print "The players", str(d) , "you want to trade away from your team has an average overall score of ", drop_score, "out of 5 stars! \n"


    if add_score > drop_score:
        print "Your Trade is worth it!"
    elif add_score < drop_score:
        print "Your Trade is not worth it!"
    else:
        print "Your Trade does not make a difference!"

    sys.stdout.flush()
if __name__ == "__main__":
    main()