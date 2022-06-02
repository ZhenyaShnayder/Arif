t=input("Введите путь к файлу ")
# C:\\Users\\днс\\OneDrive\\Рабочий стол\\new.txt
try:
    f=open(t, "r")
except:
    print("Неправильно был указан путь файла ")
    exit()
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
list1 = sorted(list1, key=lambda x: x.freq,reverse=True)# сортировка списка объектов по атрибуту: freq, создается lambda-функции, которая вернет freq объекта
#5.функция, которая найдет объект типа interval
def searchsymbol(sym, list1):
    for i in range (len(list1)):
        if sym==list1[i].sym:
            return sym
#6.для присвоения left и right
right=0
for i in list1:
    i.left=right
    right+=i.percent
    i.right=right

#7.
# left=0
# right=1
#abccaa [a,c,b]
# for i in list1:
#     left=left+(right-left)*list1[i].left
#     list1[i].left=left
#     right=left+(right-left)*list1[i].right
#     list1[i].right=right
print(list1)
