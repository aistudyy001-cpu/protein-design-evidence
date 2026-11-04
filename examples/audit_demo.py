"""Run with python -m examples.audit_demo. All coordinates are synthetic."""
import json
import numpy as np
from pdp.interface_robustness import scoped_pose_metrics
from pdp.metrics import prediction_blocks


def demo():
    target = np.array([[0., 0., 0.], [2., 0., 0.], [0., 2., 0.], [0., 0., 2.]])
    binder = np.array([[4., 0., 0.], [4., 1., 0.], [4., 0., 1.]])
    reference = {'A': target, 'B': binder}
    prediction = {'A': target.copy(), 'B': binder + [3., 0., 0.]}
    geometry = scoped_pose_metrics(reference, prediction, target_fit_positions=[1, 2, 3, 4])
    return {
        'data_origin': 'synthetic coordinate and confidence fixtures; not a protein candidate',
        'geometry': geometry,
        'confidence': prediction_blocks([[0., 2., 4.], [10., 0., 1.], [20., 1., 0.]], [.5, .7, .9], 1, 2),
        'interpretation': 'Binder shape is unchanged but binder pose moves 3 angstroms relative to the target. No biological conclusion.',
    }


if __name__ == '__main__':
    print(json.dumps(demo(), indent=2, allow_nan=False))
