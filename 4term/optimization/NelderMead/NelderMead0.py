import functools

from decimal import Decimal

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
    
    def __repr__(self):
        return str(self.coord)
    
    


class Simplex:
    
    def __init__(self, points):
        self.points = points
        
    def sort(self, key = None):
        self.points.sort(key = key)
        
    def centroid(self):
        #point_add = lambda p1, p2: tuple(x + y for x, y in zip(p1, p2))
        #return map(lambda x: x / (len(self.points) - 1), functools.reduce(point_add, self.points[:-2]))
        return Point.div_by_const(functools.reduce(Point.__add__, self.points[:-1]), (len(self.points) - 1))
    
    def best_point(self):
        return self.points[0]
    
    def worst_point(self):
        return self.points[-1]
    
    def second_worst_point(self):
        return self.points[-2]


class NelderMead:
    
    def __init__(self, objective_func, init_simplex, alpha = 1, beta = 2, gamma = 0.5, delta = 0.5, max_iter = 100, eps = 1e-3):
        self.objective_func = objective_func
        self.init_simplex = init_simplex
        
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        
        self.max_iter = max_iter
        self.eps = eps
        
        
    def NelderMead_minimize(self):
        current_simplex = self.init_simplex
        
        for iter_num in range(self.max_iter):
            current_simplex.sort(self.objective_func)
            centroid = current_simplex.centroid()
            
            # reflection
            reflection_point = centroid + (centroid - current_simplex.worst_point()).mul_by_const(self.alpha)
            
            print(centroid)
            print(reflection_point)
            
    
            if (self.objective_func(current_simplex.best_point()) <=
                self.objective_func(reflection_point) <
                self.objective_func(current_simplex.second_worst_point())):
                
                new_points = current_simplex.points[:-1]
                new_points.append(reflection_point)
                
                current_simplex = Simplex(new_points)
                
            elif (self.objective_func(reflection_point) < 
                  self.objective_func(current_simplex.best_point())):
                # expansion
                
                expansion_point = centroid + (centroid - current_simplex.worst_point()).mul_by_const(self.gamma)
                
                if (self.objective_func(expansion_point) <=
                    self.objective_func(reflection_point)):
            
            
        
            
            

def rosenbrock(point):
    x = point.coord[0]
    y = point.coord[1]
    
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

Rosenbrock = NelderMead(rosenbrock, Simplex([Point((0, 0)), Point((1, 1)), Point((0, 1))]))

Rosenbrock.minimize()

pass