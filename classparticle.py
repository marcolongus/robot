import numpy as np
import matplotlib.pyplot as plt
import sortedcontainers as st

#Constantes del sistema

#Variables
N= 20
L=20

time_f = 1000

delta_time = 0.1
active_vel = 1.

alpha	   = 20. 
p_rotation = (1/alpha)*delta_time; 


#Fijas
infinity = 10000000000000000
gamma_friction = 3.92*active_vel
radius =1.
diameter = 2*radius
dos_pi = 2*np.pi



#Arregla el problema de la indexación de numpy

class elemento(object):

	def  __init__(self,set=st.SortedSet):
		self.set = st.SortedSet()


#########################################################################

#Clase Particle

class Particle(object):

#Métodos
	
	def __init__(self,x=np.zeros(2),angle=0,velocity=active_vel, node=np.zeros(2)):

		self.x = x		
		self.angle = angle
		self.velocity = velocity
		self.node = x.astype(int)

	def nodo(self):
		self.node= np.mod(self.x.astype(int),L)

	
#Funciones

def create_particle():
	A = Particle(np.random.uniform(size=2)*L,np.random.uniform()*dos_pi)
	return A

def dx_distance(A=Particle,B=Particle):
	
	res = infinity
	dy = np.zeros(2)
	res_x = infinity
	res_y = infinity
	dx=np.zeros(shape=(3,2))

	for i in range(-1,2):
		x  = A.x + i*L		
		dx[i+1] = x - B.x

		if ( np.abs(dx[i+1][0]) < res_x ):
			dy[0]=dx[i+1][0]
			res_x=abs(dy[0])

		if ( np.abs(dx[i+1][1]) < res_y ):
			dy[1]=dx[i+1][1]
			res_y=abs(dy[1])	

	dis = np.sqrt((np.square(dy).sum()))

	if (dis <= diameter):
		inter = True
	else:
		inter = False

	result = np.append(dy,np.array([dis]))

	return result


def evolution(system=np.array, part_index=int, box=np.array ,dtype=np.object):
	
	A = system[part_index]

	potencial = np.zeros(2)
	campo = np.zeros(2)

	interact=False

	#Loop sobre todas las partículas que interactúa:

	for i in range(5):
		for j in range(5):

			for particles in box[i,j].set:

				if (particles != part_index):
					dx = dx_distance(system[part_index],system[particles])

					if(dx[2] <= diameter):
						interact=True		
						
						#calculamos potencial
						distance = np.square(dx[0:2]).sum()
						distance = np.sqrt(distance)
						potencial += np.power(distance,-3)*dx[0:2]
						potencial *= gamma_friction	

	#############################################################################

	if (interact):
		#Calculo del campo resultante
		field = np.array([np.cos(system[part_index].angle), np.sin(system[part_index].angle)])
		field *=active_vel
		field +=potencial 
						
		#Evolución		
		A.x += delta_time*field
		A.x = np.mod(A.x,L)
	
	else:
		#print(dx, dx.shape, "no interact")
		vel = active_vel*np.array([np.cos(system[part_index].angle), np.sin(system[part_index].angle)])		
		A.x += delta_time*vel
		A.x = np.mod(A.x,L)

	
	if (np.random.rand() < p_rotation ):
		A.angle=np.random.rand()*dos_pi 
	
	return A


#########################################################################














'''
x1=np.array([[1.,2.]])
x2= np.array([1.])

print(x1, x1.shape)
print(x2, x2.shape)

x3 = np.append(x1,x2)

print(x3,x3.shape)
'''


'''
#Gráfico

grafico = np.loadtxt('array.txt')

obstaculo = system[0].x.reshape(1,2)


plt.title("Trayectory") 
plt.xlabel("x axis caption") 
plt.ylabel("y axis caption")
plt.xlim(-10,10)
plt.ylim(-10,10)

plt.plot(grafico[0:,0],grafico[0:,1],"o", color='r')
plt.plot(obstaculo[0:,0], obstaculo[0:,1],"o") 
plt.show()
'''






