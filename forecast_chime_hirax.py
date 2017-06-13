import numpy as np
from cora.util import cubicspline

import simpleforecast


## Setup CHIME experiment
experiment_chime = simpleforecast.InterferometerBase()

experiment_chime.kmax = 1.0
experiment_chime.num_k = 100

# Set the array size
experiment_chime.num_x = 4
experiment_chime.num_y = 256
experiment_chime.size_x = 20.0
experiment_chime.size_y = 0.3

# Set the frequency range
experiment_chime.freq_low = 400.0  # Redshift 6
experiment_chime.freq_high = 800.0

# Set the receiver temperature and the observing time
experiment_chime.T_recv = 50.0
experiment_chime.num_year = 5.0  # not given by Anze


## Setup HIRAX experiment
experiment_hirax = simpleforecast.InterferometerBase()

# Set the array size
experiment_hirax.num_x = 32
experiment_hirax.num_y = 32
experiment_hirax.size_x = 10.0
experiment_hirax.size_y = 10.0

# Set the frequency range
experiment_hirax.freq_low = 400.0  # Redshift 6
experiment_hirax.freq_high = 800.0

# Set the receiver temperature and the observing time
experiment_hirax.T_recv = 50.0
experiment_hirax.num_year = 5.0  # not given by Anze

experiment_hirax.kmax = 1.0
experiment_hirax.num_k = 100

if __name__ == '__main__':

    import h5py

    # Generate and write out the forecast for CHIME
    sn_all = experiment_chime.signal_noise_comb()
    sn_split = experiment_chime.signal_noise_split()

    with h5py.File('sn_chime.h5') as fh:

        for ii, (z, sn) in enumerate(sn_split):

            dset = fh.create_dataset('sn_band_%i' % ii, data=sn)
            dset.attrs['z'] = z
            dset.attrs['axes'] = ('k_par', 'k_perp')

            exp = experiment_chime

            p21 = exp.signal_power(exp.kpar, exp.kperp, z)
            Tb = exp.cr.prefactor(z)
            pm = p21 / Tb**2

            dset_pk = fh.create_dataset('pk_band_%i' % ii, data=pm)
            dset_pk.attrs['T_b'] = Tb

        dset = fh.create_dataset('sn_all', data=sn_all)
        dset.attrs['axes'] = ('k_par', 'k_perp')

        fh.create_dataset('k_bin', data=experiment_chime.kbin)

    # Write out the forecast for HIRAX
    sn_all = experiment_hirax.signal_noise_comb()
    sn_split = experiment_hirax.signal_noise_split()

    with h5py.File('sn_hirax.h5') as fh:

        for ii, (z, sn) in enumerate(sn_split):

            dset = fh.create_dataset('sn_band_%i' % ii, data=sn)
            dset.attrs['z'] = z

            exp = experiment_hirax

            p21 = exp.signal_power(exp.kpar, exp.kperp, z)
            Tb = exp.cr.prefactor(z)
            pm = p21 / Tb**2

            dset_pk = fh.create_dataset('pk_band_%i' % ii, data=pm)
            dset_pk.attrs['T_b'] = Tb

        dset = fh.create_dataset('sn_all', data=sn_all)
        dset.attrs['axes'] = ('k_par', 'k_perp')

        fh.create_dataset('k_bin', data=experiment_hirax.kbin)
