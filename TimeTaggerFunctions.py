
import clr
#import Thomas Lehner's drivers
clr.AddReference("ttInterface.dll")
clr.AddReference("UsbDll.dll")

#load timetag device libraries
from TimeTag import Logic, TTInterface, Tag, Test, TimetagReader, UsbException;
from Timetag import TimeTagDevice;
from UsbDll import Tag,TTHelper;


clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application, AutoScaleMode, DialogResult, FormBorderStyle, FormWindowState, SizeGripStyle, ToolStrip, ToolStripItem, Padding, AnchorStyles, Form, Button, RichTextBox, Timer, CheckBox, SaveFileDialog, Label, TextBox, GroupBox, TabControl, TabPage, ToolTip, ToolStripMenuItem, MenuStrip, Screen, ToolStripItem, OpenFileDialog;

#reads error messages from the timetagger and prints them on the screen
def ShowErrors(form):
	flags = form.ttInterface.ReadErrorFlags();
	if (flags == 0):
		form.labelErrors.Text = "Errors: (none)";
	else:
		form.labelErrors.Text = "Errors: " + form.ttInterface.GetErrorText(flags);

#Read which channels are active, then display the tags.
def DoReadTags(form):
	form.checkBoxLevelGateActive.Checked = form.ttInterface.LevelGateActive();
	DisplayTags(form);

#save the tags to a file
def DoSaveTags(form):
	SetButtonText(form);
	if form.conversionRunning:
		form.ShowRate();
		if not form.ttInterface.GetReader().ConversionMode:
			form.conversionRunning = False;
		form.richTextBox1.AppendText("Finished !!\n");

#display the tags in the textbox
def DisplayTags(form):
	#ReadTags needs a pointer to an array of bytes and an array of integers... do do this we generate a reference to the clr datatype
	channels = clr.Reference[Array[Byte]]();
	times =clr.Reference[Array[Int64]]();
	count = form.ttInterface.ReadTags(channels,times);
	if (count == 0):
		form.message = "No Tags\n";
	else:
		displayCount = min(count, 100);
		for i in range(0,displayCount):
			#because times is now a pointer and not an array, we have to subscript it using the "value"
			time = times.Value[i];
			timeDiff = time - form.OldTime;
			form.OldTime = time;
			bin = (int)(timeDiff*1e9/form.minimum_interval);
			if bin<form.max_bins and bin>0:
				bins_frequency[bin]+=1
			ns = timeDiff * form.ttInterface.GetResolution() * 1e9;
			if (i > 1):
				form.message += "Channel: " + str(channels.Value[i]) + "  TimeDiff [ns]: " + str(ns) + "\n";      
	form.richTextBox1.Text = form.message;
	#if form.tabControl1.SelectedTab == form.tabPageHistogram:
	#	form.update_histogram(0);

#put the status in the textbox
def ShowStatus(form):
	form.richTextBox1.Clear();
	try:
		form.richTextBox1.AppendText("FPGA Version:\t" + str(form.ttInterface.GetFpgaVersion()) + "\n");
		form.richTextBox1.AppendText("Resolution/ps:\t" + str(form.ttInterface.GetResolution() * 1e12) + "\n");
		form.richTextBox1.AppendText("Errors:\t\t" + form.ttInterface.GetErrorText(form.ttInterface.ReadErrorFlags()) + "\n\n");
	except:
		print("Could not read status")
#changes the file writing button text
def SetButtonText(form):
	if not form.ttInterface.GetReader().FileSaveMode and not form.ttInterface.GetReader().ConversionMode:
		form.buttonSaveStart.Text = "Start";
	elif form.ttInterface.GetReader().FileSaveMode:
		form.buttonSaveStart.Text = "Stop";
	elif form.ttInterface.GetReader().ConversionMode:
		form.buttonSaveStart.Text = "Converting.....";

#calculates the timetag rates for the file writing tab, calculates the percentage that were caught
def ShowRate(form):
	diff = DateTime.Now - form.startTime;
	msecs = diff.TotalMilliseconds;
	tags = form.ttInterface.GetReader().SavedTags;
	rate = (tags / msecs);
	form.labelSize.Text = "ktags:" + (tags/1000.0).ToString("0.###");
	form.labelRate.Text = "ktags/sec:" + rate.ToString("0.###");
	percent = 0;
	if (form.tempTags > 0):
		percent = int(100 * tags / form.tempTags);
	else:
		percent = 100;
	if not form.ttInterface.GetReader().ConversionMode:
		percent = 100;
	form.labelPercent.Text = "percent: " + str(percent);


