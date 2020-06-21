import pygame
import sys
import math
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import os
import heapq as hq
import time

screen = pygame.display.set_mode((800,800))

class Node:
    def __init__(self, x, y):
        self.i = x
        self.j = y
        self.f = 0  # combination of distance from start and the distance to the end.
        self.g = 0  # distance from the start.
        self.h = 0  # distance to the end.
        self.neighbors = []
        self.previous = None
        self. obs = False
        self.closed = False
        self.value = 1

    def show(self, color, st):

        if not self.closed :
            pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
            pygame.display.update()

    def path(self, color, st):
        pygame.draw.rect(screen, color, (self.i * w, self.j * h, w, h), st)
        pygame.display.update()

    def addNeighbors(self, grid):
        i = self.i
        j = self.j
        if i < col - 1 and grid[self.i + 1][j].obs == False:
            self.neighbors.append(grid[self.i + 1][j])
        if i > 0 and grid[self.i - 1][j].obs == False:
            self.neighbors.append(grid[self.i - 1][j])
        if j < row - 1 and grid[self.i][j + 1].obs == False:
            self.neighbors.append(grid[self.i][j + 1])
        if j > 0 and grid[self.i][j - 1].obs == False:
            self.neighbors.append(grid[self.i][j - 1])





col = 50
grid = [0 for i in range(col)]
row = 50
openSet = []
closedSet = set()
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
grey = (220, 220, 220)
w = 800 / col
h = 800 / row

for i in range(col):
    grid[i] = [0 for i in range(row)]


for i in range(col):
    for j in range(row):
        grid[i][j] = Node(i, j)


start = grid[12][5]
end = grid[3][6]

for i in range(col):
    for j in range(row):
        grid[i][j].show((255, 255, 255), 1)

for i in range(0,row):
    grid[0][i].show(grey, 0)
    grid[0][i].obs = True
    grid[col-1][i].obs = True
    grid[col-1][i].show(grey, 0)
    grid[i][row-1].show(grey, 0)
    grid[i][0].show(grey, 0)
    grid[i][0].obs = True
    grid[i][row-1].obs = True


def onsubmit():
    global start
    global end
    global option
    st = startBox.get().split(',')
    ed = endBox.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    option = variable.get()
    window.quit()
    window.destroy()


window = Tk()
label = Label(window, text='Start(x<49,y<49): ')
startBox = Entry(window)
label1 = Label(window, text='End(x<49,y<49): ')
endBox = Entry(window)
label2 = Label(window, text="Algorithm: ")
choices = ["A-Star", "Dijkstra"]
variable = StringVar(window)
variable.set("A-Star")
algo = OptionMenu(window, variable, *choices)
var = IntVar()
showPath = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)

submit = Button(window, text='Submit', command=onsubmit)

showPath.grid(columnspan=2, row=3)
submit.grid(columnspan=2, row=4)
label1.grid(row=1, pady=3)
endBox.grid(row=1, column=1, pady=3)
startBox.grid(row=0, column=1, pady=3)
label.grid(row=0, pady=3)
label2.grid(row=2, column=1)
algo.grid(row=2, column=1)

window.update()
mainloop()

pygame.init()

if option == "A-Star":
    hq.heappush(openSet, (start.h, id(start), start))
else:
    hq.heappush(openSet, (start.g, id(start), start))


def mousePress(x):
    t = x[0]
    w = x[1]
    g1 = t // (800 // col)
    g2 = w // (800 // row)
    acess = grid[g1][g2]
    if acess != start and acess != end:
        if acess.obs == False:
            acess.obs = True
            acess.show((255, 255, 255), 0)


end.show((255, 8, 127), 0)
start.show((255, 8, 127), 0)

loop = True
while loop:
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.QUIT:
            pygame.quit()
        if pygame.mouse.get_pressed()[0]:
            try:
                pos = pygame.mouse.get_pos()
                mousePress(pos)
            except AttributeError:
                pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                loop = False
                break

