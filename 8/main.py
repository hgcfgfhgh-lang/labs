import tkinter #GUI
from tkinter import filedialog #диалог выбора файлов
import math


class Circle:
    def __init__(self, x, y, r): #координаты центра круга, радиус
        self.x, self.y, self.r = x, y, r
        self.segments = [] #список сегментов, на которые можно разделить круг
        self.is_colored = False #флаг, указывающий, раскрашен ли круг

    def divide(self, n): #Делит круг на n равных сегментов
        step = 2 * math.pi / n
        self.segments = [(i*step, (i+1)*step) for i in range(n)] #Каждый сегмент хранится как пара углов в радианах
        self.is_colored = False #Сбрасываем флаг раскраски, потому что сегменты изменились

    def draw(self, canvas, colors=None):
        canvas.delete("all") # Очищает холст перед новой отрисовкой
        if colors and self.segments: #Если переданы цвета и сегменты, закрашивает сегменты
            for i, (s,e) in enumerate(self.segments): #Используем polygon, чтобы аппроксимировать сегмент многоугольником. деление дуги на 20 точек.
                points = [self.x, self.y]
                for j in range(21):
                    a = s + (e-s)*j/20
                    points += [self.x+self.r*math.cos(a), self.y-self.r*math.sin(a)]
                canvas.create_polygon(points, fill=colors[i%len(colors)], outline="") #заливает сегмент без обводки. если сегментов больше, чем цветов, цвета повторяются
        canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, self.y+self.r, outline="black")
        for s,e in self.segments:
            canvas.create_line(self.x, self.y, self.x+self.r*math.cos(s), self.y-self.r*math.sin(s), fill="black")
        self.is_colored = bool(colors)

    def move(self, dx, dy, w, h):
        self.x = max(self.r, min(w-self.r, self.x+dx))
        self.y = max(self.r, min(h-self.r, self.y+dy))


#GUI
root = tkinter.Tk() #создаёт главное окно приложения
root.title("Lab8Chenakin") #заголовок
w,h = 400,400
canvas = tkinter.Canvas(root, width=w, height=h, bg="white") #область для рисования 400x400
canvas.pack(pady=10) #автоматически разместить элемент canvas в окне root

circles = []
current = None
colors = ["red","green","blue","yellow","purple","orange"]

#Функции
def create_test():
    global circles, current
    file_path = "test.txt"
    with open(file_path, "w") as f:
        f.write("200 200 50\n150 150 40\n250 250 30\n100 300 60\n")
    load_file(file_path)

def load_file(path=None):
    global circles, current
    if not path: #Если функция вызвана без аргумента
        path = filedialog.askopenfilename(filetypes=[("Text files","*.txt")]) #открываем диалоговое окно выбора файла
    if not path: #Если пользователь нажал Отмена
        return
    circles = []
    with open(path,"r") as f:
        for line in f:
            parts = line.split()
            if len(parts)==3:
                try:
                    x,y,r=map(float,parts)
                    circles.append(Circle(x,y,r))
                except:
                    pass #пропускаем строку
    if circles: current = circles[0]; current.draw(canvas) #первая окружность из списка

def divide_circle():
    if current:
        try:
            n=int(entry.get()) #поле ввода
            current.divide(n)
            current.draw(canvas)
        except: pass

def color_circle():
    if current and current.segments:
        current.draw(canvas, colors)

def move(dx,dy):
    if current:
        current.move(dx,dy,w,h)
        current.draw(canvas, colors if current.is_colored else None)

#Кнопки и ввод
frame = tkinter.Frame(root) #контейнер для виджетов
frame.pack() #Размещает этот фрейм в окне
tkinter.Button(frame,text="Тестовый файл",command=create_test).grid(row=0,column=0)
tkinter.Button(frame,text="Загрузить файл",command=load_file).grid(row=0,column=1)
entry=tkinter.Entry(frame,width=5); entry.grid(row=0,column=2)
tkinter.Button(frame,text="Разделить",command=divide_circle).grid(row=0,column=3)
tkinter.Button(frame,text="Раскрасить",command=color_circle).grid(row=0,column=4)

move_frame=tkinter.Frame(root); move_frame.pack()
tkinter.Button(move_frame,text="↑",command=lambda: move(0,-10)).grid(row=0,column=1)
tkinter.Button(move_frame,text="←",command=lambda: move(-10,0)).grid(row=1,column=0)
tkinter.Button(move_frame,text="→",command=lambda: move(10,0)).grid(row=1,column=2)
tkinter.Button(move_frame,text="↓",command=lambda: move(0,10)).grid(row=2,column=1)

root.mainloop()
