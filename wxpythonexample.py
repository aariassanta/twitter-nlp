''' wx_run_python_code101.py
the beginning of an very simple "IDE" for Python
tested with Python27 and wxPython291 by vegaseat  15jan2013
'''

import wx
import subprocess
import sys

class MyFrame(wx.Frame):
    def __init__(self, parent, mytitle, mysize):
        wx.Frame.__init__(self, parent, wx.ID_ANY, mytitle, size=mysize)
        self.SetBackgroundColour("#f0f0f0")

        s = "Selecciona Boletín a ejecutar:"
        self.label = wx.StaticText(self, wx.ID_ANY, s)
        #self.edit = wx.TextCtrl(self, wx.ID_ANY,
        #    value="",
        #    size=(300, 180), style=wx.TE_MULTILINE)

        self.result = wx.TextCtrl(self, wx.ID_ANY,
            value="",
            size=(600, 400), style=wx.TE_MULTILINE)

        s = "Run DOUE"
        #self.button = wx.Button(self, wx.ID_ANY, label=s)
        #self.button.SetBackgroundColour=('blue')
#
        #self.button_BOE = wx.Button(self, wx.ID_ANY, label="Run BOE")
        #self.button_BOE.SetBackgroundColour=('blue')

        #gsizer = wx.GridSizer(1, 2, 5, 5)
        #gsizer.AddMany( [(wx.Button(self, wx.ID_ANY, label='Run DOUE'), 0, wx.EXPAND),
        #                (wx.Button(self, wx.ID_ANY, label='Run BOE'), 0, wx.EXPAND)] )

        # define grid for place the buttons
        gsizer = wx.GridSizer(1, 4, 5, 5)

        # button labels to generate
        buttons = [
            'BOE', 'DOUE', 'DOCM', 'DOGC'
        ]

        # create the buttons
        for label in buttons:
            button = wx.Button(self, wx.ID_ANY, label)
            gsizer.Add(button, 0, wx.EXPAND)
            # bind mouse event to an action
            self.Bind(wx.EVT_BUTTON, self.button_click, button)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        flag1 = wx.LEFT|wx.TOP|wx.RIGHT|wx.DOWN|wx.EXPAND
        vsizer.Add(self.label, 0, flag=flag1, border=10)

        vsizer.Add(gsizer, proportion=1, flag=flag1, border=10)

        vsizer.Add(self.result, 0, flag=flag1, border=10)
        self.SetSizer(vsizer)


    def button_click(self, event):
        """run Python button has been clicked"""

        # Get label of button
        label = event.GetEventObject().GetLabel()

        # Get script name to be executed
        script = "ASECORP_" + label + ".py"

        # command to execute Python (use correct path)
        run_python = "python " + script
      
        self.result.WriteText('\n------------\n')
        self.result.WriteText('Ejecutando: ' + label + '\n')
        
        # execute the code and pipe the result to a string
        process = subprocess.Popen(run_python, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        #process = subprocess.run(['python','ASECORP_BOE.py'],
        #                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print

        # redirect stdout line to the Console Window box
        while True:
            line = process.stdout.readline()
            wx.Yield()
            if line.strip() == "":
                pass
            else:
                self.result.WriteText(line.strip())
                self.result.WriteText(str('\n'))
            if not line: break
 
        # wait till completed
        process.wait()
        # optional check 0 --> success
        print(process.returncode)
        # read the result to a string
        #result_str = process.stdout.read()
        # display the result
        self.result.WriteText('Procesado del ' + label + ' Finalizado' + '\n------------\n')


app = wx.App(0)
frame = MyFrame(None, 'The Almost IDE', (640, 520))
frame.Show()
app.MainLoop()