#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Begin of html head
print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>AMG.2025 - Audio Measurement System</title>'
print '</head>'

# Begin of html body
print '<body>'

# Welcome Message
print '<h2>Welcome to the AMG.2025 Measurement System</h2>'
print '<h3> Please choose your Measurement Method:</h3>'

# Begin of Formular
print '<form action="/cgi-bin/selection.py" method="post" target="_blank">'
print '<input type="radio" name="method" value="mls" /> Maximum Length Sequence <br />'
print '<input type="radio" name="method" value="ess" /> Exponential Sine Sweep <br/>'
print '<input type="radio" name="method" value="sds" /> Single/Dual Sine <br />'
print '<input type="submit" value="Submit" />'
print '</form>'
print '</body>'
print '</html>'
