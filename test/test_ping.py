from captcha-gene import app
import unittest


def setUpModule():
    print("setUpModule")


def tearDownModule():
    print("tearUpModule")


class FlaskTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("setUpClass")

    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    def setUp(self):
        self.app = app.test_client
        print('set up')

    def tearDown(self):
        print("tear down")

    def test_ping(self):
        request, response = self.app.get('/ping')
        self.assertEqual(response.json["msg"], 'pong')


def add_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAdd("test_ping"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = add_suite()
    runner.run(test_suite)
