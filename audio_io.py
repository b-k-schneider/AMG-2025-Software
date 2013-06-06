"""
Library for Audio I/O via OSS (/dev/dsp)
needs native OSS or emulated via aoss or padsp
needed parameters: fs, res, n_chan, sig_meas
"""

import os, sys, audioop, ossaudiodev, wave, numpy

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
    fmt_o_err = dspout.setfmt(ossaudiodev.AFMT_S16_BE)
    fmt_i_err = dspin.setfmt(ossaudiodev.AFMT_S16_BE)

    ch_o_err = dspout.channels(n_chan)
    ch_i_err = dspin.channels(n_chan)

    fs_o_err = dspout.speed(fs)
    fs_i_err = dspin.speed(fs)
    

def audio_mono_out(sig_meas):
    dspout.write(sig_meas)

def audio_stereo_out(sig_meas):

    #converts the signal to a mono signal
    stereoaudio = audioop.tostereo(sig_meas, 2, 1, 1)
    dspout.write(stereoaudio)

def audio_in(len_sp):
    #records len_sp bytes from oss device
    sys_resp = dspin.read(len_sp)
    return sys_resp


def audio_run(n_chan,sig_meas,len_sp):

    #starts the audio output and recording
    if n_chan == 2:
        audio_stereo_out(sig_meas)
    else :
        audio_mono_out(sig_meas)
    
    rec = audio_in(len_sp)
    return rec

def list_to_wav(sig_list):
    # converts list data to wav struct, to be usable for oss device
    output_signal= ''
    for j in range(len(sig_list)):
        output_signal += wave.struct.pack('h', sig_list[j])
    return output_signal



def meas_run(fs,n_chan,sig_list,len_r):

    #length for recording in bytes (recordlength/samplerate * 16bit * channels)
    len_sp = int(((len_r*fs)/1000)*16*n_chan)
    print len_sp
    #convert list to wav struct
    m_sig = list_to_wav(sig_list)

    #audio output and recording
    audio_open()
    audio_init(fs,n_chan)
    sys_rec = audio_run(n_chan,m_sig,len_sp)
    audio_close()

    return sys_rec
    

