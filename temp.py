import matplotlib.pyplot as plt
import numpy as np
import math
from PIL import Image
import csv
from matplotlib.colors import Normalize

datafile='E:\\PhD\\Mug Study\\analysis\\Statistics\\PlotData\\robotic_coffee_grasp_data.csv'
data=list(csv.reader(open(datafile)))
print(data[2])
#POINT DATASET

x=[]
y=[]

for i in range (0,199):
    x.append(float(data[i][2]))
    y.append(float(data[i][3]))

#DEFINE GRID SIZE AND RADIUS(h)
grid_size=1
h=10
#GETTING X,Y MIN AND MAX
x_min=min(x)
x_max=max(x)
y_min=min(y)
y_max=max(y)

#CONSTRUCT GRID
x_grid=np.arange(-100-h,100+h,grid_size)
y_grid=np.arange(-100-h,100+h,grid_size)
x_mesh,y_mesh=np.meshgrid(x_grid,y_grid)

#GRID CENTER POINT
xc=x_mesh+(grid_size/2)
yc=y_mesh+(grid_size/2)

#FUNCTION TO CALCULATE INTENSITY WITH QUARTIC KERNEL
def kde_quartic(d,h):
    dn=d/h
    P=(15/16)*(1-dn**2)**2
    return P



def transparent_cmap(cmap, N=255):
    mycmap = cmap
    mycmap._init()
    mycmap._lut[:,-1] = np.linspace(0, 1, N+4)
    return mycmap



#Use base cmap to create transparent
mycmap = transparent_cmap(plt.cm.jet)
#PROCESSING
intensity_list=[]
for j in range(len(xc)):
    intensity_row=[]
    for k in range(len(xc[0])):
        kde_value_list=[]
        for i in range(len(x)):
            #CALCULATE DISTANCE
            d=math.sqrt((xc[j][k]-x[i])**2+(yc[j][k]-y[i])**2) 
            if d<=h:
                p=kde_quartic(d,h)
            else:
                p=0
            kde_value_list.append(p)
        #SUM ALL INTENSITY VALUE
        p_total=sum(kde_value_list)
        intensity_row.append(p_total)
    intensity_list.append(intensity_row)

# Import image and get x and y extents
I = Image.open('C:\\Users\\Deea\\Downloads\\WPy64-3740\\mug.jpg')
p = np.asarray(I).astype('float')



fig, ax = plt.subplots(1, 1)
ax.imshow(I,extent=[-100, 100, -100, 100])
intensity=np.array(intensity_list)
cb = ax.contourf(x_mesh, y_mesh, intensity, cmap=plt.cm.jet)
plt.colorbar(cb)
plt.show()