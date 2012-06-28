from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, SIGNAL, pyqtSignal
from EuropeiWindow import MainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

group_a = "http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-a/classifiche.html"
group_b = "http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-b/classifiche.html"
group_c = "http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-c/classifiche.html"
group_d = "http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-d/classifiche.html"
results = "http://it.eurosport.yahoo.com/calcio/europei/calendario-risultati/"

flags = os.listdir('flags')
TEAMS = []
for f in flags:
    f = f.strip('.gif')
    TEAMS.append(f)

#systray.showMessage('QtNotes', 'Application minimized')

class TrayIcon(QtGui.QSystemTrayIcon):
    """creo la tray aggiungendo un segnale al click"""
    def __init__(self):
        QtGui.QSystemTrayIcon.__init__(self)

    def clicked(self):
        self.activated(QtGui.QSystemTrayIcon.Trigger)

class Ui_Manager():
    def __init__(self):
        self.MainWindow = MainGUI()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        
        trayicon = QtGui.QIcon('tray.png')
        self.tray = TrayIcon()
        self.tray.setIcon(trayicon)
        self.tray.setParent(self.MainWindow)
        self.tray.setContextMenu(self.ui.menuMenu)
        #QtCore.QObject.connect(self.ui.quitAction,  QtCore.SIGNAL("triggered()"), ui.QuitApp)
        #QtCore.QObject.connect(self.ui.showAction,  QtCore.SIGNAL("triggered()"), window.ShowWindow)
        self.tray.show()
        
        fetch_data()
        self.connect()
        self.populate()

    def get_vertical_layout(self,filename):
        """know for every group the respective QVboxLayout"""
        if filename == 'A.ini':
            return self.ui.verticalLayout_1
        if filename == 'B.ini':
            return self.ui.verticalLayout_2
        if filename == 'C.ini':
            return self.ui.verticalLayout_3
        if filename == 'D.ini':
            return self.ui.verticalLayout_4

    def add_titles(self,f):
        """create the titles of the table"""
        h= QtGui.QHBoxLayout()
        w = QtGui.QLabel('Squadra')
        h.addWidget(w)
        w = QtGui.QLabel()
        h.addWidget(w)
        w = QtGui.QLabel('P.ti')
        h.addWidget(w)
        w = QtGui.QLabel('G')
        h.addWidget(w)
        w = QtGui.QLabel('V')
        h.addWidget(w)
        w = QtGui.QLabel('N')
        h.addWidget(w)
        w = QtGui.QLabel('S')
        h.addWidget(w)
        w = QtGui.QLabel('Gf')
        h.addWidget(w)
        w = QtGui.QLabel('Gs')
        h.addWidget(w)
        w = QtGui.QLabel('+/-')
        h.addWidget(w)
        v = self.get_vertical_layout(f)
        v.addLayout(h)

    def populate(self):

        filenames = ['A.ini','B.ini','C.ini','D.ini']
        
        for f in filenames:
            self.add_titles(f)
            parser = configparser.SafeConfigParser()
            parser.read(f)
            teams = parser.sections()
            for t in teams:
                stats = parser.items(t)
                h= QtGui.QHBoxLayout()
                if t == 'Repubblica Ceca':
                    w = QtGui.QLabel('Rep. Ceca')
                else:
                    w = QtGui.QLabel(t)
                h.addWidget(w)
                image = QtGui.QLabel()
                imagepath = self.get_flag(t)
                image.setPixmap(QtGui.QPixmap(_fromUtf8(imagepath)))
                h.addWidget(image)
                #remove the position of the team
                stats.pop(2)
                for s in stats:
                    w = QtGui.QLabel(s[1])
                    h.addWidget(w)
                v = self.get_vertical_layout(f) #get the vertical layout of the tab group
                v.addLayout(h)
            #adding results
            h= QtGui.QHBoxLayout()
            w = QtGui.QLabel('Risultati Partite')
            h.addWidget(w)
            v.addLayout(h)
            
            parser = configparser.SafeConfigParser() #reset the parser ps: better way?
            parser.read('results.ini')
            sections = parser.sections()
            
            for s in sections:
                #control if a metch belong to that group
                if parser.get(s,'gruppo') == f[0]: #the first letter of the file (the group)
                    #DEBUG print(parser.items(s))
                    items = parser.items(s)
                    h= QtGui.QHBoxLayout()
                    items.pop(1) #remove the gruop information
                    for i in items:
                        value = i[1]
                        w = QtGui.QLabel(value)
                        h.addWidget(w)                        
                    v.addLayout(h)
        parser = configparser.SafeConfigParser()
        parser.read('results.ini')
        sections = parser.sections()
        for s in sections:
            if parser.get(s,'gruppo') == 'QF1' or parser.get(s,'gruppo') == 'QF2' or parser.get(s,'gruppo') == 'QF3' or parser.get(s,'gruppo') == 'QF4':
                items = parser.items(s)
                h= QtGui.QHBoxLayout()
                #remove the gruop information
                items.pop(1)
                for i in items:
                    value = i[1]
                    w = QtGui.QLabel(value)
                    h.addWidget(w)
                    if value in TEAMS:
                        image = QtGui.QLabel()
                        imagepath = self.get_flag(value)
                        image.setPixmap(QtGui.QPixmap(_fromUtf8(imagepath)))
                        h.addWidget(image)
                self.ui.quarti_finale.addLayout(h)
            if parser.get(s,'gruppo') == 'SF1' or parser.get(s,'gruppo') == 'SF2':
                items = parser.items(s)
                h= QtGui.QHBoxLayout()
                #remove the gruop information
                items.pop(1)
                for i in items:
                    value = i[1]
                    w = QtGui.QLabel(value)
                    h.addWidget(w)
                    if value in TEAMS:
                        image = QtGui.QLabel()
                        imagepath = self.get_flag(value)
                        image.setPixmap(QtGui.QPixmap(_fromUtf8(imagepath)))
                        h.addWidget(image)
                self.ui.semi_finale.addLayout(h)
            if parser.get(s,'gruppo') == 'F':
                items = parser.items(s)
                h= QtGui.QHBoxLayout()
                #remove the gruop information
                items.pop(1)
                for i in items:
                    value = i[1]
                    w = QtGui.QLabel(value)
                    h.addWidget(w)
                    if value in TEAMS:
                        image = QtGui.QLabel()
                        imagepath = self.get_flag(value)
                        image.setPixmap(QtGui.QPixmap(_fromUtf8(imagepath)))
                        h.addWidget(image)
                self.ui.finale.addLayout(h)

    def get_flag(self,t):
        return('flags/'+t+'.gif')

    def update(self):
        #controlla prima la connessione
        self.ui.setupUi(self.MainWindow)
        self.populate()

    def call_update(self):
        update_data()
        self.update()

    def connect(self):
        self.ui.actionAggiorna.connect(self.ui.actionAggiorna, SIGNAL('triggered()'), self.call_update)
        self.ui.actionEsci.connect(self.ui.actionEsci, SIGNAL('triggered()'), QtGui.qApp.quit)
        #self.tray.connect(self.tray,  SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.test)

    def test(self,r):
        if r == 3:
            if self.MainWindow.isActiveWindow():
                self.MainWindow.hide()
            else:                 
                self.MainWindow.show()

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    um = MainWindow()
    um.show()
    sys.exit(app.exec_())


    
