import heapq
import math

class CityGraph:
    def __init__(self):
        # adj list: { node_id: [(neighbor_id, weight)] }
        self.adj = {}
        self.nodes = {}

    def add_node(self, node_id, lat, lng, name=""):
        if node_id not in self.adj:
            self.adj[node_id] = []
            self.nodes[node_id] = {"lat": lat, "lng": lng, "name": name}

    def add_edge(self, u, v, weight, bidir=True):
        self.adj[u].append((v, weight))
        if bidir:
            self.adj[v].append((u, weight))

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        # Radius of the earth in km
        R = 6371.0
        
        # Convert degrees to radians
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlon = lon2_rad - lon1_rad
        dlat = lat2_rad - lat1_rad
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance

    def build_mock_india_graph(self):
        # Add a few major points in India for demo if needed
        # Coordinates roughly restricted to India bounding box
        locations = {
            "DEL": (28.6139, 77.2090, "New Delhi"),
            "MUM": (19.0760, 72.8777, "Mumbai"),
            "BLR": (12.9716, 77.5946, "Bengaluru"),
            "MAA": (13.0827, 80.2707, "Chennai"),
            "HYD": (17.3850, 78.4867, "Hyderabad"),
            "CCU": (22.5726, 88.3639, "Kolkata"),
            "PNQ": (18.5204, 73.8567, "Pune")
        }
        
        for k, v in locations.items():
            self.add_node(k, v[0], v[1], v[2])
            
        # Add some edges based on rough distances to mock a connected road network graph
        self.add_edge("DEL", "MUM", 1400)
        self.add_edge("MUM", "BLR", 980)
        self.add_edge("BLR", "MAA", 350)
        self.add_edge("MAA", "HYD", 630)
        self.add_edge("HYD", "PNQ", 560)
        self.add_edge("PNQ", "MUM", 150)
        self.add_edge("DEL", "CCU", 1500)
        self.add_edge("CCU", "HYD", 1480)

    def shortest_path(self, start, end):
        if start not in self.adj or end not in self.adj:
            return None, float('inf')
            
        # Dijkstra's ALgorithm
        dist = {node: float('inf') for node in self.adj}
        dist[start] = 0
        pq = [(0, start)]
        parent = {start: None}

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue
            if u == end:
                break
            for v, weight in self.adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u
                    heapq.heappush(pq, (dist[v], v))
        
        if dist[end] == float('inf'):
            return None, float('inf')
            
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)
        return path[::-1], dist[end]

# Initialize a global graph instance for the backend
city_graph = CityGraph()
city_graph.build_mock_india_graph()
