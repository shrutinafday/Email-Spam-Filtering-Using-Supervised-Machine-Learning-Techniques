import csv
import random
import math
import operator
import time

def loadDataset(filename,split,trainingSet=[],testSet=[]):
    with open(filename,'rb') as csvfile:
        lines=csv.reader(csvfile)
        dataset=list(lines)
        for x in range(len(dataset)):
            for y in range(58):
                dataset[x][y]=float(dataset[x][y])
            if random.random()< split:
                trainingSet.append(dataset[x])           
            else:
                testSet.append(dataset[x])
  
def euclideanDistance(instance1,instance2,length):
    distance=0
    for x in range(length):
        difference=instance1[x]-instance2[x]
        distance+= difference*difference 
    return math.sqrt(distance)

def neighbors(trainingSet,testcase,k):
    distances=[]
    length=len(testcase)-1
    for x in range(len(trainingSet)):
        dist=euclideanDistance(testcase,trainingSet[x],length)
        distances.append((trainingSet[x],dist))
    distances.sort(key=operator.itemgetter(1))
    kneighborslist=[]
    for x in range(k):
        kneighborslist.append(distances[x][0])
    return kneighborslist 

def getResponse(kneighborslist):
    DecisionVotes={}
    for x in range(len(kneighborslist)):
        decision=kneighborslist[x][-1]
        DecisionVotes[decision]=DecisionVotes.get(decision,0)+1
    return max(DecisionVotes.iteritems(), key=operator.itemgetter(1))[0] 

def getAccuracy(testSet,prediction):
    if len(testSet)!=len(prediction):
        print "some calculation error"
    correct=0    
    for i in range(len(testSet)):
        if testSet[i][-1]==prediction[i]:
            correct+=1     
    return (correct*1.0/len(testSet))*100        
            

if __name__=="__main__":
    #getting the datasets ready     
    trainingSet=[]
    testSet=[]
    split=0.67
    loadDataset('spambase.data',split,trainingSet,testSet)
    print 'Training set:'+repr(len(trainingSet))
    print 'Test Set:'+repr(len(testSet))
    #start measuring time
    start_time=time.time()
    prediction=[]
    k=3
    for x in range(len(testSet)):
        kneighbors=neighbors(trainingSet,testSet[x],k) 
        prediction.append(getResponse(kneighbors))
    end_time=time.time()
    accuracy=getAccuracy(testSet,prediction)
    #print prediction
    print ('Accuracy:'+repr(accuracy)+"%")
    simulationtime=end_time-start_time
    print "Simulation time: "+repr(simulationtime)+" seconds"    
                        