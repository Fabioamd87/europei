import urllib.request
from html.parser import HTMLParser

class TableParser(HTMLParser):

    def reset(self):                       
        # extend (called by SGMLParser.__init__)
        #my variables
        print('getting data...')
        self.inside_table_element = False
        self.inside_results_element = False
        self.data = []
        HTMLParser.reset(self)
        
    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            tableclass = [v for k, v in attrs if k=='class']
            if tableclass:
                tableclass = tableclass[0]
                if tableclass == 'football':
                    self.inside_table_element = True
                if tableclass == 'fixtures-results':
                    self.inside_results_element = True

    def handle_endtag(self, tag):
        if tag == 'table' and self.inside_table_element:
            self.inside_table_element = False
        if tag == 'table' and self.inside_results_element:
            self.inside_results_element = False
                

    def handle_data(self, data):
        "Handle the table values."

        if self.inside_table_element:
            if data != ('\\n '):
                data = data.strip('\\n ')
                self.data.append(data)

        if self.inside_results_element:
            if data != ('\\n '):
                data = data.strip('\\n ')
                self.data.append(data)
        

def read_results(url):
    sock = urllib.request.urlopen(url)
    parser = TableParser(strict=False)
    parser.feed(str(sock.read()))
    sock.close()
    parser.close()
    #salto i primi 2
    parser.data = parser.data[2:]
    #tolgo gli elementi vuoti
    while parser.data.count('')>0:
        parser.data.remove('')
    #tolgo stringe inutili
    parser.data.remove('Quarti di finale')
    parser.data.remove('Semifinale')
    parser.data.remove('Finale')
    #raccolgo 6 elementi
    i=0
    t=[]
    tab=[]
    print(parser.data)
    for d in parser.data:
        t.append(d)
        i+=1
        if i == 6:
            i=0
            tab.append(t)
            t=[]

    tmod = [t[0]]   
    tmod.append('F')
    for item in t[1:]:
        tmod.append(item)
    print(tmod)
    tab.append(tmod)
    return(tab)

def read_group(url):
    sock = urllib.request.urlopen(url)
    parser = TableParser(strict=False)
    parser.feed(str(sock.read()))
    sock.close()
    parser.close()

    i=0
    t=[]
    tab=[]
    for d in parser.data:
        t.append(d)
        i+=1
        if i == 10:
            i=0
            tab.append(t)
            t=[]
    return tab
