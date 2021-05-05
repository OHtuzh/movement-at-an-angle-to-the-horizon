import sqlite3    #import sqlite
import math 

#functions
def Velx(t, kf, mass, repeat, Velx):
    return (Velx[t-1] - kf/mass * Velx[t-1]*repeat)

def Vely(t, kf, mass, repeat, Vely, G):
    return (Vely[t-1] - (G + kf/mass * Vely[t-1])*repeat)

def maximum(arr):
    l = arr[0]
    for i in range(1, len(arr)):
        if arr[i] > l:
            l = arr[i]
    return l

def launch(alpha, V0, time1, g, k, m):
    #call
    Vx = [0 for i in range(0, 120000)]
    Vy = [0 for i in range(0, 120000)]
    x = [0, 0]
    y = [0, 0]
    Vx[0] = V0*math.cos(alpha)
    Vy[0] = V0*math.sin(alpha)


    #momential velocy per 0.0001 sec.
    for i in range(1, 120000):
        Vx[i] = Velx(i, k, m, time1, Vx)
        Vy[i] = Vely(i, k, m, time1, Vy, g)

    #graph
    i = 1
    while y[i] >= 0:
        i += 1
        x.append(x[i-1] + Vx[i-1]*time1)
        y.append(y[i-1] + Vy[i-1]*time1)
    return [maximum(x), maximum(y), i*time1]

#constants
angle = math.pi/4 #45 degrees
V = 30 #m/sec
time_sep = 0.0001 #sec
G = 9.81 #m/sec^2
kof = 0 #k-t
mass = 1 #kg

conn = sqlite3.connect("Horizont.sqlite")  
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Horizont')

profile = int(input('Выберете профиль:\n1.Скорость\n2.Коэффициент сопротивления\n3.Угол к горизонту'))

if profile == 1:
    speed = str(input("Введите скорость в м/c или напишите quit для выхода:\n"))
    cur.execute('''CREATE TABLE Horizont (Range INTEGER, Altitude INTEGER, Time INTEGER, Speed INTEGER)''')

    while speed != "quit" and speed.isdigit():
        results = launch(angle, float(speed), time_sep, G, kof, mass)
        cur.execute('''INSERT INTO Horizont (Range, Altitude, Time, Speed) VALUES(?, ?, ?, ?)''', (results[0], results[1], results[2], float(speed)))
        conn.commit()
        speed = str(input("\nВведите скорость в м/c или напишите quit для выхода:\n"))

if profile == 2:
    kf = str(input("Введите коэффициент сопротивления или напишите quit для выхода:\n"))
    cur.execute('''CREATE TABLE Horizont (Range INTEGER, Altitude INTEGER, Time INTEGER, K INTEGER)''')

    while kf != "quit" and kf.isdigit():
        results = launch(angle, V, time_sep, G, float(kf), mass)
        cur.execute('''INSERT INTO Horizont (Range, Altitude, Time, K) VALUES(?, ?, ?, ?)''', (results[0], results[1], results[2], float(kf)))
        conn.commit()
        kf = str(input("Введите коэффициент сопротивления или напишите quit для выхода:\n"))

if profile == 3:
    ang = str(input("Введите угол полёта к горизонту в градусах или напишите quit для выхода:\n"))
    cur.execute('''CREATE TABLE Horizont (Range INTEGER, Altitude INTEGER, Time INTEGER, Angle INTEGER)''')

    while ang != "quit" and ang.isdigit():
        results = launch(float(ang)*math.pi/180, V, time_sep, G, kof, mass)
        cur.execute('''INSERT INTO Horizont (Range, Altitude, Time, Angle) VALUES(?, ?, ?, ?)''', (results[0], results[1], results[2], float(ang)))
        conn.commit()
        ang = str(input("Введите угол полёта к горизонту в градусах или напишите quit для выхода:\n"))

cur.close()
