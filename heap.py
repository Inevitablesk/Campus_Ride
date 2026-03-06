import time
import heapq

class RideMatchingHeap:
    def __init__(self):
        # We use a min-heap to pick the most urgent and closest request
        # Elements will be tuples: (priority_score, timestamp, request_id, request_data)
        self.heap = []
        
    def add_ride_request(self, request_id, request_data, user_distance_to_driver):
        # Calculate a priority score based on Distance and Time
        # Lower score = higher priority
        
        # Example: prioritize closest distance heavily, with slight penalty for waiting over time.
        # Since wait_time (seconds passed) is higher the longer they wait, 
        # we subtract wait_time from score, or equivalently use current timestamp
        
        # A simple cost function: Priority = Distance (km) + Timestamp_weight
        # Closer riders get matched first. If two are same distance, earlier request gets matched
        
        timestamp = time.time()
        # Scale timestamp down so distance isn't completely ignored 
        # (Though we effectively want oldest request if distance is somewhat equal)
        # To avoid complex numbers, let's say priority is pure distance, 
        # and heap uses timestamp as tie-breaker (oldest wins).
        
        priority_score = user_distance_to_driver
        
        heapq.heappush(self.heap, (priority_score, timestamp, request_id, request_data))
        
    def get_best_match(self):
        # Time Complexity: O(log N)
        if self.heap:
            best_match = heapq.heappop(self.heap)
            return {
                "priority": best_match[0],
                "requested_at": best_match[1],
                "request_id": best_match[2],
                "details": best_match[3]
            }
        return None
        
    def peek_best_match(self):
        if self.heap:
            return self.heap[0]
        return None

# Global instance for simulation
ride_queue = RideMatchingHeap()
