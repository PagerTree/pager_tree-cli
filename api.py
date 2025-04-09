import requests
from config import API_KEY, BASE_URL

def api_create_alert(title, description):
    """Create a new alert in PagerTree."""
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {
        "title": title,
        "description": description,
    }
    response = requests.post(f"{BASE_URL}/alerts", json=payload, headers=headers)
    response.raise_for_status()  # Raise an error for bad responses
    return response.json()

def api_list_alerts(limit=10, offset=0):
    """List all alerts in PagerTree."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {"limit": limit, "offset": offset}  # Adjust based on API docs
    response = requests.get(f"{BASE_URL}/alerts", headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return {
      "data": data.get("data", []),  # List of incidents
      "total": data.get("total_count", 0),  # Total number of incidents
      "has_more": data.get("has_more", False),  # Boolean indicating if there are more incidents
      "limit": limit,
      "offset": offset
    }

def api_show_alert(alert_id):
    """Fetch a single alert by ID from PagerTree."""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(f"{BASE_URL}/alerts/{alert_id}", headers=headers)
    response.raise_for_status()
    return response.json()