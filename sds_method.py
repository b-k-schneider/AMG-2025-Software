"""
Library for the SDS measuring method
Creates a Sine or Double Sine Signal
required Parameters: fs, n_meas, f0, f1, t_sw
"""

import numpy, scipy, math

def sds_gen(fs, f0, f1, time):

    sine_one=[]
    sine_two=[]
    sds_signal=[]
    
    #generate sinewave 1

    for i in xrange(fs*time):
        ampl=math.sin((2*math.pi*i*f0)/fs)
        sine_one.append(ampl)

    #generate sinewave 2 (if f1=0 no second sinewave will be generated)

    for i in xrange(fs*time):
        ampl=math.sin((2*math.pi*i*f1)/fs)
        sine_two.append(ampl)

    #adding the sinewaves 

    for i in xrange(len(sine_one)):
        sds_signal.append((sine_one[i]+sine_two[i])/2)
        

    return sds_signal
