"""
Library for calling measurement Methods
Calls all Libraries and triggers the measurement and averages the IR
Creates graphs (IR, FFT, etc)
required Parameters: fs, rt60, n_meas, n_chan
"""


def measure_mls(fs, rt60, n_meas, n_chan):
    # calls the MLS Measurement

    import mls_method, audio_io, numpy, time
    
    # creating MLS Signal
    meas_sig = mls_method.mls_gen(rt60,fs)

    # open audio device
    audio_io.audio_open(fs,n_chan)

    for i in xrange(n_meas+1):

        print("Measurement No.", i)
        
        audio_io.meas_run(fs,n_chan,meas_sig,rt60,i)

    #closing audio device
    audio_io.audio_close()    

    ir_l_avg, ir_r_avg = average_ir_mls(n_meas, n_chan)

    return (ir_l_avg, ir_r_avg)


def average_ir_mls(n_meas, n_chan):

    import mls_method, audio_io, numpy, time

    ir_r_raw = numpy.array([])
    ir_l_raw = numpy.array([])
    
    for i in xrange(n_meas+1):

        if i==0:
            i=1

        print "Processing Response No",i
        
        ir_l, ir_r= mls_method.compute_ir(n_chan, i)

        #TODO alignment of arrays
        if i>1:
            max_diff_l=(ir_l_raw.argmax(axis=0) - ir_l.argmax(axis=0))
            #DEBUG print max_diff_l

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
            
        del(ir_l, ir_r)
        
    ir_l_avg = ir_l_raw/float(n_meas)
    ir_r_avg = ir_r_raw/float(n_meas)

    del(ir_l_raw, ir_r_raw)

    return (ir_l_avg, ir_r_avg)


def measure_ess(fs, n_meas, n_chan, f_start, f_stop, t_sweep):
    # calls the ESS Measurement

    import ess_method, audio_io, numpy, time

    ir_r_raw = numpy.array([])
    ir_l_raw = numpy.array([])

    
    # creating ESS Signal
    meas_sig = ess_method.generate_ess(fs, f_start, f_stop, t_sweep)

    # open audio device
    audio_io.audio_open(fs,n_chan)

    for i in xrange(n_meas+1):

        print("Measurement No.", i)

        #t_sweep*1000 is half the time to record in ms
        audio_io.meas_run(fs,n_chan,meas_sig,int(t_sweep*1000),i) 

    #closing audio device
    audio_io.audio_close()

    ir_l_avg, ir_r_avg = average_ir_ess(n_meas, n_chan)

    return (ir_l_avg, ir_r_avg)

def average_ir_ess(n_meas, n_chan):

    import ess_method, audio_io, numpy, time

    ir_r_raw = numpy.array([])
    ir_l_raw = numpy.array([])
    
    for i in xrange(n_meas+1):

        if i==0:
            i=1

        print "Processing Response No",i
        
        ir_l_i, ir_r_i= ess_method.compute_ir(n_chan, i)

        
        ir_l=ir_l_i.copy()
        ir_r=ir_r_i.copy()
        
        
        #TODO alignment of arrays
        if i>1:
            max_diff_l=(ir_l_raw.argmax(axis=0) - ir_l.argmax(axis=0))
            #DEBUG print max_diff_l

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
            
        del(ir_l, ir_r)
        
    ir_l_avg = ir_l_raw/float(n_meas)
    ir_r_avg = ir_r_raw/float(n_meas)

    del(ir_l_raw, ir_r_raw)

    return (ir_l_avg, ir_r_avg)

def measure_sds(fs,n_chan, f_sine1, f_sine2, t_meas):

     # calls the SDS Measurement

    import sds_method, audio_io, numpy
    
    # creating ESS Signal
    meas_sig = sds_method.generate_sds(fs, f_sine1, f_sine2, t_meas)

    # open audio device
    audio_io.audio_open(fs,n_chan)


    #t_sweep*1000 is half the time to record in ms
    audio_io.meas_run(fs,n_chan,meas_sig,int(t_meas*1000),0) 

    #closing audio device
    audio_io.audio_close()

    resp_l, resp_r = sds_method.compute_resp(n_chan)


    return (resp_l, resp_r)



