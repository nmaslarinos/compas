from math import pi
from compas.geometry import Rotation, Scale
from compas.geometry import Line
from compas.artists import Artist
from compas.colors import Color

Artist.clear()

line = Line([0, 0, 0], [3, 0, 0])
artist = Artist(line)
# artist.color = (1.0, 0.0, 0.0)

step = pi / 10.0
rotation = Rotation.from_axis_and_angle([0, 0, 1], angle=step)

for i in range(11):
    artist.draw(color=Color.from_i(i / 10))
    line.transform(rotation)

Artist.redraw()