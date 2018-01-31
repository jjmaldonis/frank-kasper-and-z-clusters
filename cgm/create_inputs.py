import numpy as np


with open('interatomic_ratios.txt') as f:
    data = f.readlines()
    data = [line.strip().split() for line in data]
    #data = [[int(line[0]), float(line[1]), float(line[2])] for line in data]
    data = [[int(line[0]), float(line[1])] for line in data]
#print(data)


for cn, rstar in data:
    radius = 2.0
    zr_zr = radius
    cu_cu = radius / rstar
    zr_cu = (zr_zr + cu_cu) / 2.0
    zr_zr_sigma = zr_zr / np.power(2, 1./6.)
    cu_cu_sigma = cu_cu / np.power(2, 1./6.)
    zr_cu_sigma = zr_cu / np.power(2, 1./6.)
    s = """
units             metal  
atom_style        atomic
boundary          f f f 

read_data     input_models/{cn}.dat

mass 1 1.0 
mass 2 1.0 

group center_atom id 1
fix freeze center_atom setforce 0.0 0.0 0.0 

pair_style lj/cut {cutoff} 
pair_coeff 1 1 {eps} {zr_zr} {cutoff} 
pair_coeff 2 2 {eps} {cu_cu} {cutoff} 
pair_coeff 1 2 {eps_btwn} {zr_cu} {cutoff} 
# R* = {rstar} for CN {cn}

pair_modify tail yes 

thermo_style custom step pe ke etotal temp press density
thermo 1
thermo_modify norm no
thermo_modify   flush yes 

dump dump_name all custom 1 tmp.dump element x y z 
dump_modify dump_name element Zr Cu
dump_modify dump_name sort id

minimize    1.0e-6 0 1000 10000
""".format(
    eps=1.0,
    eps_btwn=10.0,
    rstar=rstar,
    cn=cn,
    zr_zr=zr_zr_sigma,
    cu_cu=cu_cu_sigma,
    zr_cu=zr_cu_sigma,
    cutoff='200'
    )
    print(cn, rstar, zr_zr, cu_cu, zr_cu)
    print(cn, rstar, zr_zr_sigma, cu_cu_sigma, zr_cu_sigma)
    #with open('inputs/{cn}.in'.format(cn=cn), 'w') as f:
    #    f.write(s)
