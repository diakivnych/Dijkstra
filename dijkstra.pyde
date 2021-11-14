import math
import random

from collections import deque

# global variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

objects = {
            'graph': None,
            'selected': -1,
            'v1': -1,
            'v2': -1,
            'dijkstra_dist': [],
            'dijkstra_way': [],
           }


class Vertex:
    def __init__(self, x, y, cl=WHITE):
        self.x = x
        self.y = y
        self.cl = cl
    
    def move(self, dx, dy):
        self.x += dx * 2
        self.y += dy * 2

class Graph:
    def __init__(self, n, vtx, edges):
        self.n = n
        self.vtx = vtx
        self.edges = edges
    
    def draw(self):
        for v in range(self.n):
            for to, w in self.edges[v]:
                x1, y1 = self.vtx[v].x, self.vtx[v].y
                x2, y2 = self.vtx[to].x, self.vtx[to].y
                stroke(*BLACK)
                line(x1, y1, x2, y2)
                
                c = 20
                lam = (distance(x1, y1, x2, y2) - c ) / c
                x = (x1 + lam * x2) / (1 + lam)
                y = (y1 + lam * y2) / (1 + lam)
                a1_ = -160 * math.pi / 180
                new_x1 = (x2 - x) * math.cos(a1_) - (y2 - y) * math.sin(a1_) + x
                new_y1 = (x2 - x) * math.sin(a1_) + (y2 - y) * math.cos(a1_) + y
                
                a2_ = 160 * math.pi / 180
                new_x2 = (x2 - x) * math.cos(a2_) - (y2 - y) * math.sin(a2_) + x
                new_y2 = (x2 - x) * math.sin(a2_) + (y2 - y) * math.cos(a2_) + y
                fill(*BLUE)
                triangle(x2, y2, new_x1, new_y1, new_x2, new_y2)
                
                #weights
                textSize(10)
                fill(*RED)
                x_ = (self.vtx[v].x + self.vtx[to].x ) / 2
                y_ = (self.vtx[v].y + self.vtx[to].y ) / 2
                
                if self.vtx[v].x <= self.vtx[to].x:
                    text(str(v) + '->' + str(to) + ' w = ' + str(w), x_-25, y_-10)
                else:
                    text(str(v) + '->' + str(to) + ' w = ' + str(w), x_-5, y_+10)    
                
        for i in range(self.n):
            v = self.vtx[i]
            
            stroke(*BLACK)
            fill(*v.cl)
            circle(v.x, v.y, 30)
            
            textSize(20)
            fill(*BLACK)
            text(str(i), v.x - 5, v.y + 7)
        
        self.dijkstra()
        self.dijkstra_draw()
    
    def dijkstra(self):
        st = objects['v1']
        finish = objects['v2']
        if st == -1 or finish == -1:
            return
        
        used = [False for i in range(self.n)]
        d = [100 for i in range(self.n)]
        pr = [-1 for i in range(self.n)]
        q = set()
        
        d[st] = 0
        q.add((0, st))
        while len(q) > 0:
            v = q.pop()[1]
            used[v] = True
            
            for to, w in self.edges[v]:
                if used[to]:
                    continue
                
                if d[to] > d[v] + w:
                    q.discard((d[to], to))
                    d[to] = d[v] + w
                    q.add((d[to], to))
                    pr[to] = v
                    
        objects['dijkstra_dist'] = d
        res = []
        res.append(finish)
        v = finish
        while v != st and pr[v] != -1:
            v = pr[v]
            res.append(v)
        
        res.reverse()
        objects['dijkstra_way'] = res
    
    def dijkstra_draw(self):
        if objects['dijkstra_dist'] == []:
            return
        
        for i in range(self.n):
            v = self.vtx[i]
            
            textSize(20)
            fill(*BLUE)
            text(str(objects['dijkstra_dist'][i]), v.x + 10, v.y - 20)
        
        # draw way
        for i in range(len(objects['dijkstra_way']) - 1):
            v = objects['dijkstra_way'][i]
            to = objects['dijkstra_way'][i+1]
            strokeWeight(3)
            stroke(*GREEN)
            line(self.vtx[v].x, self.vtx[v].y, self.vtx[to].x, self.vtx[to].y)    
            strokeWeight(1)
                
        for i in objects['dijkstra_way']:
            v = self.vtx[i]
            
            stroke(*BLACK)
            fill(*GREEN)
            circle(v.x, v.y, 30)
            
            textSize(20)
            fill(*BLACK)
            text(str(i), v.x - 5, v.y + 7)
        
            
def distance(x1, y1, x2, y2):
    
    def sqr(x):
        return x * x
    
    return math.sqrt(sqr(x2-x1) + sqr(y2-y1))

def setup():
    size(500, 500)
    background(*WHITE)
    
    # input graph
    n = 7
    edges = [
             [(1, 5), (3, 2), (4, 9)],
             [(0, 3), ],
             [(1, 5), ],
             [(0, 1), (2, 10), (5, 3)],
             [(0, 2), (6, 20)],
             [],
             [(4, 8), ]
             ]
    vtx = []
    for i in range(n):
        x = random.randint(40, 460)
        y = random.randint(40, 460)
        vtx.append(Vertex(x, y))
    
    new_graph = Graph(n, vtx, edges)
    objects['graph'] = new_graph


def draw():
    background(*WHITE)
    
    if mousePressed:
        vtx = objects['graph'].vtx
        for i in range(len(vtx)):
            if distance(mouseX, mouseY, vtx[i].x, vtx[i].y) <= 20:
                objects['selected'] = i
                break
    if keyPressed:
        v = objects['selected']
        if v != -1:
            if key == 'a':
                objects['graph'].vtx[v].move(-1, 0)
            if key == 'd':
                objects['graph'].vtx[v].move(1, 0)
            if key == 'w':
                objects['graph'].vtx[v].move(0, -1)
            if key == 's':
                objects['graph'].vtx[v].move(0, 1)
    
        if key == '1' or key == '2':
            vtx = objects['graph'].vtx
            for i in range(len(vtx)):
                if distance(mouseX, mouseY, vtx[i].x, vtx[i].y) <= 20:
                    if key == '1':
                        objects['v1'] = i
                    if key == '2':
                        objects['v2'] = i
                    break
    
    objects['graph'].draw()
    
