import csv
import math
import sys
from operator import itemgetter
import numpy
import itertools
import copy


#Initialize a matrix (list of lists) with some initial number
def matrix(x,y,initial):
    return [[initial for i in range(x)] for j in range(y)]


#Calculate the euclidean distance between two coordinates
def euclidean(x1, y1, x2, y2):
    x = x1 - x2
    y = y1 - y2
    x = x * x
    y = y * y
    return math.sqrt(x + y)


#Function to look if any clients has demands
def hasDemand(clients):
    hasDemand = False
    for i in clients:
        if i[2] > 0:
            hasDemand = True
            break
    
    return hasDemand

#Greedy strategy to resolve the problem
def greedy(clients, distances, truck_capacity, verbose):
    if verbose:
        print("Starting Greedy Solution...")                                                                                                 
    
    routes = []                                                                                                                                 #List that will store the final routes
    route_distance = []                                                                                                                         #List that will store the total distance of that route
    
    while hasDemand(clients):                                                                                                                   #While some client has an active demand
        new_route = []                                                                                                                          # creates a new route
        pos = 0                                                                                                                                 #The first position always is the deposit
        capacity = truck_capacity                                                                                                               #The initial capacity is the truck capacity
        distance = 0                                                                                                                            #No distance is yet traveled
        new_route.append(pos)
        while capacity > 0:                                                                                                                     #While the new truck(route) has capacity
            next = -1                                                                                                                           
            for id, i in enumerate(clients):                                                                                                    #Search for the first client that has a demand and the demand
                if i[2] > 0 and capacity >= i[2]:                                                                                               #is less than the current capacity of the new route
                    next = id + 1                                                                                                               #When the first client is found, set it to next and stop looking
                    break
            
            if next == -1:                                                                                                                      #If no clients has been found, the truck cannot go anywere, so stop
                break                                                                                                                           # looking and send it back
            
            capacity = capacity - clients[next-1][2]                                                                                            #Reduce the capacity of the current truck ny the demand of the client
            distance = distance + distances[pos][next]                                                                                          #Add the distance to the new client to the total distance traveled
            clients[next-1][2] = 0                                                                                                                  #We satisfied the demand of the client, so set his demand to 0
            new_route.append(next)                                                                                                              #Add the client to the current route
            pos = next                                                                                                                          #Travel (set) to the place of that client
        
                                                                                                                                                #When you broke from the loop, it means that the truck has to go to the deposit
        new_route.append(0)                                                                                                                     #Add the deposit to the route of the truck
        distance = distance + distances[pos][0]                                                                                                 #Add the distance to travel to the deposit
        
        routes.append(new_route)                                                                                                                #Add the current route to the list of all routes
        route_distance.append(distance)                                                                                                         #Add the current distance traveled to the list of all distances
 

    if verbose:                                                                                                                                 #Breaking from the last loop means that all demands have been satisfied    
        print(f'A total of {len(routes)} routes were used. The routes used were:')                                                              #After, print how many routes have been utilized
        for r in range(len(routes)):
            print(f'The route with id {i} follow the path: {routes[i]}.', end='')                                                               #Then, print the data about every route, like the route itself, the distance traveled
            print(f'This route covered a distance of {route_distance[i]}.')
    
    print("Greedy Solution:")                                                                                                                   #The last thing to do is to show the short output of the strategy
    print("Routes: ")
    for r in routes:
        print(r)
    print(f'Total Distance: {sum(route_distance)}\n\n')


def best_local(clients, distances, truck_capacity, verbose):
    if verbose:
        print("Starting Best Local Solution...")
    
    routes = []
    route_distance = []
    route_usage = []
    
    while hasDemand(clients):
        new_route = []
        pos = 0
        distance = 0
        capacity = truck_capacity
        new_route.append(0)
        while(capacity > 0):
            next = -1
            best_value = -1
            
            for id, i in enumerate(clients):
                if i[2] > 0 and i[2] <= capacity and distances[pos][id+1] != 0:
                    value = i[2] / distances[pos][id+1]
                    if value > best_value:
                        next = id+1
                        best_value = value
                    
            if next == -1:
                break
            
            capacity = capacity - clients[next-1][2]
            distance = distance + distances[pos][next]
            clients[next-1][2] = 0
            new_route.append(next)
            pos = next
        
        new_route.append(0)                                                                                                                     #Add the deposit to the route of the truck
        distance = distance + distances[pos][0]                                                                                                 #Add the distance to travel to the deposit
        
        routes.append(new_route)                                                                                                                #Add the current route to the list of all routes
        route_distance.append(distance)                                                                                                         #Add the current distance traveled to the list of all distances
        route_usage.append((abs(capacity - truck_capacity)*100)/truck_capacity)                                                                 #Calculate the usage percentage and add it to the list of truck capacity usage
        
                                                                                                                                                #Breaking from the last loop means that all demands have been satisfied
    print("Best Local Solution: \nRoutes: ")                                                                                                                                     
    for i in routes:
        print(i)
    print(f'Total Distance: {sum(route_distance)}\n\n')



