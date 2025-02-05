from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.colors import Color

from compas.artists import GeometryArtist
from .artist import BlenderArtist

from compas_blender import conversions


class VectorArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing vectors in Blender.

    Parameters
    ----------
    primitive : :class:`~compas.geometry.Vector`
        A COMPAS vector.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, vector: Vector, **kwargs: Any):
        super().__init__(geometry=vector, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
        point: Optional[Point] = None,
    ) -> bpy.types.Object:
        """Draw the vector.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the vector.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        point : [float, float, float] | :class:`~compas.geometry.Point`, optional
            Point of application of the vector.
            Default is ``Point(0, 0, 0)``.

        Returns
        -------
        :blender:`bpy.types.Object`

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        point = point or (0.0, 0.0, 0.0)  # type: ignore
        start = Point(*point)  # type: ignore
        end = start + self.geometry
        line = Line(start, end)

        curve = conversions.line_to_blender_curve(line)

        obj = self.create_object(curve, name=name)
        self.update_object(obj, color=color, collection=collection)

        return obj
