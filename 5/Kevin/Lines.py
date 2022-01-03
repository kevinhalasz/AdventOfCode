import numpy as np

def get_lines():
    # Start with an empty list to place the lines
    lines = []
    
    with open('KevInput.txt','r') as input_file:
        for line in input_file:
            # Remove the \n from the end of each line
            line = line[:-1]
            
            # Break the line representaiton into its
            # two endpoints
            two_points = line.split(' -> ')
            
            # Split each point into x and y coordinates
            coordinates = [p.split(',') for p in two_points]
            lines.append(coordinates)

    # The output is a 500x2x2 array, where each 2x2 slice
    # is of the form [[x_1,y_1],[x_2,y_2]]
    return np.asarray(lines,dtype=int)

def classify_lines(lines):
    # Start with three empty 3-d arrays
    vertical, horizontal, diagonal = [np.empty([0,2,2],dtype=int) for i in range(3)]
    for line in lines:
        # If the x-coordinates of the start and end
        # are the same, it is a vertical line
        if line[0][0] == line[1][0]:
            # Turn our 2x2 array into a 1x2x2 array then concatenate it
            # to the end of our vertical line array
            vertical = np.concatenate((vertical,line.reshape(1,2,2)),dtype=int)
        
        # If the y-coordinates of the start and end
        # are the same, its a horizontal line
        elif line[0][1] == line[1][1]:
            horizontal = np.concatenate((horizontal,line.reshape(1,2,2)),dtype=int)
        
        # This very nice problem is set up so every
        # line which is not horizontal or vertical
        # is diagonal
        else:
            diagonal = np.concatenate((diagonal,line.reshape(1,2,2)),dtype=int)
    return vertical, horizontal, diagonal

def draw_horizontal(horz_lines,grid=np.zeros((1000,1000),int)):
    for line in horz_lines:
        # Define x0 and x1 so x0<x1
        x0,x1 = sorted([line[0][0],line[1][0]])
        y = line[0][1]
        
        for x in range(x0,x1+1):
            # grid[y,x] is the point with cartesian
            # coordinates (x,y)
            grid[y,x]+=1

    return grid

def draw_vertical(vert_lines,grid=np.zeros((1000,1000),int)):
    for line in vert_lines:
        y0,y1 = sorted([line[0][1],line[1][1]])
        x = line[0][0]
        
        for y in range(y0,y1+1):
            grid[y,x]+=1

    return grid


def draw_diagonal(diag_lines,grid=np.zeros((1000,1000),int)):
    for line in diag_lines:
        # Unlike for vertical and horizontal lines, we do not order
        # x0 and x1 (or y0 and y1), we just index them as they were
        # given to us
        x0,x1 = [line[0][0],line[1][0]]
        y0,y1 = [line[0][1],line[1][1]]
        
        # To deal with order, we determine which of the x-coordinates
        # is larger and which of the y-coordinates is bigger. So x_sign
        # is equal to 1 if x0<x1, and -1 if x0>x1, and y_sign is defined
        # similarly
        x_sign,y_sign = 2*(line[0]<line[1])-1
        
        # We then increment the coordinates up or down depending
        # on the signs x_sign and y_sign
        for (x,y) in zip(range(x0,x1+x_sign,x_sign),range(y0,y1+y_sign,y_sign)):
            grid[y,x]+=1

    return grid

def score(grid):
    values, counts = np.unique(grid, return_counts=True)
    
    # We want to make sure we don't undercount in the case
    # where no points are covered by exactly 0 or exactly
    # 1 line
    indicator_zero = (0 in values)
    indicator_one = (1 in values)
    start_count = indicator_one+indicator_zero
    return sum(counts[start_count:])
