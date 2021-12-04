import numpy as np


def GetConsumption():
    input_file = open("input.txt","r")
    input_array = np.asarray([list(line[:-1]) for line in input_file], dtype=int)
    gamma = "" 
    epsilon = ""
    for i in range(input_array.shape[1]):
        max = np.bincount(input_array[:,i]).argmax()
        gamma+= str(max)
        epsilon += str((1+max)%2)
    print(gamma, epsilon)
    Gamma = int(gamma,2)
    Epsilon  = int(epsilon,2)
    print(Gamma,Epsilon)
    return Gamma*Epsilon

if __name__=='__main__':
    print(GetConsumption())