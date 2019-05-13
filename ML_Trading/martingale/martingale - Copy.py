"""Assess a betting strategy. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Copyright 2018, Georgia Institute of Technology (Georgia Tech) 			  		 			     			  	   		   	  			  	
Atlanta, Georgia 30332 			  		 			     			  	   		   	  			  	
All Rights Reserved 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Template code for CS 4646/7646 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Georgia Tech asserts copyright ownership of this template and all derivative 			  		 			     			  	   		   	  			  	
works, including solutions to the projects assigned in this course. Students 			  		 			     			  	   		   	  			  	
and other users of this template code are advised not to share it with others 			  		 			     			  	   		   	  			  	
or to make it available on publicly viewable websites including repositories 			  		 			     			  	   		   	  			  	
such as github and gitlab.  This copyright statement should not be removed 			  		 			     			  	   		   	  			  	
or edited. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
We do grant permission to share solutions privately with non-students such 			  		 			     			  	   		   	  			  	
as potential employers. However, sharing with other current or future 			  		 			     			  	   		   	  			  	
students of CS 7646 is prohibited and subject to being investigated as a 			  		 			     			  	   		   	  			  	
GT honor code violation. 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
-----do not edit anything above this line--- 			  		 			     			  	   		   	  			  	
 			  		 			     			  	   		   	  			  	
Student Name: Deepika Sivakumar (replace with your name) 			  		 			     			  	   		   	  			  	
GT User ID: dsivakumar6 (replace with your User ID) 			  		 			     			  	   		   	  			  	
GT ID: 903450354 (replace with your GT ID) 			  		 			     			  	   		   	  			  	
"""

import numpy as np

def author():
        return 'dsivakumar6' # replace tb34 with your Georgia Tech username

def gtid():
    return 903450354 # replace with your GT ID number

def get_spin_result(win_prob):
    result = False
    random_num = np.random.random()
    #print 'np.random.random(): %f',random_num
    if random_num <= win_prob:
        result = True
    return result

def test_code():
    #Probability of winning a black = No. of black numbers/Total numbers + green numbers : 18/36+2 = 0.474
    win_prob = 0.474 # set appropriately to the probability of a win
    np.random.seed(gtid()) # do this only once

    # add your code here to implement the experiments
    no_of_spins = 1000
    array_size = 1001
    winnings = [None] * array_size #Array to hold the winnings after each spin
    winnings[0] = 0 #Value before the first spin
    episode_winnings = 0
    bet_amount = 1
    won = False
    for spin_count in range(1,array_size):
        if episode_winnings < 80:
            won = get_spin_result(win_prob) #Spin the wheel
            if won == True:
                episode_winnings = episode_winnings + bet_amount
                bet_amount = 1 #Reset the bet_amount for the next spin
            else:
                episode_winnings = episode_winnings - bet_amount
                bet_amount = bet_amount * 2 #Double the bet_amount if lost
            winnings[spin_count] = episode_winnings
            #print 'winnings in loop: %d',winnings[spin_count]
        else:
            print 'Reached $80'
            break
    print 'spin_count after spinning: %d', spin_count
    print 'winnings[spin_count]: %d', winnings[spin_count-1]
    if spin_count < no_of_spins:
        print 'inside if spin_count: %d', spin_count
        for i in range(spin_count, array_size):
            winnings[i] = 80
    print 'winnings[last] : %d', winnings[no_of_spins]
    
    # Added for Matplot
    print(winnings)

if __name__ == "__main__":
    test_code()
