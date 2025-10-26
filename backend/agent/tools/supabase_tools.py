import os
from supabase import create_client, Client
from typing import Optional, Dict, Any
from langchain_core.tools import tool
from agent.models.phone_details_table_schema import Phone
import re
from core.config import settings


SUPABASE_URL = settings.SUPABASE_URL
SUPABASE_KEY = settings.SUPABASE_KEY
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def fetch_single_phone_details(phone_name: str) -> Optional[Dict]:
    """
    Fetch detailed information about a phone from Supabase.

    Args:
        phone_name (str): The exact or partial model name of the phone (case-insensitive).

    Returns:
        dict: Phone details validated via Pydantic, or an error message.
    """
    if not phone_name or len(phone_name.strip()) < 2:
        return {"error": "Invalid phone name."}

    try:
        response = (
            supabase.table("phones")
            .select("*")
            .ilike("name", f"%{phone_name.strip()}%")
            .limit(1)
            .execute()
        )

        if not response.data or len(response.data) == 0:
            return {"error": f"No phone found matching '{phone_name}'."}

        phone_record = response.data[0]

        phone_obj = Phone(**phone_record)

        return phone_obj.model_dump(exclude_none=True)

    except Exception as e:
        return {"error": f"Error fetching phone details: {str(e)}"}


@tool
def fetch_phone_details(phone_name: str) -> Optional[Dict]:
    """
    Fetch detailed information about a phone from Supabase.

    Args:
        phone_name (str): The exact model name of the phone (case-insensitive).

    Returns:
        dict or None: Structured phone data, or None if not found.
    """
    return fetch_single_phone_details(phone_name)


@tool
def fetch_recommendations(criteria: Dict[str, Any], limit: int = 5) -> Optional[Dict]:
    """
    Fetch phone recommendations based on given criteria from Supabase.

    Args:
        criteria (dict): A dictionary of criteria to filter phones.
        limit (int): Number of recommendations to return. Default is 5.
    Returns:
        list or dict: List of recommended phones, or error message.
    """
    try:
        query = supabase.table("phones").select("*")

        # Apply filters based on criteria
        for key, value in criteria.items():
            # Skip invalid keys
            if key not in {
                "brand",
                "price",
                "os",
                "display_size_inch",
                "display_type",
                "refresh_rate",
                "processor",
                "ram_gb",
                "storage_gb",
                "battery_mah",
                "charging_speed_w",
                "rear_camera_mp",
                "front_camera_mp",
                "camera_features",
                "network",
                "features",
                "use_cases",
                "released_year",
            }:
                continue

            # Handle lists (e.g., features/use_cases)
            if isinstance(value, list):
                query = query.contains(key, value)

            # Handle comparison filters (<=, >=, <, >)
            elif isinstance(value, str) and re.match(
                r"^(<=|>=|<|>)\s*\d+$", value.strip()
            ):
                match = re.match(r"^(<=|>=|<|>)\s*(\d+)$", value.strip())
                if match:
                    operator, num_value = match.groups()
                    num_value = int(num_value)
                    if operator == "<=":
                        query = query.lte(key, num_value)
                    elif operator == ">=":
                        query = query.gte(key, num_value)
                    elif operator == "<":
                        query = query.lt(key, num_value)
                    elif operator == ">":
                        query = query.gt(key, num_value)

            # Handle exact match
            else:
                query = query.eq(key, value)

        response = query.limit(limit).execute()

        if not response.data or len(response.data) == 0:
            return {"error": "No recommendations found based on the given criteria."}

        return response.data

    except Exception as e:
        return {"error": f"Error fetching recommendations: {str(e)}"}


@tool
def compare_phones(phone1: str, phone2: str) -> Optional[Dict]:
    """
    Compare two phones and return their specifications side by side.

    Args:
        phone1 (str): Full Name of the first phone.
        phone2 (str): Full Name of the second phone.

    Returns:
        dict or None: Comparison data, or None if any phone not found.
    """
    details1 = fetch_single_phone_details(phone1)
    details2 = fetch_single_phone_details(phone2)

    if "error" in details1:
        return {"error": f"Phone 1 error: {details1['error']}"}
    if "error" in details2:
        return {"error": f"Phone 2 error: {details2['error']}"}

    comparison = {"phone_1": details1, "phone_2": details2}

    return comparison
