from ast import literal_eval
import re
class Color():
	"""
	Value class. Contain color.
	Can return it in two formats:
	string in html format - "#ffaabb"
	tuple - (R, G, B), where 0 < R, G, B < 256
	Constructor accept both formats
	"""
	def __init__(self, value):
		if not isinstance(value, str):
			raise TypeError
		try:
			u = literal_eval(value)
			value = '#%02x%02x%02x' % u
		except SyntaxError:
			pass
		except TypeError:
			raise ValueError
		if re.match("#[0-9,A-F,a-f][0-9,A-F,a-f][0-9,A-F,a-f][0-9,A-F,a-f][0-9,A-F,a-f][0-9,A-F,a-f]", value):
			self.__value = value
		else:
			raise ValueError
	
	def get_html(self):
		return self.__value
	
	def get_tuple(self):
		value = self.__value
		r = int(value[1:3], 16)
		g = int(value[3:5], 16)
		b = int(value[5:7], 16)
		return (r, g, b)
	
	def get(self):
		return self.get_tuple()

	def __eq__(self, other):
		return (self.get_html() == other.get_html())

def parse_color(color, palette):
	"""
	Return Color object. If parameter color is key in palette map,
	replace it on value from map. 
	Color should be string in html color format, or tuple with values
	(R, G, B).
	"""
	try:
		color = palette[color]
	except KeyError:
		pass
	return Color(color)