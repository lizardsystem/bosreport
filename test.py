"""testing bosreport"""
from bosreport import SwdesPart
from bosreport import SwdesEquidistant
from bosreport import next_month
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


class TestNextMonth(unittest.TestCase):
    def test_one(self):
        dt = datetime.datetime(2012, 12, 27, 13, 46, 0) 
        self.assertEquals(
            next_month(dt), 
            datetime.datetime(2013, 1, 1))

    def test_two(self):
        dt = datetime.datetime(2013, 1, 24) 
        self.assertEquals(
            next_month(dt), 
            datetime.datetime(2013, 2, 1))

    def test_three(self):
        dt = datetime.datetime(2013, 2, 1) 
        self.assertEquals(
            next_month(dt), 
            datetime.datetime(2013, 3, 1))


if __name__ == '__main__':
    unittest.main()
