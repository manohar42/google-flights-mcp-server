# Testing_tools/debug_import.py
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from mcp_server_base import search_multi_city



# Call the function
test_legs = [
    {"from": "LAX", "to": "JFK", "date": "2025-09-15"},
    {"from": "JFK", "to": "LAX", "date": "2025-09-20"}
]

result = search_multi_city(test_legs)
print(result)
