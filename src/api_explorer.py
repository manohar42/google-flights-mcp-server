import asyncio
import json
import os
from typing import Dict, Any
import httpx
from dotenv import load_dotenv

load_dotenv()

class GoogleFlightAPIExplorer:
    
    """Class to explore Google Flight API endpoints."""

    def __init__(self):
        
        self.api_key = os.getenv("SERPAPI_API_KEY")
        self.base_url = "https://serpapi.com/search.json"
        if not self.api_key:
            print("API key not found. Please set the SERPAPI_API_KEY environment variable.")
            exit(1)
    async def explore_basic_endpoints(self):
        """Explore basic endpoints of the Google Flight API."""
        print("\n EXPLORING BASIC FLIGHT SEARCH")
        print("=" * 50)
        params = {
            "engine": "google_flights",
            "departure_id": "JFK",        # New York JFK
            "arrival_id": "LAX",          # Los Angeles LAX  
            "outbound_date": "2025-09-01", # Future date
            "return_date": "2025-09-08",   # Return date
            "currency": "USD",
            "adults": 1,
            "api_key": self.api_key
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                print(f"Making request to: {self.base_url}")
                print(f"Parameters: {json.dumps({k:v for k,v in params.items() if k != 'api_key'}, indent=2)}")
                
                response = await client.get(self.base_url, params=params)
                
                print(f"Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    data = response.json()
                    # print("Response Data:",data)
                    await self._analyze_response_structure(data)
                else:
                    print(f"API Error: {response.status_code}")
                    print(f"Response: {response.text}")
                    
        except Exception as e:
            print(f"Request failed: {str(e)}")
    async def _analyze_response_structure(self, data: Dict[str, Any]):
        """Analyze the structure of API response"""
        
        print("\n📋 RESPONSE STRUCTURE ANALYSIS")
        print("-" * 40)
        
        # Top-level keys
        print("🔑 Top-level keys:")
        for key in data.keys():
            print(f"  • {key}")
        
        # Search parameters used
        if "search_parameters" in data:
            print(f"\n🎯 Search Parameters Used:")
            params = data["search_parameters"]
            for key, value in params.items():
                print(f"  • {key}: {value}")
        
        # Best flights analysis
        if "best_flights" in data and data["best_flights"]:
            print(f"\n🏆 Best Flights Found: {len(data['best_flights'])}")
            flight = data["best_flights"][0]  # Analyze first flight
            
            print("📄 First flight structure:")
            await self._analyze_flight_structure(flight, "  ")
        
        # Price insights
        if "price_insights" in data:
            print(f"\n💰 Price Insights Available:")
            insights = data["price_insights"]
            for key, value in insights.items():
                print(f"  • {key}: {value}")
        
        # Other flights
        if "other_flights" in data:
            print(f"\n🔄 Other Flights: {len(data['other_flights'])}")
        
        # Save full response for detailed analysis
        with open("api_response_sample.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"\n💾 Full response saved to: api_response_sample.json")
    async def _analyze_flight_structure(self, flight: Dict[str, Any], indent: str = ""):
        """Analyze individual flight structure"""
        
        for key, value in flight.items():
            if key == "flights" and isinstance(value, list):
                print(f"{indent}• {key}: [{len(value)} segments]")
                if value:  # Analyze first segment
                    segment = value[0]
                    print(f"{indent}  First segment structure:")
                    for seg_key in segment.keys():
                        print(f"{indent}    - {seg_key}")
            elif isinstance(value, dict):
                print(f"{indent}• {key}: [object with {len(value)} fields]")
                for sub_key in value.keys():
                    print(f"{indent}    - {sub_key}")
            elif isinstance(value, list):
                print(f"{indent}• {key}: [array with {len(value)} items]")
            else:
                print(f"{indent}• {key}: {value}")

    async def explore_different_search_types(self):
        """Explore different types of flight searches"""
        
        print("\n🔍 EXPLORING DIFFERENT SEARCH TYPES")
        print("=" * 50)
        
        search_types = [
            {
                "name": "One-Way Flight",
                "params": {
                    "departure_id": "LAX",
                    "arrival_id": "NRT",  # Tokyo Narita
                    "outbound_date": "2025-10-15",
                    "type": 2,  # One way
                    "adults": 1
                }
            },
            {
                "name": "Business Class Round-Trip", 
                "params": {
                    "departure_id": "SFO",
                    "arrival_id": "LHR",  # London Heathrow
                    "outbound_date": "2025-11-01",
                    "return_date": "2025-11-08", 
                    "travel_class": 3,  # Business class
                    "adults": 2
                }
            }
        ]
        
        for search_type in search_types:
            await self._test_search_type(search_type["name"], search_type["params"])

    async def _test_search_type(self, name: str, params: Dict[str, Any]):
        """Test a specific search type"""
        
        print(f"\n📋 Testing: {name}")
        print("-" * 30)
        
        # Add required parameters
        full_params = {
            "engine": "google_flights",
            "currency": "USD",
            "api_key": self.api_key,
            **params
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(self.base_url, params=full_params)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Quick analysis
                    best_flights = len(data.get("best_flights", []))
                    other_flights = len(data.get("other_flights", []))
                    has_insights = "price_insights" in data
                    
                    print(f"✅ Success: {best_flights} best flights, {other_flights} others")
                    print(f"💰 Price insights: {'Yes' if has_insights else 'No'}")
                    
                    if best_flights > 0:
                        price = data["best_flights"][0].get("price", "N/A")
                        print(f"💵 Cheapest: ${price}")
                
                else:
                    print(f"❌ Failed: {response.status_code}")
                    
        except Exception as e:
            print(f"❌ Error: {str(e)}")

    async def explore_response_fields(self):
        """Document all available response fields for MCP tool design"""
        
        print("\n📝 DOCUMENTING RESPONSE FIELDS FOR MCP TOOLS")
        print("=" * 55)
        
        # This will help us design our MCP tool schemas
        field_documentation = {
            "search_parameters": "Parameters used in the search request",
            "best_flights": "Top recommended flights with best value",
            "other_flights": "Additional flight options", 
            "price_insights": "Historical pricing and booking recommendations",
            "airports": "Airport information and codes",
            "booking_options": "Available booking sources and links"
        }
        
        print("🗂️ Key response sections for MCP tools:")
        for field, description in field_documentation.items():
            print(f"  • {field}: {description}")
        
        print("\n🛠️ This analysis will help us design:")
        print("  1. Input schemas for each MCP tool")
        print("  2. Response formatting functions") 
        print("  3. Error handling strategies")
        print("  4. Data extraction and parsing logic")
      

async def main():
    """Main function to run the API explorer."""

    print("Google Flight API Explorer")
    print("="*60)


    explorer = GoogleFlightAPIExplorer()
    await explorer.explore_basic_endpoints()

if __name__ == "__main__":
    asyncio.run(main())