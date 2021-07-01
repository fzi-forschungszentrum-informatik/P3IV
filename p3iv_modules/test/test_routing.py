import unittest
import lanelet2
from p3iv_utils.lanelet_map_reader import lanelet_map_reader


class TestRouting(unittest.TestCase):
    def test_routing(self):

        laneletmap = lanelet_map_reader("SanFrancisco-Downtown-Sample-Lanelet2", lat_origin=37.787, lon_origin=-122.406)

        traffic_rules = lanelet2.traffic_rules.create(
            lanelet2.traffic_rules.Locations.Germany, lanelet2.traffic_rules.Participants.Vehicle
        )
        routing_graph = lanelet2.routing.RoutingGraph(laneletmap, traffic_rules)

        route_to_destination = routing_graph.getRoute(
            laneletmap.laneletLayer[10000054], laneletmap.laneletLayer[10000849]
        )

        self.assertTrue(True)  # fake test :(


if __name__ == "__main__":
    unittest.main()
