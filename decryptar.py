#1.класс интервал
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
#2.считка символов и соответвующих им частот
f = open("C:\\Users\\днс\\OneDrive\\Рабочий стол\\encr.txt", "rb")
quantity = 0
accum2=''#записываем частоту
list1=[]
accum1=''#записываем символ
sym = chr(2)
while sym != chr(3):
    sym = f.read(1).decode("ascii")  #считка символа
    if sym == chr(3):
        break
    accum1 = sym  # считка символа
    sym = f.read(1).decode("ascii")  #считка символа
    while(sym!=chr(2)):
        accum2=accum2+sym
        sym=f.read(1).decode("ascii")
    quantity += int(accum2)#подсчет общего кол-ва символов в тексте
    list1.append(interval(int(accum2), 0, 0, 0, accum1))
    accum2 = ''
#3.запись значений percent, left и right
right = 0
for i in list1:
    i.percent = i.freq / quantity
    i.left = right
    right += i.percent
    i.right = right

print(list1)
#4.основной цикл для раскодирования
f2 = open("C:\\Users\\днс\\OneDrive\\Рабочий стол\\decr.txt", "w")
chet = 0
d = True
while d:
    bits = 0
    #набираем 4 байта
    for j in range(4):
        sym = f.read(1)
        sym = int.from_bytes(sym, 'little')
        bits = bits << 8
        bits = bits | sym
    cont = 0
    mask = 1 << 31
    # находим двоичную дробь
    for z in range(1, 33):
        if mask & bits != 0:
            cont += 1/(2**z)
        mask = mask >> 1
    # print(cont)
    c = True
    # print(list1)
    left = 0
    right = 1
    print(cont)
    while c:
        #print(cont)
        for i in list1:
            if i.right > cont and i.left <= cont:
                # print("1")
                leftward = left
                left = left + (right - left) * i.left
                right = leftward + (right - leftward) * i.right
                if right-left > 1/2**32:
                    f2.write(i.sym)
                    print(i.sym, left, right)
                    chet += 1
                    if quantity == chet:
                        c = False
                        d = False
                    cont = (cont - i.left) / (i.right - i.left)
                else:
                    c = False
                break
f.close()
f2.close()


#сравнение файлов
f1=open("C:\\Users\\днс\\OneDrive\\Рабочий стол\\new.txt", 'r')
f2=open("C:\\Users\\днс\\OneDrive\\Рабочий стол\\decr.txt", 'r')
sym1=f1.read(1)
sym2=f2.read(1)
while sym1 != '' or sym2!='':
    if sym1 != sym2:
        print("Файлы были не равны")
        exit()
print("Файлы были равны ")
