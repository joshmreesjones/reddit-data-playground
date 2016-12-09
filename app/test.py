import dataset
import unittest

class TestDatasetMethods(unittest.TestCase):
    def test_num_comments(self):
        self.assertEqual(dataset.num_comments(), 53851542)

if __name__ == '__main__':
    unittest.main()
