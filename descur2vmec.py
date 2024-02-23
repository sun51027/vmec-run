#!/usr/bin/python
import numpy as np

R0 = 0.45  # major radius
aspect = 1.5
elong = 2.2  # kappa
traing = 0.5  # delta
a = R0 / aspect  # minor radius
Z0 = 0.0
numPoints = 100

outputFileName = 'RPhiZ_points'
fid = open(outputFileName, 'w')
if fid == -1:
    raise ValueError('Cannot open file for writing: %s' % outputFileName)

theta = np.linspace(0, 2 * np.pi, numPoints)

fid.write('%d 1 1\n' % (numPoints))
for i in range(numPoints):
    fR = R0 + a * np.cos(theta[i] + traing * np.sin(theta[i]))
    fZ = Z0 + a * elong * np.sin(theta[i])
    fid.write('%f %f %f\n' % (fR, theta[i], fZ))

fid.close()


