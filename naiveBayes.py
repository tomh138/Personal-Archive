# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math


class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
    """
    See the project description for the specifications of the Naive Bayes classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """

    def __init__(self, legalLabels):
        self.legalLabels = legalLabels
        self.type = "naivebayes"
        self.k = 1  # this is the smoothing parameter, ** use it in your train method **
        self.automaticTuning = False  # Look at this flag to decide whether to choose k automatically ** use this in your train method **

    def setSmoothing(self, k):
        """
        This is used by the main method to change the smoothing parameter before training.
        Do not modify this method.
        """
        self.k = k

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        """
        Outside shell to call your method. Do not modify this method.
        """

        # might be useful in your code later...
        # this is a list of all features in the training set.
        self.features = list(set([f for datum in trainingData for f in datum.keys()]));

        if (self.automaticTuning):
            kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
        else:
            kgrid = [self.k]

        self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
        """
        Trains the classifier by collecting nums over the training data, and
        stores the Laplace smoothed estimates so that they can be used to classify.
        Evaluate each value of k in kgrid to choose the smoothing parameter
        that gives the best accuracy on the held-out validationData.

        trainingData and validationData are lists of feature Counters.  The corresponding
        label lists contain the numCorrect label for each datum.

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        prior = util.Counter()
        for l in trainingLabels:
            prior[l] += 1
        prior.normalize()
        self.prior = prior
        nums = {}
        sums = {}
        for x in self.features:
            nums[x] = {0: util.Counter(), 1: util.Counter()}
            sums[x] = util.Counter()
        for i, datum in enumerate(trainingData):
            y = trainingLabels[i]
            for f, value in datum.items():
                nums[f][value][y] = nums[f][value][y] + 1.0
                sums[f][y] = sums[f][y] + 1.0
        validCond = {}
        highAcc = None
        for k in kgrid or [0.0]:  # find k use highest accuracy
            numCorrect = 0
            cond = {}
            for feat in self.features:
                cond[feat] = {0: util.Counter(), 1: util.Counter()}
            for feat in self.features:  # Laplace smoothing
                for value in [0, 1]:
                    for label in self.legalLabels:
                        cond[feat][value][label] = (nums[feat][value][label] + k) / (sums[feat][label] + k * 2)
            self.cond = cond  # Check accuracy associated to k
            attempt = self.classify(validationData)
            for i, j in enumerate(attempt):
                numCorrect = numCorrect + (validationLabels[i] == j and 1.0 or 0.0)
            acc = numCorrect / len(attempt)
            if highAcc is None or acc > highAcc:  # keep best k
                highAcc = acc
                validCond = cond
                self.k = k
        self.cond = validCond

    def classify(self, testData):
        """
        Classify the data based on the posterior distribution over labels.

        You shouldn't modify this method.
        """
        guesses = []
        self.posteriors = []  # later data analysis
        for datum in testData:
            posterior = self.calculateLogJointProbabilities(datum)
            guesses.append(posterior.argMax())
            self.posteriors.append(posterior)
        return guesses

    def calculateLogJointProbabilities(self, datum):
        """
        Returns the log-joint distribution over legal labels and the datum.
        Each log-probability should be stored in the log-joint counter, e.g.
        logJoint[3] = <Estimate of log( P(Label = 3, datum) )>

        To get the list of all possible features or labels, use self.features and
        self.legalLabels.
        """
        logJoint = util.Counter()
        for x in self.legalLabels:
            logJoint[x] = math.log(self.prior[x])
            for c in self.cond:
                prob = self.cond[c][datum[c]][x]
                logJoint[x] = logJoint[x] + (prob and math.log(prob) or 0.0)
        return logJoint

    def findHighOddsFeatures(self, label1, label2):
        """
        Returns the 100 best features for the odds ratio:
                P(feature=1 | label1)/P(feature=1 | label2)

        Note: you may find 'self.features' a useful way to loop through all possible features
        """
        features = 0
        return features
