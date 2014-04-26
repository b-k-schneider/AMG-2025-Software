#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import os, sys
lib_path = os.path.abspath('scripts/')
sys.path.append(lib_path)

import meas_calls
import datetime

d=datetime.date.today()
d_string=d.isoformat()

fname_ir_l = "mls-ir-l-" + d_string
fname_fft_l = "mls-fft-l-" + d_string
fname_ir_r = "mls-ir-r-" + d_string
fname_fft_r = "mls-fft-r-" + d_string
fname_zip = "mls-measurement" + d_string

# Clearing the tmp directory
meas_calls.clear_tmp()

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
if form.getvalue('fs'):
   fs = int(form.getvalue('fs'))
else:
   fs = 44100

if form.getvalue('n_chan'):
   n_chan = int(form.getvalue('n_chan'))
else:
   n_chan = 2

if form.getvalue('n_meas'):
   n_meas = int(form.getvalue('n_meas'))
else:
   n_meas = 2

if form.getvalue('rt60'):
   rt60 = int(form.getvalue('rt60'))
else:
   rt60 = 100

if form.getvalue('avg_fft'):
    if form.getvalue('avg_fft')=="ON":
        avg_fft =int(1)
    elif form.getvalue('avg_fft')=="OFF":
        avg_fft =int(0)
    else:
        avg_fft =int(0)
else:
    avg_fft=int(0)

# Begin of html head
print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>AMG.2025 - Maximum Length Sequence Measurement</title>'
print '</head>'

# Begin of html body
print '<body>'

# Welcome Message
print '<h2> Maximum Length Sequence Measurement </h2>'

ir_l, ir_r = meas_calls.measure_mls(fs,rt60,n_meas,n_chan)
# Left Channel
sys_fft_l, freq_l = meas_calls.compute_fft(fs,ir_l)
meas_calls.plot_save_ir(fs,ir_l,fname_ir_l)
meas_calls.plot_save_fft(freq_l,sys_fft_l,fname_fft_l,avg_fft)

if n_chan>1:
# Right Channel
    sys_fft_r, freq_r = meas_calls.compute_fft(fs,ir_r)
    meas_calls.plot_save_ir(fs,ir_r,fname_ir_r)
    meas_calls.plot_save_fft(freq_r,sys_fft_r,fname_fft_r,avg_fft)

meas_calls.make_zip(fname_zip)    
print '<h3>Left Channel IR</h3>'
print '<img type="image" src="/tmp/amg2025/%s.jpg" alt="Left Channel IR">' %fname_ir_l
print '<h3>Left Channel FFT</h3>'
print '<img src="/tmp/amg2025/%s.jpg" alt="Left Channel FFT">' %fname_fft_l

if n_chan>1:
    print '<h3>Right Channel IR</h3>'
    print '<img src="/tmp/amg2025/%s.jpg" alt="Right Channel IR">' %fname_ir_r
    print '<h3>Right Channel FFT</h3>'
    print '<img src="/tmp/amg2025/%s.jpg" alt="Right Channel FFT">' %fname_fft_r

# Zipfile Download Button

print '<form method="get" action="/tmp/amg2025/%s.zip">' %fname_zip
print '<button type="submit">Download</button>'
print '</form>'

print '</body>'
print '</html>'
