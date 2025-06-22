from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

# Enums simplificados
class SceneType(str, Enum):
    GAME = "game"
    EXPERIENCE = "experience"
    GALLERY = "gallery"
    MEETING = "meeting"
    EVENT = "event"
    SHOWROOM = "showroom"
    OTHER = "other"

class SceneStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    DELETED = "deleted"

# Modelo simplificado de escena para Reflex
class Scene:
    def __init__(self,
                 name: str,
                 description: str,
                 creator_id: str,
                 scene_type: SceneType = SceneType.EXPERIENCE,
                 status: SceneStatus = SceneStatus.DRAFT,
                 is_public: bool = False,
                 width: int = 1000,
                 height: int = 1000,
                 depth: int = 1000,
                 assets: Optional[List[str]] = None,
                 objects: Optional[List[Dict[str, Any]]] = None,
                 environment: Optional[Dict[str, Any]] = None,
                 scene_file_url: Optional[str] = None,
                 thumbnail_url: Optional[str] = None):
        self.name = name
        self.description = description
        self.creator_id = creator_id
        self.scene_type = scene_type
        self.status = status
        self.is_public = is_public
        self.width = width
        self.height = height
        self.depth = depth
        self.assets = assets or []
        self.objects = objects or []
        self.environment = environment or {}
        self.scene_file_url = scene_file_url
        self.thumbnail_url = thumbnail_url
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_asset(self, asset_id: str, transform: Dict[str, Any]) -> bool:
        if asset_id and asset_id not in self.assets:
            self.assets.append(asset_id)
            self.objects.append({
                "asset_id": asset_id,
                "transform": transform,
                "added_at": datetime.utcnow().isoformat()
            })
            self.updated_at = datetime.utcnow()
            return True
        return False

    def remove_asset(self, asset_id: str) -> bool:
        if asset_id in self.assets:
            self.assets.remove(asset_id)
            self.objects = [obj for obj in self.objects if obj["asset_id"] != asset_id]
            self.updated_at = datetime.utcnow()
            return True
        return False

    def update_asset_transform(self, asset_id: str, new_transform: Dict[str, Any]) -> bool:
        for obj in self.objects:
            if obj["asset_id"] == asset_id:
                obj["transform"] = new_transform
                obj["updated_at"] = datetime.utcnow().isoformat()
                self.updated_at = datetime.utcnow()
                return True
        return False

    def update_environment(self, new_environment: Dict[str, Any]) -> None:
        self.environment.update(new_environment)
        self.updated_at = datetime.utcnow() 