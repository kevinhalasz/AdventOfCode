import numpy as np

# Read in the input file and coerce it into
# a 2-d numpy array
with open("input.txt","r") as input_file:
    input_array = np.asarray([list(line[:-1]) for line in input_file], dtype=int)


# By default, np.bincount(arr).argmax() will give 0 when there is a tie
# so we need this new method to fit the constraints of the problem's
# second part
def max_with_tiebreak1(arr):
    count = np.bincount(arr)
    if count[0] == count[1]:
        return 1
    else:
        return count.argmax()


def GetLifeSupport(arr):
    # First we process the array for the oxygen rating, checking
    # the most common value in each column succesively via the
    # col_index
    col_index = 0
    O2_array = np.copy(arr)
    # We keep going until there only one row in the array
    while O2_array.shape[0] > 1:
        max_val = max_with_tiebreak1(O2_array[:,col_index])
        # Remove all rows which do not contain the desired bit
        # in column col_index
        O2_array = O2_array[(O2_array[:,col_index]==max_val)]
        col_index+=1
    # Now we repeat the process for the carbon dioxide rating
    col_index=0
    CO2_array = np.copy(arr)
    while CO2_array.shape[0] > 1:
        max_val = max_with_tiebreak1(CO2_array[:,col_index])
        CO2_array = CO2_array[(CO2_array[:,col_index]!=max_val)]
        col_index +=1
    # Convert each of the one row arrays to binary strings
    O2 = ''.join(str(i) for i in O2_array[0])
    CO2 = ''.join(str(i) for i in CO2_array[0])
    return int(O2,2)*int(CO2,2)


def GetConsumption():
    # We will determine the binary strings corresponding to both
    # numbers, starting with the empty string in each case
    gamma = "" 
    epsilon = ""
    # We then go through the columns one-by-one
    for i in range(input_array.shape[1]):
        # Checking for the bit which occurs most often
        max = np.bincount(input_array[:,i]).argmax()
        # Add that bit to gamma
        gamma+= str(max)
        # And add the less common bit to epsilon
        epsilon += str(max^1)
    # Conver the binary strings to decimal integers
    Gamma = int(gamma,2)
    Epsilon  = int(epsilon,2)
    return Gamma*Epsilon

if __name__=='__main__':
    print(GetLifeSupport(input_array))
