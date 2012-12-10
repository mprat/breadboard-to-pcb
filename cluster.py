import random
import math
from numpy import *
#from plotGauss2D import *

#############################
# MOG class
#############################

class MOG:
    def __init__(self, pi = 0, mu = 0, var = 0):
        self.pi = pi
        self.mu = mu
        self.var = var
#    def plot(self, color = 'black'):
#        return plotGauss2D(self.mu, self.var, color=color)
    def __str__(self):
        return "[pi=%.2f,mu=%s, var=%s]"%(self.pi, self.mu.tolist(), self.var.tolist())
    __repr__ = __str__

colors = ('blue', 'yellow', 'black', 'red', 'cyan')

#############################
# Plotting
#############################

def plotMOG(X, param, colors = colors):
    fig = pl.figure()                   # make a new figure/window
    ax = fig.add_subplot(111, aspect='equal')
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    ax.set_xlim(min(x_min, y_min), max(x_max, y_max))
    ax.set_ylim(min(x_min, y_min), max(x_max, y_max))
    for (gauss, col) in zip(param, colors[:len(param)]):
        art = gauss.plot(color=col)
        ax.add_artist(art)
    plotData(X)

def plotData(X, c='green'):
    pl.plot(X[:,0:1].T[0],X[:,1:2].T[0], 'gs', c=c)
# e.plotData(pl.array([list(m.mu) for m in randmog]))


#############################
# Operations on Gaussians
#############################

def varMat(s1, s2, s12 = 0):
    return pl.array([[s1, s12], [s12, s2]])

def evaluateGaussian(pt, mu, var):
    (denom, expon) = evaluateGaussianHelper(pt, mu, var)
    return 1.0/denom * pl.exp(expon)

def evaluateGaussianHelper(pt, mu, var):
    d = len(pt)
    try:
        denom = (2.0*pl.pi)**(d/2.0) * (1/(pl.sqrt(pl.linalg.det(var))))
    except Exception, e:
        print var, "whoops"
        raise e
    expon = -0.5 * pl.dot((pt - mu).T, pl.dot(pl.linalg.inv(var), (pt - mu)))
    return (denom, expon)

def randomMOG(X, m=2, diag=False):
    (n, d) = X.shape
    if not diag:
        return [MOG(pi=1./m, 
                mu=X[random.randint(0,n-1),:], 
                var=varMat(3*random.random(), 3*random.random(), 3*random.random()-1.5)) for i in xrange(m)]
    else:
        return [MOG(pi=1./m, 
                mu=X[random.randint(0,n-1),:], 
                var=varMat(3*random.random(), 3*random.random())) for i in xrange(m)]

#############################
# EM
#############################

def responsibilities(X, MOG):
    resp = pl.zeros([len(X), len(MOG)])
    for (i, pt) in enumerate(X):
        for (j, g) in enumerate(MOG):
            resp[i,j] = g.pi * evaluateGaussian(pt, g.mu, g.var)
        resp[i, :] = resp[i, :] / sum(resp[i, :])
    return resp

runaway = 0.001
def newParams(X, resp, diag=False):
    n = pl.sum(resp, 0)

    pis = n / len(X)
    mus = (1.0/n) * pl.dot(X.T, resp)

    varks = list()
    for k in range(len(resp[0])):
        vark = pl.zeros([X.shape[1], X.shape[1]])
        centered = X - mus[:,k].T
        for (i, x) in enumerate(X):
            if diag:
                for d in range(X.shape[1]):
                    vark[d, d] += resp[i,k]*centered[i, d]**2
            else:
                vark += resp[i, k]*pl.dot(pl.array([centered[i]]).T, pl.array([centered[i]]))
        vark = vark / n[k]
        
        if pl.linalg.det(vark) <= runaway:
            print "Runaway determinant:", resp
            mus[:,k] = randomMOG(X, 1)[0] # unclear if useful
            vark = 3*eye(2)

        varks.append(vark)

    return [MOG(pi = pis[k], mu = mus[:, k], var = varks[k]) for k in range(len(pis))]
    
