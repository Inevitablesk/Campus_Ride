class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.location_data = None

class LocationTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, location_name, location_data):
        # Time Complexity: O(L) where L is length of string
        node = self.root
        for char in location_name.lower():
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.location_data = location_data

    def search_prefix(self, prefix):
        # Time Complexity: O(L) to find prefix node + DFS to retrieve
        node = self.root
        for char in prefix.lower():
            if char not in node.children:
                return []
            node = node.children[char]
            
        results = []
        self._dfs(node, prefix.lower(), results)
        
        # Sort results or return top matching
        return results

    def _dfs(self, node, prefix, results):
        if node.is_end:
            results.append({
                "name": prefix.title(),
                "data": node.location_data
            })
            
        for char, child in node.children.items():
            self._dfs(child, prefix + char, results)

# Global Instance
location_trie = LocationTrie()

# Initialize with mock nodes from India Graph representation
MOCK_LOCS = {
    "DEL": {"lat": 28.6139, "lng": 77.2090, "name": "New Delhi"},
    "MUM": {"lat": 19.0760, "lng": 72.8777, "name": "Mumbai"},
    "BLR": {"lat": 12.9716, "lng": 77.5946, "name": "Bengaluru"},
    "MAA": {"lat": 13.0827, "lng": 80.2707, "name": "Chennai"},
    "HYD": {"lat": 17.3850, "lng": 78.4867, "name": "Hyderabad"},
    "CCU": {"lat": 22.5726, "lng": 88.3639, "name": "Kolkata"},
    "PNQ": {"lat": 18.5204, "lng": 73.8567, "name": "Pune"}
}

for _id, loc in MOCK_LOCS.items():
    loc["id"] = _id
    location_trie.insert(loc["name"], loc)

