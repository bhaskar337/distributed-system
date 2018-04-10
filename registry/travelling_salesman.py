import numpy as np
import itertools

class TravelingSalesman():
  def __init__(self, num_cities):
    self.matrix = self.Generate(num_cities)
    
  ''''def Process(self, string):
    matrix = np.fromstring(string, dtype=int, sep=' ')
    return np.reshape(matrix, (int(np.sqrt(matrix.shape[0])), -1))'''
  
  @staticmethod
  def Generate(num_cities):
    b = np.random.randint(213,2571,size=(num_cities, num_cities))
    b_symm = np.ceil((b + b.T)/2).astype(int)
    np.fill_diagonal(b_symm, 0)
    #result = ' '.join(' '.join('%d' %x for x in y) for y in b_symm)
    return b_symm
  
  def Distance(self, from_node, to_node):
    return self.matrix[from_node][to_node]
  
  def Route(self):
    all_routes = list(itertools.permutations(range(self.matrix.shape[0])))
    total_cost = {}
    for route in all_routes:
      cost = []
      for value in zip(route, route[1:]):
        cost.append(self.Distance(value[0], value[1])) 
      total_cost[route] = sum(cost)
    return min(total_cost, key = total_cost.get)

def call(n):    
    n = int(n)
    route = TravelingSalesman(n).Route()
    return route