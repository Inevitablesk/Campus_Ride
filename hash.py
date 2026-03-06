import uuid

class StorageHash:
    def __init__(self):
        # We utilize Python dictionaries, which are implemented as Hash Tables
        # Time complexity of lookup, insert, delete is O(1) on average.
        self.active_rides = {}
        self.user_sessions = {}
        
    def add_active_ride(self, ride_data):
        ride_id = str(uuid.uuid4())
        self.active_rides[ride_id] = ride_data
        return ride_id
        
    def get_ride(self, ride_id):
        # O(1) Lookup
        return self.active_rides.get(ride_id)
        
    def update_ride(self, ride_id, **kwargs):
        if ride_id in self.active_rides:
            self.active_rides[ride_id].update(kwargs)
            return True
        return False
        
    def end_ride(self, ride_id):
        # O(1) Delete
        if ride_id in self.active_rides:
            del self.active_rides[ride_id]
            return True
        return False

# Global instance
data_store = StorageHash()