def logLike(X, mogs):
    s = 0
    for pt in X:
        a = list()
        for (k, mog) in enumerate(mogs):
            (denom, expon) = evaluateGaussianHelper(pt, mog.mu, mog.var)
            a.append(pl.log(mog.pi /denom) + expon)
        s += pl.logaddexp.reduce(a)
    return s

maxIter = 100
def EM(X, initMOG, convergence, diag=False):
    mog = initMOG
    ct = 0
    L = 0
    for i in range(maxIter):
        try:
            resp = responsibilities(X, mog)
            newMog = newParams(X, resp, diag)
            newL = logLike(X, newMog)
            print newL
            if abs(newL - L) < convergence:
                break
        except e:
            print "Terminated with error"
            break
        if math.isnan(newMog[0].pi):
            print "Terminated with NaN"
            break
        else:
            mog = newMog
            L = newL
            ct += 1
    print "Total of", ct, "iterations"
    return (L, mog)

#############################
# k-means
#############################

def kMeans(X, means):
    means = pl.array(means)
    assign = pl.ones(len(X))

    i = 0
    maxIter = 100
    for q in range(maxIter):
        newAssign = pl.array(assign)
        for (i, x) in enumerate(X):
            distances = [pl.norm(x-mean) for mean in means]
            cluster = distances.index(min(distances))
            newAssign[i] = cluster
        if pl.norm(newAssign - assign) < 0.1: # hack hack hack
            print "k-means converged after", q, "iterations"
            return means
        assign = newAssign

        newMeans = pl.array(means)
        for (cluster, mean) in enumerate(means):
            mine = [x for (i, x) in enumerate(X) if assign[i] == cluster]

            if len(mine) > 0:
                avg = [0 for i in X[0]]
                for x in mine:
                    avg = [avg[j] + el for (j,el) in enumerate(x)]
                avg = [el / len(mine) for el in avg]
                newMeans[cluster] = avg
            else:
                newMeans[cluster] = means[cluster]

        means = newMeans

#############################
# Cross-validation
#############################

def traintest(which):
    train = loadtxt('data/data_' + str(which) + '_small.txt')
    test = loadtxt('data/data_' + str(which) + '_large.txt')
    (ntrain, d) = train.shape
    
    trainDict = {}
    testDict = {}
    models = {}
    for k in [1, 2, 3, 4, 5]:
        kinit = [train[random.randint(0,ntrain-1),:] for i in range(k)]
        means = kMeans(train, kinit)
        mog = [MOG(pi = 1./k, mu = m, var = 3*eye(2)) for m in means]
        for diag in True, False:
            (l, c) = EM(train, mog, 0.01, diag)
            trainDict[k, diag] = l / len(train)
            testDict[k, diag] = logLike(test, c) / len(test)
            models[k, diag] = c
    
    return (trainDict, testDict, models)

def goforit(data):
    (ntrain, d) = data.shape
    trainDict = {}
    models = {}
    for k in [3, 4]:
        kinit = [data[random.randint(0,ntrain-1),:] for i in range(k)]
        means = kMeans(data, kinit)
        mog = [MOG(pi = 1./k, mu = m, var = 3*eye(2)) for m in means]
        for diag in [False]:
            (l, c) = EM(data, mog, 0.0001, diag)
            trainDict[k, diag] = l / len(data)
            models[k, diag] = c
            plotMOG(data, c)
    
    return (trainDict, models)

#############################
# Test
#############################

def data(name):
    return loadtxt('data/' + name + '.txt')

def test(X, clusters, converge, diag=False):
    randmog = randomMOG(X, clusters, diag)
    (l, c) = EM(X, randmog, converge, diag)
    plotMOG(X, c)
    pl.show()

