import sys
import time
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton, QProgressBar, QVBoxLayout, QApplication,QProgressDialog, QApplication, QWidget, QListWidget, QLabel, QVBoxLayout,QHBoxLayout
from PyQt5.QtWidgets import QLineEdit,QLabel



client_list = []

class Client():
  name = "Test"  
  time_in_queue = 1  
  number_of_files = 0
  size = 0
  weight = 0

 

  def time_increment(self):
    self.time_in_queue += 1

  def files_decrement(self):
    self.number_of_files -= 1
  
  def __init__(self, size, number_of_files, name ):
    self.number_of_files = number_of_files
    self.size = size
    self.name = name
    

  def __lt__(self, other):
         return self.weight < other.weight
  
  
class Thread(QThread):
    _signal = pyqtSignal(int)
    _name_signal = pyqtSignal(str)
    
    def __init__(self):
        super(Thread, self).__init__()
        

    def __del__(self):
        self.wait()

    def run(self):
        while 1:
            time.sleep(0.1)
            for client in client_list:
                client.weight = client.number_of_files  /  client.time_in_queue
                client_list.sort()
                
            if len(client_list) > 0:
                client = client_list[0] 
                if client.number_of_files > 0:
                    client.files_decrement()

                    self._name_signal.emit(client.name)

                    if client in client_list:
                        if client.number_of_files == 0:
                            client_list.remove(client)
                    
                    for i in range(100):
                        time.sleep(client.size/10000)
                        self._signal.emit(i)

                              
class Time(QThread):
    def __init__(self):
        super(Time, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        while 1:
            time.sleep(1)
            for client in client_list:
                client.time_increment()
                


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.setWindowTitle('LoadBalancer')
        self.btn_add = QPushButton('Dodaj')
        self.btn_start = QPushButton('Start')
        self.btn_start.clicked.connect(self.btnFunc)
        self.btn_add.clicked.connect(self.add_client)
        self.pbar1 = QProgressDialog("Client1",None,0,100)
        self.pbar2 = QProgressDialog("Client2",None,0,100)
        self.pbar3 = QProgressDialog("Client3",None,0,100)
        self.pbar4 = QProgressDialog("Client4",None,0,100)
        self.pbar5 = QProgressDialog("Client5",None,0,100)
        self.pbar1.setValue(0)
        self.pbar2.setValue(0)
        self.pbar3.setValue(0)
        self.pbar4.setValue(0)
        self.pbar5.setValue(0)
   
        # client_list.append(Client(1000,4,"Wera"))
        # client_list.append(Client(1000,7,"Arek"))
        # client_list.append(Client(1000,10,"Andrzej"))
        
        self.list = QListWidget()
        self.name_input = QLineEdit(self)
        self.number_input = QLineEdit(self)
        self.size_input = QLineEdit(self)
        self.number_input.setText("6")
        self.size_input.setText("1000")
        self.name_input.setText("Test")


        for index,client in enumerate(client_list):
            self.list.addItem(f"Klient {client.name}, pozostało plików {client.number_of_files}, waga = {round(client.weight,2)}")

        self.resize(800, 700)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox_labels = QHBoxLayout()
        self.vbox.addWidget(self.pbar1)
        self.vbox.addWidget(self.pbar2)
        self.vbox.addWidget(self.pbar3)
        self.vbox.addWidget(self.pbar4)
        self.vbox.addWidget(self.pbar5)
        self.vbox.addWidget(self.list)
        self.hbox.addWidget(self.name_input)
        self.hbox.addWidget(self.number_input)
        self.hbox.addWidget(self.size_input)        
        self.hbox_labels.addWidget(QLabel("Nazwa", self))
        self.hbox_labels.addWidget(QLabel("Ilosc", self))
        self.hbox_labels.addWidget(QLabel("Wielkosc", self))
        self.vbox.addLayout(self.hbox_labels)
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.btn_add)
        self.vbox.addWidget(self.btn_start)
        self.setLayout(self.vbox)
        self.show()

        self.thread6 = Time()
        self.thread6.start()


    def add_client(self):
        client_list.append(Client(int(self.size_input.text()),int(self.number_input.text()),self.name_input.text()))
        self.list.clear()

        for index,client in enumerate(client_list):
            self.list.addItem(f"Klient {client.name}, pozostało plików {client.number_of_files}, waga = {round(client.weight,2)}")


    def btnFunc(self):
        self.thread = Thread()
        self.thread._signal.connect(self.signal_accept1)
        self.thread._name_signal.connect(self.signal_accept1)
        self.thread.start()

        self.thread1 = Thread()
        self.thread1._signal.connect(self.signal_accept2)
        self.thread1._name_signal.connect(self.signal_accept2)
        self.thread1.start()

        self.thread2 = Thread()
        self.thread2._signal.connect(self.signal_accept3)
        self.thread2._name_signal.connect(self.signal_accept3)
        self.thread2.start()

        self.thread3 = Thread()
        self.thread3._signal.connect(self.signal_accept4)
        self.thread3._name_signal.connect(self.signal_accept4)
        self.thread3.start()

        self.thread4 = Thread()
        self.thread4._signal.connect(self.signal_accept5)
        self.thread4._name_signal.connect(self.signal_accept5)
        self.thread4.start()

        
     

    def signal_accept1(self, msg):  
        try:    
            self.pbar1.setValue(int(msg))
        except ValueError:
            self.pbar1.setLabelText(str(msg))
            self.refresh()

        if self.pbar1.value() == 99:
            self.pbar1.setValue(0)

           

    def signal_accept2(self, msg):

        try:    
            self.pbar2.setValue(int(msg))
        except ValueError:
            self.pbar2.setLabelText(str(msg))
            self.refresh()

       
        if self.pbar2.value() == 99:
            self.pbar2.setValue(0) 

            
    def signal_accept3(self, msg):

        try:    
            self.pbar3.setValue(int(msg))
        except ValueError:
            self.pbar3.setLabelText(str(msg))
            self.refresh()
        
        if self.pbar3.value() == 99:
            self.pbar3.setValue(0)

            
           

    def signal_accept4(self, msg):
        
        try:    
            self.pbar4.setValue(int(msg))
        except ValueError:
            self.pbar4.setLabelText(str(msg))
            self.refresh()

        if self.pbar4.value() == 99:
            self.pbar4.setValue(0)
            
           

    def signal_accept5(self, msg):
        try:    
            self.pbar5.setValue(int(msg))
        except ValueError:
            self.pbar5.setLabelText(str(msg))
            self.refresh()

        if self.pbar5.value() == 99:
            self.pbar5.setValue(0)

          
    def refresh(self):
        self.list.clear()
        for index,client in enumerate(client_list):
            self.list.addItem(f"Klient {client.name}, pozostało plików {client.number_of_files}, waga = {round(client.weight,2)}")

               

            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())