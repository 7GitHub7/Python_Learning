import re


# recall: * - 0 lub więcej razy,
#          + jeden lub więcej, 
#           ? występuje lub nie'
# 
# \d equivalent to [0-9]
# \D: non-digit (i.e. [^0-9]
# \s: whitespace, \S: non-whitespace
# \w: any alphanumerical ([a-zA-Z0-9_]), \W: the opposite


s = "wlazł kotek na płotek"
# s = "wlazł"
# print(re.match("wlazł", s), re.match("kot", s))  # <re.Match object; span=(0, 5), match='wlazł'> None


# m1 = re.search("tek", s)  # object of class re.Match
# if m1 != None:
#   print(m1.start(), m1.end())  # 8 11


# m2 = re.search("[kł]ot", s)
# if m2 != None:
#   print(m2.start(), m2.end())  # 6 9


def findAllAndPrint(pattern, string):
  for match in re.finditer(pattern, string):  # or: ... in re.findall(...)
    st, en = match.start(), match.end()
    print(st, en, string[st:en], end = "   ")
  print()


# findAllAndPrint("[kł]ot", s)  # 6 9 kot   16 19 łot
# findAllAndPrint("a{3,}", "aa... aaaa! ab aacaaaAaaAaaaaa")  # 6 10 aaaa   18 21 aaa   25 30 aaaaa
# findAllAndPrint("go+l", "gol! goool! Jest gooooool!!!") # 0 3 gol   5 10 goool   17 25 gooooool

# findAllAndPrint("<.+>", "<html><body><div><p>Bla-bla...</p></div></body></html>")
# # 0 54 <html><body><div><p>Bla-bla...</p></div></body></html>

# findAllAndPrint("<.+?>", "<html><body><div><p>Bla-bla...</p></div></body></html>")
# # 0 6 <html>   6 12 <body>   12 17 <div>   17 20 <p>   30 34 </p>   34 40 </div>   40 47 </body>   47 54 </html>

s = "Dziś Pan profesor ma urodziny. Życzę panu profesorowi dużo zdrowia i podwyżki profesorskiej pensji, tu prezent dla pana (kapelusz panama) i niech pan nie panikuje!"
# --> "Dziś Pan Profesor ma urodziny. Życzę Panu Profesorowi dużo zdrowia i podwyżki profesorskiej pensji, tu prezent dla Pana (kapelusz panama) i niech Pan nie panikuje!"

# print(re.sub("pan(?=(a |u | ))|profesor(?=[^s])", lambda m: m.group(0).title(), s))


# # ZADANIA
# # 1) Proszę zmodyfikować przykład z HTML tak, aby zwracane były tylko znaczniki otwierające.
findAllAndPrint("<[^/]+?>", "<html><body><div><p>Bla-bla...</p></div></body></html>")

# # 2) Proszę rozbić (re.split) podany string na nie-literze (łacińskiej). 
# #    Przykład: "Rocky 14 Już! W! Kinach!" --> ['Rocky', '', '', '', 'Ju', '', '', 'W', '', 'Kinach', '']
s = "Rocky 14 Już! W! Kinach!"
print(re.split('[^(a-z)^(A-Z)]',s))
# # 3) W przekazanym stringu znajdź wszystkie słowa powtarzające się po 1 znaku odstępu, 
# #    wyświetl oddzielając pionową kreską; przykład:
# #    "- Jadę do Baden-Baden. - A ja do do Gorzowa-Gorzowa." --> Baden-Baden|do do|Gorzowa-Gorzowa|
# #    Wskazówka: named groups ( https://docs.python.org/3/library/re.html, (?P<name>...) )
# print((?P<name>group))
s = "- Jadę do Baden-Baden. - A ja do do Gorzowa-Gorzowa."
pattern = '(?P<name>\w+).(?P=name)'
temp_string = list(s)
for i in re.finditer(pattern,s):
    temp_string[i.start()-1] = "|"
    temp_string[i.end()] = "|"
print("".join(temp_string))
