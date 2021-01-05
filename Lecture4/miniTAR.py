import shelve
import argparse
import re

class MiniTARArchive(): 
    def __init__(self,name):
        self.filename = name 
        self.shelf = None
            
    def __enter__(self): 
        self.shelf =  shelve.open(self.filename)
        return self.shelf
        
    def __exit__(self, type, value, traceback):
        self.shelf.close() 

parser = argparse.ArgumentParser()
parser.version = '1.0'
parser.add_argument('-add', '--list_files', nargs='+')
parser.add_argument('-delete_file', type = str, help = "delete specific file <str>") 
parser.add_argument("-delete_all", type=bool, help = "<True/False>")
parser.add_argument("-ls", type=bool, help = "list files <True/False>")
parser.add_argument("-re", type=str, help = "find files based on regex <str>")

args = parser.parse_args()
args = vars(args)

with MiniTARArchive("test_shelf.db") as mta: 

    if args['list_files']:
        lines = []
        for file_ in args['list_files']:
            if file_ in mta:
                raise ValueError(f"Plik {file_} już istnieje w bazie! Najpierw usun plik z bazy!")
            with open(file_, 'r') as fh:
                for line in fh:
                    lines.append(line)
                listToStr = ' '.join([str(len(lines))])     
                listToStr = listToStr +'\n'+' '.join([str(elem) for elem in lines])     
                mta[file_] = listToStr
                    
    if args['ls']:
        my_keys = list(mta.keys())
        for key in my_keys:
            print(f"Nazwa: {key} Długość pliku(ilość lini): {mta[key].split()[0]}")  

    if args['delete_all']:
        my_keys = list(mta.keys())
        for key in my_keys:
            del mta[key]
        print("Usunięto wszystkie pliki pomyślnie")      

    if args["delete_file"]:
        if args["delete_file"] in mta:
            del mta[args["delete_file"]] 
            print("Usunięto pomyślnie")
        else:    
            print("Nie ma takiego pliku")

    if args["re"]:
        my_keys = list(mta.keys())
        for key in my_keys:
            if re.search(args["re"], key):
                print(key)
