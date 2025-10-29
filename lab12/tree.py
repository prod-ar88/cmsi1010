from math import radians
from Tree.core import Tree
from PIL import Image

background_color = (210, 255, 255)
leaf_color = (158, 158, 158)
trunk_width = 150
base_trunk_color = (50, 40, 0)
small_branch_color = (110, 50, 0)
branch_gradient = (*base_trunk_color, *small_branch_color)

trunk_length = 1000
first_branch_line = (0, 0, 0, -trunk_length)
scales_and_angles = [(0.9, radians(-15)), (0.9, radians(15))]
age = 10

tree = Tree(pos=first_branch_line, branches=scales_and_angles)
tree.grow(age)
tree.move_in_rectangle()
image = Image.new("RGB", tree.get_size(), background_color)
tree.draw_on(image, branch_gradient, leaf_color, trunk_width)
image.show()
