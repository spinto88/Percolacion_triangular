import os
import ctypes as C
import networkx as nx
import random as rand
import numpy as np

libc = C.CDLL(os.getcwd() + '/axelrod_py/libc.so')

class Axl_network(nx.Graph, C.Structure):

    """
    Axelrod network: it has nagents axelrod agents, and an amount of noise in the dynamics of the system. This class inherites from the networkx.Graph the way to be described.
    """
    _fields_ = [('nagents', C.c_int),
		('a', C.POINTER(C.POINTER(C.c_int))),
		('corr', C.POINTER(C.POINTER(C.c_int)))]

    def __init__(self, n, non_zero_links, topology = 'lattice', **kwargs):
        
	"""
        Constructor: initializes the network.Graph first, and set the topology and the agents' states. 
	"""
        # Init graph properties
        nx.Graph.__init__(self)
        nx.empty_graph(n, self)
        self.nagents = n

        # Model parameters
        self.nzl = non_zero_links

	# Random seed 
	self.seed = rand.randint(0, 10**7)

        # Init agents' states
        self.init_links(non_zero_links)
 
        # Init topology
        self.set_topology(topology, **kwargs)

    def set_topology(self, topology, **kwargs):
        """
        Set the network's topology
        """
        import set_topology as setop

        self.id_topology = topology

        self.adjm = setop.set_topology(self, topology, **kwargs).toarray()

        self.a = (self.nagents * C.POINTER(C.c_int))()
        for i in range(self.nagents):
            self.a[i] = ((self.nagents) * C.c_int)(*self.adjm[i])

    def init_links(self, non_zero_links):

	import random
	from itertools import combinations
	
	nzl = random.sample(list(combinations(range(self.nagents), 2)), k = non_zero_links)

        corr_matrix = np.zeros([self.nagents, self.nagents], dtype = np.int)

        for nz in nzl:
	    corr_matrix[nz[0],nz[1]] = 1

        corr_matrix += corr_matrix.T

        self.corr = (self.nagents * C.POINTER(C.c_int))()
        for i in range(self.nagents):
            self.corr[i] = ((self.nagents) * C.c_int)(*corr_matrix[i])

        self.nzl = non_zero_links

    def evolution(self, steps = 1):
        """
	Make n steps asynchronius evolutions of the system
        """
        libc.evolution_triangle_percolation.argtypes = [C.POINTER(Axl_network)]

        libc.evolution_triangle_percolation(C.byref(self))

    def get_corr_matrix(self):

        corr_matrix = np.zeros([self.nagents, self.nagents], dtype = np.int)
        for i in range(self.nagents):
            for j in range(i+1, self.nagents):
                corr_matrix[i][j] = self.corr[i][j]

        corr_matrix += corr_matrix.T
        for i in range(self.nagents):
            corr_matrix[i][i] = 1

        return corr_matrix


    def fragments_size(self):

        corr_matrix = self.get_corr_matrix()
        final_ad_matrix = np.zeros(corr_matrix.shape, dtype = np.int)
        for i in range(self.nagents):
            for j in range(i+1, self.nagents):
                if corr_matrix[i,j] == 1 and self.adjm[i,j] == 1:
                    final_ad_matrix[i,j] = 1

        final_ad_matrix += final_ad_matrix.T
        final_graph = nx.from_numpy_array(final_ad_matrix)
        fragments = [len(x) for x in list(nx.connected_components(final_graph))]

        return fragments
 
    def save_fragments_distribution(self, fname):
	 
        fragment_sizes = [d for d in self.fragments_size()]

        fp = open(fname, 'a')
        fp.write('{},'.format(self.nzl))
        fp.write(', '.join([str(s) for s in fragment_sizes]))
        fp.write('\n')
        fp.close()
        
