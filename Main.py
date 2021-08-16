'''
Homework 3: Prim's Algorithm
Carter King
Dr. Sanders
CS 355 Advanced Algorithms
5 October 2018
Python 3
'''

import sys
import heapq
listOfCities = []

'''
Function: parseCityFile(filename)
 This function takes a .txt file of strings of cities with distances between and creates a dictionary with the 
 city as a key value and a tuple containing a distance from this city to another, with the second element being a 
 dictionary of the destination city as a key, and the distance as a value
 parameters: filename - a string of the name of the file
 returns: adjList - an adjacency Dictionary of the cities and distances from the file
'''

def parseCityFile(filename):
    global listOfCities
    adjList = {}
    myFile = open(filename,'r')

    for i, line in enumerate(myFile): #number each line of the file
        pieces = line.split(' ')  #each line split between spaces
        departCity = pieces[0].strip(' ') #first city listed in first line is departure city
        destCity = pieces[1].strip()
        pieces[len(pieces)-1].strip('\n')
        if i == 0:
            for b, piece in enumerate(pieces):
                if b == len(pieces)-1:
                    pieces[b] = pieces[b].strip()
            listOfCities = pieces #Initial list of cities, with start city in pos 0
        else:
            if departCity:
                destinationAndCost = {}
                if departCity in adjList.keys():
                    adjList[departCity][destCity] = int(pieces[2].strip()),destCity #add new city to existing city key
                    if destCity in adjList.keys():
                        adjList[destCity][departCity] = int(pieces[2].strip()),departCity #since undirected, add same for dest -> depart
                    else:
                        destinationAndCost = {} #depart not yet key value, so create tuple to add as value
                        destinationAndCost[departCity] =int(pieces[2].strip()),departCity
                        adjList[destCity] = destinationAndCost
                else:
                    destinationAndCost[destCity] = int(pieces[2].strip()), destCity
                    adjList[departCity] = destinationAndCost #dest not yet key value, so create tuple to add as value
                    if destCity in adjList.keys():
                        adjList[destCity][departCity] = int(pieces[2].strip()),departCity
                    else:
                        destinationAndCost = {}
                        destinationAndCost[departCity] =int(pieces[2].strip()),departCity #depart not yet key value, so create tuple to add as value
                        adjList[destCity] = destinationAndCost
    return adjList


'''
Function: PrimsAlg(Graph)
 This function takes in a graph as an adjaceny dictionary and uses a list for distance, visited/known, and previous
 to use Prim's Algorithm in order to create a Minimum Spanning Tree of the given graph
 parameters: Graph - an adjacency dictionary to use Prim's Algorithm on
 returns: orderOfPref - a list of tuples in the order in which the MST was created
'''

def PrimsAlg(Graph):
    global listOfCities
    known = [False] * len(listOfCities) #list of visited cities, all set to False
    distance = [sys.maxsize] *len(listOfCities) #list of distance from start to finish all set to maxsize
    previous = [None] * len(listOfCities) #list of previous city in MST, all initialized to None
    q = [] #to be used as priority queue
    visitedSet = set() #maintain set of those that have already been visited
    cityAndListPosition = []
    for j, aCity in enumerate(listOfCities):
        cityAndListPosition.append((listOfCities[j],j)) #list of tuples with position in the lists(known,distance, previous)

    baseCity = listOfCities[0] #home city
    currCity = baseCity
    visitedSet.add(currCity) #add initial city to set of those visited
    known[0] = True
    distance[0] = 0
    orderOfPop = [] #list fo keeping track
    for x in Graph[baseCity]:
        heapq.heappush(q, (Graph[baseCity][x][0], Graph[baseCity][x][1], baseCity)) #priority queue consist of tuples (distance, destCity, departCity)

    while(len(visitedSet) != len(listOfCities)): #All cities visited
        destinationCityTuple = heapq.heappop(q)
        while(str(destinationCityTuple[1]) in visitedSet): #if pop and destCity already been visited, pop again
            destinationCityTuple = heapq.heappop(q)
        orderOfPop.append(destinationCityTuple)
        currCity = destinationCityTuple[2]
        destinationCity = destinationCityTuple[1]
        visitedSet.add(destinationCity) #adding to visited, setting known to true, previous is departCity, distance kept as distance of previous + distance
        known[listOfCities.index(destinationCity)] = True
        previous[listOfCities.index(destinationCity)] = currCity
        distance[listOfCities.index(destinationCity)] = distance[listOfCities.index(currCity)] + destinationCityTuple[0]
        if destinationCity in Graph.keys(): #if city can explore other cities, add to Priority queue
            for n in Graph[destinationCity]:
                if n in visitedSet: #don't push any dest cities that have already been visited
                    continue
                else:
                    heapq.heappush(q, (Graph[destinationCity][n][0],Graph[destinationCity][n][1],destinationCity))

    return orderOfPop



def main():
    # Show them the default len is 1 unless they put values on the command line
    print(len(sys.argv))
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
    else:
        fileName = input("What .txt file would you like to use? ")
        completeGraph = parseCityFile(fileName)
        orderOfEvents = PrimsAlg(completeGraph)
        sumDistance = 0
        for n in orderOfEvents:
            sumDistance = sumDistance + n[0] #distance of MST
        print(sumDistance)
        for y in orderOfEvents: #Order new edges/nodes added to MST
            print(y[2], ' ', y[1], ' ', y[0])


main()