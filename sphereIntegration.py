import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data1 = np.loadtxt('BPD_arm.txt', delimiter='\t')
data2 = np.loadtxt('BPD_floor.txt', delimiter='\t')

#data1 = np.loadtxt('BPD_arm.txt', delimiter='\t')
#data2 = np.loadtxt('BPD_floor.txt', delimiter='\t')


radius1 = 165 # in mm
radius2 = 49 * 25.4
area = np.pi * (9.5 / 2) ** 2;

# calculate the actual angle and irradiance
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
		

# check the result
#for i in range(np.size(angle)):
#	print(i, angle[i], irradiance[i])


# interpolation 
interpolation_instance = 100
interp_angle = np.linspace(0.01, np.pi-0.01, interpolation_instance)
interp_irradiance = np.zeros(interpolation_instance)

for i in range(np.size(interp_angle)):
	cache = 0
	for j in range(np.size(angle)):
		cache = cache + 1
		if interp_angle[i] < angle[j]:
			interp_irradiance[i] = irradiance[j-1] + (interp_angle[i] - angle[j-1]) / \
													 (angle[j] - angle[j-1]) * \
													 (irradiance[j] - irradiance[j-1])
			break

# show the values
for i in range(np.size(interp_angle)):
	print(interp_angle[i]*180/np.pi, interp_irradiance[i])


# plot the values vs angle
plt.plot(interp_angle, interp_irradiance)
plt.show()

# integration in the spherical coordinate
jacobian = 2 * np.pi / np.size(interp_angle)
direct_integration = 0
angular_integration = 0
for i in range(np.size(interp_angle)):
	direct_integration = direct_integration + \
						 2 * np.pi * np.sin(interp_angle[i]) * interp_irradiance[i] * jacobian
	angular_integration = angular_integration + \
						  2 * np.pi * np.sin(interp_angle[i]) * np.cos(interp_angle[i]) * interp_irradiance[i] * jacobian

print(direct_integration, angular_integration)

	
