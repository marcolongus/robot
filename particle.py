from classparticle import *
import sortedcontainers as st
import matplotlib.patches as patches

####################################################
#Cuadricula de sets
####################################################

box = np.empty(L*L,dtype = object)

for i in range(L*L):
	box[i] = elemento()

box = box.reshape(L,L)



####################################################
#Inicialización del sistema
####################################################

file   = open("array.txt","w")

system = np.empty(N, dtype=object)
save   = np.empty(0)

for i in range(N):
	
	accepted=False

	while (not accepted):

		accepted = True
		system[i]= create_particle()

		x = system[i].node[0]
		y = system[i].node[1]

		
		for x_rang in range(-2,3):
			for y_rang in range(-2,3):

				x_m = np.mod(x + x_rang, L)
				y_m = np.mod(y + y_rang, L)

				if (len(box[x_m, y_m].set)>0):

					for elem in box[x_m, y_m].set:
						if ( dx_distance(system[i],system[elem])[2] < diameter ): 
							accepted = False

		if (accepted): 
			box[x,y].set.add(i)
			save = np.append(save,system[i].x)

save = save.reshape(N,2)
np.savetxt(file,save)

file.close()

####################################################
#Evolución
####################################################

file = open("evolution.txt","w")

for i in range(time_f):

	x_old = system[0].node[0]
	y_old = system[0].node[1]

	interact_set = np.empty(shape=(5,5),dtype=object)

	for x_rang in range(-2,3):
		for y_rang in range(-2,3):

			x_m = np.mod(x_old + x_rang, L)
			y_m = np.mod(y_old + y_rang, L)
			interact_set[x_rang+2,y_rang+2] = box[x_m,y_m]

	system[0] = evolution(system,0,interact_set)
	save = np.append(system[0].x,np.array([(i+1)*delta_time]) )
	np.savetxt(file, save.reshape(1,3))

	system[0].nodo()

	x_new = system[0].node[0]
	y_new = system[0].node[1]

	flag = False

	if ( not (0 in box[x_new,y_new].set)):
		box[x_old,y_old].set.discard(0)
		box[x_new,y_new].set.add(0)
		flag = True
	
	if flag:
		print(system[0].x, system[0].node)	
				

file.close()



####################################################
#Gráfico
####################################################

grafico  = np.loadtxt('evolution.txt')
grafico1 = np.loadtxt('array.txt')

fig, ax =plt.subplots()

plt.title("Obstacles configuration") 
plt.xlabel("x axis") 
plt.ylabel("y axis")

plt.axis('square')

plt.xlim(-1,L+1)
plt.ylim(-1,L+1)


plt.grid(color='b', linestyle='-.', linewidth=0.5)

#Graficamos la configuración inical de obstáculos

for i in range(N):

	if (i==0):
		circ = patches.Circle((grafico1[i,0], grafico1[i,1]), 1, alpha=0.7, fc='green')
		ax.add_patch(circ)
	else:
		circ = patches.Circle((grafico1[i,0], grafico1[i,1]), 1, alpha=0.7, fc='yellow')
		ax.add_patch(circ)

plt.plot(grafico1[0:,0],grafico1[0:,1], "o", color='b')



#Ahora seguimos la evolución de alguna partícula

for i in range(time_f):
	circ = patches.Circle((grafico[i,0], grafico[i,1]), 1, alpha=0.7, fc='red')
	ax.add_patch(circ)



plt.plot(grafico[0:,0],grafico[0:,1], "o", color='b')

plt.show()


























'''
####################################################
#Exploracion
####################################################

file  = open("array.txt","r")

for i in range(L):
	for j in range(L):

		if(len(box[i,j].set)>0):
			
			print(box[i,j].set, '[',i,',',j,']')


file.close()

'''