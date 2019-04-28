import numpy as np
import skfuzzy as fuzz
import math

def crisp(m,M,fy,n ):
    dist=(M-m)/(2*math.floor(n/2))
    center=m+(fy-1)*dist
    return center

def mship(m,n,numb,x):
    center = []
    memb = []
    dist = abs((n-m)/(numb-1))
    fiering = np.array([[0,0],[0,0]])

    for i in range(5):
        center.append(m+(i + 1)*dist)
    memb.append(m)
    for items in center:
        memb.append(items)
    memb.append(n)
    if x < memb[0] or x > len(memb):
        fiering = np.array([[0,0],[0,0]])
    elif x == memb[0]:
        fiering = np.array([[1,1],[0,0]])
    elif x == memb[len(memb) - 1]:
        fiering = np.array([[len(memb) - 1,1],[0,0]])

    for j in range(len(memb)):
        if x == memb[j]:
            fiering = np.array([[j+1,1],[0,0]])
            break
        elif x > memb[j] and x < memb[j + 1]:
            f1 = (x - memb[j])/(memb[j+1]-memb[j])
            f2 = (memb[j+1] - x)/(memb[j+1]-memb[j])
            fiering = np.array([[j+1,f2],[j+2, f1]])
            break
    return fiering


if __name__ == "__main__":
    x1 = np.linspace(-5, 5, num=41)
    x2 = np.linspace(-5, 5, num=41)
    TrainData = []
    for i in range(41):
        t = mship(m=-5, n=5, numb=7, x=x1[i])
        Fx11 = t[0,0]
        mFx11 = t[0,1]
        Fx12 = t[1,0]
        mFx12 = t[1,1]

        SelectFx1=Fx11
        mu_x1=mFx11
        if mFx12>mFx11:
            SelectFx1=Fx12
            mu_x1=mFx12
        for j in range(41):
            t = mship(m=-5, n=5, numb=7, x=x2[j])

            Fx21 = t[0,0]
            mFx21 = t[0,1]
            Fx22 = t[1,0]
            mFx22 = t[1,1]

            SelectFx2=Fx21
            mu_x2=mFx21
            if mFx22>mFx21:
                SelectFx2=Fx22
                mu_x2=mFx22

            y = x1[i] ** 2 + x2[j] ** 2
            t = mship(m=0, n=50, numb=7, x=y)
            Fy1 = t[0,0]
            mFy1 = t[0,1]
            Fy2 = t[1,0]
            mFy2 = t[1,1]

            SelectFy = Fy1
            mu_y = mFy1
            if mFy2 > mFy1:
                SelectFy = Fy2
                mu_y = mFy2


            FireDegree = mu_x1 * mu_x2 * mu_y
            TrainData.append([SelectFx1, SelectFx2, SelectFy, FireDegree])

    RuleBase = np.zeros((49,6))
    indx = 0
    for i in range(len(TrainData)):
        flg=0
        for j in range(49):
            if TrainData[i][0] == RuleBase[j][0] and TrainData[i][1] == RuleBase[j][1]:
                if TrainData[i][3] == RuleBase[j][3]:
                    RuleBase[j][0] = TrainData[i][0]
                    RuleBase[j][1] = TrainData[i][1]
                    RuleBase[j][2] = TrainData[i][2]
                    RuleBase[j][3] = TrainData[i][3]
                    RuleBase[j][4] = math.ceil(i/49)
                    RuleBase[j][5]= i-((math.ceil(i/49)-1)*49)
                flg = 1
        if flg == 0:
            RuleBase[indx][0] = TrainData[i][0]
            RuleBase[indx][1] = TrainData[i][1]
            RuleBase[indx][2] = TrainData[i][2]
            RuleBase[indx][3] = TrainData[i][3]
            RuleBase[indx][4] = math.ceil(i/49)
            RuleBase[indx][5]= i-((math.ceil(i/49)-1)*49)
            indx = indx + 1
            
    ruleCounter = 1
    for rule in RuleBase:
        c = crisp(m=0, M=50, fy=rule[2], n=7)
        rules = "rule " + str(ruleCounter) + ":  " + "If x1 is  A" + str(int(rule[0])) + " AND  x2 is  B" + str(int(rule[1])) + " Then y is  : " + str(int(c))
        ruleCounter += 1
        print(rules)
