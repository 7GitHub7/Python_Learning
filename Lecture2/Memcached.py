from pymemcache.client.base import Client
import json
import time

# TODO połączenie powinno być otwierane i zamykane w odpowiednich miejsach, tam gdzie używamy - czyli nie tutaj
client = Client('localhost')

class Answer(object):
    id = 0
    PP2 = ""
    ZPO = ""
    KCK = ""
    PwJS = ""
    PDSWWW = ""
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


def append_and_save(answer):
    
    id_list = []
    status = 1

    while status: 

        status = check_id(answer.id)  # sprawdzamy czy id już nie istnieje
        print(status)
        if status != None: return False # jeżeli id istnieje przerywamy i prosimy o nowe id

        id_list, cas = client.gets('id')
        if id_list is None:
            init_pymemcache()
            id_list, cas = client.gets('id')
            id_list = id_list.decode('ascii')
            id_list =json.loads(id_list)
            id_list.append(answer.id)
     
        else:
            id_list = id_list.decode('ascii')
            id_list =json.loads(id_list)
            id_list.append(answer.id)
            
        # time.sleep(10)      // do testu na kilku klientach i sprawdzeniu, że cas rzeczywiście działa(klient który połączy się w ciągu tych 10s dostanie False, ponieważ nadpiszemy atrybut cas)  

        if not status:
            if client.cas('id', json.dumps(id_list), cas):  # sprawdzamy czy od momentu pobrania listy ktoś nie dopisał id do listy przed zapisaniem 
                client.set(str(answer.id), str(answer.toJSON()))  # jeżeli poprzedni warunek został spełniony do wtedy dopiero dodajemy ankietę
                client.close()  # zamykamy połączenie z memcached
                return True
        


def check_id(id):
    return client.get(str(id))

def get_answers():
    
    answers_list = []
    id_value, cas = client.gets('id')
    if id_value is None: return False
    id_value = id_value.decode('ascii')

    id_value = str(id_value)
    id_value =json.loads(id_value)

    for i in id_value:
        answers_list.append(str(client.get(str(i))))
    return answers_list




def form():
    anwser = Answer()
    print(f"Oceń PP2-w ")
    anwser.PP2 = input()
    print(f"Oceń ZPO-lab ")
    anwser.ZPO = input()
    print(f"Oceń KCK-w ")
    anwser.KCK = input()
    print(f"Oceń PwJS-lab ")
    anwser.PwJS = input()
    print(f"Oceń PDSWWW-lab ")
    anwser.PDSWWW = input()
    status = False
    while not status:
        print(f"Podaj sowje unikalne ID ")
        anwser.id = int(input())
        status = append_and_save(anwser) 
        if status: break
        print(f"Takie id istnieje ")

def init_pymemcache():
    client.flush_all()
    l = []
    client.set('id', l)



'''uruchamiamy formularz, jeżeli memcache był wcześniej używany, zalecam wykonać init_pymemcache()
    jeżeli pymemcache jest czysty, wystarczy uruchomić form()'''

form()


'''# jeżeli chcemy zainicjować memcache'''

# init_pymemcache()  


'''
 mozemy wyswietlic wszystkie ankiety w memcache
'''
# result = get_answers() # pobieramy listę ankiet 
# for re in result:
#     print(re)



