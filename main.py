from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time
import uuid
import math

# DSA Module Imports
from dsa.graph import city_graph
from dsa.trie import location_trie
from dsa.heap import ride_queue
from dsa.hash import data_store

app = FastAPI(title="Ride-Matching API")

# Setup CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RideRequest(BaseModel):
    user_id: str
    pickup_id: str
    dropoff_id: str

@app.get("/locations/autocomplete")
def autocomplete_location(query: str):
    """
    O(L) Auto-complete prefix tree lookup for locations.
    """
    if not query:
        return []
    results = location_trie.search_prefix(query)
    return results

@app.post("/ride/request")
def request_ride(request: RideRequest):
    """
    Request a cab ride: O(V + E) shortest path -> O(log N) Heap entry
    """
    # 1. Dijkstra Path Finding
    path, total_distance = city_graph.shortest_path(request.pickup_id, request.dropoff_id)
    if not path:
        raise HTTPException(status_code=400, detail="Route unavailable")
        
    # Calculate Smart Fare Dynamic Pricing
    # Base: 40 INR + 12 INR/KM
    # Dynamic Pricing could be added based on queue size (O(1))
    base_fare = 40.0
    rate_per_km = 12.0
    computed_fare = base_fare + (total_distance * rate_per_km)
    
    # Generate Ride
    ride_data = {
        "status": "waiting",
        "user_id": request.user_id,
        "pickup": request.pickup_id,
        "dropoff": request.dropoff_id,
        "path": path,
        "total_distance_km": round(total_distance, 2),
        "estimated_fare": round(computed_fare, 2),
        "timestamp": time.time()
    }
    
    # 2. Store Active Ride using Hash (O(1))
    ride_id = data_store.add_active_ride(ride_data)
    
    # 3. Add to Ride Matching Heap Queue (O(log N))
    # Simulated driver distance; using hardcoded 5km penalty for wait/priority logic
    mock_driver_distance = 5 
    ride_queue.add_ride_request(ride_id, ride_data, mock_driver_distance)
    
    return {
        "status": "success",
        "ride_id": ride_id,
        "message": "Ride placed in matching queue",
        "details": ride_data
    }

@app.get("/ride/driver-match")
def driver_match():
    """
    Simulated Driver Polling for next available high priority ride (O(log N))
    """
    best_match = ride_queue.get_best_match()
    if not best_match:
        return {"message": "No rides in queue presently"}
        
    matched_ride_id = best_match["request_id"]
    
    # Update Active Match HashMap Status (O(1))
    data_store.update_ride(matched_ride_id, status="accepted")
    
    return best_match

@app.get("/ride/status/{ride_id}")
def ride_status(ride_id: str):
    """
    Tracking active ride requests (O(1) Hash Table Fetch)
    """
    ride = data_store.get_ride(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found.")
    return ride

@app.post("/ride/dynamic-split-share")
def check_ride_share(ride_id: str):
    """
    Dynamic Social Matching: Detects overlapping paths and applies a split
    This runs roughly in O(#Active rides) to scan overlapping rides logic
    """
    current_ride = data_store.get_ride(ride_id)
    if not current_ride or current_ride["status"] != "waiting":
        return {"available": False}

    # Highly simplified logic: finding another ride with EXACT same dropoff 
    for active_id, active_data in data_store.active_rides.items():
        if active_id != ride_id and active_data["status"] == "waiting":
            if active_data["dropoff"] == current_ride["dropoff"]:
                # Shared path logic match!
                return {
                    "available": True,
                    "matched_user_id": active_data["user_id"],
                    "savings_percent": 30, # Saving percent based on combined 2-stop overlap
                    "split_fare": round(current_ride["estimated_fare"] * 0.70, 2)
                }

    return {"available": False}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
