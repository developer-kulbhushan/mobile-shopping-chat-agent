from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Phone(BaseModel):
    """Phone model representing a mobile device with specifications"""
    
    id: Optional[int] = None
    name: str
    brand: str
    price: Optional[int] = None
    os: Optional[str] = None
    display_size_inch: Optional[float] = Field(
        None, description="Display size in inches"
    )
    display_type: Optional[str] = None
    refresh_rate: Optional[int] = None
    processor: Optional[str] = None
    ram_gb: Optional[int] = None
    storage_gb: Optional[int] = None
    battery_mah: Optional[int] = None
    charging_speed_w: Optional[int] = None
    rear_camera_mp: Optional[int] = None
    front_camera_mp: Optional[int] = None
    camera_features: Optional[str] = None
    network: Optional[str] = None
    weight_g: Optional[int] = None
    rating: Optional[float] = Field(None, ge=0, le=5)
    popularity_score: Optional[int] = 0

    # JSONB fields (arrays)
    features: List[str] = Field(default_factory=list)
    use_cases: List[str] = Field(default_factory=list)
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)

    released_year: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,  # Replaces orm_mode=True
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "OnePlus 12R",
                "brand": "OnePlus",
                "price": 39999,
                "os": "Android",
                "display_size_inch": 6.7,
                "display_type": "AMOLED",
                "refresh_rate": 120,
                "processor": "Snapdragon 8 Gen 2",
                "ram_gb": 8,
                "storage_gb": 128,
                "battery_mah": 5500,
                "charging_speed_w": 100,
                "rear_camera_mp": 50,
                "front_camera_mp": 16,
                "camera_features": "OIS, Wide Angle, Night Mode",
                "network": "5G",
                "weight_g": 204,
                "rating": 4.5,
                "popularity_score": 92,
                "features": ["AMOLED Display", "Fast Charging", "Flagship Chipset"],
                "use_cases": ["Gaming", "Photography"],
                "pros": ["Fast performance", "Vibrant screen"],
                "cons": ["No wireless charging"],
                "released_year": 2024,
            }
        }
    )