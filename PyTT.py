'''
PyTT - Python TimeTag software
Converted from C# by Catherine Holloway
Original TimeTag Explorer by Thomas Lehner
19/09/2013
'''

#here we will try to import the library... hopefully this works for both Windows and Linux
try: 
	import clr
	clr.AddReference("ttInterface.dll")
	clr.AddReference("System.Windows.Forms")

except:
	print('Could not load .Net dynamically loaded library. Ignore this if using Linux')

try:
	import ctypes
	TimeTag = cdll.LoadLibrary("libtimetag.so")
except:
	print('Could not load Shared object file. Ignore this if using Windows')
	
#load libraries
from TimeTag import Logic, TTInterface, Tag, Test, TimetagReader, UsbException;

from System.Windows.Forms import Application
#FormTimetagExplorer contains all of the windows forms designer information, as well as the event handlers and helper methods
from FormTimetagExplorer import FormTimetagExplorer;
mf = FormTimetagExplorer();
Application.Run(mf)