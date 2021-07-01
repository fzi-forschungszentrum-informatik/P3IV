import warnings
import lanelet2
from matplotlib.axes import Axes
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from p3iv_utils.lanelet_map_reader import lanelet_map_reader
from .map_imagery import MapImagery


type_colors = {
    "virtual": "blue",
    "curbstone": "black",
    "line_thin": "white",
    "line_thick": "white",
    "pedestrian_marking": "white",
    "bike_marking": "white",
    "stop_line": "white",
    "road_border": "black",
    "guard_rail": "black",
    "traffic_sign": "red",
    "tree": "green",
    "Streetlamp": "yellow",
    "bus-stop": "yellow",
    "tram-stop": "yellow",
    "waste-container": "brown",
    "plant-pot": "green",
}


class PlotLanelet2Map(object):
    """
    [borrow & adapt the lanelet2 visualisation package]
    (https://github.com/interaction-dataset/interaction-dataset/blob/8e53eecfa9cdcb2203517af2f8ed154ad40c2956/python/utils/map_vis_lanelet2.py)
    """

    def __init__(self, axes, laneletmap, lat_origin=0.0, lon_origin=0.0, imagery_data=None):
        self.laneletmap = lanelet_map_reader(laneletmap, lat_origin=lat_origin, lon_origin=lon_origin)

        assert isinstance(axes, Axes)
        self.ax = axes
        self.ax.set_xlabel("Easting $(m)$")
        self.ax.set_ylabel("Northing $(m)$")

        x_min, x_max, y_min, y_max = self._get_map_bounds(self.laneletmap)

        th = 10.0
        self.ax.set_xlim([x_min - th, x_max + th])
        self.ax.set_ylim([y_min - th, y_max + th])
        # self.ax.grid()
        self.ax.set_aspect("equal", adjustable="box")  # plt.axis('equal')

        if imagery_data:
            self._add_linestringlayer_objects()
            map_img = MapImagery(self.ax, imagery_data[0], x_min, x_max, y_min, y_max)
            map_img.display_image()
        else:
            self._add_linestringlayer_objects()
            self._add_laneletlayer_objects()
            self._add_arealayer_objects()

    def _add_linestringlayer_objects(self):

        unknown_linestring_types = list()
        unknown_linestring_IDs = list()
        for ls in self.laneletmap.lineStringLayer:
            if "type" not in list(ls.attributes.keys()):
                unknown_linestring_IDs.append(str(ls.id))

            elif ls.attributes["type"] == "line_thin":
                if "subtype" in list(ls.attributes.keys()) and ls.attributes["subtype"] == "dashed":
                    type_dict = dict(color="white", linewidth=1, zorder=1, dashes=[10, 10])
                else:
                    type_dict = dict(color="white", linewidth=1, zorder=1)
            elif ls.attributes["type"] == "line_thick":
                if "subtype" in list(ls.attributes.keys()) and ls.attributes["subtype"] == "dashed":
                    type_dict = dict(color="white", linewidth=2, zorder=1, dashes=[10, 10])
                else:
                    type_dict = dict(color="white", linewidth=2, zorder=1)
            elif ls.attributes["type"] == "pedestrian_marking":
                type_dict = dict(color="white", linewidth=1, zorder=1, dashes=[5, 10])
            elif ls.attributes["type"] == "bike_marking":
                type_dict = dict(color="white", linewidth=1, zorder=1, dashes=[5, 10])
            elif ls.attributes["type"] == "virtual":
                continue
            elif ls.attributes["type"] in list(type_colors.keys()):
                type_dict = dict(color=type_colors[ls.attributes["type"]], linewidth=1, zorder=1)
            else:
                if ls.attributes["type"] not in unknown_linestring_types:
                    unknown_linestring_types.append(ls.attributes["type"])
                continue

            ls_points_x = [pt.x for pt in ls]
            ls_points_y = [pt.y for pt in ls]

            self.ax.plot(ls_points_x, ls_points_y, **type_dict)

        if len(unknown_linestring_types) != 0:
            print(("Found the following unknown types, did not plot them: " + str(unknown_linestring_types)))
            warnings.warn(
                "\nIDs \n" + str(unknown_linestring_IDs) + "\nLinestring type must be specified", stacklevel=0
            )

    def _add_laneletlayer_objects(self):
        lanelets = []
        for ll in self.laneletmap.laneletLayer:
            points = [[pt.x, pt.y] for pt in ll.polygon2d()]
            polygon = Polygon(points, True)
            lanelets.append(polygon)

        ll_patches = PatchCollection(lanelets, facecolors="lightgray", edgecolors="None")
        self.ax.add_collection(ll_patches)

        if len(self.laneletmap.laneletLayer) == 0:
            self.ax.patch.set_facecolor("lightgrey")

    def _add_arealayer_objects(self):
        areas = []
        for area in self.laneletmap.areaLayer:
            if area.attributes["subtype"] == "keepout":
                points = [[pt.x, pt.y] for pt in area.outerBoundPolygon()]
                polygon = Polygon(points, True)
                areas.append(polygon)

        area_patches = PatchCollection(areas, facecolors="darkgray", edgecolors="None")
        self.ax.add_collection(area_patches)

    @staticmethod
    def _get_map_bounds(laneletmap):
        x_min = 1e9
        x_max = -1e9
        y_min = 1e9
        y_max = -1e9

        for point in laneletmap.pointLayer:
            x_min = min(point.x, x_min)
            x_max = max(point.x, x_max)
            y_min = min(point.y, y_min)
            y_max = max(point.y, y_max)

        return [x_min, x_max, y_min, y_max]