def compute_fft(fs, ir):

    import scipy.signal, numpy
    from scipy import fftpack

    # creating asymmetric bartlett window for spectral analysis
    window_bart = scipy.signal.bartlett(len(ir),sym=False)

    # windowing the impulse response
    ir_wind = ir * window_bart

    #computing fft
    sig_fft=fftpack.rfft(ir_wind)

    #setting length of fft
    n=sig_fft.size 
    timestep=1/float(fs)

    #generating frequencies according to fft points
    freq=fftpack.rfftfreq(n,d=timestep) 

    #normalizing fft
    sys_fft=abs(sig_fft)/n

    
    # TODO FFT computing
    return sys_fft, freq

def window_ir(ir):

    #TODO Windowing IR for Filtering

    return ir_win

def plot_save_ir(fs, ir, filename):
    #Plots Impulse Responses as Images
    import numpy
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import wave
    import audio_io

    png_name="/tmp/amg2025/"+filename+".jpg"
    txt_name="/tmp/amg2025/"+filename+".txt"
    wav_name="/tmp/amg2025/"+filename+".wav"
    
    numpy.savetxt(txt_name, ir, fmt='%10.5f', delimiter=';', newline='\n')

    plt.xlabel('Samples')
    plt.ylabel('Value')
    
    plt.plot(ir)
    plt.savefig(png_name)
    plt.clf()

    adjust=29205.0/float(ir[ir.argmax()])

    # save .wav file
    sf = wave.open(wav_name, 'w')
    sf.setparams((1, 2, fs, 0, 'NONE', 'no compression'))
    
    for j in range(len(ir)):
        ir_wav = wave.struct.pack('<h', int(ir[j]*adjust))
        sf.writeframesraw(ir_wav)


    sf.close()
    
    return

def plot_save_fft(freq, sys_fft, filename,avg):
    #Plots FFT as Image

    import numpy
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import scipy.signal

    png_name="/tmp/amg2025/"+filename+".jpg"
    txt_name="/tmp/amg2025/"+filename+".txt"
    
    # filtering the fft by an average filter
    if avg>0:
        print "Average Filtering On"
        avg_fft = scipy.signal.medfilt(sys_fft, 333)

        #scaling to dB
        avg_fft=20*numpy.log10(avg_fft)
        numpy.savetxt(txt_name, avg_fft, fmt='%10.5f', delimiter=';', newline='\n') 
        # TODO axis Labeling, maybe scaling to frequencies
        plt.plot(freq,avg_fft)
    else:
        print "Average Filtering Off"

        #scaling to dB
        sys_fft=20*numpy.log10(sys_fft)
        numpy.savetxt(txt_name, sys_fft, fmt='%10.5f', delimiter=';', newline='\n') 
        plt.plot(freq,sys_fft)


    plt.xlabel('Frequency in Hz')
    plt.ylabel('dB')
    plt.xscale('log')
    
    plt.grid(True)
    plt.savefig(png_name)
    plt.clf()
    
    return


def make_zip(file_name):
    import zipfile
    import os
    import shutil
    # Packing the results in a Zip File

    zip_name="/tmp/"+file_name+".zip"

    zf=zipfile.ZipFile(zip_name, "w")
    
    folder="/tmp/amg2025/"
    
    for the_file in os.listdir(folder):
    
        if the_file==zip_name:
            print "bla"

        else:
            file_path=os.path.join(folder,the_file)

            if os.path.isfile(file_path):
                zf.write(file_path)
            
    zf.close()

    shutil.move(zip_name,folder)

    return
    
def clear_tmp():
    # Clearing the tmp folder

    import os

    folder="/tmp/amg2025/"
    for the_file in os.listdir(folder):
        file_path=os.path.join(folder,the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e

    return



