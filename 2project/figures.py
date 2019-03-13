from PIL import Image
from PIL import ImageDraw
from math import sqrt
from colors import parse_color, Color
import functools

def checkColor(f):
	"""
	Test whether among *args is one which type is Color
	"""
	def wrapper(*args, **kwargs):
		color = list(filter(lambda x: isinstance(x, Color), args))
		if not color:
			raise TypeError
		else:
			return f(*args, **kwargs)
	return wrapper

def isParameter(parameters):
	"""
	Check if in first argument from args, which type is dict
	have key - x and whether value of it has proper type.
	Takes tuple (x, type)
	"""
	x = parameters[0]
	type = parameters[1]
	def decorator(f):
		def wrapper(*args, **kwargs):
			if isinstance(x, str):
				maps = list(filter(lambda x: isinstance(x, dict), args))
				map = maps[0]
				try:
					map[x]
				except KeyError:
					raise ValueError
				if not isinstance(map[x], type):
					raise TypeError
				return f(*args, **kwargs)
			else:
				raise KeyError
		return wrapper
	return decorator


class Figure(object):
	"""
	Interface. Demand methods:
	draw(image)
	parse(parameters, palette, default_color)
	"""
	def draw(self, image):
		"""
		Draw proper figure on image. 
		Image: PIL.Image
		"""
		pass
	@staticmethod
	def parse(parameters, palette, default_color):
		"""
		Take:
		parameters: map with properties of figure
		palette: map of defined colors ie. {"black": "#000000", "white": (255, 255, 255)}
		default_color: object of type Color
		return object of type Figure
		"""
		pass
				
class Polygon(Figure):
	"""
	Implement Figure. Represent object of type polygon.
	Gather information about nodes and color of figure.
	"""
	@checkColor
	def __init__(self, xy, color):
		"""
		xy: list of nodes: ex. [[1, 2], [2, 3], [3, 9]]
		color: object of type Color
		"""
		try:
			self.points = list(map(lambda x: tuple(x), xy))
		except TypeError:
			raise Exception("Incorrect list of nodes in Polygon")
		self.color = color

	def draw(self, image):
		"""
		Draw polygon on image.
		image: object of class PIL.Image
		"""
		draw = ImageDraw.Draw(image)
		draw.polygon(self.points, self.color.get())

	@staticmethod
	@checkColor
	@isParameter(('points', list))
	def parse(parameters, palette, default_color):
		"""
		Demand parameters:
		'points': list of points in format [[1, 2], [2, 3], [3, 3]]
		if 'color' is not specified, default_color is set
		"""
		return Polygon(
			parameters['points'],
			default_color if 'color' not in parameters else parse_color(parameters['color'], palette)
		)

class Point(Figure):
	"""
	Implements Figure.
	Gather information about placement of point and its color.
	"""
	@checkColor
	def __init__(self, x, y, color):
		"""
		x - int
		y - int
		color - Color
		"""
		self.x = x
		self.y = y
		self.color = color

	def draw(self, image):
		"""
		Draw point on image.
		image: object of class PIL.Image
		"""
		draw = ImageDraw.Draw(image)
		draw.point([self.x, self.y], self.color.get())

	@staticmethod
	@isParameter(('x', int))
	@isParameter(('y', int))
	@checkColor
	def parse(parameters, palette, default_color):
		"""
		Demand parameters:
		'x', 'y', (optional)'color',
		If color is not specified, then default_color is used
		"""
		return Point(
			parameters['x'],
			parameters['y'],
			default_color if 'color' not in parameters else parse_color(parameters['color'], palette)
		)

class Rectangle(Figure):
	"""
	Implements Figure. Gather information about
	position of rectangle, its size and color.
	"""
	@checkColor
	def __init__(self, x, y, width, height, color):
		"""
		Types:
		x, y, width, height - int
		color - Color
		"""
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.color = color

	def draw(self, image):
		"""
		Draw rectangle on image.
		image: object of class PIL.Image
		"""
		draw = ImageDraw.Draw(image)
		draw.rectangle(
			[self.x, self.y, self.x + self.width, self.y + self.height], 
			self.color.get()
		)
	
	@staticmethod
	@isParameter(('x', int))
	@isParameter(('y', int))
	@isParameter(('width', int))
	@isParameter(('height', int))
	@checkColor
	def parse(parameters, palette, default_color):
		"""
		Return Rectangle object.
		parameters - map
		palette - map with key: literal name of color, value: string accepted by Color
		default_color - Color object, set when color is not specified in parameters
		Demand: 
		parameters['x'] - int
		parameters['y'] - int
		parameters['width'] - int
		parameters['height'] - int
		(optional)parameters['color'] - str
		"""
		return Rectangle(
			parameters['x'], 
			parameters['y'],
			parameters['width'],
			parameters['height'],
			default_color if 'color' not in parameters else parse_color(parameters['color'], palette)
		)

class Square(Rectangle):
	"""
	Implements Figure. Gather information about
	position of square, its size and color.
	"""
	@staticmethod
	@isParameter(('x', int))
	@isParameter(('y', int))
	@isParameter(('size', int))
	@checkColor
	def parse(parameters, palette, default_color):
		"""
		Return Square object.
		parameters - map
		palette - map with key: literal name of color, value: string accepted by Color
		default_color - Color object, set when color is not specified in parameters
		Demand: 
		parameters['x'] - int
		parameters['y'] - int
		parameters['size'] - int
		(optional)parameters['color'] - str
		"""
		size = parameters['size']
		return Square(
			parameters['x'],
			parameters['y'],
			size,
			size,
			default_color if 'color' not in parameters else parse_color(parameters['color'], palette)
		)

class Circle(Figure):
	"""
	Implements Figure. Gather information about
	position of circle, its radius and color.
	"""
	@checkColor
	def __init__(self, x, y, radius, color):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color

	def get_bounding_box_coordinates(self):
		"""
		Return list with coordinates of box bounding circle.
		Format: [x_upper_left, y_upper_left, x_bottom_right, y_bottom_right]
		"""
		start_x = self.x - self.radius
		start_y = self.y - self.radius
		end_x = self.x + self.radius
		end_y = self.y + self.radius
		return [start_x, start_y, end_x, end_y]

	def draw(self, image):
		"""
		Draw circle on image.
		image: object of class PIL.Image
		"""
		draw = ImageDraw.Draw(image)
		draw.ellipse(
			self.get_bounding_box_coordinates(),
			self.color.get()
		)

	@staticmethod
	@isParameter(('x', int))
	@isParameter(('y', int))
	@isParameter(('radius', int))
	@checkColor
	def parse(parameters, palette, default_color):
		"""
		Return Circle object.
		parameters - map
		palette - map with key: literal name of color, value: string accepted by Color
		default_color - Color object, set when color is not specified in parameters
		Demand: 
		parameters['x'] - int
		parameters['y'] - int
		parameters['radius'] - int
		(optional)parameters['color'] - str
		"""
		return Circle(
			parameters['x'],
			parameters['y'],
			parameters['radius'],
			default_color if 'color' not in parameters else parse_color(parameters['color'], palette)
		)

@isParameter(('type', str))
def parse_figure(parameters, palette, default_color):
	"""
	Parse parameters and return proper Figure object.
	Demand:
	parameters['type'] - str - type of figure.
	"""
	figures = {
		'point': Point,
		'polygon': Polygon,
		'rectangle': Rectangle,
		'square': Square,
		'circle': Circle
	}

	return figures[parameters['type']].parse(parameters, palette, default_color)
