import os
# t=input("Введите путь к файлу ")
l=5#количество вложений
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
    right+=i.percent
    i.right=right
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
f2.write(chr(4).encode('ascii'))#для фиктивных нулей (потом перпишу сюда нормальное значение)
for i in range(256):
    if(frequencies[i]!=0):
        f2.write(chr(i).encode("ascii"))#символ
        f2.write(str(frequencies[i]).encode("ascii"))#частота, соответствующая символу
        f2.write(chr(2).encode("ascii"))#разделитель между символами с частотами
f2.write(chr(3).encode("ascii"))#разделитель между сообщением, которое кодировали и между символами с частотами
#8.Основная функция, будем стараться закодировать 5 символов в 4-х байтах
left=0
right=1
sym = f.read(1)
obj = searchsymbol(sym, list1)
while sym != '':
    #проверку бы еще если break внутри сработал, еще проверка на нули фиктивные
    #получаем промежуток, с которым потом будем работать
    for i in range (l):
        leftward = left
        left = left+(right-left)*obj.left
        right = leftward+(right-leftward)*obj.right
        # print(left, right)
        sym = f.read(1)
        obj = searchsymbol(sym, list1)
        if sym == '':
            break
    bits = 0
    i = 0
    cont = 0
    #берем самую левую точку, которая входит в промежуток [left, right)
    while True:
        if cont >= left and cont < right:#входит в промежуток
            bits << 32-i
            for i in range(l):
                d = 2 ** 8 - 1
                d = d & (bits << 32 - i*8)#!!!!!!!!!сомнительная строчка
                f2.write(chr(d).encode("ascii"))
            break
        bits = bits << 1
        # print(bits+1/(2**i),right)
        if (cont + (1/(2**i))) < right:
            bits = bits | 1
            cont += (1/(2**i))
        i += 1
    print(bits)
f.close()
f2.close()
#подсчёт сжатия
a = os.stat("C:\\Users\\днс\\OneDrive\\Рабочий стол\\new.txt").st_size
b = os.stat("C:\\Users\\днс\\OneDrive\\Рабочий стол\\encr.txt").st_size
print(f"Сжатие: {(b/a)*100}%")