import os
from supabase import Client
from typing import Any, Dict, List, Union, Optional
from langchain_core.tools import tool
from agent.models.phone_details_table_schema import Phone
import re
from core.config import settings
import json
from core.supabase_client import get_supabase_client


supabase: Client = get_supabase_client()


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
def fetch_recommendations(
    criteria: Dict[str, Any], limit: int = 5
) -> Union[List[Dict[str, Any]], Dict[str, str]]:
    """
    Fetch phone recommendations from Supabase based on given criteria.
    - Uses 'ilike' for text partial match.
    - Uses 'cs' for JSONB containment.
    - Combines 'features' and 'use_cases' via OR if both present.
    """
    try:
        query = supabase.table("phones").select("*")

        VALID_KEYS = {
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
        }

        TEXT_FIELDS = {
            "brand",
            "os",
            "display_type",
            "processor",
            "network",
            "camera_features",
        }
        FLOAT_FIELDS = {"display_size_inch"}
        JSONB_FIELDS = {"features", "use_cases"}

        feature_filter = None
        usecase_filter = None

        for key, value in criteria.items():
            if key not in VALID_KEYS:
                continue

            # Handle JSONB list filters (contains)
            if key in JSONB_FIELDS:
                # Ensure value is a list, even if user gives a single string
                if isinstance(value, str):
                    value = [value]
                if key == "features":
                    feature_filter = f"{key}=cs.{json.dumps(value)}"
                elif key == "use_cases":
                    usecase_filter = f"{key}=cs.{json.dumps(value)}"
                else:
                    query = query.filter(key, "cs", json.dumps(value))
                continue

            # Handle numeric comparisons (<=, >=, <, >)
            if isinstance(value, str) and re.match(
                r"^(<=|>=|<|>)\s*\d+(\.\d+)?$", value.strip()
            ):
                op, num_str = re.match(
                    r"^(<=|>=|<|>)\s*(\d+(\.\d+)?)$", value.strip()
                ).groups()[0:2]
                num_value = (
                    float(num_str) if key in FLOAT_FIELDS else int(float(num_str))
                )
                if op == "<=":
                    query = query.lte(key, num_value)
                elif op == ">=":
                    query = query.gte(key, num_value)
                elif op == "<":
                    query = query.lt(key, num_value)
                elif op == ">":
                    query = query.gt(key, num_value)
                continue

            # Handle case-insensitive "contains" text match
            if isinstance(value, str) and key in TEXT_FIELDS:
                query = query.ilike(key, f"%{value.lower()}%")
                continue

            # Default equality
            query = query.eq(key, value)

        # Apply OR between features & use_cases
        if feature_filter and usecase_filter:
            query = query.or_(f"({feature_filter},{usecase_filter})")
        elif feature_filter:
            query = query.filter("features", "cs", json.dumps(criteria["features"]))
        elif usecase_filter:
            query = query.filter("use_cases", "cs", json.dumps(criteria["use_cases"]))

        # Order & execute
        query = query.order("popularity_score", desc=True).order("rating", desc=True)
        response = query.limit(limit).execute()

        if not response.data:
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
