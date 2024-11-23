

population = [8, 16, 32, 64]

selection_range = len(population)
for lordosis in range(0, selection_range):
    for group in range(selection_range-1, lordosis, -1): # Define mating range

        female = population[lordosis]
        male = population[group]
        print(female, male)
    print()