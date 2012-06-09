from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, SIGNAL, pyqtSignal
from gui import Ui_MainWindow
from europei import read_group
import os.path
import configparser

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

group_a = "http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-a/classifiche.html"
group_b = "http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-b/classifiche.html"
group_c = "http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-c/classifiche.html"
group_d = "http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-d/classifiche.html"

class Ui_Manager():
    def __init__(self):
        self.MainWindow = QtGui.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()
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
        w = QtGui.QLabel('Pos.')
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
                w = QtGui.QLabel(t)
                h.addWidget(w)
                for s in stats:
                    w = QtGui.QLabel(s[1])
                    h.addWidget(w)
                v = self.get_vertical_layout(f)
                v.addLayout(h)

    def update(self):
        self.ui.setupUi(self.MainWindow)
        self.populate()
        """
        filenames = ['A.ini','B.ini','C.ini','D.ini']

        for f in filenames:
            parser = configparser.SafeConfigParser()
            parser.read(f)
            teams = parser.sections()
            v = self.get_vertical_layout(f)
            hboxes = v.children()
            for t, h in teams, hboxes[1:]:
                stats = parser.items(t)
                ws = h.children()
                for s, w in stats, ws:
                    print(s)
                    print(w.getText())
        """
    def call_update(self):
        update_data()
        self.update()

    def connect(self):
        self.ui.actionAggiorna.connect(self.ui.actionAggiorna, SIGNAL('triggered()'), self.call_update)

def create_config(filename, url):

    G = read_group(url)
    parser = configparser.SafeConfigParser()
    parser.add_section(G[1][1])
    parser.add_section(G[2][1])
    parser.add_section(G[3][1])
    parser.add_section(G[4][1])

    parser.set(G[1][1], G[0][0], G[1][0])
    for i in range(2,10):
        parser.set(G[1][1], G[0][i], G[1][i])

    parser.set(G[2][1], G[0][0], G[2][0])
    for i in range(2,10):
        parser.set(G[2][1], G[0][i], G[1][i])

    parser.set(G[3][1], G[0][0], G[3][0])
    for i in range(2,10):
        parser.set(G[3][1], G[0][i], G[1][i])

    parser.set(G[4][1], G[0][0], G[4][0])
    for i in range(2,10):
        parser.set(G[4][1], G[0][i], G[1][i])

    f = open(filename+'.ini', 'w')
    parser.write(f)
    f.close()
    
def fetch_data():
    if not os.path.exists("A.ini"):
        create_config('A', group_a)
    if not os.path.exists("B.ini"):
        create_config('B', group_b)
    if not os.path.exists("C.ini"):
        create_config('C', group_c)
    if not os.path.exists("D.ini"):
        create_config('D', group_d)

def update_data():
    print('updating data...')
    create_config('A', group_a)
    create_config('B', group_b)
    create_config('C', group_c)
    create_config('D', group_d)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    um = Ui_Manager()
    #populate(ui)
    #connect(ui)
    sys.exit(app.exec_())


    
