from PyQt4 import QtCore, QtGui
from gui import Ui_TabWidget
from europei import read_group

def populate(ui):
    A = read_group("http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-a/classifiche.html")
    B = read_group("http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-b/classifiche.html")
    C = read_group("http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-c/classifiche.html")
    D = read_group("http://it.eurosport.yahoo.com/calcio/euro-2012/gruppo-d/classifiche.html")
    
    fixed_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)

    for row in A:
        h= QtGui.QHBoxLayout()
        for element in row:
            w = QtGui.QLabel()
            w.setText(element)            
            if element == row[0]:
                #FIXME
                fixed_policy.setHeightForWidth(w.sizePolicy().hasHeightForWidth())
            h.addWidget(w)
        ui.verticalLayout_1.addLayout(h)

    for row in B:
        h= QtGui.QHBoxLayout()
        for element in row:
            w = QtGui.QLabel()
            w.setText(element)
            h.addWidget(w)
        ui.verticalLayout_2.addLayout(h)

    for row in C:
        h= QtGui.QHBoxLayout()
        for element in row:
            w = QtGui.QLabel()
            w.setText(element)
            h.addWidget(w)
        ui.verticalLayout_3.addLayout(h)

    for row in D:
        h= QtGui.QHBoxLayout()
        for element in row:
            w = QtGui.QLabel()
            w.setText(element)
            h.addWidget(w)
        ui.verticalLayout_4.addLayout(h)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TabWidget = QtGui.QTabWidget()
    ui = Ui_TabWidget()
    ui.setupUi(TabWidget)
    TabWidget.show()
    populate(ui)

    sys.exit(app.exec_())


    
