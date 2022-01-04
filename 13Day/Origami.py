import numpy as np

def unpack_data():
    dots, folds = [],[]
    
    with open('KevInput.txt','r') as input_file:
        # We will keep reading lines until we get to the break
        # statement corresponding to the jump from dots to
        # folds in the input file
        while True:
            line = input_file.readline()
            if line == '\n':
                break
            # Get rid of the \n at the end of each line
            line = line[:-1]
            # Add the coordinates of each dot as list of
            # length 2
            dots.append(line.split(','))
    
        # Now every line we read will be part of the folds
        # portion of the input file
        for line in input_file:
            # We start by looking for the location of 'x='
            x_place = line.find('x=')
            # If 'x=' does not occur in the line, x_place = -1
            if x_place > 0:
                # We denote a fold along the line x=n by ('x','n')
                folds.append(('x',line[x_place+2:-1]))
            else:
                # We know that every fold has the form x=n or y=n
                y_place = line.find('y=')
                folds.append(('y',line[y_place+2:-1]))
    
    return np.asarray(dots,dtype=int), folds

def mark_dots(dots):
    # We first need to find the dimensions of our grid
    x_max,y_max = dots.max(axis=0)
    
    # Then we define the grid
    grid = np.zeros((y_max+1,x_max+1),bool)
    
    # And mark each dot on the grid
    for dot in dots:
        grid[dot[1],dot[0]] = True
    
    return grid


def x_fold(grid,line):
    # We make a copy of the right-hand side of the grid
    new_grid = grid[:,line+1:].copy()
    
    # Then make a copy of the left-hand side before folding
    old_grid = grid[:,:line].copy()
    
    # Find where the dots are on the left-hand side
    y_true, x_true = np.where(old_grid==True)
    
    # Then project the x-coordinates across x=line
    x_true = line-1-x_true
    
    # Mark the dots which appear after folding
    for point in zip(y_true,x_true):
        new_grid[point] = True
    
    return new_grid

def score(grid):
    return np.sum(grid)

if __name__=='__main__':
    dots, folds = unpack_data()
    grid = mark_dots(dots)
    # This is kind of cheating, because I know the first fold is an x-fold
    grid = x_fold(grid,int(folds[0][1]))
    print(score(grid))
