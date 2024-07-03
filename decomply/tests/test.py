import unittest
from decomply import Decomply


class TestDecomply(unittest.TestCase):

    def test_decomply_example(self):
        def apply(_, item): return item + 1

        decomply_instance = Decomply(apply=apply)
        input_data = {
            "First Layer": {
                "Second layer": 3,
                "_Second layer 2nd element": 4
            }
        }
        expected_output = {
            "First Layer": {
                "Second layer": 4
            }
        }
        self.assertEqual(decomply_instance.decomply(input_data), expected_output)

    def test_decomply_example2(self):
        input_data = {
            "First Layer": {
                "Second layer": 3,
                "_Second layer 2nd element": 4,
                "Second layer 3rd element": [
                    42,
                    69
                ]
            },
            "First layer 2nd element": {
                "fuu": {
                    "fuu 1st entry": 6,
                    "fuu 2nd entry": 10,
                    "fuu 3rd entry": {
                        "I will be dropped": 0
                    }
                }
            }
        }
        expected_output = {
            "First Layer": {
                "Second layer": 4,
                "_Second layer 2nd element": 5,
                "Second layer 3rd element": [
                    42,
                    69,
                    666
                ]
            },
            "First layer 2nd element": {
                "fuu": {
                    "fuu 1st entry": 7,
                    "fuu 2nd entry": 11,
                    "fuu 3rd entry": {}
                }
            }
        }
        out = Decomply(
            traverse=lambda _, item: not isinstance(item, list),
            apply=lambda _, item: item +
            [666] if isinstance(item, list) else item + 1,
            delete=lambda trace, _: len(trace) > 3
        ).decomply(input_data)
        self.assertEqual(out, expected_output)


if __name__ == '__main__':
    unittest.main()
