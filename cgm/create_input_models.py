import numpy as np
import sys

num_pts = int(sys.argv[1])
indices = np.arange(0, num_pts, dtype=float) + 0.5

phi = np.arccos(1 - 2*indices/num_pts)
theta = np.pi * (1 + 5**0.5) * indices

x, y, z = np.cos(theta) * np.sin(phi), np.sin(theta) * np.sin(phi), np.cos(phi);

print('comment')
print()
print(num_pts+1, 'atoms')
print()
print('2 atom types')
print()
size = 100.0
print("""-{0} {0} xlo xhi
-{0} {0} ylo yhi
-{0} {0} zlo zhi""".format(size))
print()
print('Atoms')
print()
print('1 1 0 0 0')
for natoms, (i,j,k) in enumerate(zip(x,y,z), start=2):
    print(natoms, '2', i, j, k)


"""
comment

15 atoms

2 atom types

-1.0 1.0 xlo xhi
-1.0 1.0 ylo yhi
-1.0 1.0 zlo zhi

Atoms

1 1 0 0 0
2 2 -0.33413792 -0.35625461 -0.87260215
3 2  0.17218082  0.95011611  0.26006374
4 2  0.02198741 -0.99437216  0.10363668
5 2  0.52765926  0.75155846  0.39589845
6 2  0.32930148  0.93201338 -0.15136578
7 2  0.38435623  0.84769805  0.36562044
8 2 -0.77055373 -0.1995969  -0.60531646
9 2  0.46810601  0.74870105 -0.4693863 
10 2 -0.02517232  0.80096978 -0.59817536
11 2  0.56262423  0.27898442  0.77821698
12 2 -0.55214448  0.79072637 -0.26436393
13 2 -0.27269491 -0.78388676  0.55781631
14 2  0.69648329 -0.71364073 -0.07501952
15 2 -0.40867748  0.41050472  0.81514943
"""
