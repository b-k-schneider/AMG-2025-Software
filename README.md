AMG-2025-Software
=================

Repository for AMG-2025 Project

Sources for Python 2.7
now Based on pyaudio v19
needed Modules:
scipy
numpy
matplotlib
pyaudio


add symbolic link in your directory where your python cgiserver lives to tmp:
$: ln -s /tmp tmp

cgi-server.py and also all scripts in the cgi-bin folder must be marked as execute
$: chmod +x cgi-server.py
in cgi-bin/:
$: chmod +x  amg_2025.py ess_full.py mls_full.py sds_full.py selection.py 