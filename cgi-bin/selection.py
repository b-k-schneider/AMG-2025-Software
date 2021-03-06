#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
if form.getvalue('method'):
   method = form.getvalue('method')
else:
   method = "Not set"

if method=="mls":
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
    print '<h3> Please Input your Measurement Parameters:</h3>'

    # Begin of Formular
    print '<form action="/cgi-bin/mls_full.py" method="post" target="_blank">' 
    print 'Sample Rate:         <input type="text" name="fs" value="44100" >  <br />'
    print 'No. of Channels:     <input type="text" name="n_chan" value="2" >  <br />'
    print 'No. of Measurements: <input type="text" name="n_meas" value="1" >  <br />'
    print 'Estimated RT60:      <input type="text" name="rt60" value="100" >  <br />'
    print '<input type="checkbox" name="avg_fft" value="ON" /> Average FFT <br />'
    print '<input type="submit" value="Submit" />'
    print '</form>'
    print '</body>'
    print '</html>'

elif method=="ess":

    # Begin of html head
    print "Content-type:text/html\r\n\r\n"
    print '<html>'
    print '<head>'
    print '<title>AMG.2025 - Audio Measurement System</title>'
    print '</head>'

    # Begin of html body
    print '<body>'

    # Welcome Message
    print '<h2>Exponential Sine Sweep Measurement</h2>'
    print '<h3> Please Input your Measurement Parameters:</h3>'

    # Begin of Formular
    print '<form action="/cgi-bin/ess_full.py" method="post" target="_blank">' 
    print 'Sample Rate:         <input type="text" name="fs" value="44100" >  <br />'
    print 'No. of Channels:     <input type="text" name="n_chan" value="2" >  <br />'
    print 'No. of Measurements: <input type="text" name="n_meas" value="1" >  <br />'
    print 'Start Frequency:     <input type="text" name="f_0" value="20" >  <br />'
    print 'Stop Frequency:      <input type="text" name="f_1" value="22000" >  <br />'
    print 'Sweep Time:          <input type="text" name="t_sweep" value="5" >  <br />'
    print '<input type="checkbox" name="avg_fft" value="ON" /> Average FFT <br />'
    print '<input type="submit" value="Submit" />'
    print '</form>'
    print '</body>'
    print '</html>'

elif method=="sds":

    # Begin of html head
    print "Content-type:text/html\r\n\r\n"
    print '<html>'
    print '<head>'
    print '<title>AMG.2025 - Single / Dual Sine Measurement </title>'
    print '</head>'

    # Begin of html body
    print '<body>'

    # Welcome Message
    print '<h2>Single / Dual Sine Measurement</h2>'
    print '<h3> Please Input your Measurement Parameters:</h3>'

    # Begin of Formular
    print '<form action="/cgi-bin/sds_full.py" method="post" target="_blank">' 
    print 'Sample Rate:         <input type="text" name="fs" value="44100" >  <br />'
    print 'No. of Channels:     <input type="text" name="n_chan" value="2" >  <br />'
    print 'Frequency One:       <input type="text" name="f_0" value="440" >  <br />'
    print 'Frequency Two (opt): <input type="text" name="f_1" value="1000" >  <br />'
    print 'Length: <input type="text" name="t_sweep" value="5" >  <br />'
    print '<input type="checkbox" name="avg_fft" value="ON" /> Average FFT <br />'
    print '<input type="submit" value="Submit" />'
    print '</form>'
    print '</body>'
    print '</html>'
