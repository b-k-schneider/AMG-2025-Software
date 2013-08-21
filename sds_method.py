"""
Library for the SDS measuring method
Creates a Sine or Double Sine Signal
required Parameters: fs, n_meas, f0, f1, t_sw
"""

import numpy, scipy, math

def generate_sds(fs, f_0, f_1, t_meas):

    sine_one=[]
    sine_two=[]
    sds_signal=[]

    
    print "fs=",fs
    print "f_sine1=",f_0
    print "f_sine2=",f_1
    
    #generate sinewave 1

    for i in xrange(fs*t_meas):
        ampl=math.sin((2*math.pi*i*f_0)/fs)
        sine_one.append(ampl)

    #generate sinewave 2 (if f1=0 no second sinewave will be generated)
    if f_1>0:

        for i in xrange(fs*t_meas):
            ampl=math.sin((2*math.pi*i*f_1)/fs)
            sine_two.append(ampl)

        #adding the sinewaves 

        for i in xrange(len(sine_one)):
            sds_signal.append((sine_one[i]+sine_two[i])/2)
        print "Debug: Two Sines"
        
    else:
                        
        sds_signal=sine_one
        print "Debug: Only one Sine"

    return sds_signal

def compute_resp(n_chan):

    import audio_io
    import scipy.signal
    import scipy.fftpack
    # if mono, only leftchannels are used

    
    #Extracting Channels
    resp_l, resp_r, meas_l, meas_r=audio_io.extract_channels(n_chan,0)
    
    
    return (resp_l, resp_r)

