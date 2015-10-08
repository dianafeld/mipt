import functools

from decimal import Decimal
import math


class Point:
    
    def __init__(self, coord_tuple):
        self.coord = coord_tuple
        
        
    def __add__(self, other):
        return Point(tuple(x + y for x, y in zip(self.coord, other.coord)))
    
    def __sub__(self, other):
        return Point(tuple(x - y for x, y in zip(self.coord, other.coord)))
    
    def mul_by_const(self, const):
        return Point(tuple(map(lambda x: x * const, self.coord)))    
    
    def div_by_const(self, const):
        return Point(tuple(map(lambda x: x / const, self.coord)))
    
    def dist(self, other):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(self.coord, other.coord)))
    
    def __repr__(self):
        return ' '.join(map(str, map(float, self.coord)))
    
    


class Simplex:
    
    def __init__(self, points):
        self.points = points
        
    def sort(self, key = None):
        self.points.sort(key = key)
        
    def centroid(self):
        return Point.div_by_const(functools.reduce(Point.__add__, self.points[:-1]), (len(self.points) - 1))
    
    def best_point(self):
        return self.points[0]
    
    def worst_point(self):
        return self.points[-1]
    
    def second_worst_point(self):
        return self.points[-2]
    
    def replace_worst(self, new_point):
        del self.points[-1]
        self.points.append(new_point)
        
        
    def standart_error(self, func):
        mean = sum(func(p) for p in self.points) / len(self.points)
        stderr = math.sqrt(sum((func(p) - mean) ** 2 for p in self.points)) / len(self.points)
        return stderr
        

def NelderMead_minimize(objective_func, init_simplex,
    rho = Decimal(1), chi = Decimal(2), gamma = Decimal(0.5), sigma = Decimal(0.5), max_iter = 10000, eps = Decimal(1e-6)):
    
    current_simplex = init_simplex
    
    for iter_num in range(max_iter):
        current_simplex.sort(objective_func)
        centroid = current_simplex.centroid()
        
        accepted_point = None
        
        # reflection
        reflection_point = centroid + (centroid - current_simplex.worst_point()).mul_by_const(rho)   

        if (objective_func(current_simplex.best_point()) <=
            objective_func(reflection_point) <
            objective_func(current_simplex.second_worst_point())):
            
            accepted_point = reflection_point
            
        elif (objective_func(reflection_point) < 
              objective_func(current_simplex.best_point())):
            
            # expansion
            expansion_point = centroid + (reflection_point - centroid).mul_by_const(chi)
            
            if (objective_func(expansion_point) <
                objective_func(reflection_point)):
                
                accepted_point = expansion_point
            else:         
                accepted_point = reflection_point
                
        else:
            # contract
            
            if (objective_func(reflection_point) <
                objective_func(current_simplex.worst_point())):
                # outside contract
                outside_contract_point = centroid + (reflection_point - centroid).mul_by_const(gamma)
                
                if (objective_func(outside_contract_point) <= objective_func(reflection_point)):
                    
                    accepted_point = outside_contract_point
                    
            else: 
                # inside contract
                inside_contract_point = centroid + (centroid - current_simplex.worst_point()).mul_by_const(-gamma)
                
                if (objective_func(inside_contract_point) < objective_func(current_simplex.worst_point())):

                    accepted_point = inside_contract_point
                    
                    
        if accepted_point is not None:
            current_simplex.replace_worst(accepted_point)   
            
        else:
            # shrink
            
            new_points = list(map(lambda p: current_simplex.best_point() + (p - current_simplex.best_point()).mul_by_const(sigma),
                current_simplex.points))
                    
            current_simplex = Simplex(new_points)
        
        if current_simplex.standart_error(objective_func) < eps:
            return current_simplex.best_point(), iter_num + 1
            
    return current_simplex.best_point(), max_iter
            


def sphere(point):
    x = point.coord[0]
    y = point.coord[1]
    
    return x ** 2 + y ** 2      
            

def rosenbrock(point):
    x = point.coord[0]
    y = point.coord[1]
    
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

def himmelblau(point):
    x = point.coord[0]
    y = point.coord[1]
    
    return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2


def ackley(point):
    x = point.coord[0]
    y = point.coord[1]
    
    return -20 * math.e ** (0.2 * math.sqrt(0.5 * (x ** 2 + y ** 2))) - math.e ** (0.5 *  (math.cos(2 * math.pi * x) + math.cos(2 * math.pi * y))) + 20 + math.e


x_min, iter_num = NelderMead_minimize(sphere, Simplex([Point((Decimal(0), Decimal(0))), Point((Decimal(2.5), Decimal(2.5))), Point((Decimal(-2.5), Decimal(2.5)))]))


print('Minimum point {0}'.format(x_min))

print('Iterations {0}'.format(iter_num))




