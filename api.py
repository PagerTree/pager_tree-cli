import requests
import os
import configparser
from typing import Optional, List, Dict, Any

class PagerTreeClient:
    def __init__(self, config_file: Optional[str] = None):
        """Initialize PagerTree client with configuration."""
        # Load configuration
        self.config = self._load_config(config_file)

        # Set up base URL and API key
        self.base_url = self.config.get('DEFAULT', 'BASE_URL', fallback=os.getenv('PAGERTREE_BASE_URL', 'https://api.pagertree.com/api/v4'))
        self.api_key = self.config.get('DEFAULT', 'API_KEY',  fallback=os.getenv('PAGERTREE_API_KEY'))
        self.user_agent = "PagerTree-Python-CLI-Client/1.0"

        if not self.api_key:
            raise ValueError("API_KEY must be provided via environment variable or config file")

        # Set up default headers
        self.default_headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": self.user_agent
        }

        # Create a session for persistent connections
        self.session = requests.Session()
        self.session.headers.update(self.default_headers)

    def _load_config(self, config_file: Optional[str]) -> configparser.ConfigParser:
        """Load configuration from file or return empty config."""
        config = configparser.ConfigParser()
        if config_file and os.path.exists(config_file):
            config.read(config_file)
        return config

    def create_alert(self, title: str, description: Optional[str] = None, 
                    team_ids: Optional[List[str]] = None, 
                    destination_router_ids: Optional[List[str]] = None,
                    destination_account_user_ids: Optional[List[str]] = None,
                    urgency: str = "medium", tags: Optional[List[str]] = None,
                    alias: Optional[str] = None, incident: bool = False,
                    incident_severity: Optional[str] = None,
                    incident_message: Optional[str] = None) -> Dict[str, Any]:
        """Create a new alert in PagerTree."""
        payload = {
            "title": title,
            "description": description,
            "destination_team_ids": team_ids,
            "destination_route_ids": destination_router_ids,
            "destination_account_user_ids": destination_account_user_ids,
            "urgency": urgency,
            "tags": tags,
            "thirdparty_id": alias,
            "meta": {
                "incident": incident,
                "incident_severity": incident_severity,
                "incident_message": incident_message
            }
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = self.session.post(f"{self.base_url}/alerts", json=payload)
        response.raise_for_status()
        return response.json()

    def list_alerts(self, limit: int = 10, offset: int = 0, 
                   status: Optional[str] = None, search: Optional[str] = None) -> Dict[str, Any]:
        """List all alerts in PagerTree."""
        params = {k: v for k, v in {"limit": limit, "offset": offset, "status": status, "q": search}.items() 
                 if v is not None}
        response = self.session.get(f"{self.base_url}/alerts", params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "data": data.get("data", []),
            "total": data.get("total_count", 0),
            "has_more": data.get("has_more", False),
            "limit": limit,
            "offset": offset
        }

    def show_alert(self, alert_id: str) -> Dict[str, Any]:
        """Fetch a single alert by ID from PagerTree."""
        response = self.session.get(f"{self.base_url}/alerts/{alert_id}")
        response.raise_for_status()
        return response.json()

    def delete_alert(self, alert_id: str) -> Dict[str, Any]:
        """Delete an alert in PagerTree."""
        response = self.session.delete(f"{self.base_url}/alerts/{alert_id}")
        response.raise_for_status()
        return response.json() if response.content else {"message": "Alert deleted successfully"}

    def acknowledge_alert(self, alert_id: str) -> Dict[str, Any]:
        """Acknowledge an alert in PagerTree."""
        response = self.session.post(f"{self.base_url}/alerts/{alert_id}/acknowledge")
        response.raise_for_status()
        return response.json()

    def reject_alert(self, alert_id: str) -> Dict[str, Any]:
        """Reject an alert in PagerTree."""
        response = self.session.post(f"{self.base_url}/alerts/{alert_id}/reject")
        response.raise_for_status()
        return response.json()

    def resolve_alert(self, alert_id: str) -> Dict[str, Any]:
        """Resolve an alert in PagerTree."""
        response = self.session.post(f"{self.base_url}/alerts/{alert_id}/resolve")
        response.raise_for_status()
        return response.json()

    def create_alert_comment(self, alert_id: str, comment: str) -> Dict[str, Any]:
        """Create a comment on an alert in PagerTree."""
        payload = {"body": comment}
        response = self.session.post(f"{self.base_url}/alerts/{alert_id}/comments", json=payload)
        response.raise_for_status()
        return response.json()

    def list_alert_comments(self, alert_id: str, limit: int = 10, 
                          offset: int = 0) -> Dict[str, Any]:
        """List all comments for a specific alert in PagerTree."""
        params = {k: v for k, v in {"limit": limit, "offset": offset}.items() if v is not None}
        response = self.session.get(f"{self.base_url}/alerts/{alert_id}/comments", params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "data": data.get("data", []),
            "total": data.get("total_count", 0),
            "has_more": data.get("has_more", False),
            "limit": limit,
            "offset": offset
        }