"""testing bosreport"""
from bosreport import SwdesPart
from bosreport import SwdesEquidistant
import unittest
import datetime

class TestSwdesPart(unittest.TestCase):
    def setUp(self):
        self.s = SwdesPart(
            '4,4,0,0,1,4,31-8-2012 12:00:0',
            'TG,GN',
            [0.0, 1.1, 2.2])
    
    def tearDown(self):
        pass

    def test_data(self):
        self.assertEquals(
            self.s.data,
            {datetime.datetime(2012, 8, 31, 12, 0): 0.0,
             datetime.datetime(2012, 8, 31, 12, 15): 1.1,
             datetime.datetime(2012, 8, 31, 12, 30): 2.2,})

    def test_header(self):
        self.assertEquals(
            self.s.start_date,
            datetime.datetime(2012, 8, 31, 12, 0))

    def test_header_two(self):
        self.assertEquals(
            self.s.location, 'TG')
        self.assertEquals(
            self.s.parameter, 'GN')


if __name__ == '__main__':
    unittest.main()
