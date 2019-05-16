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
import matplotlib #TODO: Uncomment before submitting
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np

def author():
        return 'dsivakumar6' # replace tb34 with your Georgia Tech username

def gtid():
    return 903450354 # replace with your GT ID number

def get_spin_result(win_prob):
    result = False
    random_num = np.random.random()
    if random_num <= win_prob:
        result = True
    return result

# Function to generate graph
def generate_graph(title, filename):
    plt.axis([0,300,-256,+100])
    plt.xlabel('Spin Count')
    plt.ylabel('Episode Winnings')
    plt.title(title)
    plt.legend()
    plt.savefig(filename)
    plt.close()

def test_code():
    # Probability of winning a black = No. of black numbers/(Total numbers + green numbers) : 18/(36+2) = 0.474
    win_prob = 0.474 # set appropriately to the probability of a win
    np.random.seed(gtid()) # do this only once

    # add your code here to implement the experiments
    # Initialize variables
    no_of_spins = 1000
    winnings_array_size = no_of_spins + 1
    trail_winnings = []

    ############################ 
    # Experiment 1 - Figure 1
    ############################ 
    # Set the plot values
    plot_color =['salmon', 'salmon', 'royalblue', 'royalblue', 'gold', 'gold', 'orange','orange','green','green']
    
    no_of_runs = 10
    for run in range (0, no_of_runs):
        winnings = [0] * winnings_array_size # Array to hold the winnings after each spin
        winnings[0] = 0 # Value before the first spin
        episode_winnings = 0
        bet_amount = 1
        won = False
        for spin_count in range(1,winnings_array_size):
            if episode_winnings < 80:
                won = get_spin_result(win_prob) #Spin the wheel
                if won == True:
                    episode_winnings = episode_winnings + bet_amount
                    bet_amount = 1 # Reset the bet_amount for the next spin
                else:
                    episode_winnings = episode_winnings - bet_amount
                    bet_amount = bet_amount * 2 # Double the bet_amount if lost
                winnings[spin_count] = episode_winnings
            else: # Break the loop once the episode_winnings reaches $80
                winnings[spin_count] = 80
                break
        # Set rest of the values in the winnings array to 80
        if spin_count < no_of_spins:
            for i in range(spin_count, winnings_array_size):
                winnings[i] = 80
#        trail_winnings.append(winnings)
        # Plot the graph for each run
        if run % 2 == 0:
            plt.plot(winnings,marker='', color=plot_color[run], linewidth=2, label='Trail '+str(run+1))
        else:
            plt.plot(winnings,marker='', color=plot_color[run], linewidth=2, linestyle='dashed', label='Trail '+str(run+1))

    # Generate the graph
    generate_graph('Figure 1','figure1.png')

    ############################ 
    # Experiment 1 - Figure 2
    ############################ 
    no_of_runs = 1000
    trail_winnings = []

    for run in range (0,no_of_runs):
        winnings = [0] * winnings_array_size # Array to hold the winnings after each spin
        winnings[0] = 0 # Value before the first spin
        episode_winnings = 0
        bet_amount = 1
        won = False
        for spin_count in range(1,winnings_array_size):
            if episode_winnings < 80:
                won = get_spin_result(win_prob) # Spin the wheel
                if won == True:
                    episode_winnings = episode_winnings + bet_amount
                    bet_amount = 1 # Reset the bet_amount for the next spin
                else:
                    episode_winnings = episode_winnings - bet_amount
                    bet_amount = bet_amount * 2 # Double the bet_amount if lost
                winnings[spin_count] = episode_winnings
            else: # Break the loop once the episode_winnings reaches $80
                winnings[spin_count] = 80
                break
        # Set rest of the values in the winnings array to 80
        if spin_count < no_of_spins:
            for i in range(spin_count, winnings_array_size):
                winnings[i] = 80
        # Store the winnings for each run
        trail_winnings.append(winnings)

    # Convert it into np array to calculate mean
    trail_winnings_array = np.array(trail_winnings)
    mean = trail_winnings_array.mean(axis=0)
    std_dev = trail_winnings_array.std(axis=0)

    # Generate the graph
    plt.plot(mean,marker='', color='green', linewidth=2, label='Mean')
    plt.plot(mean+std_dev,marker='', color='orange', linewidth=2, label='Mean + Standard Deviation')
    plt.plot(mean-std_dev,marker='', color='royalblue', linewidth=2, label='Mean - Standard Deviation')

    generate_graph('Figure 2', 'figure2.png')

    ############################ 
    # Experiment 1 - Figure 3
    ############################ 
    median = np.median(trail_winnings_array,axis=0)

    # Generate the graph
    plt.plot(median,marker='', color='green', linewidth=2, label='Median')
    plt.plot(median + std_dev,marker='', color='orange', linewidth=2, label='Median + Standard Deviation')
    plt.plot(median - std_dev,marker='', color='royalblue', linewidth=2, label='Median - Standard Deviation')

    generate_graph('Figure 3', 'figure3.png')

    ############################ 
    # Experiment 2 - Figure 4
    ############################ 
    trail_winnings = []
    no_of_runs=1000

    for run in range (0,no_of_runs):
        winnings = [0] * winnings_array_size # Array to hold the winnings after each spin
        winnings[0] = 0 # Value before the first spin
        episode_winnings = 0
        bet_amount = 1
        won = False
        isUpperlimitFlag = False
        for spin_count in range(1,winnings_array_size):
            if episode_winnings < 80 and episode_winnings > -256:
                won = get_spin_result(win_prob) # Spin the wheel
                if won == True:
                    episode_winnings = episode_winnings + bet_amount
                    bet_amount = 1 # Reset the bet_amount for the next spin
                else:
                    episode_winnings = episode_winnings - bet_amount

                    if bet_amount >= episode_winnings + 256:
                        bet_amount = episode_winnings + 256
                    else:
                        bet_amount = bet_amount * 2 # Double the bet_amount if lost
                winnings[spin_count] = episode_winnings
            else:
                if episode_winnings == 80:
                    winnings[spin_count] = 80
                    isUpperlimitFlag = True
                if episode_winnings <= -256:
                    winnings[spin_count] = -256
                    isUpperlimitFlag = False
                break

        if spin_count < no_of_spins:
            if isUpperlimitFlag == True:
                for i in range(spin_count, winnings_array_size):
                    winnings[i] = 80
            else:
                for i in range(spin_count, winnings_array_size):
                    winnings[i] = -256
        # Store the values for each run
        trail_winnings.append(winnings)

    # Convert it into np array to calculate mean
    trail_winnings_array=np.array(trail_winnings)

    mean = trail_winnings_array.mean(axis=0)
    std_dev = trail_winnings_array.std(axis=0)

    # Generate the graph
    plt.plot(mean,marker='', color='green', linewidth=2, label='Mean')
    plt.plot(mean+std_dev,marker='', color='orange', linewidth=2, label='Mean + Standard Deviation')
    plt.plot(mean-std_dev,marker='', color='royalblue', linewidth=2, label='Mean - Standard Deviation')

    generate_graph('Figure 4', 'figure4.png')

    ############################ 
    # Experiment 2 - Figure 5
    ############################ 
    median = np.median(trail_winnings_array,axis=0)

    # Generate the graph
    plt.plot(median, marker='', color='green', linewidth=2, label='Median')
    plt.plot(median + std_dev, marker='', color='orange', linewidth=2, label='Median + Standard Deviation')
    plt.plot(median - std_dev,marker='', color='royalblue', linewidth=2, label='Median - Standard Deviation')

    generate_graph('Figure 5', 'figure5.png')

if __name__ == "__main__":
    test_code()
