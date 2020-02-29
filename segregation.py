lla #!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Davide Di Matteo - Web Science - TU Graz
# Segregation exercise

# I have run this using the native python3 launcher for MacOS.

import numpy
import random
import matplotlib.pylab as plt
import seaborn as sns


def filename_generator(path):
    '''A simple generator for plot filenames.'''
    counter = 0
    while(True):
        yield( path + "/plot_%02d.png" % counter)
        counter +=1

plot_filename = filename_generator("submission")


def perform():
    # TODO Student: Implement Task from
    #   from http://kti.tugraz.at/staff/socialcomputing/courses/webscience/ex1.html
    #   or   http://kti.tugraz.at/staff/socialcomputing/courses/webscience/ex2.html

    number_of_iterations = 20
    counter_of_A = 0
    counter_of_B = 0
    grid = numpy.zeros([100,100])
    for i in range(4000):
        # random agent type A
        while True:
            x = random.randint(0, 99)
            y = random.randint(0, 99)
            if grid[x, y] == 0:  # Check if the cell is empty in order to place an agent
                grid[x, y] = 1  # type A = 1
                counter_of_A = counter_of_A + 1
                break
            else:
                continue
        # random agent type B
        while True:
            x = random.randint(0, 99)
            y = random.randint(0, 99)
            if grid[x, y] == 0:  # Check if the cell is empty in order to place an agent
                grid[x, y] = 2  # type B = 2
                counter_of_B = counter_of_B + 1
                break
            else:
                continue
    print("A is %d and B is %d" % (counter_of_A, counter_of_B)) #just checking how many As and Bs
    # initial heat map
    heatmap(grid, "Heat-Map before recollocation", "x", "y")
    # calculate happiness
    grid_happy = cal_happy(grid)
    # covert grid_happy to array to show distribution of happiness
    grid_dist = numpy.zeros(10000)
    for x in range(100):
        for y in range(100):
            grid_dist[(x + 1) * (y + 1) - 1] = grid_happy[x, y]
    distplot(grid_dist, "Initial distribution of the happiness", "x", "y")
    # Relocate unhappy agent for number_of_iterations iteration
    for i in range(number_of_iterations):

        # I have implemented two functions for the recollocation, the first one move one unhappy agent per iteration (20 iteratoions).
        # The other one moves all the unhappy agents per iteration (always 20 iteratoions). I have noticed that with this second function
        # there is a notable differences between the starting and the ending plots, so I have decided to use that one. If you prefer the
        # other one you are free to change (lines 75-76).
        # However, while in the heatmap I can tell the difference before and after the recollocation, I cannot tell very good what
        # happens in the distribution of happiness graph.

        # move_unhappy_1(grid, grid_happy) # --- CHOOSE WHAT TO PERFORM (1 agent)
        move_unhappy(grid, grid_happy)  # --- CHOOSE WHAT TO PERFORM (all agents iteration)

        # recalculate happiness
        grid_happy = cal_happy(grid)
    # draw final heatmap
    heatmap(grid, "Heat-map after recollocation", "x", "y")
    # covert grid_happy to array to show distribution of happiness
    grid_dist = numpy.zeros(10000)
    for x in range(100):
        for y in range(100):
            grid_dist[(x + 1) * (y + 1) - 1] = grid_happy[x, y]
    distplot(grid_dist, "Final distribution of the happiness", "x", "y")
    return grid

# calculate happiness
def cal_happy(grid):
    ret = numpy.zeros([100, 100])
    for x in range(100):
        for y in range(100):
            if grid[x, y] == 0: # if cell is empty, no need to calculate, and happiness is 0
                continue
            sameType = 0  # same type neighborhood number
            unsameType = 0  # unsame type neighborhood number
            for ix in [-1, 0 ,1]:
                for iy in [-1, 0, 1]:
                    if (ix == 0 and iy == 0) or x+ix<0 or x+ix>99 or y+iy<0 or y+iy>99: # if self or out of map, no need to count
                        continue
                    elif grid[x+ix, y+iy] == 0: # if neighborhood is empty, no need count
                        continue
                    elif grid[x+ix, y+iy] == grid[x, y]: # add same type count
                        sameType += 1
                    else:
                        unsameType += 1  # add unsame type count
            if sameType == 0 and unsameType == 0:  # an agent who lives among otherwise empty cells is 100% happy
                ret[x, y] = 1
            else:  # calculate happiness
                ret[x, y] = sameType / (sameType + unsameType)
    return ret

# Relocate an unhappy agent to a random empty cell one iteration.
def move_unhappy_1(grid, grid_happy):
    while True:
        x = random.randint(0, 99)
        y = random.randint(0, 99)
        if grid_happy[x, y] >= 0.5 or grid[x, y] == 0:  # if happy agent or empty cell, continue
            continue
        else:
            while True:
                # random new location
                mx = random.randint(0, 99)
                my = random.randint(0, 99)
                if grid[mx, my] == 0: # if new location is empty, relocate agent
                    grid[mx, my] = grid[x, y]
                    grid[x, y] = 0
                    break
            break

# Relocate all unhappy agents to a random empty cell. one iteration
def move_unhappy(grid, grid_happy):
    for x in range(100):
        for y in range(100):
            if grid_happy[x, y] >= 0.5 or grid[x, y] == 0:   # if happy agent or empty cell, continue
                continue
            else:
                while True:
                    # random new location
                    mx = random.randint(0, 99)
                    my = random.randint(0, 99)
                    if grid[mx, my] == 0:  # if new location is empty, relocate agent
                        grid[mx, my] = grid[x, y]
                        grid[x, y] = 0
                        break

def distplot(values, title, xlabel, ylabel):
    ''' Plots the distribution of values in the given array
        and stores the plot to the submission folder.
    '''
    global plot_filename
    plt.figure(figsize=(10,6))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    sns.distplot(values, ax=plt.axes())
    plt.savefig(next(plot_filename))


def heatmap(values, title="", xlabel="", ylabel=""):
    ''' Plots the given 2D array as a heatmap and
        stores the resulting plot to the submission folder.
    '''
    global plot_filename
    plt.figure(figsize=(20,12)) # I have doubled the img size
    ax = plt.axes()
    sns.heatmap(values, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.savefig(next(plot_filename))


if __name__ == '__main__':
    results = perform()
