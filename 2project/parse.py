import sys
import json
import math
from PIL import Image
from colors import parse_color
from figures import parse_figure

def parse_figures(figures, palette, default_color):
	"""
	Return list of Figure objects. 
	figures - list of maps describing figure
	palette - map with user defined colors
	default_color - color set, when no color is specified in description of figure
	"""
	return list(map(lambda x: parse_figure(x, palette, default_color), figures))

def set_screen_properties(values_map, palette):
	"""
	Return 3-tuple (size, default color, background_color)
	Demand keys in map: 'width', 'height', 'fg_color', 'bg_color'
	""" 
	size = (values_map['width'], values_map['height'])
	default_color = parse_color(values_map['fg_color'], palette)
	background_color = parse_color(values_map['bg_color'], palette)
	return (size, default_color, background_color)

def parse_file(file_name):
	"""
	Read file in json format and return map of values
	""" 
	json_file = open(file_name, 'r')
	whole_file = json_file.read()
	jsonMap = json.loads(whole_file)
	json_file.close()
	return jsonMap

def main():
	"""
	Format of argv:
	-o fileToSave fileToOpen
	--output fileToSave fileToOpen
	fileToOpen
	"""
	if sys.argv[1] == '-o' or sys.argv[1] == '--output':
		save_to_file = True
		file_to_save = sys.argv[2]
		path = sys.argv[3]
	else:
		save_to_file = False
		path = sys.argv[1]
	
	json_map = parse_file(path)
	screen_properties = set_screen_properties(json_map['Screen'], json_map['Palette'])
	im = Image.new('RGB', screen_properties[0], screen_properties[2].get())
	try:
		my_list = parse_figures(json_map['Figures'], json_map['Palette'], screen_properties[1])
	except (KeyError, ValueError, TypeError):
		print("File is incorrect")
		return 
	list(map(lambda x: x.draw(im), my_list))
	im.show()

	if save_to_file:
		im.save(file_to_save + ".png", "PNG")

if __name__ == "__main__":
	main()
