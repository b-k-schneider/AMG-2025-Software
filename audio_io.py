"""
Library for Audio I/O via OSS (/dev/dsp)
needs native OSS or emulated via aoss or padsp
needed parameters: fs, res, n_chan, sig_meas
"""

import os, sys, audioop, ossaudiodev, wave, numpy, scipy.io.wavfile, pyaudio



def audio_open(fs,n_chan):
    global pya
    global stream
    global sys_wav
    global FORMAT
    FORMAT = pyaudio.paInt16
    global chunk
    chunk=1024
    

    print("Instanting PyAudio")
    
    pya= pyaudio.PyAudio()

    print("Opening Audio Device")

        
    stream = pya.open(format = FORMAT,
                                    channels = n_chan,
                                    rate = fs,
                                    input = True,
                                    output = True,
                                    frames_per_buffer = chunk,
                                    input_device_index = 1,
                                    output_device_index = 1)
    
    print("Audio Device Opened...")

    stream.start_stream()

    
        


def audio_close():

    global stream
    global stream
    global pya
        
    stream.stop_stream()
    
    pya.terminate()

    print("Audio Device Closed...")


def audio_mono_out(sig_meas,fs,n_chan):

    global stream

    
    # save .wav file
    sf = wave.open("/tmp/meas_mono.wav", 'w')
    sf.setparams((2, n_chan, fs, 0, 'NONE', 'no compression'))
    sf.writeframesraw(sig_meas)
    sf.close()

    stream.write(sig_meas)
    

def audio_stereo_out(sig_meas,fs,n_chan):

    global stream

    

    #converts the signal to a stereo signal
    stereoaudio = audioop.tostereo(sig_meas, 2, 1, 1)
    #DEBUG sna=len(stereoaudio)
    #DEBUG print sna

    # save .wav file
    sf = wave.open("/tmp/meas_stereo.wav", 'w')
    sf.setparams((2, n_chan, fs, 0, 'NONE', 'no compression'))
    sf.writeframesraw(stereoaudio)
    sf.close()

    stream.write(stereoaudio)
    



def audio_in(rt60,fs,n_chan):

    global stream
    global sys_wav
    import time

    frames = []

    for i in range(0, int(fs / 1024*(2.5*rt60/1000.0))):
        data = stream.read(1024)
        frames.append(data)
    
    # recording to .wav file
    sys_wav = wave.open("/tmp/sysresp.wav", 'w')
    sys_wav.setparams((2, n_chan, fs, 0, 'NONE', 'no compression'))
    sys_wav.writeframes(b''.join(frames))
    sys_wav.close()

    del(frames)
    
    
    return 


def audio_run(n_chan,sig_meas,rt60,fs):

    #starts the audio output and recording
    

    if n_chan == 2:
        audio_stereo_out(sig_meas,fs,n_chan)
    else :
        audio_mono_out(sig_meas,fs,n_chan)

    audio_in(rt60,fs,n_chan)
    
    return 



def list_to_wav(sig_list):

    # converts list data to wav struct, to be usable for oss device

    output_signal= ''
    # scaling to -1dB signal ((2^16)/2)*-1dB
    for j in range(len(sig_list)):
        output_signal += wave.struct.pack('<h', (sig_list[j]*29205))
    print ("Signal converted")
    return output_signal


def extract_channels(n_chan):

    #extracts data out of both wavefiles into 4 arrays
    
    #splitting of the tuple
    if n_chan == 2:
        fs,meas_array = scipy.io.wavfile.read("/tmp/meas_stereo.wav")
    else :
        fs,meas_array = scipy.io.wavfile.read("/tmp/meas_mono.wav")

    fs,resp_array = scipy.io.wavfile.read("/tmp/sysresp.wav")


    #creation of empty arrays
    resp_l=numpy.empty(len(resp_array))
    resp_r=numpy.empty(len(resp_array))
    meas_l=numpy.empty(len(meas_array))
    meas_r=numpy.empty(len(meas_array))

    
    if n_chan == 2:

        # splitting into channels
        # and converting from 16bit INT to Float
        for i in xrange(len(resp_array)):
            resp_l[i] =(resp_array[i,0]/32767.0)
            resp_r[i] =(resp_array[i,1]/32767.0)    

        for i in xrange(len(meas_array)):
            meas_l[i] =(meas_array[i,0]/32767.0)
            meas_r[i] =(meas_array[i,1]/32767.0)

    else:
        
        # mono got only one channel
        
        resp_l =(resp_array/32767.0)
        meas_l =(meas_array/32767.0)
	
    return (resp_l, resp_r, meas_l, meas_r)
    


def meas_run(fs,n_chan,sig_list,rt60):

    
    #length for recording in samples ((recordlength*samplerate)/1000)
    len_sp = int((((2.5*rt60)/1000.0)*fs)/1024)
    #DEBUG print len_sp
    #convert list to wav struct
    m_sig = list_to_wav(sig_list)

    #Playing Measurement Signal and Recordung System Response
    audio_run(n_chan,m_sig,rt60,fs)

    #Extracting Channels
    resp_l, resp_r, meas_l, meas_r=extract_channels(n_chan)
    
  
    return (resp_l, resp_r, meas_l, meas_r)
    


