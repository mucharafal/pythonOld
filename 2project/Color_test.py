import unittest
from colors import *

class TestColorClass(unittest.TestCase):

	def test_init(self):
		t = Color("#ffaa00")
		self.assertEqual("#ffaa00", t._Color__value)
		t = Color('(255, 170, 0)')
		self.assertEqual("#ffaa00", t._Color__value)
		with self.assertRaises(Exception):
			Color("ala") 
			Color("(255, 1)")
			Color("(255, 1, 100, 2)")
			Color("[1,2,3]")

	def test_get_html(self):
		t = Color("#ffaa00")
		self.assertEqual(t.get_html(), "#ffaa00")
		self.assertNotEqual(t.get_html(), "#ffaa01")
		self.assertNotEqual(t.get_html(), "ffaa00")
		t = Color('(0, 0, 0)')
		self.assertEqual(t.get_html(), "#000000")
		t = Color('(0, 0, 10)')
		self.assertEqual(t.get_html(), "#00000a")
		t = Color('(0, 0, 256)')
		self.assertEqual(t.get_html(), "#0000100")

	def test_get_tuple(self):
		t = Color("#ffaa00")
		self.assertEqual(t.get_tuple(), (255, 170, 0))

	def test_eq(self):
		p = Color("#ff00ff")
		q = Color("(255, 0, 255)")
		self.assertEqual(p, q)
		r = Color("#f0f0f0")
		self.assertNotEqual(r, p)

	def test_errors(self):
		with self.assertRaises(ValueError):
			t = Color("#ff")
			t = Color("(255, 1)")
			t = Color("[255, 1]")
			t = Color("#alakot")

class TestParseColor(unittest.TestCase):

	def test_parse_color(self):
		a = parse_color("#ff00ff", {})
		self.assertEqual(a.get_tuple(), (255, 0, 255))
		a = parse_color('magenta', {'magenta': '(255, 0, 255)'})
		self.assertEqual(a.get_tuple(), (255, 0, 255))
		
		
if __name__ == '__main__':
	unittest.main()