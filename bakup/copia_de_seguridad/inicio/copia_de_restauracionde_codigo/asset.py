from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enum simplificado de tipos de asset
class AssetType(str, Enum):
    MODEL_3D = "3d_model"
    TEXTURE = "texture"
    SOUND = "sound"
    ANIMATION = "animation"
    SCENE = "scene"
    CHARACTER = "character"
    VEHICLE = "vehicle"
    BUILDING = "building"
    NATURE = "nature"
    EFFECT = "effect"
    OTHER = "other"

# Modelo simplificado de asset para Reflex
class Asset:
    def __init__(self,
                 name: str,
                 asset_type: AssetType,
                 creator_id: str,
                 file_url: str,
                 description: str = "",
                 metadata: Optional[Dict[str, Any]] = None,
                 tags: Optional[List[str]] = None,
                 categories: Optional[List[str]] = None,
                 thumbnail_url: Optional[str] = None):
        self.name = name
        self.asset_type = asset_type
        self.creator_id = creator_id
        self.file_url = file_url
        self.description = description
        self.metadata = metadata or {}
        self.tags = tags or []
        self.categories = categories or []
        self.thumbnail_url = thumbnail_url
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_tag(self, tag: str) -> bool:
        if tag and tag not in self.tags:
            self.tags.append(tag.lower())
            self.updated_at = datetime.utcnow()
            return True
        return False

    def add_category(self, category: str) -> bool:
        if category and category not in self.categories:
            self.categories.append(category)
            self.updated_at = datetime.utcnow()
            return True
        return False

    def update_metadata(self, new_metadata: Dict[str, Any]) -> None:
        self.metadata.update(new_metadata)
        self.updated_at = datetime.utcnow() 