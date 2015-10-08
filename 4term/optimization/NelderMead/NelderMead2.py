import functools

from decimal import Decimal
import math


from subprocess import Popen, PIPE

gnuplot = r'C:\Program Files (x86)\gnuplot\bin\gnuplot' 
plot=Popen([gnuplot,'-persist'],stdin=PIPE,stdout=PIPE,stderr=PIPE) 
#plot.stdin.write(b'''set view map\n
#set logscale z 10\n
#unset surface\n
#unset label\n
#set contour base\n
#set xrange [-2:2]
#set yrange[-0.5:3]

#f(x, y) = (1 - x) ** 2 + 100 * (y - x ** 2) ** 2
#splot f(x, y) notitle 

#set table 'contour.dat'  
#replot  
#unset table 
#reset  
#plot 'contour.dat' with line notitle, "tri.txt" u 1:2 w lines notitle
#''')
#plot.stdin.flush()

counter = 0
nr = 0
ne = 0
noc = 0
nic = 0
ns = 0

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
        
    def __repr__(self):
        return ' {0}\n'.format( (counter) / 100).join(map(str, self.points)) + ' {0} \n'.format( (counter) / 100) + str(self.points[0]) + ' {0} \n\n'.format((counter) / 100)
        

def NelderMead_minimize(objective_func, init_simplex,
    rho = Decimal(1), chi = Decimal(2), gamma = Decimal(0.5), sigma = Decimal(0.5), max_iter = 10000, eps = Decimal(1e-6)):
    
    global counter
    global nr, ne, noc, nic, ns
    current_simplex = init_simplex
    
    f.write(current_simplex.__repr__())
    
    for iter_num in range(max_iter):
        current_simplex.sort(objective_func)
        centroid = current_simplex.centroid()
        
        counter += 1
        accepted_point = None
        
        # reflection
        reflection_point = centroid + (centroid - current_simplex.worst_point()).mul_by_const(rho)
        
        #print(centroid)
        #print(reflection_point)
        

        if (objective_func(current_simplex.best_point()) <=
            objective_func(reflection_point) <
            objective_func(current_simplex.second_worst_point())):
            
            nr += 1
            accepted_point = reflection_point
            
        elif (objective_func(reflection_point) < 
              objective_func(current_simplex.best_point())):
            
            # expansion
            expansion_point = centroid + (reflection_point - centroid).mul_by_const(chi)
            
            if (objective_func(expansion_point) <
                objective_func(reflection_point)):
                ne += 1
                accepted_point = expansion_point
            else:         
                nr += 1
                accepted_point = reflection_point
                
        else:
            # contract
            
            if (objective_func(reflection_point) <
                objective_func(current_simplex.worst_point())):
                # outside contract
                outside_contract_point = centroid + (reflection_point - centroid).mul_by_const(gamma)
                
                if (objective_func(outside_contract_point) <= objective_func(reflection_point)):
                    noc += 1
                    accepted_point = outside_contract_point
                    
            else: 
                # inside contract
                inside_contract_point = centroid + (centroid - current_simplex.worst_point()).mul_by_const(-gamma)
                
                if (objective_func(inside_contract_point) < objective_func(current_simplex.worst_point())):
                    nic += 1
                    accepted_point = inside_contract_point
                    
                    
        if accepted_point is not None:
            current_simplex.replace_worst(accepted_point)   
            
        else:
            # shrink
            
            new_points = list(map(lambda p: current_simplex.best_point() + (p - current_simplex.best_point()).mul_by_const(sigma),
                current_simplex.points))
                    
            current_simplex = Simplex(new_points)
            ns += 1
        
        f.write(current_simplex.__repr__())
        
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

def mckinnon(point):
    x = point.coord[0]
    y = point.coord[1] 
    
    return ((x > 0) and (360 * x ** 2 + y ** 2 + y) or (6 * x ** 2 + y ** 2 + y))



f = open('trian.txt', 'w')

x_min, iter_num = NelderMead_minimize(sphere, Simplex([Point((Decimal(0), Decimal(0))), Point((Decimal(2.5), Decimal(2.5))), Point((Decimal(-2.5), Decimal(2.5)))]))

print(nr, ne, noc, nic, ns)
print(iter_num)

print(math.sqrt((x_min.coord[0] - 0) ** 2 + (x_min.coord[1] - 0) ** 2))

#print(math.sqrt((x_min.coord[0] + Decimal(2.805118)) ** 2 + (x_min.coord[1] - Decimal(3.131312)) ** 2))
#print(math.sqrt((x_min.coord[0] - Decimal(3)) ** 2 + (x_min.coord[1] - Decimal(2)) ** 2))

#print(NelderMead_minimize(himmelblau, Simplex([Point((Decimal(100), Decimal(100))), Point((Decimal(200), Decimal(200))), Point((Decimal(200), Decimal(100)))])))


#print(NelderMead_minimize(mckinnon, Simplex([Point((Decimal(0), Decimal(0))), Point((Decimal(1), Decimal(1))), Point(((Decimal((1 + math.sqrt(Decimal(33))) / 8)), Decimal((1 - math.sqrt(Decimal(33))) / 8)))])))
f.close()



plot.stdin.write(b'''

set view map\n
#set logscale z 10\n
unset surface\n
unset label\n
set contour base\n
set xrange [-3:3]
set yrange [-3:3]

f(x, y) = -20 * exp(0.2 * sqrt(0.5 * (x ** 2 + y ** 2))) - exp(0.5 *  (cos(2 * pi * x) + cos(2 * pi * y))) + 20 + exp(1)
splot f(x, y) notitle 

set table 'contour.dat'  
replot  
unset table 
reset  
set terminal postscript eps color
set output 'rrr.eps'
unset colorbox
plot 'contour.dat' with line notitle  lt rgb '#339933', "trian.txt" u 1:2:3 with lines lc palette notitle 

''')


plot.stdin.flush()


#, "trian.txt" u 1:2 w lines notitle

#lt palette frac $3'
#set terminal pngcairo size 3000px 3000px
#set output "my-plot2.png"
#