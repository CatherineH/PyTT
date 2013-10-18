

import clr

#Importing things from windows .Net assemblies

clr.AddReference("System")
clr.AddReference("System.Core")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.ComponentModel")
clr.AddReference("System.Drawing")
#import Thomas Lehner's drivers
clr.AddReference("ttInterface.dll")
clr.AddReference("UsbDll.dll")
clr.AddReference("ZedGraph.dll")

#load timetag device libraries
from TimeTag import Logic, TTInterface, Tag, Test, TimetagReader, UsbException;
from Timetag import TimeTagDevice;
from UsbDll import Tag,TTHelper;
#load the zedgraph library for histogram graph
from ZedGraph import ZedGraphControl;
#this module is used for importing saved parameters
from ParaHandling import ParaHandling;
#this module defines a control for all of the buttons on the Logic tab 
from LogicChooser import *;
from WindowsControlsHelperFunctions import *
from TimeTaggerFunctions import *
#Now for all the windows things we'll need
from System import DateTime, Array, Byte;
from System.Runtime.CompilerServices import StrongBox;
from System.ComponentModel import Container;
from System.Drawing import ContentAlignment, Font, Point, Size, FontStyle, GraphicsUnit;
from System.Windows.Forms import Application, AutoScaleMode, DialogResult, FormBorderStyle, FormWindowState, SizeGripStyle, ToolStrip, ToolStripItem, Padding, AnchorStyles, Form, Button, RichTextBox, Timer, CheckBox, SaveFileDialog, Label, TextBox, GroupBox, TabControl, TabPage, ToolTip, ToolStripMenuItem, MenuStrip, Screen, ToolStripItem, OpenFileDialog;

