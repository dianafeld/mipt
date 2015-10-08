



#import subprocess
#proc = subprocess.Popen([gnuplot,'-p'], 
                        #shell=True,
                        #stdin=PIPE,
                        #)

from subprocess import Popen, PIPE

gnuplot = r'C:\Program Files (x86)\gnuplot\bin\gnuplot' 
plot=Popen([gnuplot,'-persist'],stdin=PIPE)#,stdout=PIPE,stderr=PIPE) 
plot.stdin.write(b'''set view map\n
set logscale z 10\n
unset surface\n
unset label\n
set contour base\n
set xrange [-2:2]
set yrange[-0.5:3]

f(x, y) = (1 - x) ** 2 + 100 * (y - x ** 2) ** 2
splot f(x, y) notitle 

set table 'contour.dat'  
replot  
unset table 
reset  
plot 'contour.dat' with line notitle, "tri.txt" u 1:2 w lines notitle
''')


plot.stdin.flush()

#plot.stdin.write(b'''set zrange [0:1000]\n
#''')
#plot.stdin.write(b"set yrange [0:1]\n")
#plot.stdin.write(b"set xrange [-1:1]\n")
#plot.stdin.write(b"splot (1 - x) ** 2 + 100 * (y - x ** 2) ** 2\n")

# \n


#, "tri.txt" u 1:2:(g($1,$2)) w lines notitle