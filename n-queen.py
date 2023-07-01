import random
import time
import numpy as np
from matplotlib import pyplot as plt

def initialize_population(population_size, N):
    population = []
    for i in range(population_size):
        child = []
        for j in range(N):
            child.append(random.randint(1,N))
        child.append(0)      #add rank of each genes at the end of that
        population.append(child)
    return population

def crossover(population):       #crossover 2 parent and make 2 children (logic  : half from each parent)
    children = []
    for i in range(0, len(population), 2):
        child1 = population[i][:N//2] + population[i+1][N//2:N] + [0]
        child2 = population[i+1][:N//2] + population[i][N//2:N] + [0]
        children.append(child1)
        children.append(child2)
    return children

def mutation(children, rate, N):
    #choose rate percent of children and do mutation on them
    chosen_size = int(len(children)*rate)
    children_index = []
    chosen_index = []
    for i in range(len(children)):    #children_index = [0, 1, 2, ... , len(children)-1]
        children_index.append(i)
    for i in range(chosen_size):      #choose some of the children_index as chosen_index (sample make them not repeated)
        chosen_index = random.sample(children_index, chosen_size)
    for i in range(chosen_size):
        chosen_chromosome = random.randint(0, N-1)
        new_value = random.randint(1, N)
        children[chosen_index[i]][chosen_chromosome] = new_value
    return children

def fitness(population, N):
    #calculating conflicts
    for i in range(len(population)):
        conflict = 0
        for j in range(N):
            for k in range(j+1,N):
                if(population[i][j] == population[i][k]):    #check column
                    conflict += 1
                if(abs(j - k) == abs(population[i][j] - population[i][k])):    #check diagonal
                    conflict += 1
        population[i][N] = conflict
    #sort chromosomes based on conflicts
    for i in range(len(population)):
        minimum = i
        for j in range(i, len(population)):
            if(population[j][N] < population[minimum][N]):
                minimum = j
        population[i] , population[minimum] = population[minimum] , population[i]
    
    return population

def answers(population, N):
    answers = []
    for i in range(len(population)):
        if(population[i][N] == 0):
            if(population[i] not in answers):
                answers.append(population[i])
    print("The algorithm find", len(answers), "answers:")
    for i in range(len(answers)):
        print(answers[i])
    return len(answers)

def GA_performance(N, population_size, rate):
    start_time = time.time() 
    population = initialize_population(population_size, N)
    # print("primary population:")
    # print(population)

    children = crossover(population)
    # print("population after crossover:")
    population += children
    # print(population)
    # print("children after crossover:")
    # print(children)

    children = mutation(children, rate, N)
    # print("children after mutation:")
    # print(children)

    population += children
    population = fitness(population, N)
    # print("population after fitness")
    # print(population)
    num_of_answers = answers(population, N)

    exe_time = time.time() - start_time
    performance = num_of_answers / exe_time
    print("The execution time is:", exe_time)
    print("performance:", performance)
    print("_________________________________________________")
    return performance

def mutation_rate_effect(N):
    population_size = 100   #fixed
    rate = 0
    for i in range(20):
        performance = GA_performance(N, population_size, rate)
        plt.plot(rate, performance, marker="o", color="red")
        rate += 0.05
    plt.xlabel('rate')
    plt.ylabel('performance')
    plt.show()

def population_size_effect(N):
    rate = 0.2    #fixed
    population_size = 100
    for i in range(20):
        performance = GA_performance(N, population_size, rate)
        plt.plot(population_size, performance, marker="o", color="blue")
        population_size += 100
    plt.xlabel('population size')
    plt.ylabel('performance')
    plt.show()
    
#__________MAIN___________
N = 4
mutation_rate_effect(N=4)
# population_size_effect(N=4)