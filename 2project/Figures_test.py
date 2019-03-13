import unittest
from figures import Figure, Point, Polygon, Rectangle, Circle, Square, parse_figure
from colors import Color

class TestPolygon(unittest.TestCase):

	def test_parsing(self):
		p = Polygon.parse({'points': [[1,2], [0,9]], 'color': "#332211"}, {}, Color("#990011"))
		self.assertEqual(p.points, [(1, 2), (0, 9)])
		self.assertEqual(p.color, Color("#332211"))

	def test_diffrent_color_place(self):
		p = Polygon.parse({'points': [[1, 2]]}, {}, Color("#332211"))
		self.assertEqual(p.points, [(1, 2)])
		self.assertEqual(p.color, Color("#332211"))

		p = Polygon.parse({'points': [[1, 2], [2, 3] , [2, 3]], 'color': 'magenta'}, {'magenta': '(255, 0, 255)'}, Color("#332211"))
		self.assertEqual(p.points, [(1, 2), (2, 3), (2, 3)])
		self.assertEqual(p.color, Color("#ff00ff"))

	def test_errors(self):
		with self.assertRaises(ValueError):
			Polygon.parse({'point': [[1, 2]]}, {}, Color("#332211"))
			Polygon.parse({'points': [[1,2], [0,9]], 'color': "#3321"}, {}, Color("#990011"))
			Polygon.parse({'points': [[1,2], [0,9]], 'color': "#332211"}, {}, Color("#11"))
		with self.assertRaises(TypeError):
			Polygon.parse({'points': (1)}, {}, Color("#332211"))

class TestPoint(unittest.TestCase):
	def test_parse(self):
		p = Point.parse({'x': 10, 'y': 2, 'color': '(255, 0, 255)'}, {}, Color("#990011"))
		self.assertEqual(p.x, 10)
		self.assertEqual(p.y, 2)
		self.assertEqual(p.color, Color("#ff00ff"))

	def test_diffrent_color_place(self):
		p = Point.parse({'x': 10, 'y': 2, 'color': 'cos'}, {'cos': "#123456"}, Color("#990011"))
		self.assertEqual(p.color, Color("#123456"))

		p = Point.parse({'x': 10, 'y': 2}, {'cos': "123456"}, Color("#123456"))
		self.assertEqual(p.color, Color("#123456"))

	def test_errors(self):
		with self.assertRaises(ValueError):
			Point.parse({'x': 10, 'color': '(255, 0, 255)'}, {}, Color("#990011"))
			Point.parse({'y': 2, 'color': '(255, 0, 255)'}, {}, Color("#990011"))
		
		with self.assertRaises(TypeError):
			Point.parse({'x': 10, 'y': "", 'color': '(255, 0, 255)'}, {}, Color("#990011"))
			Point.parse({'x': {}, 'y': 2, 'color': '(255, 0, 255)'}, {}, Color("#990011"))

class TestRectangle(unittest.TestCase):
	def test_parse(self):
		p = Rectangle.parse({'x': 1, 'y': 2, 'height': 2, 'width': 3}, {}, Color("#123456"))
		self.assertEqual(p.x, 1)
		self.assertEqual(p.y, 2)
		self.assertEqual(p.height, 2)
		self.assertEqual(p.width, 3)
		self.assertEqual(p.color, Color("#123456"))

	def test_diffrent_color_place(self):
		p = Rectangle.parse({'x': 1, 'y': 2, 'height': 2, 'width': 3, 'color': "(0, 255, 0)"}, {}, Color("#123456"))
		self.assertEqual(p.color, Color("#00ff00"))

		p = Rectangle.parse({'x': 1, 'y': 2, 'height': 2, 'width': 3, 'color': "cos"}, {"cos": "#00ff00"}, Color("#123456"))
		self.assertEqual(p.color, Color("#00ff00"))
	def test_errors(self):
		with self.assertRaises(ValueError):
			Rectangle.parse({'y': 2, 'height': 2, 'width': 3}, {}, Color("#123456"))
			Rectangle.parse({'x': 1, 'height': 2, 'width': 3}, {}, Color("#123456"))
			Rectangle.parse({'x': 1, 'y': 2, 'width': 3}, {}, Color("#123456"))
			Rectangle.parse({'x': 1, 'y': 2, 'height': 2}, {}, Color("#123456"))
			Rectangle.parse({'x': 1, 'y': 2, 'height': 2, 'width': 3}, {}, 1)
		
		with self.assertRaises(TypeError):
			Rectangle.parse({'x': {}, 'y': 2, 'height': 2, 'width': 3}, {}, Color("#123456"))
			Rectangle.parse({'x': 1, 'y': (), 'height': 1, 'width': 3, 'color': "(0, 255, 0)"}, {}, Color("#123456"))
			Rectangle.parse({'x': 1, 'y': 2, 'height': [], 'width': 3, 'color': "(0, 255, 0)"}, {}, Color("#123456"))
			Rectangle.parse({'x': 1, 'y': 2, 'height': 2, 'width': "", 'color': "(0, 255, 0)"}, {}, Color("#123456"))
			Rectangle.parse({'x': 1, 'y': 2, 'height': 2, 'width': 3, 'color': "(0, 255, 0)"}, {}, 1)
	
