import csv
import math
import sys
from operator import itemgetter
import numpy
import itertools


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


def greedy(clients, distances, truck_capacity):                                                                                                 #Greedy strategy to resolve the problem
    routes = []                                                                                                                                 #List that will store the final routes
    route_distance = []                                                                                                                         #List that will store the total distance of that route
    route_usage = []                                                                                                                            #List that will store the truck capacity usage (in float)
  
    
    while hasDemand(clients):                                                                                                                   #While some client has an active demand
        new_route = []                                                                                                                          #creates a new route
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
            
            capacity = capacity - clients[next-1][2]                                                                                              #Reduce the capacity of the current truck ny the demand of the client
            distance = distance + distances[pos][next]                                                                                          #Add the distance to the new client to the total distance traveled
            clients[next-1][2] = 0                                                                                                                  #We satisfied the demand of the client, so set his demand to 0
            new_route.append(next)                                                                                                              #Add the client to the current route
            pos = next                                                                                                                          #Travel (set) to the place of that client
        
                                                                                                                                                #When you broke from the loop, it means that the truck has to go to the deposit
        new_route.append(0)                                                                                                      #Add the deposit to the route of the truck
        distance = distance + distances[pos][0]                                                                                  #Add the distance to travel to the deposit
        
        routes.append(new_route)                                                                                                                #Add the current route to the list of all routes
        route_distance.append(distance)                                                                                                         #Add the current distance traveled to the list of all distances
        route_usage.append((abs(capacity - truck_capacity)*100)/truck_capacity)                                                                 #Calculate the usage percentage and add it to the list of truck capacity usage
        

                                                                                                                                                #Breaking from the last loop means that all demands have been satisfied
    for id, i in enumerate(clients):                                                                                                            # so now you only need to display what happened during the execution
        print(f'Client {id+1} Demands: {i[2]}')                                                                                                   #First, print the demand, just to make sure that everything is ok
    
    print(f'Um total de {len(routes)} rotas foram utilizadas. Na sequência dados sobre estas rotas estão dispostos:')                           #After, print how many routes have been utilized
    for i in range(len(routes)):
        print(f'A rota com id {i} seguiu o seguinte caminho: {routes[i]}.')                                                                     #Then, print the data about every route, like the route itself, the distance traveled
        print(f'Essa rota percorreu uma distância de {route_distance[i]} e aproveitou {route_usage[i]}% da capacidade do caminhão.')            # and the truck capacity usage percentage
    


def best_local(clients, distances, truck_capacity):
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
        
        new_route.append(0)                                                                                                      #Add the deposit to the route of the truck
        distance = distance + distances[pos][0]                                                                                  #Add the distance to travel to the deposit
        
        routes.append(new_route)                                                                                                                #Add the current route to the list of all routes
        route_distance.append(distance)                                                                                                         #Add the current distance traveled to the list of all distances
        route_usage.append((abs(capacity - truck_capacity)*100)/truck_capacity)                                                                 #Calculate the usage percentage and add it to the list of truck capacity usage
        
                                                                                                                                                #Breaking from the last loop means that all demands have been satisfied
                                                                                                                                                
    for i in routes:
        print(i)
    print(sum(route_distance))



def brute_force(clients, distances, truck_capacity):
    test = 0
            
    
    





if __name__ == '__main__':
    #Reading Document
    with open('vrpnc99.txt', 'r') as f:
        reader = csv.reader(f, delimiter=' ', skipinitialspace=True)
        
        row1 = next(reader)                                                                                                                 #Row 1 has the number of clients and the truck capacity
        n_clients = int(row1[0])
        truck_capacity = int(row1[1])
        
        print(f'Number of Clients = {n_clients}, Truck Capacity = {truck_capacity}')                                                        #Outputs these parameters
        
        row2 = next(reader)                                                                                                                 #Row 2 has the coordinates of the deposit
        deposit = [int(row2[0]), int(row2[1])]
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
    
    for id, i in enumerate((clients)):                                                                                                           #Uptdate the matrix with the distance between the deposit and every client
        distances[0][id+1] = euclidean(deposit[0], deposit[1], i[0], i[1])                                    #and the distance from every client to the deposit
        distances[id+1][0] = euclidean(deposit[0], deposit[1], i[0], i[1])
    
    for idi, i in enumerate(clients):                                                                                                       #Update the matrix with the distances between every client
        for idj, j in enumerate(clients):
            distances[idi+1][idj+1] = euclidean(i[0], i[1], j[0], j[1])
            
    
    #greedy(clients, distances, truck_capacity)                                                                                              #Calls the greedy algoritm to resolve the problem
    #best_local(clients, distances, truck_capacity)
    brute_force(clients, distances, truck_capacity)
    
    