import json
from mcp.server.fastmcp import FastMCP
import os
import httpx 
from datetime import datetime
from dotenv import load_dotenv
from typing import List, Dict, Optional,Any
import requests
load_dotenv()

mcp = FastMCP("Google Flights MCP")
DUFFEL_TOKEN = os.getenv("DUFFEL_TOKEN")
DUFFEL_VERSION = "v2"
DUFFEL_BASE = "https://api.duffel.com/"
if not DUFFEL_TOKEN:
    raise ValueError("DUFFEL_TOKEN is not set. Please set it in the .env file.")


@mcp.resource("mcp://airports")
def get_airports():
    """Get a list of airports."""
    airports =        [
    {"id": "ATL", "name": "Hartsfield–Jackson Atlanta International Airport", "city": "Atlanta"},
    {"id": "DFW", "name": "Dallas/Fort Worth International Airport", "city": "Dallas–Fort Worth"},
    {"id": "DEN", "name": "Denver International Airport", "city": "Denver"},
    {"id": "LAX", "name": "Los Angeles International Airport", "city": "Los Angeles"},
    {"id": "ORD", "name": "O'Hare International Airport", "city": "Chicago"},
    {"id": "JFK", "name": "John F. Kennedy International Airport", "city": "New York City"},
    {"id": "MCO", "name": "Orlando International Airport", "city": "Orlando"},
    {"id": "LAS", "name": "Harry Reid International Airport", "city": "Las Vegas"},
    {"id": "CLT", "name": "Charlotte Douglas International Airport", "city": "Charlotte"},
    {"id": "MIA", "name": "Miami International Airport", "city": "Miami"},
    {"id": "PHX", "name": "Phoenix Sky Harbor International Airport", "city": "Phoenix"},
    {"id": "SEA", "name": "Seattle–Tacoma International Airport", "city": "Seattle"},
    {"id": "SFO", "name": "San Francisco International Airport", "city": "San Francisco"},
    {"id": "EWR", "name": "Newark Liberty International Airport", "city": "Newark"},
    {"id": "IAH", "name": "George Bush Intercontinental Airport", "city": "Houston"},
    {"id": "BOS", "name": "Logan International Airport", "city": "Boston"},
    {"id": "MSP", "name": "Minneapolis–Saint Paul International Airport", "city": "Minneapolis–Saint Paul"},
    {"id": "FLL", "name": "Fort Lauderdale–Hollywood International Airport", "city": "Fort Lauderdale"},
    {"id": "LGA", "name": "LaGuardia Airport", "city": "New York City"},
    {"id": "DTW", "name": "Detroit Metropolitan Airport", "city": "Detroit"},
    {"id": "PHL", "name": "Philadelphia International Airport", "city": "Philadelphia"},
    {"id": "SLC", "name": "Salt Lake City International Airport", "city": "Salt Lake City"},
    {"id": "BWI", "name": "Baltimore/Washington International Airport", "city": "Baltimore–Washington"},
    {"id": "IAD", "name": "Washington Dulles International Airport", "city": "Washington, D.C."},
    {"id": "SAN", "name": "San Diego International Airport", "city": "San Diego"},
    {"id": "TPA", "name": "Tampa International Airport", "city": "Tampa"},
    {"id": "BNA", "name": "Nashville International Airport", "city": "Nashville"},
    {"id": "RDU", "name": "Raleigh–Durham International Airport", "city": "Raleigh/Durham"}
]

    return airports



@mcp.tool()
def search_flights(
    departure_id: str,
    arrival_id: str,
    outbound_date: str,
    return_date: Optional[str] = None, 
    travel_class: str = "economy",
    adults: int = 1
):

    """Search for flights between two airports."""
    
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the SERPAPI_API_KEY environment variable.")
    
    base_url = "https://serpapi.com/search"
    if return_date:
        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "return_date": return_date,
            "travel_class": "1" if travel_class == "economy" else "3",
            "adults": adults,
            "type": 1 if return_date else 2, 
            "api_key": api_key
        }
    else:
        params = {
            "engine": "google_flights",
            "departure_id": departure_id,
            "arrival_id": arrival_id,
            "outbound_date": outbound_date,
            "travel_class": "1" if travel_class == "economy" else "3",
            "adults": adults,
            "return_date": None,
            "type": 2,  # 2 for one way
            "api_key": api_key
        }
    
    with httpx.Client() as client:
        response = client.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        # Fixed: Corrected syntax error
        raise Exception(f"API Error: {response.status_code} - {response.text}")

