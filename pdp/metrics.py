"""Metrics with explicit residue blocks; no model-agnostic acceptance thresholds."""
import math


def prediction_blocks(pae, plddt, target_length, binder_length):
    if target_length < 0 or binder_length < 1:
        raise ValueError('Invalid target/binder lengths')
    length=target_length+binder_length
    if len(pae)!=length or any(len(row)!=length for row in pae) or len(plddt)!=length:
        raise ValueError('Confidence array shapes do not match declared residue blocks')
    if any(not math.isfinite(float(v)) or v<0 for row in pae for v in row):
        raise ValueError('PAE contains invalid values')
    if any(not math.isfinite(float(v)) or not 0<=v<=1 for v in plddt):
        raise ValueError('Expected ColabDesign pLDDT in [0,1]')
    result={'binder_plddt_0_1':sum(plddt[target_length:])/binder_length}
    if target_length:
        a=[pae[i][j] for i in range(target_length) for j in range(target_length,length)]
        b=[pae[i][j] for i in range(target_length,length) for j in range(target_length)]
        result.update({'target_rows_binder_columns_pae_mean_angstrom':sum(a)/len(a),
                       'binder_rows_target_columns_pae_mean_angstrom':sum(b)/len(b),
                       'symmetric_cross_chain_pae_mean_angstrom':(sum(a)+sum(b))/(len(a)+len(b))})
    return result
