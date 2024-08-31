import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data1 = np.loadtxt('arm.txt', delimiter='\t')
data2 = np.loadtxt('floor.txt', delimiter='\t')



radius1 = 145 # in mm
radius2 = 150
area = np.pi * (9.5 / 2) ** 2;

# calculate the actual angle
cache = 0
angle1 = np.array([])
for v in data1[:,0]:
	cache = cache + v / radius1
	angle1 = np.append(angle1, cache)
irradiance1 = data1[:,1] / area * radius1
	
cache = 0
angle2 = np.array([])
for v in data2[:,0]:
	cache = cache + v / radius2
	angle2 = np.append(angle2, cache)
irradiance2 = data2[:,1] / area * radius2

# combine the values
angle = np.array([])
irradiance = np.array([])
cache1 = 0
cache2 = 0
while cache1 < angle1.size or cache2 < angle2.size:	
	# conditions one cache reaches the end
	if cache2 == angle2.size:
		angle = np.append(angle, angle1[cache1])
		irradiance = np.append(irradiance, irradiance1[cache1])
		cache1 = cache1 + 1
	elif cache1 == angle1.size:
		angle = np.append(angle, angle2[cache2])
		irradiance = np.append(irradiance, irradiance2[cache2])
		cache2 = cache2 + 1
		
	elif angle1[cache1] < angle2[cache2]:
		angle = np.append(angle, angle1[cache1])
		irradiance = np.append(irradiance, irradiance1[cache1])
		cache1 = cache1 + 1
	else:
		angle = np.append(angle, angle2[cache2])
		irradiance = np.append(irradiance, irradiance2[cache2])
		cache2 = cache2 + 1
# interpolation and integration
interp_angle = np.linspace(0.01, np.pi-0.01, 100)
interp_irradiance = np.zeros(100)

for i in range(np.size(interp_angle)):
	cache = 0
	for j in range(np.size(angle)):
		cache = cache + 1
		#print(interp_angle[i], angle[j])
		if interp_angle[i] < angle[j]:
			interp_irradiance[i] = irradiance[j] + (interp_angle[i] - angle[j-1]) / \
													 (angle[j] - angle[j-1]) * \
													 (irradiance[j] - irradiance[j-1])
			break


# plot the values vs angle
plt.plot(interp_angle, interp_irradiance)
plt.show()
