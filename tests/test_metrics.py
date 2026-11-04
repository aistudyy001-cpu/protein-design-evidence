import unittest
from pdp.metrics import prediction_blocks

class BlockTests(unittest.TestCase):
    def test_directional_blocks_exclude_within_chain(self):
        result=prediction_blocks([[999,2,4],[10,999,999],[20,999,999]],[0.1,0.7,0.9],1,2)
        self.assertAlmostEqual(result['binder_plddt_0_1'],0.8)
        self.assertEqual(result['target_rows_binder_columns_pae_mean_angstrom'],3)
        self.assertEqual(result['binder_rows_target_columns_pae_mean_angstrom'],15)
        self.assertEqual(result['symmetric_cross_chain_pae_mean_angstrom'],9)
    def test_monomer_has_no_interface_score(self):
        result=prediction_blocks([[0,2],[3,0]],[0.5,0.7],0,2)
        self.assertEqual(set(result),{'binder_plddt_0_1'})
    def test_shapes_scale_and_nan_rejected(self):
        for pae,p in [([[0]],[80]),([[float('nan')]],[0.8]),([[0,1]],[0.8])]:
            with self.assertRaises(ValueError):prediction_blocks(pae,p,0,1)
