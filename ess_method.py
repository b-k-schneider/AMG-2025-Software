"""
Library for the ESS measuring method
Creates the ESS and calculates the Impulse Response from the System Response
required Parameters: fs, rt60, n_meas, f0, f1, t_sw
"""

import numpy, scipy
from scipy.signal import chirp

def generate_ess(fs, f0, f1, t_sw):

    #compute Sweep time in samples

    n_samp = int(fs * t_sw)

    #generate time vector
    t_vec = numpy.linspace(0, t_sw, n_samp)

    #generate sine sweep
    m_sig = chirp(t_vec, f0, t_sw , f1, method='logarithmic')
    
    m_sig_list = m_sig.tolist()

    return m_sig_list


def compute_ir(n_chan, index):

    import audio_io
    import scipy.signal
    import scipy.fftpack
    # if mono, only leftchannels are used

    
    #Extracting Channels
    resp_l, resp_r, meas_l, meas_r=audio_io.extract_channels(n_chan,index)
    
    # calculating the inverse filter
        
    meas_fft_l = scipy.fftpack.fft(meas_l)
    meas_fft_l= meas_fft_l/meas_fft_l.size
    inv_meas_l = 1/meas_fft_l
    inv_filter_l =scipy.fftpack.ifft(inv_meas_l)

    meas_fft_r = scipy.fftpack.fft(meas_r)
    meas_fft_r= meas_fft_r/meas_fft_r.size
    inv_meas_r = 1/meas_fft_r
    inv_filter_r =scipy.fftpack.ifft(inv_meas_r)    

    #convolve system response with the inverse filter
    ir_l = scipy.signal.fftconvolve(resp_l,inv_filter_l)    
    ir_r = scipy.signal.fftconvolve(resp_r,inv_filter_r) 
    
    return (ir_l, ir_r)

    

    
