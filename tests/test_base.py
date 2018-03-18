import unittest


class BaseTestCase(unittest.TestCase):
    @classmethod
    def get_request_data(cls, name):
        file = './request_data/{0}/{1}.json'.format(cls.__name__, name)
        with open(file) as json_file:
            data = json_file.read()
        return data


if __name__ == '__main__':
    unittest.main()
