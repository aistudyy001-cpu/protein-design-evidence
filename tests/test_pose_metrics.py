import unittest
import numpy as np
from pdp.interface_robustness import scoped_pose_metrics


class PoseMetricsTests(unittest.TestCase):
    def setUp(self):
        self.reference = {
            'A': np.array([[0., 0., 0.], [2., 0., 0.], [0., 2., 0.], [0., 0., 2.]]),
            'B': np.array([[4., 0., 0.], [4., 1., 0.], [4., 0., 1.]]),
        }

    def measure(self, prediction):
        return scoped_pose_metrics(self.reference, prediction, target_fit_positions=[1, 2, 3, 4])

    def test_binder_translation_changes_pose_but_not_shape(self):
        result = self.measure({'A': self.reference['A'].copy(), 'B': self.reference['B'] + [3., 0., 0.]})
        self.assertAlmostEqual(result['binder_CA_RMSD_after_target_fit_A'], 3.)
        self.assertAlmostEqual(result['binder_CA_shape_RMSD_after_self_fit_A'], 0.)

    def test_whole_complex_rigid_motion_is_removed(self):
        rotation = np.array([[0., -1., 0.], [1., 0., 0.], [0., 0., 1.]])
        transformed = {k: v @ rotation + [10., 20., 30.] for k, v in self.reference.items()}
        result = self.measure(transformed)
        self.assertAlmostEqual(result['binder_CA_RMSD_after_target_fit_A'], 0.)
        self.assertAlmostEqual(result['global_complex_CA_RMSD_A'], 0.)

    def test_missing_selected_coordinates_are_rejected(self):
        prediction = {k: v.copy() for k, v in self.reference.items()}
        prediction['A'][0] = np.nan
        with self.assertRaises(ValueError):
            self.measure(prediction)
