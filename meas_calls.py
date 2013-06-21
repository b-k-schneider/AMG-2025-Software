"""
Library for calling measurement Methods
Calls all Libraries and triggers the measurement and averages the IR
Creates graphs (IR, FFT, etc)
required Parameters: fs, rt60, n_meas, n_chan
"""


def measure_mls(fs, rt60, n_meas, n_chan):
    # calls the MLS Measurement

    import mls_method, audio_io, numpy
    
    # creating MLS Signal
    meas_sig = mls_method.mls_gen(rt60,fs)

    ir_r_raw = numpy.array([])
    ir_l_raw = numpy.array([])
    
    # measuring n_meas times and averaging the IR's
    for i in xrange(n_meas):

        print("Measurement No.", i)
        
        resp_l, resp_r, meas_l, meas_r= audio_io.meas_run(fs,n_chan,meas_sig,rt60)
        ir_l, ir_r= mls_method.compute_ir(resp_l, resp_r, meas_l, meas_r)
        
        #TODO alignment of arrays
        if i>0:
            max_diff_l=(ir_l_raw.argmax(axis=0) - ir_l.argmax(axis=0))
            print max_diff_l

            ir_l = numpy.roll(ir_l, max_diff_l)
            ir_r = numpy.roll(ir_r, max_diff_l)
            
        if len(ir_l)>len(ir_l_raw):   
            #resize the arrays and add them
            ir_l_raw.resize(ir_l.shape)
            ir_r_raw.resize(ir_r.shape)

            ir_l_raw += ir_l
            ir_r_raw += ir_r

        else:
            ir_l.resize(ir_l_raw.shape)
            ir_r.resize(ir_r_raw.shape)

            ir_l_raw += ir_l
            ir_r_raw += ir_r
            
        del(resp_l, resp_r, meas_l, meas_r, ir_l, ir_r)

    ir_l_avg = ir_l_raw/float(n_meas)
    ir_r_avg = ir_r_raw/float(n_meas)

    del(ir_l_raw, ir_r_raw)

    return (ir_l_avg, ir_r_avg)

def measure_ess(fs, n_meas, n_chan, f_start, f_stop, t_sweep):

    # TODO ess measurement
    return (ir_l_avg, ir_r_avg)


def measure_sds(fs, f_sine1, f_sine2):

    # TODO sds measurement
    return sys_resp

def compute_fft(fs, meas_signal):
    
    # TODO FFT computing
    return fft

def plot_ir(fs, ir, filename):
    #Plots Impulse Responses as Images
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    # TODO axis Labeling, maybe scaling to time
    plt.plot(ir)
    plt.savefig(filename)
    
    return

def plot_fft(fs, fft, filename):
    #Plots FFT as Image
    
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    # TODO axis Labeling, maybe scaling to frequencies
    plt.plot(fft)
    plt.savefig(filename)
    
    return


    
    
