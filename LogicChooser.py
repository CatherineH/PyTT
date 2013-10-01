import clr
clr.AddReference("System")
from System import *
clr.AddReference("System.Collections")
from System.Collections import *
clr.AddReference("System.ComponentModel")
from System.ComponentModel import *
clr.AddReference("System.Drawing")
from System.Drawing import *
clr.AddReference("System.Data")
from System.Data import *
#clr.AddReference("System.Text")
#from System.Text import *
clr.AddReference("System.Windows")
from System.Windows import *
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import AutoScaleMode, Button, Control;
#this class defines the logic chooser control (i.e. the matrix of channel buttons on the logicchooser tab)
class LogicChooser(Control):
	def __init__(self):
		self.button1 = Button();
		self.button2 = Button();
		self.button3 = Button();
		self.button4 = Button();
		self.button5 = Button();
		self.button6 = Button();
		self.button7 = Button();
		self.button8 = Button();
		self.button9 = Button();
		self.button10 = Button();
		self.button11 = Button();
		self.button12 = Button();
		self.button13 = Button();
		self.button14 = Button();
		self.button15 = Button();
		self.button16 = Button();
		self.SuspendLayout();
		# 
		# button1
		# 
		self.button1.Location = Point(-1, 0);
		self.button1.Name = "button1";
		self.button1.Size = Size(18, 23);
		self.button1.TabIndex = 0;
		self.button1.Text = " ";
		self.button1.UseVisualStyleBackColor = True;
		self.button1.Click += EventHandler(self.button_Click);		# 
		# button2
		# 
		self.button2.Location = Point(16, 0);
		self.button2.Name = "button2";
		self.button2.Size = Size(18, 23);
		self.button2.TabIndex = 0;
		self.button2.Text = " ";
		self.button2.UseVisualStyleBackColor = True;
		self.button2.Click += EventHandler(self.button_Click);
		# 
		# button3
		# 
		self.button3.Location = Point(33, 0);
		self.button3.Name = "button3";
		self.button3.Size = Size(18, 23);
		self.button3.TabIndex = 0;
		self.button3.Text = " ";
		self.button3.UseVisualStyleBackColor = True;
		self.button3.Click += EventHandler(self.button_Click);
		# 
		# button4
		# 
		self.button4.Location = Point(50, 0);
		self.button4.Name = "button4";
		self.button4.Size = Size(18, 23);
		self.button4.TabIndex = 1;
		self.button4.Text = " ";
		self.button4.UseVisualStyleBackColor = True;
		self.button4.Click += EventHandler(self.button_Click);
		# 
		# button5
		# 
		self.button5.Location = Point(67, 0);
		self.button5.Name = "button5";
		self.button5.Size = Size(18, 23);
		self.button5.TabIndex = 0;
		self.button5.Text = " ";
		self.button5.UseVisualStyleBackColor = True;
		self.button5.Click += EventHandler(self.button_Click);
		# 
		# button6
		# 
		self.button6.Location = Point(84, 0);
		self.button6.Name = "button6";
		self.button6.Size = Size(18, 23);
		self.button6.TabIndex = 0;
		self.button6.Text = " ";
		self.button6.UseVisualStyleBackColor = True;
		self.button6.Click += EventHandler(self.button_Click);
		# 
		# button7
		# 
		self.button7.Location = Point(101, 0);
		self.button7.Name = "button7";
		self.button7.Size = Size(18, 23);
		self.button7.TabIndex = 0;
		self.button7.Text = " ";
		self.button7.UseVisualStyleBackColor = True;
		self.button7.Click += EventHandler(self.button_Click);
		# 
		# button8
		# 
		self.button8.Location = Point(118, 0);
		self.button8.Name = "button8";
		self.button8.Size = Size(18, 23);
		self.button8.TabIndex = 1;
		self.button8.Text = " ";
		self.button8.UseVisualStyleBackColor = True;
		self.button8.Click += EventHandler(self.button_Click);
		# 
		# button9
		# 
		self.button9.Location = Point(135, 0);
		self.button9.Name = "button9";
		self.button9.Size = Size(18, 23);
		self.button9.TabIndex = 8;
		self.button9.Text = " ";
		self.button9.UseVisualStyleBackColor = True;
		self.button9.Click += EventHandler(self.button_Click);
		# 
		# button10
		# 
		self.button10.Location = Point(152, 0);
		self.button10.Name = "button10";
		self.button10.Size = Size(18, 23);
		self.button10.TabIndex = 7;
		self.button10.Text = " ";
		self.button10.UseVisualStyleBackColor = True;
		self.button10.Click += EventHandler(self.button_Click);
		# 
		# button11
		# 
		self.button11.Location = Point(169, 0);
		self.button11.Name = "button11";
		self.button11.Size = Size(18, 23);
		self.button11.TabIndex = 9;
		self.button11.Text = " ";
		self.button11.UseVisualStyleBackColor = True;
		self.button11.Click += EventHandler(self.button_Click);
		# 
		# button12
		# 
		self.button12.Location = Point(186, 0);
		self.button12.Name = "button12";
		self.button12.Size = Size(18, 23);
		self.button12.TabIndex = 6;
		self.button12.Text = " ";
		self.button12.UseVisualStyleBackColor = True;
		self.button12.Click += EventHandler(self.button_Click);
		# 
		# button13
		# 
		self.button13.Location = Point(203, 0);
		self.button13.Name = "button13";
		self.button13.Size = Size(18, 23);
		self.button13.TabIndex = 2;
		self.button13.Text = " ";
		self.button13.UseVisualStyleBackColor = True;
		self.button13.Click += EventHandler(self.button_Click);
		# 
		# button14
		# 
		self.button14.Location = Point(220, 0);
		self.button14.Name = "button14";
		self.button14.Size = Size(18, 23);
		self.button14.TabIndex = 3;
		self.button14.Text = " ";
		self.button14.UseVisualStyleBackColor = True;
		self.button14.Click += EventHandler(self.button_Click);
		# 
		# button15
		# 
		self.button15.Location = Point(237, 0);
		self.button15.Name = "button15";
		self.button15.Size = Size(18, 23);
		self.button15.TabIndex = 4;
		self.button15.Text = " ";
		self.button15.UseVisualStyleBackColor = True;
		self.button15.Click += EventHandler(self.button_Click);
		# 
		# button16
		# 
		self.button16.Location = Point(254, 0);
		self.button16.Name = "button16";
		self.button16.Size = Size(18, 23);
		self.button16.TabIndex = 5;
		self.button16.Text = " ";
		self.button16.UseVisualStyleBackColor = True;
		self.button16.Click += EventHandler(self.button_Click);
		# 
		# LogicChooser
		# 
		self.AutoScaleDimensions = SizeF(6, 13);
		self.AutoScaleMode = AutoScaleMode.Font;
		self.Controls = [];
		'''
		self.Controls.Add(self.button9);
		self.Controls.Add(self.button10);
		self.Controls.Add(self.button11);
		self.Controls.Add(self.button12);
		self.Controls.Add(self.button13);
		self.Controls.Add(self.button14);
		self.Controls.Add(self.button15);
		self.Controls.Add(self.button16);
		self.Controls.Add(self.button8);
		self.Controls.Add(self.button7);
		self.Controls.Add(self.button4);
		self.Controls.Add(self.button6);
		self.Controls.Add(self.button3);
		self.Controls.Add(self.button5);
		self.Controls.Add(self.button2);
		self.Controls.Add(self.button1);
		'''
		self.Controls.Add(self.button1);
		self.Controls.Add(self.button2);
		self.Controls.Add(self.button3);
		self.Controls.Add(self.button4);
		self.Controls.Add(self.button5);
		self.Controls.Add(self.button6);
		self.Controls.Add(self.button7);
		self.Controls.Add(self.button8);
		self.Controls.Add(self.button9);
		self.Controls.Add(self.button10);
		self.Controls.Add(self.button11);
		self.Controls.Add(self.button12);
		self.Controls.Add(self.button13);
		self.Controls.Add(self.button14);
		self.Controls.Add(self.button15);
		self.Controls.Add(self.button16);
		self.Name = "LogicChooser";
		self.Size = Size(272, 23);
		self.ResumeLayout(False);

		self.bList = []
		for c in self.Controls:
			if type(c) is Button:
				#print("added button "+c.Name+" Pos:"+str(c.Location) )
				self.bList.Add(c)
		
		for b in self.bList:
			b.Text = self.GetIndex(b)
			self.SetColor(b)
			b.TabIndex = 17-self.bList.IndexOf(b)
			
	def GetIndex (self,b):
		ind = self.bList.IndexOf(b)
		ind+=1
		ind %= 10
		return ind.ToString()
	def SetColor (self,b):
		if (b.Text == "+" or b.Text == "-"):
			b.ForeColor = Color.Black
		else:
			b.ForeColor = Color.DarkGray
	def button_Click (self,sender,e):
		if type(sender) is Button:
			b = sender
			if (b.Text == "+"):
				b.Text = "-"
			elif (b.Text == "-"):
				b.Text = self.GetIndex(b)
			else:
				b.Text = "+"
				index= -1
			'''
			for i in range(0,16):
				if (self.bList[i] == b):
					index = i
				if (index == -1):
					MessageBox.Show("not found")
			'''
			self.SetColor(b)
	def GetPos (self):
		ret= 0
		for i in range(0,16):
			if (self.bList[i].Text == "+"):
				ret += (1 << i)
		return ret
	def GetNeg (self):
		ret = 0
		for i in range(0,16):
			if (self.bList[i].Text == "-"):
				ret += (1 << i)
		return ret

