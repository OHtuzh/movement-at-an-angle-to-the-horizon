from matplotlib import pyplot as plt
import math 


#constants
alpha = math.pi/6 #30 degrees
V0 = 30 #m/sec
time1 = 0.0001 #sec
g = 9.81 #m/s^2
k = 2 #
m = 10 #kg

#call
Vx = [0 for i in range(0, 120000)]
Vy = [0 for i in range(0, 120000)]
x = [0, 0]
y = [0, 0]
Vx[0] = V0*math.cos(alpha)
Vy[0] = V0*math.sin(alpha)

#functions
def Velx(t, kf, mass, repeat, Velx):
    return (Velx[t-1] - kf/mass * Velx[t-1]*repeat)

def Vely(t, kf, mass, repeat, Vely, G):
    return (Vely[t-1] - (G + kf/mass * Vely[t-1])*repeat)

for i in range(1, 120000):
    Vx[i] = Velx(i, k, m, time1, Vx)
    Vy[i] = Vely(i, k, m, time1, Vy, g)


i = 1
while y[i] >= 0:
    i += 1
    x.append(x[i-1] + Vx[i-1]*time1)
    y.append(y[i-1] + Vy[i-1]*time1)


plt.plot(x, y)
plt.show()
