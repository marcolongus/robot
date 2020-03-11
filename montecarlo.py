import numpy as np

tiros=300


##############################################
#Montecarlos
##############################################

def condition(x=np.array,y=np.array):

	inside=False

	in_circle = x-y
	in_circle = np.square(in_circle)

	if (in_circle.sum()<=1):
		inside= True

	return inside 

##############################################
#Tiros
##############################################

shoots = np.random.rand(2,tiros)

y = np.zeros(2)

counter = 0

for i in range(tiros):
	flag = condition(shoots[...,i],y)
	if (flag):
		counter+=1


print(counter/tiros)

	