import unittest
from test.module import Caculator
class test_ca(unittest.TestCase):
    def setUp(self):
        self.cal = Caculator(8,4)

    def tearDown(self):
        pass

    def test_add(self):
        '''加法测试'''
        result = self.cal.add(3,4)
        self.assertEqual(result,7)

    def test_sub(self):
        '''减法测试'''
        result = self.cal.Sub()
        self.assertEqual(result,4)

    def test_mul(self):
        '''乘法测试'''
        result = self.cal.mul()
        self.assertEqual(result,32)

    def test_div(self):
        '''除法测试'''
        result = self.cal.div()
        self.assertEqual(result,2)

if __name__=="__main__":
    suit = unittest.TestSuite()
    suit.addTests(unittest.TestLoader().loadTestsFromTestCase(test_ca))
    suit.addTest(test_ca("test_div"))
    suit.addTest(test_ca("test_mul"))
    # suit.addTest(test_ca("test_sub"))
    suit.addTest(test_ca("test_add"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suit)