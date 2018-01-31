import numpy as np


def calculate_natoms(cn):
    natoms = 1000
    a = -0.68248  # +- 0.0842
    b = 0.10514  # +- 0.00724
    snatoms = a + b * cn
    snatoms = int(round(snatoms * natoms))
    lnatoms = natoms - snatoms
    print(cn, snatoms, lnatoms)
    return snatoms, lnatoms

with open('interatomic_ratios.txt') as f:
    data = f.readlines()
    data = [line.strip().split() for line in data]
    data = [[int(line[0]), float(line[1])] for line in data]


for cn, rstar in data:
    include = [9, 10, 11, 12, 13, 14, 15]
    if cn not in include:
        continue
    snatoms, lnatoms = calculate_natoms(cn)
    radius = 2.0
    large_large = radius
    small_small = radius / rstar
    large_small = (large_large + small_small) / 2.0
    ll_sigma = large_large / np.power(2, 1./6.)
    ss_sigma = small_small / np.power(2, 1./6.)
    ls_sigma = large_small / np.power(2, 1./6.)
    s = """
units             lj
atom_style        atomic
boundary          p p p

variable l equal 18.5  # correct for CN 11, 0.1 T (lj units); depends on lj parameters, including cutoff
region boxid block  0.0 ${{l}}  0.0 ${{l}}  0.0 ${{l}}
create_box 2 boxid

variable s equal {snatoms}
variable l equal {lnatoms}
create_atoms 1 random {{s}} 9879 boxid 
create_atoms 2 random {{l}} 8987 boxid

mass 1 1.0
mass 2 1.0

velocity all create 1.0 87287 dist gaussian

pair_style lj/cut 6
pair_coeff 1 1 10.0 {ss} 6
pair_coeff 2 2 10.0 {ll} 6
pair_coeff 1 2 12.0 {ls} 6

dump dump_name all custom 100 tmp.dump element x y z 
dump_modify dump_name element Cu Zr
dump_modify dump_name sort id

#thermo_style custom step pe ke etotal temp press density lx
thermo_style custom step pe temp press lx
thermo 100
thermo_modify norm no

# CGM to alleviate any major issues withthe initial atom positions
minimize          1.0e-4 1.0e-6 10000 100000

timestep 0.001

# Equilibrate the current box so alleviate any other issues with the initial atom positions
fix md all nve
run 5000
unfix md

# CGM again before we start the real MD
minimize          1.0e-4 1.0e-6 10000 100000

# Let the box size equilibrate at low T and 1 P
fix md all npt temp 0.1 0.1 0.1 iso 1 1 1
run 50000
unfix md

# Heat up the system to a liquid
fix md all npt temp 0.1 20 1.0 iso 1 1 1  # thermostat controller gain = 0.1 (units of time, bigger is less tight control)
run 500000
unfix md

# Quench the liquid
fix md all npt temp 20 0.1 1.0 iso 1 1 1
run 500000
unfix md

# Finalize with a CGM
minimize          1.0e-4 1.0e-6 10000 100000
""".format(ss=ss_sigma,
           ll=ll_sigma,
           ls=ls_sigma,
           snatoms=snatoms,
           lnatoms=lnatoms
           )
    with open('inputs/{cn}.in'.format(cn=cn), 'w') as f:
        f.write(s)
