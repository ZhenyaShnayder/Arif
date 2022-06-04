import os
# t=input("Введите путь к файлу ")
# C:\\Users\\днс\\OneDrive\\Рабочий стол\\new.txt
# try:
#     f=open(t, "r")
# except:
#     print("Неправильно был указан путь файла ")
#     exit()
f=open("C:\\Users\\днс\\OneDrive\\Рабочий стол\\new.txt", "r")
# 1.подсчет частот
# создание псевдо-ассоциативного массива
frequencies=[0 for i in range (256)]
quantity=0
sym=f.read(1)
while sym!='':
    frequencies[ord(sym)] +=1
    quantity+=1
    sym=f.read(1)
f.seek(0)
#2.класс интервал
class interval:
    #конструктор
    def __init__(self, freq, percent, left, right, sym):
        self.freq=freq
        self.percent=percent
        self.left=left
        self.right=right
        self.sym = sym
    def __str__(self):
        return self.sym+' freq='+str(self.freq)+' percent='+str(self.percent)+' left='+str(self.left)+' right='+str(self.right)
    def __repr__(self):
        return f"sym={self.sym}, freq={self.freq}, percent={self.percent}, left={self.left}, right={self.right};"
#3.Создание списка
list1=[]
for i in range (256):
    if frequencies[i] != 0:
        list1.append(interval(frequencies[i], frequencies[i]/quantity, 0, 0, chr(i)))
#4.сортировка списка по частотам, сортировка от наибольшей к наименьшей частоте
list1 = sorted(list1, key=lambda x: x.freq, reverse=True)# сортировка списка объектов по атрибуту: freq, создается lambda-функции, которая вернет freq объекта
#5.функция, которая найдет объект типа interval
def searchsymbol(sym, list1):
    for i in list1:
        if sym == i.sym:
            return i
#6.для присвоения left и right значений
right=0
for i in list1:
    i.left=right
    right += i.percent
    i.right = right
print(list1)
#7.Сразу запишем в файл, в котором будет закодированная информация, частоты и символы
# way=input("Введите путь к файлу ")
# f2=open("C:\\Users\\днс\\OneDrive\\Рабочий стол\\encr.txt", "wb")
# try:
#     f2=open(way, "wb")
# except:
#     print("Неправильно был указан путь файла ")
#     exit()
f2=open("C:\\Users\\днс\\OneDrive\\Рабочий стол\\encr.txt", "wb")
for i in list1:
        f2.write(i.sym.encode("ascii"))#символ
        f2.write(str(i.freq).encode("ascii"))#частота, соответствующая символу
        f2.write(chr(2).encode("ascii"))#разделитель между символами с частотами
f2.write(chr(3).encode("ascii"))#разделитель между сообщением, которое кодировали и между символами с частотами
#8.Основная функция, будем стараться закодировать 5 символов в 4-х байтах
flag = True
sym = f.read(1)
while flag:
    left = 0
    right = 1
    #получаем промежуток, с которым потом будем работать
    l = 0
    while True:
        obj = searchsymbol(sym, list1)
        leftward = left
        left2 = left + (right - left) * obj.left
        right2 = leftward + (right - leftward) * obj.right
        if (right2-left2) > 1/2**32:
            # print(sym, left2, right2)
            sym = f.read(1)
            left = left2
            right = right2
            if sym == '':
                flag = False
                break
        else:
            break
    # print("+")
    bits = 0
    i = 1
    cont = 0
    #берем точку, которая входит в промежуток [left, right)
    for i in range(1, 33):
        bits = bits << 1
        if cont+1/2**i < right:
            cont += 1/2**i
            bits = bits | 1
    # print(cont)
    for i in range(4):
        d = 255
        d = d & (bits >> 24 - i*8)
        f2.write(d.to_bytes(1, byteorder='little'))
f.close()
f2.close()
#подсчёт сжатия
a = os.stat("C:\\Users\\днс\\OneDrive\\Рабочий стол\\new.txt").st_size
b = os.stat("C:\\Users\\днс\\OneDrive\\Рабочий стол\\encr.txt").st_size
print(f"Сжатие: {(b/a)*100} %")