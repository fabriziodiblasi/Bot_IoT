# lstm autoencoder predict sequence
import numpy as np

seq_in = np.array([])
in_file = open("dataset.txt","r")
#text = in_file.read()
for i in in_file.read().split():
    print(i)
    i = int(i)
    if i !=0 and i<900 :
        #print(i)
        seq_in = np.append(seq_in,int(i))
in_file.close()

print(seq_in)
media = np.mean(seq_in)
print("Media :",media)
sigma = np.std(seq_in)
print("Sigma : ",sigma)


c = 0
a = 1/(sigma * np.sqrt(2*np.pi))*np.exp((-1/2) * ((c-media)**2/sigma**2))
print ("X = ",c,"\nValore Gaussiana :", a)

c = 4
a = 1/(sigma * np.sqrt(2*np.pi))*np.exp((-1/2) * ((c-media)**2/sigma**2))
print ("X = ",c,"\nValore Gaussiana :", a)

c = 250
a = 1/(sigma * np.sqrt(2*np.pi))*np.exp((-1/2) * ((c-media)**2/sigma**2))
print ("X = ",c,"\nValore Gaussiana :", a)

c = 500
a = 1/(sigma * np.sqrt(2*np.pi))*np.exp((-1/2) * ((c-media)**2/sigma**2))
print ("X = ",c,"\nValore Gaussiana :", a)