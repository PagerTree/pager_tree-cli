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

    # ALERTS
    # =======

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
                   status: Optional[str] = None, search: Optional[str] = None, alias: Optional[str] = None) -> Dict[str, Any]:
        """List all alerts in PagerTree."""
        params = {k: v for k, v in {"limit": limit, "offset": offset, "status": status, "q": search, "thirdparty_id": alias}.items() 
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

    # BROADCASTS
    # =========

    def create_broadcast(
        self,
        title: str,
        description: Optional[str] = None,
        destination_account_user_ids: Optional[List[str]] = None,
        destination_team_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a new broadcast in PagerTree."""
        payload = {
            "title": title,
            "description": description,
            "destination_account_user_ids": destination_account_user_ids or [],
            "destination_team_ids": destination_team_ids or []
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = self.session.post(f"{self.base_url}/broadcasts", json=payload)
        response.raise_for_status()
        return response.json()

    def list_broadcasts(self, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """List all broadcasts in PagerTree."""
        params = {k: v for k, v in {"limit": limit, "offset": offset}.items() if v is not None}
        response = self.session.get(f"{self.base_url}/broadcasts", params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "data": data.get("data", []),
            "total": data.get("total_count", 0),
            "has_more": data.get("has_more", False),
            "limit": limit,
            "offset": offset
        }

    def show_broadcast(self, broadcast_id: str) -> Dict[str, Any]:
        """Fetch a single broadcast by ID from PagerTree."""
        response = self.session.get(f"{self.base_url}/broadcasts/{broadcast_id}")
        response.raise_for_status()
        return response.json()

    def update_broadcast(
        self,
        broadcast_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        destination_account_user_ids: Optional[List[str]] = None,
        destination_team_ids: Optional[List[str]] = None,
        response_requested: Optional[bool] = None,
        response_requested_by: Optional[str] = None,
        status: Optional[str] = None,
        notify_sms: Optional[bool] = None,
        notify_push: Optional[bool] = None,
        notify_email: Optional[bool] = None,
        notify_slack: Optional[bool] = None,
        notify_voice: Optional[bool] = None,
        notify_whatsapp: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Update a broadcast in PagerTree."""
        payload = {
            "title": title,
            "description": description,
            "destination_account_user_ids": destination_account_user_ids,
            "destination_team_ids": destination_team_ids,
            "response_requested": response_requested,
            "response_requested_by": response_requested_by,
            "status": status,
            "meta": {
                "notify_sms": notify_sms,
                "notify_push": notify_push,
                "notify_email": notify_email,
                "notify_slack": notify_slack,
                "notify_voice": notify_voice,
                "notify_whatsapp": notify_whatsapp
            }
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        if "meta" in payload:
            payload["meta"] = {k: v for k, v in payload["meta"].items() if v is not None}
        response = self.session.put(f"{self.base_url}/broadcasts/{broadcast_id}", json=payload)
        response.raise_for_status()
        return response.json()

    def delete_broadcast(self, broadcast_id: str) -> Dict[str, Any]:
        """Delete a broadcast in PagerTree."""
        response = self.session.delete(f"{self.base_url}/broadcasts/{broadcast_id}")
        response.raise_for_status()
        return response.json() if response.content else {"message": "Broadcast deleted successfully"}

    # TEAMS
    # ======

    def create_team(
        self,
        name: str,
        notes: Optional[str] = None,
        member_account_user_ids: Optional[List[str]] = None,
        admin_account_user_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Create a new team in PagerTree."""
        payload = {
            "name": name,
            "notes": notes,
            "member_account_user_ids": member_account_user_ids or [],
            "admin_account_user_ids": admin_account_user_ids or []
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = self.session.post(f"{self.base_url}/teams", json=payload)
        response.raise_for_status()
        return response.json()

    def list_teams(self, limit: int = 10, offset: int = 0, search: Optional[str] = None) -> Dict[str, Any]:
        """List all teams in PagerTree."""
        params = {k: v for k, v in {"limit": limit, "offset": offset, "q": search}.items() if v is not None}
        response = self.session.get(f"{self.base_url}/teams", params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "data": data.get("data", []),
            "total": data.get("total_count", 0),
            "has_more": data.get("has_more", False),
            "limit": limit,
            "offset": offset
        }

    def show_team(self, team_id: str) -> Dict[str, Any]:
        """Fetch a single team by ID from PagerTree."""
        response = self.session.get(f"{self.base_url}/teams/{team_id}")
        response.raise_for_status()
        return response.json()

    def update_team(
        self,
        team_id: str,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        member_account_user_ids: Optional[List[str]] = None,
        admin_account_user_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Update a team in PagerTree."""
        payload = {
            "name": name,
            "notes": notes,
            "member_account_user_ids": member_account_user_ids,
            "admin_account_user_ids": admin_account_user_ids
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        response = self.session.put(f"{self.base_url}/teams/{team_id}", json=payload)
        response.raise_for_status()
        return response.json()

    def delete_team(self, team_id: str) -> Dict[str, Any]:
        """Delete a team in PagerTree."""
        response = self.session.delete(f"{self.base_url}/teams/{team_id}")
        response.raise_for_status()
        return response.json() if response.content else {"message": "Team deleted successfully"}

    def get_team_current_oncall(self, team_id: str) -> Dict[str, Any]:
        """Fetch current on-call users for a team in PagerTree."""
        response = self.session.get(f"{self.base_url}/teams/{team_id}/current_oncall")
        response.raise_for_status()
        return response.json()

    def get_team_alerts(self, team_id: str, limit: int = 10, offset: int = 0) -> Dict[str, Any]:
        """Fetch alerts for a specific team in PagerTree."""
        params = {k: v for k, v in {"limit": limit, "offset": offset}.items() if v is not None}
        response = self.session.get(f"{self.base_url}/teams/{team_id}/alerts", params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "data": data.get("data", []),
            "total": data.get("total_count", 0),
            "has_more": data.get("has_more", False),
            "limit": limit,
            "offset": offset
        }

    # USERS
    # ======

    def create_user(self, name: str, email: str, roles: Optional[Dict[str, bool]] = None, team_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Create a new account user in PagerTree."""
        payload = {
            "user_attributes": {
                "name": name,
                "emails_attributes": [{"email": email}]
            },
            "roles": roles or {},
            "team_ids": team_ids or []
        }
        response = self.session.post(f"{self.base_url}/account_users", json=payload)
        response.raise_for_status()
        return response.json()

    def list_users(self, limit: int = 10, offset: int = 0, search: Optional[str] = None) -> Dict[str, Any]:
        """List all users in PagerTree."""
        params = {k: v for k, v in {"limit": limit, "offset": offset, "q": search}.items() if v is not None}
        response = self.session.get(f"{self.base_url}/account_users", params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "data": data.get("data", []),
            "total": data.get("total_count", 0),
            "has_more": data.get("has_more", False),
            "limit": limit,
            "offset": offset
        }

    def show_user(self, user_id: str) -> Dict[str, Any]:
        """Fetch a single user by ID from PagerTree."""
        response = self.session.get(f"{self.base_url}/account_users/{user_id}")
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Update an account user in PagerTree."""
        payload = {}
        if name:
            payload["user_attributes"] = {}
            payload["user_attributes"]["name"] = name
        payload = {k: v for k, v in payload.items() if v}
        response = self.session.put(f"{self.base_url}/account_users/{user_id}", json=payload)
        response.raise_for_status()
        return response.json()

    def delete_user(self, user_id: str) -> Dict[str, Any]:
        """Delete a user in PagerTree."""
        response = self.session.delete(f"{self.base_url}/account_users/{user_id}")
        response.raise_for_status()
        return response.json() if response.content else {"message": "User deleted successfully"}