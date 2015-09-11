import unittest
from music22 import diastema as di
from numpy import log2,log10

class Test_intervals(unittest.TestCase):
    
    def test_savart_converter(self):
        inter = 4/3.
        inter_sav = log10(inter)*1000
        self.assertEqual(inter_sav, di.savart(inter))

    def test_cent_converter(self):
	inter = 4/3.
	inter_cent = log2(inter)*1200
	self.assertEqual(inter_cent, di.cent(inter))

    def test_dias_following_unit(self):
	global unit
	di.set_unit("savart")
	self.assertEqual(di.dias(3/2.),di.savart(3/2.))
	di.set_unit("cent")
	self.assertEqual(di.dias(3/2.),di.cent(3/2.))

    def test_set_unit_arguments(self):
        unit = "coucou"
        self.assertRaises(ValueError, di.set_unit, unit )

    def test_get_inter_ref(self):
        di.set_unit('savart')
        inter = 300
        self.assertEqual(di.get_inter_ref(inter)[1],"2/1")

if __name__ == '__main__':
    unittest.main()
