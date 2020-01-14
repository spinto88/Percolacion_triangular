from axelrod_py import *

rand.seed(123452)

for N in [64, 128, 256, 512, 768, 1024, 2048]:

  M = 0.5*N*(N-1)
    
  for topology in ['lattice', 'random_regular']:

    if topology == 'random_regular':

        for degree in [4, 16, N]:

            mysys = Axl_network(n = N, non_zero_links = 100, topology = topology, degree = degree)

            for i in range(1000):

                for nz in [int(m) for m in np.logspace(0, np.log10(M), 61)]:
                    mysys.init_links(nz)
                    mysys.evolution()

                    mysys.save_fragments_distribution("RGDegree{}_N{}.dat".format(degree,N))

    else:

        if N in [64, 256, 1024]:

            mysys = Axl_network(n = N, non_zero_links = 100, topology = topology)

            for i in range(1000):

                for nz in [int(m) for m in np.logspace(0, np.log10(M), 61)]:
                    mysys.init_links(nz)
                    mysys.evolution()

                    mysys.save_fragments_distribution("Lattice_N{}.dat".format(N))


