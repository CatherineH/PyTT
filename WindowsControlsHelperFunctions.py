import clr
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application, AutoScaleMode, DialogResult, FormBorderStyle, FormWindowState, SizeGripStyle, ToolStrip, ToolStripItem, Padding, AnchorStyles, Form, Button, RichTextBox, Timer, CheckBox, SaveFileDialog, Label, TextBox, GroupBox, TabControl, TabPage, ToolTip, ToolStripMenuItem, MenuStrip, Screen, ToolStripItem, OpenFileDialog;
#this module defines a control for all of the buttons on the Logic tab 
from LogicChooser import *;
from TimeTaggerFunctions import *;

#copies the control
def DublicateControl(dest,source, i, offset):
	dest.Left = source.Left;
	dest.Size = source.Size;
	dest.Text = source.Text;
	dest.Top = source.Top + offset * i;
	dest.Name = source.Name+str(i);
	dest.TabIndex = source.TabIndex + i * 10;
	dest.Enabled = source.Enabled;
	return dest

def DublicateLogic(form):
	form.choosers.append(form.logicChooser1)
	#remove the placeholder controls created in __init__
	form.tabPageLogic.Controls.Remove(form.logicChooser1);
	form.tabPageLogic.Controls.Remove(form.labelPatternRate);
	#for each row in the logic choosers
	for i in range(0, form.MaxPattern):
		offset = 22;
		lc = LogicChooser();
		lc.Top = form.logicChooser1.Top + i * offset;
		lc.Left = form.logicChooser1.Left;
		lc.Visible = True;
		lc.TabIndex = form.logicChooser1.TabIndex + 20 * i;
		lc.Name = form.logicChooser1.Name + str(i);
		form.choosers.append(lc)
		#for each button for the channel selectors
		for j in range(0,form.MaxPattern):
			form.choosers[i].Controls[j].Top = form.logicChooser1.Top + i * offset;
			form.choosers[i].Controls[j].Left += form.logicChooser1.Left;
			form.tabPageLogic.Controls.Add(form.choosers[i].Controls[j]);
		l=Label();
		#form.DublicateControl(l, form.labelPatternRate, i, offset);
		DublicateControl(l, form.labelPatternRate, i, offset);
		l.TextAlign = form.labelPatternRate.TextAlign;
		form.patternRateLabels[1+i] = l;
		form.tabPageLogic.Controls.Add(l);
		
def DublicateInputs(form):
	offset = 18;
	#remove placeholder controls from designers 
	form.tabPageInputs.Controls.Remove(form.textBoxInputName);
	form.tabPageInputs.Controls.Remove(form.textBoxInputLevel);
	form.tabPageInputs.Controls.Remove(form.checkBoxInvers);
	form.tabPageInputs.Controls.Remove(form.buttonLed);
	for i in range(0,16):
		#channel name labels
		tb=TextBox();
		#form.DublicateControl(tb, form.textBoxInputName, i, offset);
		DublicateControl(tb, form.textBoxInputName, i, offset);
		tb.Text = "Input " + str(i+1);
		form.nameBoxes[i] = tb;
		form.tabPageInputs.Controls.Add(tb);
		#voltage inputs
		tb =TextBox();
		#form.DublicateControl(tb, form.textBoxInputLevel, i, offset);
		DublicateControl(tb, form.textBoxInputLevel, i, offset);
		form.voltageBoxes[i] = tb;
		form.tabPageInputs.Controls.Add(tb);
		#negative input level voltage checkboxes
		cb =CheckBox();
		#form.DublicateControl(cb, form.checkBoxInvers, i, offset);
		DublicateControl(cb, form.checkBoxInvers, i, offset);
		form.tabPageInputs.Controls.Add(cb);
		form.negativeBoxes[i] = cb;
		form.negativeBoxes[i].CheckedChanged +=form.CheckedChanged;
		#active indicators
		b =Button();
		#b = form.DublicateControl(b, form.buttonLed, i, offset);
		DublicateControl(b, form.buttonLed, i, offset);
		form.tabPageInputs.Controls.Add(b);
		form.ledButtons[i]= b;
	
def DublicateDelays(form):
	offset = 18;
	#remove placeholder controls
	form.tabPageDelay.Controls.Remove(form.textBoxDelay);
	form.tabPageDelay.Controls.Remove(form.labelDelayName);
	for i in range(0,16):
		tb = TextBox();
		#form.DublicateControl(tb, form.textBoxDelay, i, offset);
		DublicateControl(tb, form.textBoxDelay, i, offset);
		form.tabPageDelay.Controls.Add(tb);
		form.delayBoxes[i] = tb;
		lb = Label();
		#form.DublicateControl(lb, form.labelDelayName, i, offset);
		DublicateControl(lb, form.labelDelayName, i, offset);
		lb.Text = form.nameBoxes[i].Text;
		form.tabPageDelay.Controls.Add(lb);
		form.delayLabels[i] = lb;
	
def FindCheckBox(form, box, nameBoxes):
	for i in range(0,len(nameBoxes)):
		if (nameBoxes[i] == box):
			return i;

	return -1;
	

#this method controls the labels on the Connect and Calibrate buttons and allows controls to be enabled
def SwitchGui(form,p):
	form.tabControl1.Enabled = p
	form.labelErrors.Enabled = p
	form.buttonCalibrate.Enabled = p
	form.calibrateToolStripMenuItem.Enabled = p
	form.infoToolStripMenuItem1.Enabled = p
	#form.Text = InitialText
	if p:
	#	form.Text = Text+ " (Connected)"
		form.connectToolStripMenuItem.Text = "Disconnect"
		form.buttonConnect.Text = "Disconnect"
	else:
	#	form.Text = Text + " (Disconnected))"
		form.connectToolStripMenuItem.Text = "Connect"
		form.buttonConnect.Text = "Connect"
		form.calibrateToolStripMenuItem.Text= "Calibrate"
		form.buttonCalibrate.Text = "Calibrate"	