# ... rest of your tools remain the same
@mcp.tool()
def get_flight_details(flight_id: str):
    """Get details for a specific flight."""
    
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Please set the SERPAPI_API_KEY environment variable.")
    
    base_url = "https://serpapi.com/search"
    params = {
        "engine": "google_flights",
        "flight_id": flight_id,
        "api_key": api_key
    }
    
    with httpx.Client() as client:
        response = client.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

@mcp.tool()
def search_multi_city(
    legs: List[Dict], 
    travel_class: str = "economy",
    adults: int = 1
):
    """Search for multi-city/complex itinerary flights using SERP API"""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERP API key is required")
    
    if len(legs) < 2:
        raise ValueError("Multi-city search requires at least 2 legs")
    
    base_url = "https://serpapi.com/search"
    
   
    travel_class_map = {
        "economy": "1",
        "premium_economy": "2", 
        "business": "3",
        "first": "4"
    }
    
    multi_city_data = []
    for leg in legs:
        multi_city_data.append({
            "departure_id": leg["from"],
            "arrival_id": leg["to"],
            "date": leg["date"]
        })
    
    params = {
        "engine": "google_flights",
        "type": "3",  # Multi-city type
        "multi_city_json": json.dumps(multi_city_data),
        "adults": adults,
        "travel_class": travel_class_map.get(travel_class.lower(), "1"),
        "api_key": api_key
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()

        result = {
            "search_completed": True,
            "total_legs": len(legs),
            "multi_city_results": {
                "best_flights": data.get("best_flights", []),
                "other_flights": data.get("other_flights", []),
                "airports": data.get("airports", {}),
                "search_metadata": data.get("search_metadata", {}),
                "legs_info": legs
            }
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Error in multi-city search: {e}")
        return {
            "search_completed": False,
            "total_legs": len(legs),
            "multi_city_results": [],
            "error": str(e)
        }

def _safe_err(e: requests.HTTPError):
    try:
        return e.response.json()
    except Exception:
        return getattr(e.response, "text", str(e))
    
def duffel_headers():
    """Generate headers for Duffel API requests."""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Duffel-Version": DUFFEL_VERSION,
        "Authorization": f"Bearer {DUFFEL_TOKEN}"
    }

def duffel_get(path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    r = requests.get(f"{DUFFEL_BASE}{path}", headers=duffel_headers(), params=params, timeout=30)
    r.raise_for_status()
    return r.json()

def duffel_post(path: str, data: Dict[str, Any]) -> Dict[str, Any]:
    r = requests.post(f"{DUFFEL_BASE}{path}", headers=duffel_headers(), data=json.dumps({"data": data}), timeout=45)
    r.raise_for_status()
    return r.json()

@mcp.tool()
def duffel_create_offer_request(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    cabin_class: str = "economy",
    adults: int = 1,
    children: int = 0,
    infants: int = 0,
    return_offers: bool = True
):
    """
    Create a Duffel Offer Request and return offers (each has an id you can book).
    For one-way set only the outbound slice; for round-trip include both slices.
    """
    slices = [{"origin": origin, "destination": destination, "departure_date": departure_date}]
    if return_date:
        slices.append({"origin": destination, "destination": origin, "departure_date": return_date})

    passengers = []
    for _ in range(adults):
        passengers.append({"type": "adult"})
    for _ in range(children):
        passengers.append({"type": "child"})
    for _ in range(infants):
        passengers.append({"type": "infant_without_seat"})

    data = {
        "slices": slices,
        "passengers": passengers,
        "cabin_class": cabin_class,
        # If you prefer streaming/batching, set return_offers False and fetch via /air/offers
    }

    try:
        # POST /air/offer_requests?return_offers=true|false
        path = f"/air/offer_requests?return_offers={'true' if return_offers else 'false'}"
        resp = duffel_post(path, data)
        offer_request = resp.get("data", {})
        offers = offer_request.get("offers", [])
        return {
            "offer_request_id": offer_request.get("id"),
            "offers": offers  # each item has an "id" field -> this is your offer_id
        }
    except requests.HTTPError as e:
        return {"error": True, "message": str(e), "details": getattr(e.response, "text", None)}

@mcp.tool()
def duffel_list_offers(offer_request_id: str, sort: Optional[str] = None, limit: int = 50):
    """
    Retrieve offers for a given offer_request_id and return their IDs and key fields.
    """
    params = {"offer_request_id": offer_request_id, "limit": str(limit)}
    if sort:
        params["sort"] = sort
    try:
        res = duffel_get("/air/offers", params=params)
        offers = res.get("data", [])
        return {"offers": offers}
    except requests.HTTPError as e:
        return {"error": True, "message": str(e), "details": getattr(e.response, "text", None)}


# ---------- Duffel booking tools (MCP) ----------

@mcp.tool()
def booking_validate_or_price_offer(offer_id: str):
    """
    Validate and fetch the latest pricing/availability for an offer.
    GET /air/offers/{offer_id}
    """
    try:
        res = duffel_get(f"/air/offers/{offer_id}")
        return {"offer": res.get("data")}
    except requests.HTTPError as e:
        return {"error": True, "message": str(e), "details": _safe_err(e)}



@mcp.tool()
def booking_list_services_and_seatmaps(offer_id: str):
    """
    List ancillaries/services (bags, paid seats, etc.) and seat maps for an offer.
    - Seat maps: GET /air/seat_maps?offer_id=...
    - Services:  GET /air/offer_services?offer_id=...
    """
    try:
        seat_maps = duffel_get("/air/seat_maps", params={"offer_id": offer_id}).get("data", [])
        services = duffel_get("/air/offer_services", params={"offer_id": offer_id}).get("data", [])
        return {
            "services": services,   # may include bags, chargeable seats, etc.
            "seat_maps": seat_maps  # renderable data for seat selection
        }
    except requests.HTTPError as e:
        return {"error": True, "message": str(e), "details": _safe_err(e)}


@mcp.tool()
def booking_create_order(
    offer_id: str,
    passengers: List[Dict],
    payments: Optional[List[Dict]] = None,
    services: Optional[List[Dict]] = None,
    type: str = "instant",   # "instant" or "hold"
    metadata: Optional[Dict] = None,
    contact: Optional[Dict] = None
):
    """
    Create a Duffel order.
    - Instant purchase: include payments=[{type: 'balance', amount, currency}]
    - Hold: set type='hold' and omit payments (only allowed when offer is hold-eligible)
      POST /air/orders
    """
    try:
        payload = {
            "selected_offers": [offer_id],
            "passengers": passengers,
        }
        if services:
            payload["services"] = services
        if metadata:
            payload["metadata"] = metadata
        if contact:
            payload["contact"] = contact

        if type == "hold":
            payload["type"] = "hold"
        else:
            if not payments:
                return {"error": True, "message": "payments are required for instant purchase orders"}
            payload["payments"] = payments

        res = duffel_post("air/orders", payload)
        order = res.get("data")
        return {"order": order}
    except requests.HTTPError as e:
        return {"error": True, "message": str(e), "details": _safe_err(e)}


@mcp.tool()
def booking_pay_for_order(order_id: str, amount: str, currency: str, payment_type: str = "balance"):
    """
    Pay for a hold order using Duffel Payments.
    - POST /air/payments
    - amount and currency must match order.total_amount and order.total_currency
    """
    try:
        payload = {
            "order_id": order_id,
            "payment": {
                "type": payment_type,     # typically "balance" unless enabled otherwise
                "amount": amount,
                "currency": currency
            }
        }
        res = duffel_post("/air/payments", payload)
        return {"payment": res.get("data")}
    except requests.HTTPError as e:
        return {"error": True, "message": str(e), "details": _safe_err(e)}


@mcp.tool()
def booking_get_order_status(order_id: str):
    """
    Retrieve latest order state including payment_status and documents (tickets).
    - GET /air/orders/{order_id}
    """
    try:
        res = duffel_get(f"/air/orders/{order_id}")
        order = res.get("data")
        return {
            "order": order,
            "payment_status": (order or {}).get("payment_status"),
            "documents": (order or {}).get("documents")
        }
    except requests.HTTPError as e:
        return {"error": True, "message": str(e), "details": _safe_err(e)}



if __name__ == "__main__":
    mcp.run(
        transport="http",  
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )