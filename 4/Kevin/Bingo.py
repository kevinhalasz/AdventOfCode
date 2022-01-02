import numpy as np

def setup_game():
    with open('../KevinsInput.txt','r') as input_file:
        # Begin by creating a 1-d array of the numbers to be read,
        # which appear in the first line of the input file
        stream_raw = input_file.readline()[:-1]
        stream = stream_raw.split(',')
        stream = np.asarray(stream,dtype=int)
        
        # Next, create a 100x5x5 array of bingo boards
        the_rest = input_file.read()
    
    # We do this by first breaking up the long string into
    # one string for each board
    boards_raw = the_rest.split('\n\n')
    # Then breaking the boards into rows
    boards = [board.split('\n') for board in boards_raw]
    
    # And finally, we turn the string corresponding to each
    # row into a list
    board_pre_array=[]
    for board in boards:
        new_board = []
        for row in board:
            # We add this condition to avoid the empty rows
            # given by the leading and ending \n in the_rest
            if len(row) > 1:
                # And we do these operations to avoid the
                #  pesky space in front of one digit numbers
                row = row.replace('  ',' ')
                if row[0] == ' ':
                    row = row[1:]
                new_board.append(row.split(' '))
        board_pre_array.append(new_board)

    # The output here is the stream of numbers to be called the the
    # 3-d array of boards
    return stream, np.asarray(board_pre_array,dtype=int)

# Given a board, we want to find all possible
# values for row sums and column sums to check
# if any row or column has all entries marked
def row_col_sums(board):
    row_sums = np.sum(board,axis=0)
    col_sums = np.sum(board,axis=1)
    return np.union1d(row_sums,col_sums)


def score(board, call):
    sums = row_col_sums(board)
    if -5 in sums:
        # To sum up to unmarked entries, we need to add
        # the number of negative ones which appear to
        # sum of the entires in the marked board
        num_marked = np.unique(board,return_counts=True)[1][0]
        # Return the number just called times the sum
        # of the unmarked entries in the winning board
        return call*(np.sum(board)+num_marked)
    
    # If the board is not a winner, give it a score
    # of -1
    return -1

def win_game(stream, boards):
    # Go through the numbers called one-by-one
    for call in stream:
        # Determine wehre the called number appears on each board
        board_index,row_index,column_index = np.where(boards==call)
        
        # Loop over each entry on any board containing the called
        # number
        for entry in zip(board_index,row_index,column_index):
            # Mark the called entry equal with -1
            boards[entry] = -1
            this_score = score(boards[entry[0]], call)
            
            # If the board is a winner, it will receive a score
            # other than the dummy score of -1
            if this_score>0:
                return this_score

# Here we return a pair, the first entry of which is the new
# set of boards obtained by removing a winning board, the
# second of which is a 0/1 indicator for whether we ended
# up removing the active board
def remove_winner(boards, active_index):
    board = boards[active_index]
    sums = row_col_sums(board)
    
    if -5 in sums:
        return np.delete(boards,active_index,axis=0), 1
    
    else:
        return boards, 0


def lose_game(stream,boards):
    for call in stream:
        # Determine wehre the called number appears on each board
        board_index,row_index,column_index = np.where(boards==call)
        
        # Because we will be deleting boards as we go along, we
        # need to keep track of how many boards have been deleted
        # and adjust indices accordingly. We keep track with the
        # integer loss, which counts how many boards have been
        # removed while processing the current call
        loss=0
        
        # Loop over each entry on any board containing the called
        # number
        for entry in zip(board_index,row_index,column_index):
            # Here we resent the indices to take any boards
            # already removed during the processing of the
            # current call
            entry = (entry[0]-loss,entry[1],entry[2])
            
            # Mark the called entry equal with -1
            boards[entry] = -1
            
            # If there is more than one board left, we will
            # remove winning boards
            if boards.shape[0]>1:
                removal_info = remove_winner(boards,entry[0])
                # We may have a new set of boards, or if the
                # given board was not a winnder, we get the
                # same set of boards back
                boards = removal_info[0]
                # If we removed a board, we need to add one
                # to the loss counter
                loss += removal_info[1]
            
            # Otherwise, there is only one board left, and we want
            # to determine if it one and, if so, its score
            else:
                this_score = score(boards[entry[0]], call)
                if this_score>0:
                    return this_score
                    

