import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


'''
0 blue
1 green
2 yellow
3 orange
4 nothing
'''
color_maps = [2, 1, 0, 3, 3, 1, 0, 3, 2, 1, 0]## current map starting at cell#2 and ending at cell#12 ###print(color_maps[1], len(color_maps))
curState = np.ones(11)*1.0/11.0 #print(curState)
measuModel = np.matrix('0.60 0.20 0.05 0.05;0.20 0.60 0.05 0.05;0.05 0.05 0.65 0.20;0.05 0.05 0.15 0.60;0.10 0.10 0.10 0.10') #print(measuModel[2,3])
stateModel = np.matrix('0.85 0.05 0.05; 0.10 0.90 0.10; 0.05 0.05 0.85') #print(stateModel[0,0])

def statePredict(u,stateModel,curState):
    predState = np.zeros(11)
    for i,val in enumerate(predState):
        predState[i] += stateModel[2,u+1]*curState[i-1]
        predState[i] += stateModel[1,u+1]*curState[i]
        if i == len(curState)-1:
            predState[i] += stateModel[0,u+1]*curState[0]
        else:
            predState[i] += stateModel[0,u+1]*curState[i+1]
    return predState

def stateUpdate(z,predState,measuModel):
    updatedState = np.zeros(11)
    summation = 0
    for i in range(0,len(predState)):
        summation += measuModel[z,color_maps[i]]*predState[i]
    for i in range(0,len(predState)):
        updatedState[i] = (measuModel[z,color_maps[i]] * predState[i])/summation
    return updatedState,summation


def hplot(curState):
    objects = ('2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
    y_pos = np.arange(len(objects))
    plt.bar(y_pos, curState, color=['yellow', 'green', 'blue', 'orange', 'orange', 'green', 'blue', 'orange', 'yellow', 'green', 'blue'],align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.xticks(rotation=90)
    plt.ylabel('Probability')
    plt.title('Location')
    plt.axes().xaxis.grid(False)  # vertical lines
    plt.show(block=False)
    plt.pause(1)
    plt.close()

'''
0 blue
1 green
2 yellow
3 orange
4 nothing
'''
U = [1,1,1,1,1,1,1,1,0,1,1,1]
Z = [3,2,1,0,4,1,0,1,3,2,1,0]

for j in range(0,len(U)):
    hplot(curState)
    u = U[j]
    z = Z[j]
    predState = statePredict(u,stateModel,curState)
    #print('predState:',predState)
    #print(sum(predState))
    curState,summation = stateUpdate(z,predState,measuModel)
    print('curState:',curState)

    #print(sum(curState))
    hplot(curState)