class TestSquare(unittest.TestCase):

	def test_parse(self):
		p = Square.parse({'x': 1, 'y': 2, 'size': 3}, {}, Color("#123456"))
		self.assertEqual(p.x, 1)
		self.assertEqual(p.y, 2)
		self.assertEqual(p.width, 3)
		self.assertEqual(p.height, 3)
		self.assertEqual(p.color, Color("#123456"))

	def test_diffrent_color_place(self):
		p = Square.parse({'x': 1, 'y': 2, 'size': 3, 'color': "(0, 255, 0)"}, {}, Color("#123456"))
		self.assertEqual(p.color, Color("#00ff00"))

		p = Square.parse({'x': 1, 'y': 2, 'size': 3, 'color': "cos"}, {"cos": "#00ff00"}, Color("#123456"))
		self.assertEqual(p.color, Color("#00ff00"))

	def test_errors(self):
		with self.assertRaises(ValueError):
			Square.parse({'y': 2, 'size': 3}, {}, Color("#123456"))
			Square.parse({'xp': 1, 'y': 2, 'size': 3}, {}, Color("#123456"))
			Square.parse({'x': 1, 'size': 3}, {}, Color("#123456"))
			Square.parse({'x': 1, 'y': 2}, {}, Color("#123456"))
			Square.parse({'x': 1, 'y': 2, 'size': 3}, {}, Color("fajny"))
			Square.parse({'x': 1, 'y': 2, 'size': 3, 'color': "nic"}, {"cos": "#00ff00"}, Color("#123456"))

		with self.assertRaises(TypeError):
			Square.parse({'x': "", 'y': 2, 'size': 3}, {}, Color("#123456"))
			Square.parse({'x': 1, 'y': {}, 'size': 3}, {}, Color("#123456"))
			Square.parse({'x': 1, 'y': 2, 'size': 1.0}, {}, Color("#123456"))
			Square.parse({'x': 1, 'y': 2, 'size': 3}, {}, 1)

class TestCircle(unittest.TestCase):
	def test_parse(self):
		c = Circle.parse({'x': 1, 'y': 2, 'radius': 3}, {}, Color("#123456"))
		self.assertEqual(c.x, 1)
		self.assertEqual(c.y, 2)
		self.assertEqual(c.radius, 3)
		self.assertEqual(c.color, Color("#123456"))

	def test_diffrent_color_place(self):
		c = Circle.parse({'x': 1, 'y': 2, 'radius': 3, 'color': '#0000ff'}, {}, Color("#123456"))
		self.assertEqual(c.color, Color("#0000ff"))

		c = Circle.parse({'x': 1, 'y': 2, 'radius': 3, 'color': 'aaa'}, {'aaa': "#ff0000"}, Color("#123456"))
		self.assertEqual(c.color, Color("#ff0000"))

	def test_errors(self):
		with self.assertRaises(ValueError):
			Circle.parse({'xq': 1, 'y': 2, 'radius': 3}, {}, Color("#123456"))
			Circle.parse({'y': 2, 'radius': 3}, {}, Color("#123456"))
			Circle.parse({'x': 1, 'yq': 2, 'radius': 3}, {}, Color("#123456"))
			Circle.parse({'x': 1, 'radius': 3}, {}, Color("#123456"))
			Circle.parse({'x': 1, 'y': 2, 'radiusqq': 3}, {}, Color("#123456"))
			Circle.parse({'x': 1, 'y': 2}, {}, Color("#123456"))
		with self.assertRaises(ValueError):
			Circle.parse({'x': 1, 'y': 2, 'radius': 3}, {}, Color("#123456"))

		with self.assertRaises(TypeError):
			Circle.parse({'x': (), 'y': 2, 'radius': 3}, {}, Color("#123456"))
			Circle.parse({'x': 1, 'y': [], 'radius': 3}, {}, Color("#123456"))
			Circle.parse({'x': 1, 'y': 2, 'radius': {}}, {}, Color("#123456"))
			Circle.parse({'x': 1, 'y': 2, 'radius': {}}, {}, Color("#123456"))
			Circle.parse({'x': 1, 'y': 2, 'radius': 3}, {}, Color("#1"))

class TestParse(unittest.TestCase):
	def test_parse(self):
		p = parse_figure({'type': 'circle', 'x': 1, 'y': 2, 'radius': 3}, {}, Color("#123456"))
		self.assertTrue(isinstance(p, Figure))
		self.assertTrue(isinstance(p, Circle))
		

if __name__ == '__main__':
	unittest.main()