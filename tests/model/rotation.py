from fylm.model.rotation import Rotation, RotationSet
import unittest


class MockExperiment(object):
    def __init__(self):
        self.data_dir = None
        self.fields_of_view = None
        self.time_periods = None
        self.base_path = None
        self.field_of_view_count = None
        

class RotationSetTests(unittest.TestCase):
    def setUp(self):
        experiment = MockExperiment()
        experiment.data_dir = "/home/lulz/"
        experiment.fields_of_view = [1, 2, 3, 4, 5, 6, 7, 8]
        experiment.field_of_view_count = 8
        experiment.time_periods = [1, 2, 3]
        self.rset = RotationSet(experiment)

    def test_expected_rotations(self):
        rotations = [r for r in self.rset._expected]
        self.assertEqual(len(rotations), 8)

    def test_add_current_rotation(self):
        # two valid names
        self.rset.add_existing_data_file("fov1.txt")
        self.rset.add_existing_data_file("fov5.txt")
        # two invalid names
        self.rset.add_existing_data_file("rotation.txt")
        self.rset.add_existing_data_file("tp-fov-rotation.txt")
        self.assertEqual(len(self.rset._current_filenames), 2)

    def test_remaining_rotations(self):
        self.rset.add_existing_data_file("fov1.txt")
        self.rset.add_existing_data_file("fov5.txt")
        rotations = [r for r in self.rset.remaining]
        self.assertEqual(len(rotations), 6)


class RotationTests(unittest.TestCase):
    def setUp(self):
        experiment = MockExperiment()
        experiment.data_dir = "/home/lulz/141117"
        self.rotation = Rotation()
        self.rotation.base_path = experiment.data_dir + "/rotation"
        self.rotation.time_period = 2
        self.rotation.field_of_view = 3

    def test_path(self):
        self.assertEqual(self.rotation.path, "/home/lulz/141117/rotation/fov3.txt")

    def test_line(self):
        self.rotation._offset = 5.6363
        self.assertEqual("\n".join(self.rotation.lines), "5.6363")

    def test_set_offset(self):
        self.rotation.offset = "5.6363"
        self.assertAlmostEqual(self.rotation.offset, 5.6363)

    def test_load(self):
        self.assertIsNone(self.rotation.offset)
        self.rotation.load(["\n3.4215\n"])
        self.assertAlmostEqual(self.rotation.offset, 3.4215)