import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from generator import *
import math
import random
from optparse import OptionParser
from generator import distributions

# This one is similar to Fig 2c in Rahman, et. al., except we randomly assign
# each task to a level, ensuring that each level is assigned at least one 
# task. Then for each task t in levels 1..L we choose x tasks from the level
# above to set as parents of t, where:
#
#   1 <= x <= min(size(level above), floor(W/2))
#
# To ensure each root task is given at least one childe, for each task t in 
# the root level we choose x tasks from the level below to make as children 
# of t, where x is given as:
#
#   1 <= x <= min(size(level below), floor(W/2))
# 
# As a result of this process, dependencies are only created between tasks in
# adjacent levels of the workflows. This gives more regular-looking workflows.
# The rules for Fig 2c given in the paper can produce really complex workflows
# that often come out looking like pyramids or diamonds because of the task
# selection rules.



class RandLevel():
    def __init__(self):
        self.parser = OptionParser()
        self.parser.add_option("-D", "--dax", dest="daxfile",
                help="Write workflow DAX to FILE", metavar="FILE")
        self.parser.add_option("-d", "--dot", dest="dotfile",
                help="Write workflow DOT to FILE", metavar="FILE")
    
    def setoptions(self, parser):
        self.parser.add_option("-N", "--numtasks", dest="tasks", metavar="n", type="int", default=500,
            help="Number of tasks in workflow [default: %default]")
        self.parser.add_option("-L", "--numlevels", dest="levels", metavar="n", type="int", default=10,
            help="Number of levels in the workflow [default: %default]")
            
        self.parser.add_option("", "--rtlow", dest="rtlow", metavar="t", type="float", default=5,
            help="Lower bound on runtime in seconds [default: %default]")
        self.parser.add_option("", "--rthigh", dest="rthigh", metavar="t", type="float", default=50,
            help="Upper bound on runtime in seconds [default: %default]")
            
        self.parser.add_option("", "--slow", dest="slow", metavar="t", type="float", default=1,
            help="Lower bound on file size in GB [default: %default]")
        self.parser.add_option("", "--shigh", dest="shigh", metavar="t", type="float", default=5,
            help="Upper bound on file size in GB [default: %default]")

        self.parser.add_option("", "--milow", dest="milow", metavar="t", type="float", default=1000,
            help="Lower bound on file size in GB [default: %default]")
        self.parser.add_option("", "--mihigh", dest="mihigh", metavar="t", type="float", default=10000,
            help="Upper bound on file size in GB [default: %default]")
        
    def genworkflow(self, options):
        return self.randlevel(options.tasks, options.levels, distributions.UniformDistribution(options.rtlow, options.rthigh), distributions.UniformDistribution(options.slow, options.shigh),distributions.UniformDistribution(options.milow, options.mihigh))
    
    
    def randlevel(self,N, L, runtimeDist,sizeDist,miDist):
        #    Approximate width of workflow
        W = int(math.ceil(N/float(L)))
    
        # Maximum in degree of a task
        max_id = int(math.floor(W/float(2)))
    
        w = Workflow(name="randlevel", description="""Random workflow (Similar to Figure 2c in Rahman et al, but level-oriented)""")
    
        tasks = []
        levels = [list() for l in range(0,L)]
        for i in range(0,N):
            tout = File("task_%d_out.dat"%i, size=sizeDist()*KB)
            t = Job(id="task_%d"%i, namespace="rand", name="Task", runtime=runtimeDist()*SECONDS, MI=miDist(),outputs=[tout])
            w.addJob(t)
            tasks.append(t)
        
            if i < L: # Ensure each level gets one task
                levels[i].append(t)
            else:
                level = random.randint(0,L-1)
                levels[level].append(t)
    
        # Choose random children for root level
        # Make sure each root task gets a child
        for t in levels[0]:
            k = random.randint(1, min(max_id, len(levels[1])))
        
            children = random.sample(levels[1], k)
        
            for c in children:
                for i in t.outputs:
                    c.addInput(i)
    
        # For levels 1..L choose random parents
        for l in range(1,L):
            for t in levels[l]:
                k = random.randint(1, min(max_id, len(levels[l-1])))
            
                # make sure level 1 doesn't get too many connections to level 0
                k = max(0, k - len(t.inputs))
            
                parents = random.sample(levels[l-1], k)
                for p in parents:
                    for o in p.outputs:
                        t.addInput(o)
    
        return w

    #RandLevel().main(*args)

#if __name__ == '__main__':
#  main("-D","sankalp.xml")
