import clr;
clr.AddReference("System")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Drawing")
from System import EventHandler;
from System.Drawing import Font, FontStyle;
from System.Windows.Forms import CheckBox, GroupBox, KeyPressEventHandler, TabControl, TabPage, TextBox;
#this class handles reading in default timetag values 

class ParaHandling:

	def __init__(self, name):
		self.ParaKennung = name + ": 0";
		self.SaveNames = [];
		self.ControlList= [];
		self.OnTransmitValue = None;
		self.OnCheckedChanged = None;
		
	def Init(self,tabControl):
		self.ListControls(tabControl);
		self.SetEventHandler();
    
	def SaveAdditional(self,T):
		self.SaveNames.append(T.Name);
		
	def MarkNoSave(self, c):
		self.ControlList.Remove(c);

	def textBox_KeyPress(self, sender, e):
		if (e.KeyChar == 13):
			self.TransmitValue(sender);
			e.Handled = True;
			
	def SetEventHandler(self):
		for c in self.ControlList:
			tb = c;
			if type(tb) is TextBox:
				tb.TextChanged += EventHandler(self.tb_TextChanged);
				tb.Leave += EventHandler(self.tb_Leave);
				tb.KeyPress += KeyPressEventHandler(this.textBox_KeyPress);
			cb = c;
			if type(cb) is CheckBox:
				cb.CheckedChanged += EventHandler(self.CheckedChanged);
            
	def ListControls(self,tabControl):
		self.ListControlsSub(tabControl);
		
	def ListControlsSub(self,cc):
		if cc is TabControl:
			for c in cc.TabPages:
				self.ListControlsSub(c);
		elif cc is GroupBox:
			for c in cc.Controls:
				self.ListControlsSub(c);
		elif cc is TabPage:
			for c in cc.Controls:
				self.ListControlsSub(c);
		elif cc is TextBox or cc is CheckBox:
			self.ControlList.Append(cc);
		elif cc.GetType().Name in self.SaveNames:
			self.ControlList.Append(cc);

	def LoadData(self,FileName):
		try:
			with open(FileName): pass
			r = open(FileName, 'r') or die
			kennung = r.readline();
			if (kennung != self.ParaKennung):
				if (MessageBox.Show("Parameter Versions do not match. Read anyway ?", "hallo ?", MessageBoxButtons.YesNo) != DialogResult.Yes):
					return;
			while True:
				line = r.readline();
				if (line == None):
					break;
				pos = line.index(':');
				name = line[:pos];
				value = line[pos + 1:];
				self.LoadControl(name, value);
			if r != None :
				r.Close();
		except IOError:
			print("File "+FileName+" does not exist. Saved parameters not loaded")

	def LoadControl(self, name, value):
		for c in self.ControlList:
			if (c.Name == name):
				if type(c) is CheckBox:
					c.Checked = value != "0";
				else:
					c.Text = value;
					if type(c) is TextBox:
						self.TransmitValue(c);
				break;


	def TransmitValue(self, tb):
		if (self.OnTransmitValue != None):
			self.OnTransmitValue = EventHandler(tb, None);
		FontNormal(tb);

	def RetransmitData(self):
		for cc in self.ControlList:
			if (type(cc) is TextBox):
				TransmitValue(cc);
			if (type(cc) is CheckBox):
				self.CheckedChanged(cc, None);
				
	def CheckedChanged(self,cb,args):
		if (OnCheckedChanged != null):
			OnCheckedChanged(cb, args);
	
	def SaveData(self, FileName):
		w = open(FileName, 'w')
		try:
			w.writeline(self.ParaKennung);
			for tb in self.ControlList:
				if type(tb) is CheckBox:
					if tb.Checked:
						value = "1"
					else:
						value = "0"
					w.writeline(tb.Name + ":" + value);
				else:
					if type(tb) is TextBox:
						w.writeline(tb.Name + ":" + tb.Text);
					else:
						w.WriteLine(tb.Name + ":" + tb.Text);
		finally:
			w.close();
			
	def tb_Leave(self,sender,e):
		self.TransmitValue(sender);
	
	def tb_TextChanged(self,sender,e):
		t = sender
		if not t.Font.Italic:
			t.Font = Font(t.Font, FontStyle.Italic);
			
	def FontNormal(box):
		if box.Font.Italic:
			box.Font = Font(box.Font, FontStyle.Regular);
	
	def ReadMinMax(self,tb,min,max):
		value = self.ReadUserValue(tb);
		if (value < min):
			value = min;
			tb.Text = str(value);
		if (value > max):
			value = max;
			tb.Text = str(value)
		return value;
		
	def ReadUserValue(self,tb):
		tb.Text = tb.Text.replace(',', '.');
		text = tb.Text;
		value = float(text);
		return value;