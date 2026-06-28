import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict, field


SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'saves')
SAVE_VERSION = 1


@dataclass
class ProfileData:
    id: str
    name: str
    character_class: str
    level: int
    xp: int
    xp_to_next: int
    gold: int
    
    maxhealth: int
    health: int
    attack: int
    defense: int
    mana: int
    maxmana: int
    accuracy: int
    speed: int
    crit_chance: int
    mana_regen: int
    
    stat_points: int
    base_maxhealth: int
    base_attack: int
    base_defense: int
    base_mana: int
    base_accuracy: int
    base_speed: int
    base_crit_chance: int
    base_mana_regen: int
    
    inventory: List[Dict] = field(default_factory=list)
    equipment: Dict[str, Optional[str]] = field(default_factory=lambda: {
        "main_hand": None, "chest": None, "ring": None, "amulet": None, "boots": None
    })
    skills: List[str] = field(default_factory=list)
    completed_battles: int = 0
    total_damage_dealt: int = 0
    total_damage_taken: int = 0
    total_healed: int = 0
    critical_hits: int = 0
    enemies_defeated: Dict[str, int] = field(default_factory=dict)
    achievements: List[str] = field(default_factory=list)
    quests_completed: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_played: str = field(default_factory=lambda: datetime.now().isoformat())
    playtime_seconds: int = 0
    save_version: int = SAVE_VERSION


