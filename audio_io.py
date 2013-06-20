"""
Library for Audio I/O via OSS (/dev/dsp)
needs native OSS or emulated via aoss or padsp
needed parameters: fs, res, n_chan, sig_meas
"""

import os, sys, audioop, ossaudiodev, wave, numpy, scipy.io.wavfile

def audio_open():

    global dspout
    global dspin

    # Open 2 file handles
    dspout = ossaudiodev.open('/dev/dsp', 'w')
    dspin = ossaudiodev.open('/dev/dsp', 'r')



def audio_close():

    #closes the oss devices
    global dspout
    global dspin

    dspout.close()
    dspin.close()



def audio_init(fs,n_chan):


    # Configure OSS Device Resolution, Mono/Stereo, Samplerate, non-Blocking Mode
    fmt_o_err = dspout.setfmt(ossaudiodev.AFMT_S16_LE)
    fmt_i_err = dspin.setfmt(ossaudiodev.AFMT_S16_LE)

    ch_o_err = dspout.channels(n_chan)
    ch_i_err = dspin.channels(n_chan)

    fs_o_err = dspout.speed(fs)
    fs_i_err = dspin.speed(fs)
    


def audio_mono_out(sig_meas):
    
    # save .wav file
    sf = wave.open("/tmp/meas_mono.wav", 'w')
    sf.setparams((2, 1, 44100, 0, 'NONE', 'no compression'))
    sf.writeframesraw(sig_meas)
    sf.close()

    dspout.write(sig_meas)


def audio_stereo_out(sig_meas):

    #converts the signal to a stereo signal
    stereoaudio = audioop.tostereo(sig_meas, 2, 1, 1)
    #sna=len(stereoaudio)
    #print sna

    # save .wav file
    sf = wave.open("/tmp/meas_stereo.wav", 'w')
    sf.setparams((2, 2, 44100, 0, 'NONE', 'no compression'))
    sf.writeframesraw(stereoaudio)
    sf.close()


    dspout.write(stereoaudio)



def audio_in(len_sp,n_chan):
    #records len_sp bytes from oss device
    sys_resp=''
    for i in range(len_sp):
        sys_resp += dspin.read(16*n_chan*256)
    

    
    return sys_resp


def audio_run(n_chan,sig_meas,len_sp):

    #starts the audio output and recording
    

    if n_chan == 2:
        audio_stereo_out(sig_meas)
    else :
        audio_mono_out(sig_meas)

    rec = audio_in(len_sp,n_chan)
    
    return rec



def list_to_wav(sig_list):

    # converts list data to wav struct, to be usable for oss device

    output_signal= ''

    for j in range(len(sig_list)):
        output_signal += wave.struct.pack('<h', (sig_list[j]*29204))
    return output_signal


def extract_channels(n_chan):

    #extracts data out of both wavefiles into 4 arrays
    if n_chan == 2:
        fs,meas_array = scipy.io.wavfile.read("/tmp/meas_stereo.wav")
    else :
        fs,meas_array = scipy.io.wavfile.read("/tmp/meas_mono.wav")

    fs,resp_array = scipy.io.wavfile.read("/tmp/sysresp.wav")

    resp_l=numpy.zeros(len(resp_array))
    resp_r=numpy.zeros(len(resp_array))
    meas_l=numpy.zeros(len(meas_array))
    meas_r=numpy.zeros(len(meas_array))


    if n_chan == 2:
    
        for i in xrange(len(resp_array)):
            resp_l[i] =resp_array[i,0]
            resp_r[i] =resp_array[i,1]    

        for i in xrange(len(meas_array)):
            meas_l[i] =meas_array[i,0]
            meas_r[i] =meas_array[i,1]

    else:

        resp_l =resp_array
        meas_l =meas_array
	
    return (resp_l, resp_r, meas_l, meas_r)
    


def meas_run(fs,n_chan,sig_list,rt60):

    
    
    #length for recording in samples ((recordlength*samplerate)/1000)
    len_sp = int(((2*rt60*fs)/1000)/256)
    print len_sp
    #convert list to wav struct
    m_sig = list_to_wav(sig_list)

    #audio output and recording
    audio_open()
    audio_init(fs,n_chan)
    sys_rec = audio_run(n_chan,m_sig,len_sp)
    audio_close()

    # save .wav file
    sf = wave.open("/tmp/sysresp.wav", 'w')
    sf.setparams((2, 2, 44100, 0, 'NONE', 'no compression'))
    sf.writeframesraw(sys_rec)
    sf.close()

    resp_l, resp_r, meas_l, meas_r=extract_channels(n_chan)
    
  
    return (resp_l, resp_r, meas_l, meas_r)
    