for i in range(col):
    for j in range(row):
        grid[i][j].addNeighbors(grid)


def heurisitic(n, e):
    d = math.sqrt((n.i - e.i)**2 + (n.j - e.j)**2)
    #d = abs(n.i - e.i) + abs(n.j - e.j)
    return d
print(openSet)


def dijkstras():
    end.show((255, 8, 127), 0)
    start.show((255, 8, 127), 0)
    if len(openSet) > 0:
        current = openSet[0][2]

        if current == end:
            print('done', current.g)
            print("%s seconds"%(time.time() - start_time))
            start.show((255, 8, 127), 0)
            temp = current.g
            for i in range(round(current.g)):
                current.closed = False
                current.show((0, 0, 255), 0)
                current = current.previous
            end.show((255, 8, 127), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', (
                        'The program finished, the shortest distance \n to the path is ' + str(
                    temp) + ' blocks away, \n would you like to re run the program?'))
            if result:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        hq.heappop(openSet)
        closedSet.add(current)
        neighbors = current.neighbors
        for i in range(len(neighbors)):
            nodes = set([x[2] for x in openSet])
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tmpG = current.g + current.value
                if neighbor in nodes:
                    if neighbor.g > tmpG:
                        neighbor.g = tmpG
                else:
                    neighbor.g = tmpG
                    hq.heappush(openSet, (neighbor.g, id(neighbor), neighbor))

            if neighbor.previous is None:
                neighbor.previous = current

    if var.get():
        for i in range(len(openSet)):
            openSet[i][2].show(green, 0)

        for i in closedSet:
            if i != start:
                i.show(red, 0)

    current.closed = True

def aStar():
    end.show((255, 8, 127), 0)
    start.show((255, 8, 127), 0)
    if len(openSet) > 0:
        current = openSet[0][2]

        if current == end:
            print('done', current.f)
            print("%s seconds" % (time.time() - start_time))
            start.show((255, 8, 127), 0)
            temp = current.f
            for i in range(round(current.f)):
                current.closed = False
                current.show((0, 0, 255), 0)
                current = current.previous
            end.show((255, 8, 127), 0)

            Tk().wm_withdraw()
            result = messagebox.askokcancel('Program Finished', (
                        'The program finished, the shortest distance \n to the path is ' + str(
                    temp) + ' blocks away, \n would you like to re run the program?'))
            if result:
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                ag = True
                while ag:
                    ev = pygame.event.get()
                    for event in ev:
                        if event.type == pygame.KEYDOWN:
                            ag = False
                            break
            pygame.quit()

        hq.heappop(openSet)
        closedSet.add(current)
        neighbors = current.neighbors
        for i in range(len(neighbors)):
            nodes = set([x[2] for x in openSet])
            neighbor = neighbors[i]
            if neighbor not in closedSet:
                tmpG = current.g + current.value
                if neighbor in nodes:
                    if neighbor.g > tmpG:
                        neighbor.g = tmpG
                else:
                    neighbor.g = tmpG
                    neighbor.h = heurisitic(neighbor, end)
                    neighbor.f = neighbor.g + neighbor.h
                    hq.heappush(openSet, (neighbor.f, id(neighbor), neighbor))

            neighbor.h = heurisitic(neighbor, end)
            neighbor.f = neighbor.g + neighbor.h

            if neighbor.previous is None:
                neighbor.previous = current

    if var.get():
        for i in range(len(openSet)):
            openSet[i][2].show(green, 0)

        for i in closedSet:
            if i != start:
                i.show(red, 0)

    current.closed = True


start_time = time.time()
while True:
    ev = pygame.event.poll()
    if ev.type == pygame.QUIT:
        pygame.quit()
        exit()
    pygame.display.update()
    if option == "A-Star":
        aStar()
    else:
        dijkstras()