class SaveManager:
    def __init__(self):
        os.makedirs(SAVE_DIR, exist_ok=True)
    
    def get_save_path(self, profile_id: str) -> str:
        return os.path.join(SAVE_DIR, f"{profile_id}.json")
    
    def get_all_profiles(self) -> List[Dict]:
        profiles = []
        if not os.path.exists(SAVE_DIR):
            return profiles
        
        for filename in os.listdir(SAVE_DIR):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(SAVE_DIR, filename), 'r') as f:
                        data = json.load(f)
                        profiles.append({
                            'id': data.get('id', filename[:-5]),
                            'name': data.get('name', 'Unknown'),
                            'character_class': data.get('character_class', 'knight'),
                            'level': data.get('level', 1),
                            'gold': data.get('gold', 0),
                            'completed_battles': data.get('completed_battles', 0),
                            'last_played': data.get('last_played', ''),
                            'playtime_seconds': data.get('playtime_seconds', 0)
                        })
                except Exception as e:
                    print(f"Error loading profile {filename}: {e}")
        
        profiles.sort(key=lambda x: x['last_played'], reverse=True)
        return profiles
    
    def create_profile(self, name: str, character_class: str, class_data: Dict) -> ProfileData:
        stats = class_data['primary_stats']
        profile_id = name.lower().replace(' ', '_') + '_' + datetime.now().strftime('%Y%m%d_%H%M%S')
        
        profile = ProfileData(
            id=profile_id,
            name=name,
            character_class=character_class,
            level=1,
            xp=0,
            xp_to_next=100,
            gold=100,
            
            maxhealth=stats['maxhealth'],
            health=stats['maxhealth'],
            attack=stats['attack'],
            defense=stats['defense'],
            mana=stats['mana'],
            maxmana=stats['mana'],
            accuracy=stats['accuracy'],
            speed=stats['speed'],
            crit_chance=stats['crit_chance'],
            mana_regen=class_data.get('mana_regen', 3),
            
            stat_points=0,
            base_maxhealth=stats['maxhealth'],
            base_attack=stats['attack'],
            base_defense=stats['defense'],
            base_mana=stats['mana'],
            base_accuracy=stats['accuracy'],
            base_speed=stats['speed'],
            base_crit_chance=stats['crit_chance'],
            base_mana_regen=class_data.get('mana_regen', 3),
            
            inventory=[],
            equipment={"main_hand": None, "chest": None, "ring": None, "amulet": None, "boots": None},
            skills=class_data.get('starting_skills', []),
        )
        
        self.save_profile(profile)
        return profile
    
    def save_profile(self, profile: ProfileData) -> bool:
        try:
            profile.last_played = datetime.now().isoformat()
            path = self.get_save_path(profile.id)
            with open(path, 'w') as f:
                json.dump(asdict(profile), f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def load_profile(self, profile_id: str) -> Optional[ProfileData]:
        try:
            path = self.get_save_path(profile_id)
            if not os.path.exists(path):
                return None
            with open(path, 'r') as f:
                data = json.load(f)
            return ProfileData(**data)
        except Exception as e:
            print(f"Error loading profile: {e}")
            return None
    
    def delete_profile(self, profile_id: str) -> bool:
        try:
            path = self.get_save_path(profile_id)
            if os.path.exists(path):
                os.remove(path)
            return True
        except Exception as e:
            print(f"Error deleting profile: {e}")
            return False
    
    def rename_profile(self, profile_id: str, new_name: str) -> bool:
        profile = self.load_profile(profile_id)
        if not profile:
            return False
        
        old_path = self.get_save_path(profile_id)
        profile.name = new_name
        profile.id = new_name.lower().replace(' ', '_') + '_' + profile.id.split('_')[-1]
        new_path = self.get_save_path(profile.id)
        
        if old_path != new_path and os.path.exists(old_path):
            os.remove(old_path)
        
        return self.save_profile(profile)
    
    def apply_to_player(self, profile: ProfileData, player) -> None:
        player.name = profile.name
        player.character_class = profile.character_class
        player.level = profile.level
        player.xp = profile.xp
        player.xp_to_next = profile.xp_to_next
        player.gold = profile.gold
        
        player.maxhealth = profile.maxhealth
        player.health = profile.health
        player.attack = profile.attack
        player.defense = profile.defense
        player.mana = profile.mana
        player.maxmana = profile.maxmana
        player.accuracy = profile.accuracy
        player.speed = profile.speed
        player.crit_chance = profile.crit_chance
        player.mana_regen = profile.mana_regen
        
        player.stat_points = profile.stat_points
        player.base_maxhealth = profile.base_maxhealth
        player.base_attack = profile.base_attack
        player.base_defense = profile.base_defense
        player.base_mana = profile.base_mana
        player.base_accuracy = profile.base_accuracy
        player.base_speed = profile.base_speed
        player.base_crit_chance = profile.base_crit_chance
        player.base_mana_regen = profile.base_mana_regen
        
        player.inventory = profile.inventory
        player.equipment = profile.equipment
        player.skills = profile.skills
        player.completed_battles = profile.completed_battles
        player.total_damage_dealt = profile.total_damage_dealt
        player.total_damage_taken = profile.total_damage_taken
        player.total_healed = profile.total_healed
        player.critical_hits = profile.critical_hits
        player.enemies_defeated = profile.enemies_defeated
        player.achievements = profile.achievements
        player.quests_completed = profile.quests_completed
        player.playtime_seconds = profile.playtime_seconds
    
    def extract_from_player(self, player) -> ProfileData:
        return ProfileData(
            id=player.profile_id,
            name=player.name,
            character_class=player.character_class,
            level=player.level,
            xp=player.xp,
            xp_to_next=player.xp_to_next,
            gold=player.gold,
            maxhealth=player.maxhealth,
            health=player.health,
            attack=player.attack,
            defense=player.defense,
            mana=player.mana,
            maxmana=player.maxmana,
            accuracy=player.accuracy,
            speed=player.speed,
            crit_chance=player.crit_chance,
            mana_regen=player.mana_regen,
            stat_points=player.stat_points,
            base_maxhealth=player.base_maxhealth,
            base_attack=player.base_attack,
            base_defense=player.base_defense,
            base_mana=player.base_mana,
            base_accuracy=player.base_accuracy,
            base_speed=player.base_speed,
            base_crit_chance=player.base_crit_chance,
            base_mana_regen=player.base_mana_regen,
            inventory=player.inventory,
            equipment=player.equipment,
            skills=player.skills,
            completed_battles=player.completed_battles,
            total_damage_dealt=player.total_damage_dealt,
            total_damage_taken=player.total_damage_taken,
            total_healed=player.total_healed,
            critical_hits=player.critical_hits,
            enemies_defeated=player.enemies_defeated,
            achievements=player.achievements,
            quests_completed=player.quests_completed,
            created_at=player.created_at,
            last_played=datetime.now().isoformat(),
            playtime_seconds=player.playtime_seconds,
            save_version=SAVE_VERSION
        )