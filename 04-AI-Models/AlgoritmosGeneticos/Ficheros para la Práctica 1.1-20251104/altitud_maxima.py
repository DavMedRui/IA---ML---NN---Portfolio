import numpy
import pygad

import elevaciones as elev

mapa = elev.obtener_mapa()
# Vamos a maximizar la altitud para las coordenadas x, y

def fitness_func(ga_instance, solution, solution_idx): # Optimiza la máxima altitud
	maxX , maxY = mapa.shape
	x = int(solution[0])
	y = int(solution[1])
	if x >= maxX or y >= maxY:
		return -1000	
	return mapa[x][y]

def fitness_func_minima(ga_instance, solution, solution_idx):
    # Esta función optimiza la mínima altitud
    maxX, maxY = mapa.shape
    x = int(solution[0])
    y = int(solution[1])
    # Si sale de los límites o si está en el mar
    if x >= maxX or y >= maxY or x < 0 or y < 0 or mapa[x][y] <= 0:
        return -1000
    return 1 / (mapa[x][y]+1e-6) #Le sumamos un valor pequeño para evitar división por cero


    


# Next is to prepare the parameters of PyGAD. Here is an example for a set of parameters


#fitness_function = fitness_func

num_generations = 300 #Antes 25. Explora espacio de bussqueda
num_parents_mating = 40 #Antes 40

sol_per_pop = 3500 #Antes 2000
num_genes = 2
mutation_num_genes=1


init_range_low = [0,0]
init_range_high = [2000,1000]

parent_selection_type = "tournament" #antes "sss"
keep_parents = 5 #antes 1

crossover_type = "two_points"

mutation_type = "random"
mutation_percent_genes = 12 #Antes 30
gene_type = int

# After the parameters are prepared, an instance of the pygad.GA class is created.

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       mutation_num_genes=mutation_num_genes,
                       gene_type=gene_type)

ga_instance_minima = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_func_minima,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       mutation_num_genes=mutation_num_genes,
                       gene_type=gene_type)

# After creating the instance, the run() method is called to start the optimization.

ga_instance.run()

# After the run() method completes, information about the best solution found by PyGAD can be accessed.

solution, solution_fitness, solution_idx = ga_instance.best_solution()
x_max, y_max= int(solution[0]), int(solution[1])#Guardo las coordenadas
alt_max = mapa[x_max, y_max]
print("Parameters of the best solution : {solution}".format(solution=solution))

print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
ga_instance.plot_fitness()

prediction = mapa[int(solution[0]),int(solution[1])]
print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))
print("Valor de altitud maximo encontrado: ",alt_max)

# ================== Ahora el mínimo ==================
print("="*60)

ga_instance_minima.run()

solution, solution_fitness, solution_idx = ga_instance_minima.best_solution()
x_min, y_min = int(solution[0]), int(solution[1])
alt_min = mapa[x_min, y_min]
print("Parameters of the best solution : {solution}".format(solution=solution))

print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
ga_instance_minima.plot_fitness()

prediction = mapa[int(solution[0]),int(solution[1])]
print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))
print("Valor de altitud minimo encontrado: ",alt_min)



elev.mostrar_mapa(mapa, punto_max=(x_max, y_max), punto_min=(x_min, y_min))