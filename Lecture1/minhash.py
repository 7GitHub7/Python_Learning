"""1"""

# akapity.txt, 11 blocks of text separeted by empty line
#DONE
"""2"""

#DONE
"""3"""
import re
import uuid
import time


filename = "akapity.txt"
strings_list = []

with open(filename) as f:
    content = f.readlines()
for line in content:
    if re.match(r'^\s*$', line): #has only \t\n\r and whitespace
        continue
    else:
         strings_list.append(line.rstrip()) 

#seed list
seed_list = []
for i in range(100):
    seed_list.append(uuid.uuid4().int & (1<<64)-1)


def getHash(chars,i):
    return hash(chars)^seed_list[i]

"""4"""

time1 = time.time()
Q = 15  #
string_length = 0  # string length
substring_start = 0
substring_end = 0
string_hash_list = []
j = 0

#iterate for strings
for string in strings_list:   
    string_length = len(string)
    string_hash_list.append([])
    # iterate seeds list
    for i in range(100):
        temp_hash_list = []
        substring_start = 0
        substring_end = 15
        # generate hash list based on seed from list above and chars from string with step 15
        for k in range(string_length - Q + 1):
            substring_end = substring_start + Q
            txt = string[substring_start:substring_end]
            temp_hash_list.append(getHash(txt,i))
            substring_start = substring_end 
        # find min hash value and put to list (100 hashes per string)    
        string_hash_list[j].append(min(temp_hash_list))        
    j+=1

time2 = time.time()   

"""5"""
counter = 0 
#count the same hashes in lists, if greater or equals than 30 then print message  
for j in range(len(string_hash_list) - 1):
    for i in range(j+1,len(string_hash_list)-1):
        counter = 0
        for hash_s in string_hash_list[j]:
            if string_hash_list[i].count(hash_s) > 0:
                counter+=1

        if counter >= 30:
            print("Akapity: {} oraz {} są podobne. Ilość powtórzeń to: {}".format(i,j, counter))

print(time2-time1)





