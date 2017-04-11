import csv
import numpy as np  # http://www.numpy.org
from math import log
import random

from CSE6242HW4Tester import generateSubmissionFile


"""
Here, X is assumed to be a matrix with n rows and d columns
where n is the number of samples
and d is the number of features of each sample

Also, y is assumed to be a vector of n labels
"""

# Enter your name here
myname = "Lei-Wenxiang"

def Entropy(dataset):
    if len(dataset) == 0:
        return 0

    y = [k[-1] for k in dataset]
    total = len(y)
    num1 = sum(i for i in y)
    num0 = total - num1
    p1 = float(num1) / total
    p2 = float(num0) / total
    if p1 != 0. and p2 != 0.:
        return -p1 * log(p1, 2) - p2 * log(p2, 2)
    else:
        return 0

def splitDataSet(X, y, axis, value):
    retX1 = []
    retY1 = []
    retX2 = []
    retY2 = []
    for i in range(len(X)):
        if X[i][axis] <= value:
            retX1.append(X[i])
            retY1.append(y[i])
        else:
            retX2.append(X[i])
            retY2.append(y[i])
    return (retX1, retY1, retX2, retY2)

def chooseBestFeatureToSplit(X,y,indice):
    dataset = np.c_[X,y]
    baseEntropy = Entropy(dataset)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in indice:
        vals = [example[i] for example in X]
        univals = sorted(set(vals))
        newEntropy = 0.0
        #for value in univals:
        c = 0
        while c <25:
            c+=1
            value = random.choice(univals)
            #bestValue = value
            subX1,subY1,subX2,subY2 = splitDataSet(X, y, i, value)
            p1 = len(subY1)/float(len(X))
            p2 = len(subY2)/float(len(X))
            subdataset1 = np.c_[subX1,subY1]
            subdataset2 = np.c_[subX2,subY2]
            newEntropy = p1 * Entropy(subdataset1) + p2 * Entropy(subdataset2)
            infoGain = baseEntropy - newEntropy
            if (infoGain > bestInfoGain):
                bestInfoGain = infoGain
                bestFeature = i
                bestValue = value
        """
        for value in univals:
            subX1,subY1,subX2,subY2 = splitDataSet(X, y, i, value)
            p1 = len(subY1)/float(len(X))
            p2 = len(subY2)/float(len(X))
            subdataset1 = np.c_[subX1,subY1]
            subdataset2 = np.c_[subX2,subY2]
            newEntropy = p1 * Entropy(subdataset1) + p2 * Entropy(subdataset2)
            infoGain = baseEntropy - newEntropy
            if (infoGain > bestInfoGain):
                bestInfoGain = infoGain
                bestFeature = i
                bestValue = value
        """
    return bestFeature,bestValue

def majorityCnt(quality):
    total=len(quality)
    num_1=sum(quality)
    num_0=total-num_1
    if num_1>=num_0:
        return 1
    else:
        return 0

def creatTree(X, y, depth, indice):
    nrow=len(X)
    ncol=len(y)
    quality = [i for i in y]
    depth += 1
    if ncol == 1:
        return majorityCnt(quality)
    elif nrow <=50:
        return majorityCnt(quality)
    elif depth > 4:
        return majorityCnt(quality)
    elif len(quality)==sum(quality):
        return 1
    elif sum(quality)==0:
        return 0
    else:
        bestFeat,bestVal = chooseBestFeatureToSplit(X,y,indice)
        tree = {bestFeat:{}}
        subX1,subY1,subX2,subY2 = splitDataSet(X, y, bestFeat, bestVal)
        tree[bestFeat]["<=" + str(bestVal)] = creatTree(subX1, subY1, depth, indice)
        tree[bestFeat][">" + str(bestVal)] = creatTree(subX2, subY2, depth, indice)
        return tree

class RandomForest(object):
    class __DecisionTree(object):
        tree = {}
        def learn(self, X, y, indice):
            # TODO: train decision tree and store it in self.tree
            self.tree = creatTree(X,y,0,indice)

        def classify(self, test_instance):
            # TODO: return predicted label for a single instance using self.tree
            result = 0
            myTree = self.tree
            while type(myTree)==dict:
                index=myTree.keys()[0]
                value = float(test_instance[index])
                myTree = myTree[index]
                myValueStr = myTree.keys()[0]
                if ">" in myValueStr:
                    myValue = float(myValueStr[1:])
                    if value <= myValue:
                        myTree = myTree[myTree.keys()[1]]
                    else:
                        myTree = myTree[myTree.keys()[0]]
                else:
                    myValue = float(myValueStr[2:])
                    if value <= myValue:
                        myTree = myTree[myTree.keys()[0]]
                    else:
                        myTree = myTree[myTree.keys()[1]]
            result = int(myTree)
            return result
            #return 0

    decision_trees = []

    def __init__(self, num_trees):
        # TODO: do initialization here, you can change the function signature according to your need
        self.num_trees = num_trees
        self.decision_trees = [self.__DecisionTree()] * num_trees

    # You MUST NOT change this signature
    def fit(self, X, y):
        # TODO: train `num_trees` decision trees

        for i in range(self.num_trees):
            sub_X=[]
            sub_y=[]
            for n in range(len(X)):
                r= int(np.random.random_integers(0,len(X)-1))
                sub_X.append(X[r])
                sub_y.append(y[r])
            numFeatures = len(X[0])
            indice = np.random.choice(numFeatures, size=4, replace=False)
            self.decision_trees[i].learn(sub_X,sub_y,indice)
            print indice   
            print i+1

    # You MUST NOT change this signature
    def predict(self, X):
        y = np.array([], dtype = int)

        for instance in X:
            votes = np.array([decision_tree.classify(instance)
                              for decision_tree in self.decision_trees])

            counts = np.bincount(votes)

            y = np.append(y, np.argmax(counts))

        return y


def main():
    X = []
    y = []

    # Load data set
    with open("hw4-data.csv") as f:
        next(f, None)

        for line in csv.reader(f, delimiter = ","):
            X.append(line[:-1])
            y.append(line[-1])

    X = np.array(X, dtype = float)
    y = np.array(y, dtype = int)

    # Split training/test sets
    # You need to modify the following code for cross validation #10-fold cross-validation
    total = 0   
    K = 10
    for index in range(K):
        X_train = np.array([x for i, x in enumerate(X) if i % K != index], dtype = float)
        y_train = np.array([z for i, z in enumerate(y) if i % K != index], dtype = int)
        X_test  = np.array([x for i, x in enumerate(X) if i % K == index], dtype = float)
        y_test  = np.array([z for i, z in enumerate(y) if i % K == index], dtype = int)
        print str(index+1) +"-fold-crossvalidation"
        #Default #attribute is 3
        randomForest = RandomForest(50)#999 is number of decision trees  # Initialize according to your implementation

        randomForest.fit(X_train, y_train)

        y_predicted = randomForest.predict(X_test)

        results = [prediction == truth for prediction, truth in zip(y_predicted, y_test)]

        # Accuracy
        accuracy = float(results.count(True)) / float(len(results))
        total += accuracy
    Acc_Avg = total/10
    print "accuracy: %.4f" % Acc_Avg

    #generateSubmissionFile(myname, randomForest)


main()
