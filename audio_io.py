"""
Library for Audio I/O via OSS (/dev/dsp)
needs native OSS or emulated via aoss or padsp
needed parameters: fs, res, n_chan, sig_meas
"""

import os, sys, audioop, ossaudiodev, wave


# Open 2 file handles
dspout = ossaudiodev.open('/dev/dsp', 'w')
dspin = ossaudiodev.open('/dev/dsp', 'r')


def audio_init(fs,n_chan):


    # Configure OSS Device Resolution, Mono/Stereo, Samplerate, non-Blocking Mode
    fmt_o_err = dspout.setfmt(ossaudiodev.AFMT_S16_BE)
    fmt_i_err = dspin.setfmt(ossaudiodev.AFMT_S16_BE)

    ch_o_err = dspout.channels(n_chan)
    ch_i_err = dspin.channels(n_chan)

    fs_o_err = dspout.speed(fs)
    fs_i_err = dspin.speed(fs)

    #TODO error catching, maybe buffer setting?
    

def audio_mono_out(sig_meas):
    dspout.write(sig_meas)

def audio_stereo_out(sig_meas):
    stereoaudio = audioop.tostereo(sig_meas, 2, 1, 1)
    dspout.write(stereoaudio)

def audio_in():
    sys_resp = dspin.read(512)


def audio_run(n_chan,sig_meas):
    if n_chan == 2:
        audio_stereo_out(sig_meas)
    else :
        audio_mono_out(sig_meas)
    
    audio_in()


def list_to_wav(sig_list):
    output_signal= ''
    for j in range(len(sig_list)):
        output_signal += wave.struct.pack('h', sig_list[j])
    return output_signal



def meas_run(fs,n_chan,sig_list):

    m_sig=list_to_wav(sig_list)
    audio_init(fs,n_chan)
    audio_run(n_chan,m_sig)