class FormTimetagExplorer(Form):
	
	def __init__(self):
		
		self.ParaFileName= "standard.timetag";
		#ttInterface is used for most of the communication with the timetagger, Logic is used for communication with the device's logic. They are both null until "Connect" is clicked
		self.ttInterface = None;
		self.Logic = None;
		self.inversionMask = 0;
		self.choosers = [];
		self.ModeList = [];
		self.Labview = False;
		#message that appears in the textbox
		self.message = "";
		#maxPattern defines the number of channels on the timetag unit
		self.MaxPattern = 16;
		
		#several tabs have duplicate controls, which are stored in lists
		self.patternRateLabels = [1]*(self.MaxPattern+1);
		self.nameBoxes = [1]*(self.MaxPattern+1);
		self.voltageBoxes = [1]*(self.MaxPattern+1);
		self.negativeBoxes = [1]*(self.MaxPattern+1);
		self.ledButtons = [1]*(self.MaxPattern+1);
		self.delayBoxes = [1]*(self.MaxPattern+1);
		self.delayLabels = [1]*(self.MaxPattern+1);	
		#initialize all of the controls
		self.logicChooser1 = LogicChooser();
		self.components = Container();
		self.buttonConnect = Button();
		self.buttonLabview = Button();
		self.richTextBox1 =  RichTextBox();
		#every time Timer1 ticks, the timetags are read
		self.timer1 =  Timer(self.components);
		#every time timerLogic ticks, the counts are read off of the logic. It should only be enabled when checkBoxUseLogic is true
		self.timerLogic =  Timer(self.components);
		#every time timerButton ticks, the timetag parameters are checked, and the channel indicators on the inputs tab are updated		
		self.timerButtons =  Timer(self.components);
		
		self.checkBoxReadTags =  CheckBox();
		self.saveFileDialog1 =  SaveFileDialog();
		self.saveFileDialog2 =  SaveFileDialog();
		self.checkBoxEdgeGate =  CheckBox();
		self.labelErrors =  Label();
		self.textBoxGateWidth =  TextBox();
		self.label3 =  Label();
		self.textBoxGatePosition =  TextBox();
		self.groupBoxEdgeGate =  GroupBox();
		self.label14 =  Label();
		self.buttonCalibrate =  Button();
		self.checkBoxUseLevelGate =  CheckBox();
		self.checkBoxLevelGateActive =  CheckBox();
		self.checkBoxUse10MHz =  CheckBox();
		self.tabControl1 =  TabControl();
		self.tabPageTimeTag =  TabPage();
		self.tabPageSaveTags =  TabPage();
		self.tabPageHistogram =  TabPage();
		self.checkBoxSaveTags =  CheckBox();
		self.labelSize =  Label();
		self.label1 =  Label();
		self.rawFileName =  TextBox();
		self.buttonSaveStart =  Button();
		self.labelPercent =  Label();
		self.button1 =  Button();
		self.labelRate =  Label();
		self.label2 =  Label();
		self.button2 =  Button();
		self.outputFileName =  TextBox();
		self.tabPageInputs =  TabPage();
		self.label10 =  Label();
		self.label9 =  Label();
		self.label8 =  Label();
		self.label7 =  Label();
		self.buttonLed =  Button();
		self.checkBoxInvers =  CheckBox();
		self.textBoxInputLevel =  TextBox();
		self.textBoxInputName =  TextBox();
		self.tabPageDelay =  TabPage();
		self.textBox4 =  TextBox();
		self.label13 =  Label();
		self.label12 =  Label();
		self.textBoxDelay =  TextBox();
		self.labelDelayName =  Label();
		self.tabPageLogic =  TabPage();
		self.label5 =  Label();
		self.label6 =  Label();
		self.textBoxWindow =  TextBox();
		self.textBoxCycle =  TextBox();
		self.label11 =  Label();
		self.labelPatternRate =  Label();
		self.checkBoxUseLogic =  CheckBox();
		self.tabPageDebug =  TabPage();
		self.buttonReadUsb =  Button();
		self.toolTip1 =  ToolTip(self.components);
		self.menuStrip1 =  MenuStrip();
		self.fileToolStripMenuItem =  ToolStripMenuItem();
		self.openToolStripMenuItem =  ToolStripMenuItem();
		self.saveToolStripMenuItem =  ToolStripMenuItem();
		self.saveasToolStripMenuItem =  ToolStripMenuItem();
		self.deviceToolStripMenuItem =  ToolStripMenuItem();
		self.connectToolStripMenuItem =  ToolStripMenuItem();
		self.calibrateToolStripMenuItem =  ToolStripMenuItem();
		self.infoToolStripMenuItem1 =  ToolStripMenuItem();
		self.openFileDialog1 =  OpenFileDialog();
		self.saveFileDialog3 =  SaveFileDialog();
		self.groupBoxEdgeGate.SuspendLayout();
		self.tabControl1.SuspendLayout();
		self.tabPageTimeTag.SuspendLayout();
		self.tabPageSaveTags.SuspendLayout();
		self.tabPageHistogram.SuspendLayout();
		self.tabPageInputs.SuspendLayout();
		self.tabPageDelay.SuspendLayout();
		self.tabPageLogic.SuspendLayout();
		self.tabPageDebug.SuspendLayout();
		self.menuStrip1.SuspendLayout();
		self.SuspendLayout();
		self.histoGraph = ZedGraphControl();
		
		#histogram calculation data... right now I"m just looking at a basic way of doing it.
		self.minimum_interval = 0.156;
		self.max_bins = 100;
		self.bins_frequency =[0]*self.max_bins;
		#self.myBar;
				
		#now for all of the VisualStudio generated designer code
		    # 
		    # buttonConnect
		    # 
		self.buttonConnect.Location =  Point(18, 33);
		self.buttonConnect.Name = "buttonConnect";
		self.buttonConnect.Size =  Size(75, 23);		
		self.buttonConnect.TabIndex = 0;
		self.buttonConnect.Text = "Connect";
		self.buttonConnect.UseVisualStyleBackColor = True;
		self.buttonConnect.Click +=  self.buttonConnect_Click;
				    # 
		    # buttonConnect
		    # 
		self.buttonLabview.Location =  Point(308, 33);
		self.buttonLabview.Name = "buttonLabview";
		self.buttonLabview.Size =  Size(75, 23);		
		self.buttonLabview.TabIndex = 0;
		self.buttonLabview.Text = "Labview";
		self.buttonLabview.UseVisualStyleBackColor = True;
		self.buttonLabview.Click +=  self.buttonLabview_Click;
		    # 
		    # richTextBox1
		    # 
		self.richTextBox1.Anchor = (AnchorStyles.Left | AnchorStyles.Right |
		          AnchorStyles.Bottom | AnchorStyles.Top);
		self.richTextBox1.Font =  Font("Courier ", 8.25, FontStyle.Regular, GraphicsUnit.Point, 0);
		self.richTextBox1.Location =  Point(510, 84);
		self.richTextBox1.Name = "richTextBox1";
		self.richTextBox1.Size =  Size(359, 350);
		self.richTextBox1.TabIndex = 2;
		self.richTextBox1.Text = "";
		    # 
		    # timer1
		    # 
		self.timer1.Tick +=  self.timer1_Tick;
		    # 
		    # checkBoxReadTags
		    # 
		self.checkBoxReadTags.AutoSize = True;
		self.checkBoxReadTags.Location =  Point(16, 17);
		self.checkBoxReadTags.Name = "checkBoxReadTags";
		self.checkBoxReadTags.Size =  Size(76, 17);
		self.checkBoxReadTags.TabIndex = 3;
		self.checkBoxReadTags.Text = "ReadTags";
		self.checkBoxReadTags.UseVisualStyleBackColor = True;
		self.checkBoxReadTags.CheckedChanged +=  self.checkBoxReadTags_CheckedChanged;
		    # 
		    # checkBoxEdgeGate
		    # 
		self.checkBoxEdgeGate.AutoSize = True;
		self.checkBoxEdgeGate.Enabled = False;
		self.checkBoxEdgeGate.Location =  Point(16, 108);
		self.checkBoxEdgeGate.Name = "checkBoxEdgeGate";
		self.checkBoxEdgeGate.Size =  Size(93, 17);
		self.checkBoxEdgeGate.TabIndex = 13;
		self.checkBoxEdgeGate.Text = "UseEdgeGate";
		self.checkBoxEdgeGate.UseVisualStyleBackColor = True;
		self.checkBoxEdgeGate.CheckedChanged += self.TransmitValue;
		    # 
		    # labelErrors
		    # 
		self.labelErrors.AutoSize = True;
		self.labelErrors.Font =  Font("Microsoft Sans Serif", 8.25, FontStyle.Regular, GraphicsUnit.Point, 0);
		self.labelErrors.Location =  Point(194, 38);
		self.labelErrors.Name = "labelErrors";
		self.labelErrors.Size =  Size(37, 13);
		self.labelErrors.TabIndex = 14;
		self.labelErrors.Text = "Errors:";
		    # 
		    # textBoxGateWidth
		    # 
		self.textBoxGateWidth.Location =  Point(132, 15);
		self.textBoxGateWidth.Name = "textBoxGateWidth";
		self.textBoxGateWidth.Size =  Size(100, 20);
		self.textBoxGateWidth.TabIndex = 15;
		self.textBoxGateWidth.Text = "100";
		    # 
		    # label3
		    # 
		self.label3.AutoSize = True;
		self.label3.Location =  Point(6, 44);
		self.label3.Name = "label3";
		#self.label3.Size =  Size(83, 13);
		self.label3.Size =  Size(160, 20);
		
		self.label3.TabIndex = 14;
		self.label3.Text = "GatePosition/ns";
		    # 
		    # textBoxGatePosition
		    # 
		self.textBoxGatePosition.Location =  Point(132, 41);
		self.textBoxGatePosition.Name = "textBoxGatePosition";
		self.textBoxGatePosition.Size =  Size(100, 20);
		self.textBoxGatePosition.TabIndex = 15;
		self.textBoxGatePosition.Text = "0";
		    # 
		    # groupBoxEdgeGate
		    # 
		self.groupBoxEdgeGate.Controls.Add(self.textBoxGateWidth);
		self.groupBoxEdgeGate.Controls.Add(self.textBoxGatePosition);
		self.groupBoxEdgeGate.Controls.Add(self.label14);
		self.groupBoxEdgeGate.Controls.Add(self.label3);
		self.groupBoxEdgeGate.Enabled = False;
		self.groupBoxEdgeGate.Location =  Point(52, 131);
		self.groupBoxEdgeGate.Name = "groupBoxEdgeGate";
		self.groupBoxEdgeGate.Size =  Size(238, 78);
		self.groupBoxEdgeGate.TabIndex = 16;
		self.groupBoxEdgeGate.TabStop = False;
		self.groupBoxEdgeGate.EnabledChanged +=  self.groupBoxEdgeGate_EnabledChanged;
		    # 
		    # label14
		    # 
		self.label14.AutoSize = True;
		self.label14.Location =  Point(6, 18);
		self.label14.Name = "label14";
		self.label14.Size =  Size(74, 13);
		self.label14.TabIndex = 14;
		self.label14.Text = "GateWidth/ns";
		    # 
		    # buttonCalibrate
		    # 
		self.buttonCalibrate.Location =  Point(106, 33);
		self.buttonCalibrate.Name = "buttonCalibrate";
		self.buttonCalibrate.Size =  Size(75, 23);
		self.buttonCalibrate.TabIndex = 0;
		self.buttonCalibrate.Text = "Calibrate";
		self.buttonCalibrate.UseVisualStyleBackColor = True;
		self.buttonCalibrate.Click +=  self.buttonCalibrate_Click;
		    # 
		    # checkBoxUseLevelGate
		    # 
		self.checkBoxUseLevelGate.AutoSize = True;
		self.checkBoxUseLevelGate.Enabled = False;
		self.checkBoxUseLevelGate.Location =  Point(16, 83);
		self.checkBoxUseLevelGate.Name = "checkBoxUseLevelGate";
		self.checkBoxUseLevelGate.Size =  Size(94, 17);
		self.checkBoxUseLevelGate.TabIndex = 13;
		self.checkBoxUseLevelGate.Text = "UseLevelGate";
		self.checkBoxUseLevelGate.UseVisualStyleBackColor = True;
		    # 
		    # checkBoxLevelGateActive
		    # 
		self.checkBoxLevelGateActive.AutoSize = True;
		self.checkBoxLevelGateActive.Enabled = False;
		self.checkBoxLevelGateActive.Location =  Point(184, 83);
		self.checkBoxLevelGateActive.Name = "checkBoxLevelGateActive";
		self.checkBoxLevelGateActive.Size =  Size(105, 17);
		self.checkBoxLevelGateActive.TabIndex = 13;
		self.checkBoxLevelGateActive.Text = "LevelGateActive";
		self.checkBoxLevelGateActive.UseVisualStyleBackColor = True;
		    # 
		    # checkBoxUse10MHz
		    # 
		self.checkBoxUse10MHz.AutoSize = True;
		self.checkBoxUse10MHz.Enabled = False;
		self.checkBoxUse10MHz.Location =  Point(16, 60);
		self.checkBoxUse10MHz.Name = "checkBoxUse10MHz";
		self.checkBoxUse10MHz.Size =  Size(79, 17);
		self.checkBoxUse10MHz.TabIndex = 13;
		self.checkBoxUse10MHz.Text = "Use10MHz";
		self.checkBoxUse10MHz.UseVisualStyleBackColor = True;
		    # 
		    # tabControl1
		    # 
		self.tabControl1.Anchor = (((AnchorStyles.Top | AnchorStyles.Bottom)| AnchorStyles.Left));
		self.tabControl1.Controls.Add(self.tabPageTimeTag);
		self.tabControl1.Controls.Add(self.tabPageSaveTags);
		self.tabControl1.Controls.Add(self.tabPageHistogram);
		self.tabControl1.Controls.Add(self.tabPageInputs);
		self.tabControl1.Controls.Add(self.tabPageDelay);
		self.tabControl1.Controls.Add(self.tabPageLogic);
		self.tabControl1.Controls.Add(self.tabPageDebug);
		self.tabControl1.Location =  Point(14, 62);
		self.tabControl1.Name = "tabControl1";
		self.tabControl1.SelectedIndex = 0;
		self.tabControl1.Size =  Size(483, 374);
		self.tabControl1.TabIndex = 17;
		    # 
		    # tabPageTimeTag
		    # 
		self.tabPageTimeTag.Controls.Add(self.checkBoxEdgeGate);
		self.tabPageTimeTag.Controls.Add(self.checkBoxUse10MHz);
		self.tabPageTimeTag.Controls.Add(self.groupBoxEdgeGate);
		self.tabPageTimeTag.Controls.Add(self.checkBoxReadTags);
		self.tabPageTimeTag.Controls.Add(self.checkBoxLevelGateActive);
		self.tabPageTimeTag.Controls.Add(self.checkBoxUseLevelGate);
		self.tabPageTimeTag.Location =  Point(4, 22);
		self.tabPageTimeTag.Name = "tabPageTimeTag";
		self.tabPageTimeTag.Padding =  Padding(3);
		self.tabPageTimeTag.Size =  Size(475, 348);
		self.tabPageTimeTag.TabIndex = 0;
		self.tabPageTimeTag.Text = "TimeTag";
		self.tabPageTimeTag.UseVisualStyleBackColor = True;
		    # 
		    # tabPageSaveTags
		    # 
		self.tabPageSaveTags.Controls.Add(self.checkBoxSaveTags);
		self.tabPageSaveTags.Controls.Add(self.labelSize);
		self.tabPageSaveTags.Controls.Add(self.label1);
		self.tabPageSaveTags.Controls.Add(self.rawFileName);
		self.tabPageSaveTags.Controls.Add(self.buttonSaveStart);
		self.tabPageSaveTags.Controls.Add(self.labelPercent);
		self.tabPageSaveTags.Controls.Add(self.button1);
		self.tabPageSaveTags.Controls.Add(self.labelRate);
		self.tabPageSaveTags.Controls.Add(self.label2);
		self.tabPageSaveTags.Controls.Add(self.button2);
		self.tabPageSaveTags.Controls.Add(self.outputFileName);
		self.tabPageSaveTags.Location =  Point(4, 22);
		self.tabPageSaveTags.Name = "tabPageSaveTags";
		self.tabPageSaveTags.Size =  Size(475, 348);
		self.tabPageSaveTags.TabIndex = 4;
		self.tabPageSaveTags.Text = "SaveTags";
		self.tabPageSaveTags.UseVisualStyleBackColor = True;
						    # 
		    # tabPageHistogram
		    # 
		self.tabPageHistogram.Controls.Add(self.histoGraph)
		self.tabPageHistogram.Location =  Point(4, 22);
		self.tabPageHistogram.Name = "tabPageHistogram";
		self.tabPageHistogram.Size =  Size(475, 348);
		self.tabPageHistogram.TabIndex = 5;
		self.tabPageHistogram.Text = "Histogram";
		self.tabPageHistogram.UseVisualStyleBackColor = True;
		    # 
		    # checkBoxSaveTags
		    # 
		self.checkBoxSaveTags.AutoSize = True;
		self.checkBoxSaveTags.Location =  Point(28, 18);
		self.checkBoxSaveTags.Name = "checkBoxSaveTags";
		self.checkBoxSaveTags.Size =  Size(80, 17);
		self.checkBoxSaveTags.TabIndex = 13;
		self.checkBoxSaveTags.Text = "SaveToFile";
		self.checkBoxSaveTags.UseVisualStyleBackColor = True;
		self.checkBoxSaveTags.CheckedChanged +=  self.checkBoxSaveTags_CheckedChanged;
		    # 
		    # labelSize
		    # 
		self.labelSize.AutoSize = True;
		self.labelSize.Enabled = False;
		self.labelSize.Location =  Point(47, 177);
		self.labelSize.Name = "labelSize";
		self.labelSize.Size =  Size(31, 13);
		self.labelSize.TabIndex = 14;
		self.labelSize.Text = "Tags";
		    # 
		    # label1
		    # 
		self.label1.AutoSize = True;
		self.label1.Enabled = False;
		self.label1.Location =  Point(47, 51);
		self.label1.Name = "label1";
		self.label1.Size =  Size(50, 13);
		self.label1.TabIndex = 15;
		self.label1.Text = "TempFile";
		    # 
		    # rawFileName
		    # 
		self.rawFileName.Enabled = False;
		self.rawFileName.Location =  Point(122, 48);
		self.rawFileName.Name = "rawFileName";
		self.rawFileName.Size =  Size(177, 20);
		self.rawFileName.TabIndex = 16;
		self.rawFileName.Text = "raw.dat";
		    # 
		    # buttonSaveStart
		    # 
		self.buttonSaveStart.Enabled = False;
		self.buttonSaveStart.Location =  Point(50, 129);
		self.buttonSaveStart.Name = "buttonSaveStart";
		self.buttonSaveStart.Size =  Size(75, 23);
		self.buttonSaveStart.TabIndex = 0;
		self.buttonSaveStart.Text = "Start";
		self.buttonSaveStart.UseVisualStyleBackColor = True;
		self.buttonSaveStart.Click +=  self.buttonSaveStart_Click;
		    # 
		    # labelPercent
		    # 
		self.labelPercent.AutoSize = True;
		self.labelPercent.Enabled = False;
		self.labelPercent.Location =  Point(47, 227);
		self.labelPercent.Name = "labelPercent";
		self.labelPercent.Size =  Size(44, 13);
		self.labelPercent.TabIndex = 21;
		self.labelPercent.Text = "Percent";
		    # 
		    # button1
		    # 
		self.button1.Enabled = False;
		self.button1.Location =  Point(318, 46);
		self.button1.Name = "button1";
		self.button1.Size =  Size(39, 23);
		self.button1.TabIndex = 17;
		self.button1.Text = "...";
		self.button1.UseVisualStyleBackColor = True;
		self.button1.Click +=  self.button1_Click;
		    # 
		    # labelRate
		    # 
		self.labelRate.AutoSize = True;
		self.labelRate.Enabled = False;
		self.labelRate.Location =  Point(48, 203);
		self.labelRate.Name = "labelRate";
		self.labelRate.Size =  Size(30, 13);
		self.labelRate.TabIndex = 22;
		self.labelRate.Text = "Rate";
		    # 
		    # label2
		    # 
		self.label2.AutoSize = True;
		self.label2.Enabled = False;
		self.label2.Location =  Point(47, 75);
		self.label2.Name = "label2";
		self.label2.Size =  Size(55, 13);
		self.label2.TabIndex = 18;
		self.label2.Text = "OutputFile";
		    # 
		    # button2
		    # 
		self.button2.Enabled = False;
		self.button2.Location =  Point(318, 74);
		self.button2.Name = "button2";
		self.button2.Size =  Size(39, 23);
		self.button2.TabIndex = 20;
		self.button2.Text = "...";
		self.button2.UseVisualStyleBackColor = True;
		self.button2.Click +=  self.button2_Click;
		    # 
		    # outputFileName
		    # 
		self.outputFileName.Enabled = False;
		self.outputFileName.Location =  Point(122, 72);
		self.outputFileName.Name = "outputFileName";
		self.outputFileName.Size =  Size(177, 20);
		self.outputFileName.TabIndex = 19;
		self.outputFileName.Text = "tags.txt";
		    # 
		    # tabPageInputs
		    # 
		self.tabPageInputs.Controls.Add(self.label10);
		self.tabPageInputs.Controls.Add(self.label9);
		self.tabPageInputs.Controls.Add(self.label8);
		self.tabPageInputs.Controls.Add(self.label7);
		self.tabPageInputs.Controls.Add(self.buttonLed);
		self.tabPageInputs.Controls.Add(self.checkBoxInvers);
		self.tabPageInputs.Controls.Add(self.textBoxInputLevel);
		self.tabPageInputs.Controls.Add(self.textBoxInputName);
		self.tabPageInputs.Location =  Point(4, 22);
		self.tabPageInputs.Name = "tabPageInputs";
		self.tabPageInputs.Size =  Size(475, 348);
		self.tabPageInputs.TabIndex = 2;
		self.tabPageInputs.Text = "Inputs";
		self.tabPageInputs.UseVisualStyleBackColor = True;
		    # 
		    # label10
		    # 
		self.label10.AutoSize = True;
		self.label10.Location =  Point(163, 17);
		self.label10.Name = "label10";
		self.label10.Size =  Size(32, 13);
		self.label10.TabIndex = 20;
		self.label10.Text = "Edge";
		    # 
		    # label9
		    # 
		self.label9.AutoSize = True;
		self.label9.Location =  Point(244, 17);
		self.label9.Name = "label9";
		self.label9.Size =  Size(37, 13);
		self.label9.TabIndex = 20;
		self.label9.Text = "Active";
		    # 
		    # label8
		    # 
		self.label8.AutoSize = True;
		self.label8.Location =  Point(85, 17);
		self.label8.Name = "label8";
		self.label8.Size =  Size(51, 13);
		self.label8.TabIndex = 20;
		self.label8.Text = "Level / V";
		    # 
		    # label7
		    # 
		self.label7.AutoSize = True;
		self.label7.Location =  Point(17, 17);
		self.label7.Name = "label7";
		self.label7.Size =  Size(35, 13);
		self.label7.TabIndex = 20;
		self.label7.Text = "Name";
		    # 
		    # buttonLed
		    # 
		self.buttonLed.Location =  Point(247, 39);
		self.buttonLed.Name = "buttonLed";
		self.buttonLed.Size =  Size(18, 16);
		self.buttonLed.TabIndex = 4;
		self.buttonLed.UseVisualStyleBackColor = True;
		    # 
		    # checkBoxInvers
		    # 
		self.checkBoxInvers.AutoSize = True;
		self.checkBoxInvers.Location =  Point(166, 39);
		self.checkBoxInvers.Name = "checkBoxInvers";
		self.checkBoxInvers.Size =  Size(69, 17);
		self.checkBoxInvers.TabIndex = 3;
		self.checkBoxInvers.Text = "Negative";
		self.checkBoxInvers.UseVisualStyleBackColor = True;
		    # 
		    # textBoxInputLevel
		    # 
		self.textBoxInputLevel.Location =  Point(88, 39);
		self.textBoxInputLevel.Name = "textBoxInputLevel";
		self.textBoxInputLevel.Size =  Size(58, 20);
		self.textBoxInputLevel.TabIndex = 2;
		self.textBoxInputLevel.Text = "1,0";
		    # 
		    # textBoxInputName
		    # 
		self.textBoxInputName.Location =  Point(17, 39);
		self.textBoxInputName.Name = "textBoxInputName";
		self.textBoxInputName.Size =  Size(58, 20);
		self.textBoxInputName.TabIndex = 1;
		self.textBoxInputName.Text = "Input1";
		    # 
		    # tabPageDelay
		    # 
		self.tabPageDelay.Controls.Add(self.textBox4);
		self.tabPageDelay.Controls.Add(self.label13);
		self.tabPageDelay.Controls.Add(self.label12);
		self.tabPageDelay.Controls.Add(self.textBoxDelay);
		self.tabPageDelay.Controls.Add(self.labelDelayName);
		self.tabPageDelay.Location =  Point(4, 22);
		self.tabPageDelay.Name = "tabPageDelay";
		self.tabPageDelay.Size =  Size(475, 348);
		self.tabPageDelay.TabIndex = 3;
		self.tabPageDelay.Text = "Delay";
		self.tabPageDelay.UseVisualStyleBackColor = True;
		    # 
		    # textBox4
		    # 
		self.textBox4.Location =  Point(-106, 20);
		self.textBox4.Name = "textBox4";
		self.textBox4.Size =  Size(100, 20);
		self.textBox4.TabIndex = 16;
		self.textBox4.Text = "delay";
		    # 
		    # label13
		    # 
		self.label13.AutoSize = True;
		self.label13.Location =  Point(145, 23);
		self.label13.Name = "label13";
		self.label13.Size =  Size(35, 13);
		self.label13.TabIndex = 0;
		self.label13.Text = "Name";
		    # 
		    # label12
		    # 
		self.label12.AutoSize = True;
		self.label12.Location =  Point(22, 23);
		self.label12.Name = "label12";
		self.label12.Size =  Size(56, 13);
		self.label12.TabIndex = 0;
		self.label12.Text = "Delay / ns";
		    # 
		    # textBoxDelay
		    # 
		self.textBoxDelay.Location =  Point(17, 47);
		self.textBoxDelay.Name = "textBoxDelay";
		self.textBoxDelay.Size =  Size(100, 20);
		self.textBoxDelay.TabIndex = 16;
		self.textBoxDelay.Text = "0";
		    # 
		    # labelDelayName
		    # 
		self.labelDelayName.AutoSize = True;
		self.labelDelayName.Location =  Point(145, 50);
		self.labelDelayName.Name = "labelDelayName";
		self.labelDelayName.Size =  Size(64, 13);
		self.labelDelayName.TabIndex = 0;
		self.labelDelayName.Text = "Input 11111";
		    # 
		    # tabPageLogic
		    # 
		self.tabPageLogic.AutoScroll = True;
		self.tabPageLogic.Controls.Add(self.label5);
		self.tabPageLogic.Controls.Add(self.label6);
		self.tabPageLogic.Controls.Add(self.textBoxWindow);
		self.tabPageLogic.Controls.Add(self.textBoxCycle);
		self.tabPageLogic.Controls.Add(self.label11);
		self.tabPageLogic.Controls.Add(self.labelPatternRate);
		self.tabPageLogic.Controls.Add(self.checkBoxUseLogic);
		self.tabPageLogic.Controls.Add(self.logicChooser1);
		self.tabPageLogic.Location =  Point(4, 22);
		self.tabPageLogic.Name = "tabPageLogic";
		self.tabPageLogic.Padding =  Padding(3);
		self.tabPageLogic.Size =  Size(475, 348);
		self.tabPageLogic.TabIndex = 1;
		self.tabPageLogic.Text = "Logic";
		self.tabPageLogic.UseVisualStyleBackColor = True;
		    # 
		    # label5
		    # 
		self.label5.AutoSize = True;
		self.label5.Enabled = False;
		self.label5.Location =  Point(121, 77);
		self.label5.Name = "label5";
		self.label5.Size =  Size(130, 13);
		self.label5.TabIndex = 17;
		self.label5.Text = "Coincidence Window / ns";
		    # 
		    # label6
		    # 
		self.label6.AutoSize = True;
		self.label6.Enabled = False;
		self.label6.Location =  Point(123, 51);
		self.label6.Name = "label6";
		self.label6.Size =  Size(116, 13);
		self.label6.TabIndex = 17;
		self.label6.Text = "Aprox. Cycle Time / ms";
		    # 
		    # textBoxWindow
		    # 
		self.textBoxWindow.Enabled = False;
		self.textBoxWindow.Location =  Point(15, 74);
		self.textBoxWindow.Name = "textBoxWindow";
		self.textBoxWindow.Size =  Size(100, 20);
		self.textBoxWindow.TabIndex = 3;
		self.textBoxWindow.Text = "100";
		    # 
		    # textBoxCycle
		    # 
		self.textBoxCycle.Enabled = False;
		self.textBoxCycle.Location =  Point(14, 48);
		self.textBoxCycle.Name = "textBoxCycle";
		self.textBoxCycle.Size =  Size(100, 20);
		self.textBoxCycle.TabIndex = 2;
		self.textBoxCycle.Text = "100";
		    # 
		    # label11
		    # 
		self.label11.Anchor = ((AnchorStyles.Top | AnchorStyles.Right));
		self.label11.Enabled = False;
		self.label11.Location =  Point(318, 94);
		self.label11.Name = "label11";
		self.label11.Size =  Size(67, 13);
		self.label11.TabIndex = 2;
		self.label11.Text = "kHz";
		self.label11.TextAlign = ContentAlignment.TopRight;
		    # 
		    # labelPatternRate
		    # 
		self.labelPatternRate.Anchor = ((AnchorStyles.Top | AnchorStyles.Right));
		self.labelPatternRate.Enabled = False;
		self.labelPatternRate.Location =  Point(304, 116);
		self.labelPatternRate.Name = "labelPatternRate";
		self.labelPatternRate.Size =  Size(67, 13);
		self.labelPatternRate.TabIndex = 2;
		self.labelPatternRate.Text = "0,000";
		self.labelPatternRate.TextAlign = ContentAlignment.TopRight;
		    # 
		    # checkBoxUseLogic
		    # 
		self.checkBoxUseLogic.AutoSize = True;
		self.checkBoxUseLogic.Location =  Point(16, 21);
		self.checkBoxUseLogic.Name = "checkBoxUseLogic";
		self.checkBoxUseLogic.Size =  Size(71, 17);
		self.checkBoxUseLogic.TabIndex = 1;
		self.checkBoxUseLogic.Text = "UseLogic";
		self.checkBoxUseLogic.UseVisualStyleBackColor = True;
		self.checkBoxUseLogic.CheckedChanged +=  self.checkBoxUseLogic_CheckedChanged;
		
				#
		# logicChooser1
		# 
		self.logicChooser1.Enabled = True;
		self.logicChooser1.Location = Point(14, 110);
		self.logicChooser1.Name = "logicChooser1";
		self.logicChooser1.Size = Size(277, 30);
		self.logicChooser1.TabIndex = 4;
	
		     #
		    # tabPageDebug
		    # 
		self.tabPageDebug.Controls.Add(self.buttonReadUsb);
		self.tabPageDebug.Location =  Point(4, 22);
		self.tabPageDebug.Name = "tabPageDebug";
		self.tabPageDebug.Size =  Size(475, 348);
		self.tabPageDebug.TabIndex = 5;
		self.tabPageDebug.Text = "Debug";
		self.tabPageDebug.UseVisualStyleBackColor = True;
		    # 
		    # buttonReadUsb
		    # 
		self.buttonReadUsb.Location =  Point(17, 39);
		self.buttonReadUsb.Name = "buttonReadUsb";
		self.buttonReadUsb.Size =  Size(75, 23);
		self.buttonReadUsb.TabIndex = 0;
		self.buttonReadUsb.Text = "ReadUsb";
		self.buttonReadUsb.UseVisualStyleBackColor = True;
		self.buttonReadUsb.Click +=  self.buttonReadUsb_Click;
		    # 
		    # timerLogic
		    # 
		self.timerLogic.Tick +=  self.timerLogic_Tick;
		    # 
		    # menuStrip1
		    # 

		self.menuStrip1.Items.Add(self.fileToolStripMenuItem);
		self.menuStrip1.Items.Add(self.deviceToolStripMenuItem);
		self.menuStrip1.Location =  Point(0, 0);
		self.menuStrip1.Name = "menuStrip1";
		self.menuStrip1.Size =  Size(881, 24);
		self.menuStrip1.TabIndex = 20;
		self.menuStrip1.Text = "menuStrip1";
		    # 
		    # fileToolStripMenuItem
		    # 


		self.fileToolStripMenuItem.DropDownItems.Add(self.openToolStripMenuItem);
		self.fileToolStripMenuItem.DropDownItems.Add(self.saveToolStripMenuItem);
		self.fileToolStripMenuItem.DropDownItems.Add(self.saveasToolStripMenuItem);
		self.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
		self.fileToolStripMenuItem.Size =  Size(35, 20);
		self.fileToolStripMenuItem.Text = "File";
		    # 
		    # openToolStripMenuItem
		    # 
		self.openToolStripMenuItem.Name = "openToolStripMenuItem";
		self.openToolStripMenuItem.Size =  Size(123, 22);
		self.openToolStripMenuItem.Text = "&Open";
		self.openToolStripMenuItem.Click +=  self.openToolStripMenuItem_Click;
		    # 
		    # saveToolStripMenuItem
		    # 
		self.saveToolStripMenuItem.Name = "saveToolStripMenuItem";
		self.saveToolStripMenuItem.Size =  Size(123, 22);
		self.saveToolStripMenuItem.Text = "&Save";
		self.saveToolStripMenuItem.Click +=  self.saveToolStripMenuItem_Click;
		    # 
		    # saveasToolStripMenuItem
		    # 
		self.saveasToolStripMenuItem.Name = "saveasToolStripMenuItem";
		self.saveasToolStripMenuItem.Size =  Size(123, 22);
		self.saveasToolStripMenuItem.Text = "Save &as";
		self.saveasToolStripMenuItem.Click +=  self.saveasToolStripMenuItem_Click;
		    # 
		    # deviceToolStripMenuItem
		    # 
		self.deviceToolStripMenuItem.DropDownItems.Add(self.connectToolStripMenuItem)
		self.deviceToolStripMenuItem.DropDownItems.Add(self.calibrateToolStripMenuItem)
		self.deviceToolStripMenuItem.DropDownItems.Add(self.infoToolStripMenuItem1)
        #, self.calibrateToolStripMenuItem, self.infoToolStripMenuItem1]);
		self.deviceToolStripMenuItem.Name = "deviceToolStripMenuItem";
		self.deviceToolStripMenuItem.Size =  Size(51, 20);
		self.deviceToolStripMenuItem.Text = "Device";
		    # 
		    # connectToolStripMenuItem
		    # 
		self.connectToolStripMenuItem.Name = "connectToolStripMenuItem";
		self.connectToolStripMenuItem.Size =  Size(128, 22);
		self.connectToolStripMenuItem.Text = "&Connect";
		self.connectToolStripMenuItem.Click +=  self.connectToolStripMenuItem_Click;
		    # 
		    # calibrateToolStripMenuItem
		    # 
		self.calibrateToolStripMenuItem.Name = "calibrateToolStripMenuItem";
		self.calibrateToolStripMenuItem.Size =  Size(128, 22);
		self.calibrateToolStripMenuItem.Text = "C&alibrate";
		self.calibrateToolStripMenuItem.Click +=  self.calibrateToolStripMenuItem_Click;
		    # 
		    # infoToolStripMenuItem1
		    # 
		self.infoToolStripMenuItem1.Name = "infoToolStripMenuItem1";
		self.infoToolStripMenuItem1.Size =  Size(128, 22);
		self.infoToolStripMenuItem1.Text = "&Info";
		self.infoToolStripMenuItem1.Click +=  self.infoToolStripMenuItem1_Click;
		    # 
		    # openFileDialog1
		    # 
		self.openFileDialog1.FileName = "openFileDialog1";
		    # 
		    # timerButtons
		    # 
		self.timerButtons.Enabled = True;
		self.timerButtons.Tick +=  self.timerButtons_Tick;
		
		# 
		# histoGraph
		#
		self.histoGraph.Location = Point(10, 10);
		self.histoGraph.Name = "histoGraph";
		self.histoGraph.ScrollGrace = 0;
		self.histoGraph.ScrollMaxX = 0;
		self.histoGraph.ScrollMaxY = 0;
		self.histoGraph.ScrollMaxY2 = 0;
		self.histoGraph.ScrollMinX = 0;
		self.histoGraph.ScrollMinY = 0;
		self.histoGraph.ScrollMinY2 = 0;
		self.histoGraph.Size = Size(400, 250);
		self.histoGraphPane = self.histoGraph.GraphPane;
		self.histoGraphPane.Title.Text = "Gyroscope information";
		self.histoGraphPane.XAxis.Title.Text = "Time (ns)";
		self.histoGraphPane.YAxis.Title.Text = "Frequency";
		    # 
		    # FormTimetagExplorer
		    # 
		self.AutoScaleDimensions =  Size(1, 2);
		self.AutoScaleMode = AutoScaleMode.Font;
		self.ClientSize =  Size(881, 448);
		self.Controls.Add(self.tabControl1);
		self.Controls.Add(self.richTextBox1);
		self.Controls.Add(self.buttonCalibrate);
		self.Controls.Add(self.labelErrors);
		self.Controls.Add(self.buttonConnect);
		self.Controls.Add(self.buttonLabview);
		self.Controls.Add(self.menuStrip1);
		self.MainMenuStrip = self.menuStrip1;
		#self.MaximizeBox = False;
		#self.MaximumSize =  Size(1500, 958);
		self.Name = "FormTimetagExplorer";
		#self.SizeGripStyle = SizeGripStyle.Hide;
		self.Text = "PyTT";
		self.Load +=  self.FormTimetagDemo_Load;
		self.FormClosed +=  self.FormTimetagDemo_FormClosed;
		self.groupBoxEdgeGate.ResumeLayout(False);
		self.groupBoxEdgeGate.PerformLayout();
		self.tabControl1.ResumeLayout(False);
		self.tabPageTimeTag.ResumeLayout(False);
		self.tabPageTimeTag.PerformLayout();
		self.tabPageSaveTags.ResumeLayout(False);
		self.tabPageSaveTags.PerformLayout();
		self.tabPageInputs.ResumeLayout(False);
		self.tabPageInputs.PerformLayout();
		self.tabPageDelay.ResumeLayout(False);
		self.tabPageDelay.PerformLayout();
		self.tabPageLogic.ResumeLayout(False);
		self.tabPageLogic.PerformLayout();
		self.tabPageDebug.ResumeLayout(False);
		self.menuStrip1.ResumeLayout(False);
		self.menuStrip1.PerformLayout();
		
		self.conversionRunning = False;
		self.OldTime = 0;
		self.paraHandling = ParaHandling("TIMETAG");
		self.InitialText = "";
		
		self.ResumeLayout(False);
		self.PerformLayout();

    #The following methods are event handlers
	def checkBoxUseLogic_CheckedChanged(self, sender, event):
		#DisableOtherModes(sender);
		#turn off saving timetags
		self.checkBoxSaveTags.Enabled = False;
		#if checkBoxUseLogic is checked, enable all other controls (i.e. the matrix of buttons) 
		for c in self.tabPageLogic.Controls:
			if c != self.checkBoxUseLogic:
				c.Enabled = self.checkBoxUseLogic.Checked;
		if sender.Checked:
			#initiate a new connection to the Logic if none exists
			if self.Logic == None:
				if self.ttInterface != None:
					self.Logic = Logic(self.ttInterface);
			#now switch logic mode (not exactly sure what this does...)
			if self.Logic != None:
				self.Logic.SwitchLogicMode();
				self.timerLogic.Enabled = True;
				self.timer1.Enabled = False;
		else:
			self.timerLogic.Enabled = False;
			self.timer1.Enabled = True;
			self.Logic = None;

	def checkBoxReadTags_CheckedChanged(self, sender, event):
		#DisableOtherModes(sender);
		#enable all the controls on the Timetag page if Read tags is clicked
		for c in self.tabPageTimeTag.Controls:
			if c != self.checkBoxReadTags:
				c.Enabled = self.checkBoxReadTags.Checked;
		self.checkBoxUseLogic.Enabled = False;
		#start or stop reading timetags
		if self.checkBoxReadTags.Checked:
			self.ttInterface.StartTimetags();
		else:
			self.ttInterface.StopTimetags();

	#save tag buttons
	def button1_Click(self, sender, event):
		self.saveFileDialog1.FileName= self.rawFileName.Text;
		self.saveFileDialog1.ShowDialog();
		self.rawFileName.Text= self.saveFileDialog1.FileName;

	def button2_Click(self, sender, event):
		self.saveFileDialog2.FileName = self.outputFileName.Text;
		self.saveFileDialog2.ShowDialog();
		self.outputFileName.Text = self.saveFileDialog2.FileName;

	#Connect and Calibrate functions
	def buttonConnect_Click(self, sender, event):
		self.Connect()

	def Connect(self):
		#check if timetag interface connection exists, if not, create it, else disconnect
		if self.ttInterface == None:
			self.TryConnect()
		else:
			self.Disconnect()

	def buttonCalibrate_Click(self, sender, event):
		self.Calibrate();
	
	def buttonLabview_Click(self, sender, event):
		self.Labview = switchLabview(self, self.Labview)

        
	def Calibrate(self):
		#DisableOtherModes(None);
		self.richTextBox1.Clear();
		self.richTextBox1.AppendText("Calibration running\n")
		#self.Application.DoEvents();
		self.ttInterface.Calibrate();
		self.richTextBox1.AppendText("Calibration completed");
		self.calibrateToolStripMenuItem.Text = self.buttonCalibrate.Text = "Calibrated";

	def timer1_Tick(self, sender, event):
		if self.ttInterface != None:
			ShowErrors(self);
		if self.checkBoxReadTags.Checked:
			DoReadTags(self);
		elif self.checkBoxSaveTags.Checked:
			DoSaveTags(self);
		
	#an unused exception handling method, for potential future use, because I haven't figured out how to convert exception handling correctly between C# and python...
	def HandleException(ex):
		if ex is UsbDll.UsbException:
			self.Disconnect();
			self.richTextBox1.Text = "Error: " + ex.Message;
		else:
			MessageBox.Show("Error: " + ex.Message);

	#sends new values to the timetagger when GatePosition and GateWidth are changed.
	def groupBoxEdgeGate_EnabledChanged(self, sender, event):
		if sender.Enabled:
			self.TransmitValue(self.textBoxGatePosition, None);
			self.TransmitValue(self.textBoxGateWidth, None);

	def checkBoxSaveTags_CheckedChanged(self, sender, event):
		#DisableOtherModes(sender);
		self.checkBoxUseLogic.Enabled = False;
		for c in self.tabPageSaveTags.Controls:
			if c != self.checkBoxSaveTags:
				c.Enabled = self.checkBoxSaveTags.Checked;
		for c in self.tabPageTimeTag.Controls:
			if c != self.checkBoxReadTags:
				c.Enabled = self.checkBoxSaveTags.Checked;

	def buttonSaveStart_Click(self, sender, event):
		if not self.ttInterface.GetReader().ConversionMode and not self.ttInterface.GetReader().FileSaveMode:
			self.startTime = DateTime.Now;
			self.ttInterface.StartTimetags();
			self.ttInterface.GetReader().StartSaving(self.rawFileName.Text);
			SetButtonText(self);
			self.richTextBox1.Clear();
			self.richTextBox1.AppendText("Reading data....\n");
		elif self.ttInterface.GetReader().FileSaveMode:
			self.ttInterface.GetReader().StopSaving();
			self.tempTags = self.ttInterface.GetReader().SavedTags;
			self.startTime = DateTime.Now;
			self.ttInterface.GetReader().StartConverting(self.outputFileName.Text);
			self.conversionRunning = True;
			self.SetButtonText();
			ShowRate(self);
			self.richTextBox1.AppendText("Converting....\n");

	def buttonReadUsb_Click(self, sender, event):        
		self.richTextBox1.Clear();
		self.timer1.Enabled= False;
		for i in range(0,100):
			if self.ttInterface != None:
				self.richTextBox1.AppendText(" "+str(i)+":"+str(self.ttInterface.GetTest().GetUsb().ReadUsbPara(i))+"\n");

	def timerLogic_Tick(self, sender, event):
		self.LogicTimer();

	def LogicTimer(self):
		ShowErrors(self);
		self.Logic.ReadLogic();
		tmCount = self.Logic.GetTimeCounter();
		self.message += String.Format("0,101,10:0.###\n\n", "Cycle / ms", tmCount / 200000.0);
		self.message += String.Format("0,101,102,10 \n", "Name", "Count", "kHz");
		for  i in range(0,16):
			scount = self.Logic.CalcCount(1 << i, 0);
			sfreq = 200e3 * scount / tmCount;
			self.message += String.Format("0,101,102,10:0.000 \n", self.nameBoxes[i].Text, str(scount), str(sfreq));
			self.message += "\n";
			for  i in range(0, self.MaxPattern):
				pos = self.choosers[i].GetPos();
				neg = self.choosers[i].GetNeg();
				if pos == 0:
					count = 0;
				else:
					count = self.Logic.CalcCount(pos, neg);
				self.labelPatternRate.Text = "pos:" + str(pos) + " neg:" + str(neg);
				freq = 0;
				if tmCount != 0:
					freq = 200e3 * count / tmCount;
				self.patternRateLabels[i+1].Text = freq.ToString("0.000");
				self.message += String.Format("0,101,102,10:0.000 \n", "Pattern " + str(i + 1), str(count), str(freq));
		self.richTextBox1.Text = self.message;
		
	def openToolStripMenuItem_Click(self, sender, event):
		self.LoadData();

	def saveToolStripMenuItem_Click(self, sender, event):
		self.SaveData();

	def saveasToolStripMenuItem_Click(self, sender, event):
		self.SaveAs();
		
	def connectToolStripMenuItem_Click(self, sender, event):
		self.Connect();

	def calibrateToolStripMenuItem_Click(self, sender, event):
		self.Calibrate();      

	#when Info is clicked from the dropdown menu. Right now it just writes it to the console because I haven't figured out a good way of doing message boxes in python 
	def infoToolStripMenuItem1_Click(self, sender, event):
		if self.ttInterface == None:
			self.message = "No device connected";
		else:
			self.message = "FPGA Version:\t" + str(self.ttInterface.GetFpgaVersion()) + "\n" + "Resolution/ps:\t" + str(self.ttInterface.GetResolution() * 1e12) + "\n";
		self.richTextBox1.Text = self.message;

	#the following timer is active on the Inputs tab, and makes sure that the channel active indicators match the parameters off of the timetagger	
	def timerButtons_Tick(self, sender, event):
		if self.tabControl1.SelectedTab == self.tabPageInputs:
			if self.ttInterface != None:
				status= self.ttInterface.GetTest().ReadMeasurement(2);
				for i in range(0,16):
					if (status & (1 << (i+1))) != 0:
						self.ledButtons[i].BackColor = Color.Blue;
					else:
						self.ledButtons[i].BackColor = self.buttonCalibrate.BackColor;

	def FormTimetagDemo_Load(self, sender, event):
		#self.TopMost = True;
		#self.FormBorderStyle = FormBorderStyle.None;
		#self.WindowState = FormWindowState.Maximized;
		self.WindowState = FormWindowState.Normal;
		self.tabControl1.TabPages.Remove(self.tabPageDebug);
		self.tabControl1.Size =  Size(self.Width/2, self.Height-62);
		self.richTextBox1.Location =  Point(self.Width/2+30, 84);
		self.richTextBox1.Size = Size(self.Width/2 -60,self.Height-90);
		#duplicates the rows of logic selector buttons on the Logic tabs
		DublicateLogic(self);
		#duplicates the negative edge/voltage settings for the input channels
		DublicateInputs(self);
		#duplicates the delay inputs on the delay tabs
		DublicateDelays(self);
		#not sure if these things are doing anything...
		self.paraHandling.SaveAdditional(LogicChooser());
		self.paraHandling.Init(self.tabControl1);
		self.ModeList.Add(self.checkBoxUseLogic);
		self.ModeList.Add(self.checkBoxReadTags);
		self.ModeList.Add(self.checkBoxSaveTags);
		for c in self.ModeList:
			self.paraHandling.MarkNoSave(c);
		self.paraHandling.MarkNoSave(self.checkBoxEdgeGate);
		#Thomas Lehner originally wrote a ParaHandling class to handle the event handling for the repeated checkboxes etc, but it currently doesn't work because IronPython doesn't like EventHandlers as used by C#. In future, I could replace this with Python Event handlers, but at the moment it's easier just to force the functions to be forceably attached to their event handlers
		#self.paraHandling.OnTransmitValue += EventHandler(self.TransmitValue(),self.checkBoxEdgeGate);
		#Directory.SetCurrentDirectory(Environment.GetFolderPath(Environment.SpecialFolder.Personal));
		self.InitialText = Text;
		SwitchGui(self,False);
		self.paraHandling.LoadData(self.ParaFileName);
		
	def FormTimetagDemo_FormClosed(self, sender, event):
		self.DoClose();
		
	#closes the interface
	def DoClose(self):        
		if self.ttInterface != None:
			self.ttInterface.Close();
			
	def TryConnect(self):
		if not self.UsbDllCheck():
			return
		try:
			self.ttInterface = TTInterface()
			self.ttInterface.Open(1)
			SwitchGui(self,True)
			self.Logic = Logic(self.ttInterface)
			#read parameters
			features = self.ttInterface.GetTest().ReadMeasurement(18)
			self.checkBoxUseLogic.Enabled = (features & 1) != 0
			self.checkBoxReadTags.Enabled = (features & 2) != 0
			self.checkBoxSaveTags.Enabled = (features & 2) != 0
			self.paraHandling.RetransmitData()
			self.timer1.Enabled = True
		except:
			print("did not find device")
		ShowStatus(self)
		
	#shuts down the connection and does some cleanup
	def Disconnect(self):
		self.timer1.Enabled = False
		self.timerLogic.Enabled = False
		#DisableOtherModes(None)
		self.ttInterface.Close()
		self.ttInterface = None
		SwitchGui(self,False)

			
	def UsbDllCheck(self):        
		try:
			self.OpenUsbDll();
			return True;
		except:  
			print "Can't open usbdll.dll. ";
			return False;
				
	def OpenUsbDll(self):
		#UsbDll.UsbInterface usb = new UsbDll.UsbInterface();
		tags = Tag;
	
	#sends the values of gate widths, positions, delays, negative edges etc to the timetagger
	def TransmitValue(self, sender, args):
		if (self.ttInterface == None or not self.ttInterface.IsOpen()):
			return;
		box = sender;
		if (box == self.textBoxCycle):
			self.timerLogic.Interval = self.paraHandling.ReadMinMax(box, 10, 10000);
		elif (box == self.textBoxWindow):
			resolution = 5.0 / 32;
			maxWindow = ((1 << 18) - 1) * resolution;
			window = self.paraHandling.ReadMinMax(box, 0, maxWindow);
			iwindow = (int)(window / resolution + 0.5);
			self.Logic.SetWindowWidth(iwindow);
			window = iwindow * resolution;
			box.Text = window.ToString("0.###");
		elif (box == self.textBoxGateWidth):
			if not self.groupBoxEdgeGate.Enabled:
				return;
			res = self.ttInterface.GetResolution() * 1e9;
			width = self.paraHandling.ReadMinMax(self.textBoxGateWidth, 0, ((1 << 18)-1) * res);
			ticks = (int)(width / res);
			self.Logic.SetWindowWidth(ticks);
			box.Text = (ticks* res).ToString("0.###");
		elif (box == self.textBoxGatePosition):
			if ( not self.groupBoxEdgeGate.Enabled):
				return;
			res = self.ttInterface.GetResolution() * 1e9;
			limit = ((1 << 17) - 1) * res;
			position = self.paraHandling.ReadMinMax(self.textBoxGatePosition, -limit, limit);
			ticks = (position / res);
			for i in range(1,17):  #Negative position -> inputs are shifted
				if ticks <0:
					self.ttInterface.SetDelay(i,-ticks)
				else:
					self.ttInterface.SetDelay(i, 0)
			if ticks>0:
				self.ttInterface.SetDelay(8, ticks)
			else:
				self.ttInterface.SetDelay(8, 0)
			box.Text = (ticks * res).ToString("0.###");
		elif FindCheckBox(box, self.nameBoxes)!= -1:
			index = FindCheckBox(box,self.nameBoxes)
			self.delayLabels[index].Text = box.Text;
		elif FindCheckBox(box, self.voltageBoxes) != -1:
			index = FindCheckBox(box, self.voltageBoxes)
			volt= paraHandling.ReadMinMax(box, -2, 2);
			self.ttInterface.SetInputThreshold(index+1, volt);
		elif FindCheckBox(box, self.delayBoxes) != -1:
			index = self.FindCheckBox(box, self.delayBoxes)
			resolution = 5.0 / 32;
			maxDelay = ((1 << 18) - 1) * resolution;
			delay = self.paraHandling.ReadMinMax(box, 0, maxDelay);
			idelay = (int)(delay / resolution+0.5);
			self.ttInterface.SetDelay(index + 1, idelay);
			delay = idelay * resolution;
			box.Text = delay.ToString("0.###");
	
	#loads default parameters from the saved file
	def LoadData(self):
		self.openFileDialog1.FileName = self.ParaFileName;
		self.openFileDialog1.Filter = "Timetag Para|*.timetag";
		if self.openFileDialog1.ShowDialog() == DialogResult.OK:
			self.ParaFileName = self.openFileDialog1.FileName;
			self.paraHandling.LoadData(self.ParaFileName);
			

	
	#updates the value in the histogram
	def update_histogram(self,blarg):
		y = Array[float]((self.bins_frequency))
		myBar = self.histoGraphPane.AddBar( "Curve 1", None, y, Color.Red )
        #self.myBar.Bar.Fill = Fill( Color.Red, Color.White, Color.Red )
		
	#turns the values of the checkboxes into an inversionMask to send the parameters to the timetagger
	def CheckedChanged(form,sender,e):
		cb = sender;
		if type(cb) is CheckBox:
			index = FindCheckBox(cb, form.negativeBoxes)
			if form.ttInterface == None or not form.ttInterface.IsOpen():
				return;
			if (cb == form.checkBoxUse10MHz):
				form.ttInterface.Use10MHz(cb.Checked);
			elif (cb == form.checkBoxEdgeGate):
				form.groupBoxEdgeGate.Enabled = form.checkBoxEdgeGate.Checked;
				form.ttInterface.UseTimetagGate(form.checkBoxEdgeGate.Checked);
			elif (cb == form.checkBoxUseLevelGate):
				form.ttInterface.UseLevelGate(cb.Checked);
			elif (index != -1):
				if (cb.Checked):
					form.inversionMask = form.inversionMask | (1 << index);
				else:
					form.inversionMask = form.inversionMask & ~(1 << index);
				form.ttInterface.SetInversionMask(form.inversionMask);