def brute_force(clients, distances, truck_capacity, verbose):
    
    if verbose:
        print("Starting Brute Force Solution...")
        
    lst = numpy.arange(1, len(clients)+1)
    lst_p = itertools.permutations(lst, len(clients))
    
    if verbose:
        print("List of permutations Created")

    solutions = {}

    for idx, permutation in enumerate(lst_p):
        routes = []
        route_distance = []
        clients_ = copy.deepcopy(clients)
        while hasDemand(clients_):
            new_route = []
            capacity = truck_capacity
            pos = 0
            distance = 0
            new_route.append(pos)
            while capacity > 0:
                next = -1                                                                                                                           
                for i in permutation:                                                                                                               #Search for the first client that has a demand and the demand
                    if clients_[i-1][2] > 0 and capacity >= clients_[i-1][2]:                                                                       #is less than the current capacity of the new route
                        next = i                                                                                                                    #When the first client is found, set it to next and stop looking
                        break
                
                if next == -1:                                                                                                                      #If no clients has been found, the truck cannot go anywere, so stop
                    break                                                                                                                           # looking and send it back
                
                capacity = capacity - clients_[next-1][2]                                                                                            #Reduce the capacity of the current truck ny the demand of the client
                distance = distance + distances[pos][next]                                                                                          #Add the distance to the new client to the total distance traveled
                clients_[next-1][2] = 0                                                                                                              #We satisfied the demand of the client, so set his demand to 0
                new_route.append(next)                                                                                                              #Add the client to the current route
                pos = next                                                                                                                          #Travel (set) to the place of that client
            
                                                                                                                                                    #When you broke from the loop, it means that the truck has to go to the deposit
            new_route.append(0)                                                                                                                     #Add the deposit to the route of the truck
            distance = distance + distances[pos][0]                                                                                                 #Add the distance to travel to the deposit
            
            routes.append(new_route)                                                                                                                #Add the current route to the list of all routes
            route_distance.append(distance)                                                                                                         #Add the current distance traveled to the list of all distances
        
        routes_distance = sum(route_distance)
        solutions.update({sum(route_distance):routes})
        if verbose:
            print(f"Permutation {permutation} n° {idx+1} out of {math.factorial(len(clients))+1} checked.\nThe added Solution is {routes_distance}:{routes}\n\n")
    
    
    solutions = dict(sorted(solutions.items()))

    best_route = solutions.get(list(solutions.keys())[0])

    print('Brute Force Best Solution:\nRoutes:')
    for r in best_route:
        print(r)
    print(f'Total distance: {list(solutions.keys())[0]}\n\n')



if __name__ == '__main__':
    
    args = len(sys.argv)
    if args != 4:
        print("Remember to pass two arguments: the name of the file, followed by the type of output and then the chosen strategy")
        print("The types of outputs are: \'0\' for simple output or \'1\' for verbose output")
        print("For the algorithms chosen: \'greedy\' for the greedy strategy, \'bestlocal\' for the best local strategy, \'bruteforce\' for the Brute Force strategy or \'all\' to run all the strategy")
        sys.exit()
        
    filename = sys.argv[1]
    
    verbose = None
    if int(sys.argv[2]) == 0:
        verbose = False
    elif int(sys.argv[2]) == 1:
        verbose = True
    else:
        print("Check the number given for the type of output: \'0\' for simple output or \'1\' for verbose output")
    
    
    #Reading Document
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
        
        row1 = next(reader)                                                                                                                 #Row 1 has the number of clients and the truck capacity
        n_clients = int(row1[0])
        truck_capacity = int(row1[1])
        
        
        row2 = next(reader)                                                                                                                 #Row 2 has the coordinates of the deposit
        deposit = [int(row2[0]), int(row2[1])]
        if verbose:
            print(f'Number of Clients = {n_clients}, Truck Capacity = {truck_capacity}')                                                        #Outputs these parameters
            print(f'Deposit coordinates: x={deposit[0]}, y={deposit[1]}')                                                                       #Outputs the deposit coordinates
        
        clients = []                                                                                                                        #Creates a list that will store all the clients
        
        for row in reader:                                                                                                                  #Every client has 3 parameters, [0] contains the x coordinate,
            pos_x = int(row[0])                                                                                                             #[1] contains the y coordinate and 3 contais the demand of the client
            pos_y = int(row[1])
            demand = int(row[2])
            clients.append([pos_x, pos_y, demand])

    distances = matrix(len(clients)+1, len(clients)+1, sys.maxsize)                                                                         #creates a matrix (list of lists) with a high number, representing the
                                                                                                                                            #distance between the 2 axis. Example: distances[1][2] contains the
                                                                                                                                            #distance between the client 1 and the client 2
    
    for idi, i in enumerate(clients):                                                                                                       #Update the matrix with the distances between every client
        for idj, j in enumerate(clients):
            distances[idi+1][idj+1] = euclidean(i[0], i[1], j[0], j[1])
        distances[0][id+1] = euclidean(deposit[0], deposit[1], i[0], i[1])                                                                  #Uptdate the matrix with the distance between the deposit and every client
        distances[id+1][0] = euclidean(deposit[0], deposit[1], i[0], i[1])                                                                  # and the distance from every client to the deposit
   
    
    strategy = str(sys.argv[3])
    print(f'\nChosen strategy: {strategy}\n')
    
    if strategy == 'greedy' or strategy == 'all':
        greedy(copy.deepcopy(clients), distances, truck_capacity, verbose)                                                                  #Calls the greedy strategy to solve the problem
    if strategy == 'bestlocal' or strategy == 'all':
        best_local(copy.deepcopy(clients), distances, truck_capacity, verbose)                                                              #Calls the Best Local strategy to solve the problem
    if strategy == 'bruteforce' or strategy == 'all':
        brute_force(copy.deepcopy(clients), distances, truck_capacity, verbose)                                                             #Calls the Brute Force strategy to solve the problem
    
    