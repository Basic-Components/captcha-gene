import base64
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).absolute().parent.parent.joinpath("img-gene")))
print(sys.path)
from img_gene import app
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

    def test_captcha(self):
        request, response = self.app.post('/captcha')
        #self.assertEqual(response.json["msg"], 'pong')
        with open("message.txt","w") as f:
            f.write(response.json["msg"])
        with open("pic.png","wb") as f:
             content = base64.b64decode(response.json["img_b64"])
             f.write(content)

    def test_qr(self):
        request, response = self.app.post('/qr',json={
            "content":"测试测试"
        })
        with open("qr.png","wb") as f:
            content = base64.b64decode(response.json["img_b64"])
            f.write(content)


def add_suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAdd("test_captcha"))
    suite.addTest(TestAdd("test_qr"))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = add_suite()
    runner.run(test_suite)
