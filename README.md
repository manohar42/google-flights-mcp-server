# ✈️ GCP Flights Search & Booking MCP Server

This project provides a **local MCP server** that allows you to:

- Search flights via **Google Flights (SerpAPI)**, including:
  - One-way
  - Round-trip
  - Multi-city itineraries
- Perform bookings and offer management via the **Duffel API**
- Expose the above functions as **MCP tools** for integration in AI-powered workflows

---

## 📂 Project Structure
```
.
├── src/
│ └── mcp_server_base.py # Main MCP server, flight search, and booking tools
├── Testing_tools/
│ └── tool_tester.py # Simple script to test multi-city flight search
├── .env # Environment variables (API keys)
└── requirements.txt # Python dependencies

```

## 🛠 Requirements

You’ll need:
```
- **Python** 3.9+
- **SerpAPI API key** for Google Flights search
- **Duffel API key** for flight booking
- Install dependencies:
  pip install httpx requests python-dotenv fastmcp
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:
```
SerpAPI key for Google Flights
SERPAPI_API_KEY=your_serpapi_key_here

Duffel API key for booking
DUFFEL_TOKEN=your_duffel_api_key_here
```

Both keys are **required** for full functionality:

- Without `SERPAPI_API_KEY`, flight searches will fail
- Without `DUFFEL_TOKEN`, booking and offer tools will fail

---

## 🚀 Running the MCP Server

From the project root:

python src/mcp_server_base.py

```

The server will start at:

http://127.0.0.1:8000

```

---

## ⚙️ MCP Tools Available

### 1️⃣ Flight Search Tools

- **`search_flights(departure_id, arrival_id, outbound_date, return_date=None)`**
  - Searches one-way or round trips via Google Flights
- **`search_multi_city(legs, travel_class="economy", adults=1)`**
  - Searches multi-city flight itineraries
```
Example `legs` format:
[
{"from": "LAX", "to": "JFK", "date": "2025-09-15"},
{"from": "JFK", "to": "LAX", "date": "2025-09-20"}
]

```

### 2️⃣ Booking Tools (Duffel API)

- `duffel_create_offer_request`
- `duffel_list_offers`
- `booking_validate_or_price_offer`
- `booking_list_services_and_seatmaps`
- `booking_create_order`
- `booking_get_order_status`
- `booking_pay_for_order`

---

## 🧪 Testing the Multi-City Search

Run directly without the MCP server:

python Testing_tools/tool_tester.py

```

Example output:
{
"search_completed": true,
"total_legs": 2,
"multi_city_results": {
"best_flights": [...],
"other_flights": [...],
"airports": {...},
"search_metadata": {...},
"legs_info": [
{"from": "LAX", "to": "JFK", "date": "2025-09-15"},
{"from": "JFK", "to": "LAX", "date": "2025-09-20"}
]
}
}

```

---

## 🛡 Error Handling

- Missing API keys will raise:
  ValueError: SERP API key is required

```
or
ValueError: DUFFEL_TOKEN is not set

```

- Network/API errors return a JSON object with `error: True` and details

---

## 🌐 API References

- **Google Flights Search** via SerpAPI
- **Duffel API** docs at duffel.com
---
