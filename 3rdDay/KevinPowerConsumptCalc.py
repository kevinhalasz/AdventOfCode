import numpy as np

input_file = open("input.txt","r")
input_array = np.asarray([list(line[:-1]) for line in input_file], dtype=int)
  
def max_with_tiebreak1(arr):
    count = np.bincount(arr)
    if count[0] == count[1]:
        return 1
    else:
        return count.argmax()

def GetLifeSupport(arr):
    col_index = 0
    O2_array = np.copy(arr)
    CO2_array = np.copy(arr)
    while O2_array.shape[0] > 1:
        max_val = max_with_tiebreak1(O2_array[:,col_index])
        O2_array = O2_array[(O2_array[:,col_index]==max_val)]
        col_index+=1
    col_index=0
    while CO2_array.shape[0] > 1:
        max_val = max_with_tiebreak1(CO2_array[:,col_index])
        CO2_array = CO2_array[(CO2_array[:,col_index]!=max_val)]
        col_index +=1
    O2 = ''.join(str(i) for i in O2_array[0])
    CO2 = ''.join(str(i) for i in CO2_array[0])
    return int(O2,2)*int(CO2,2)


def GetConsumption():
    gamma = "" 
    epsilon = ""
    for i in range(input_array.shape[1]):
        max = np.bincount(input_array[:,i]).argmax()
        gamma+= str(max)
        epsilon += str((1+max)%2)
    Gamma = int(gamma,2)
    Epsilon  = int(epsilon,2)
    return Gamma*Epsilon

if __name__=='__main__':
    print(GetLifeSupport(input_array))
