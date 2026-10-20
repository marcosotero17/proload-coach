# database.py
import json
import os
from datetime import datetime, timedelta
from config import TEAMS_DATA_FILE, DATA_DIR
import uuid
from pathlib import Path

class Database:
    def __init__(self):
        self.file_path = TEAMS_DATA_FILE
        self.ensure_data_file()
    
    def ensure_data_file(self):
        """Crea el archivo de datos si no existe"""
        if not os.path.exists(self.file_path):
            initial_data = {
                "teams": [],
                "last_updated": datetime.now().isoformat()
            }
            self.save(initial_data)
    
    def load(self):
        """Carga todos los datos"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"teams": [], "last_updated": datetime.now().isoformat()}
    
    def save(self, data):
        """Guarda todos los datos"""
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_team(self, team_name, coach_name, coach_password):
        """Crea un nuevo equipo"""
        data = self.load()
        
        team_id = str(uuid.uuid4())[:8]
        unique_code = str(uuid.uuid4())[:12]
        
        new_team = {
            "id": team_id,
            "name": team_name,
            "coach_name": coach_name,
            "coach_password": coach_password,  # En producción: hashear con bcrypt
            "unique_code": unique_code,
            "created_date": datetime.now().isoformat(),
            "players": [],
            "sessions": []
        }
        
        data["teams"].append(new_team)
        data["last_updated"] = datetime.now().isoformat()
        self.save(data)
        
        return team_id, unique_code
    
    def get_team_by_code(self, unique_code):
        """Obtiene equipo por código único"""
        data = self.load()
        for team in data["teams"]:
            if team["unique_code"] == unique_code:
                return team
        return None
    
    def get_team_by_id(self, team_id):
        """Obtiene equipo por ID"""
        data = self.load()
        for team in data["teams"]:
            if team["id"] == team_id:
                return team
        return None
    
    def get_all_teams(self):
        """Obtiene todos los equipos"""
        data = self.load()
        return data["teams"]
    
    def add_player_to_team(self, team_id, player_name):
        """Añade un jugador al equipo"""
        data = self.load()
        
        for team in data["teams"]:
            if team["id"] == team_id:
                player = {
                    "id": str(uuid.uuid4())[:8],
                    "name": player_name,
                    "added_date": datetime.now().isoformat(),
                    "active": True,
                    "anthropometry": [],
                    "performance_tests": []
                }
                team["players"].append(player)
                break
        
        data["last_updated"] = datetime.now().isoformat()
        self.save(data)
    
    def remove_player_from_team(self, team_id, player_id):
        """Marca un jugador como inactivo"""
        data = self.load()
        
        for team in data["teams"]:
            if team["id"] == team_id:
                for player in team["players"]:
                    if player["id"] == player_id:
                        player["active"] = False
                break
        
        data["last_updated"] = datetime.now().isoformat()
        self.save(data)
    
    def record_session(self, team_id, player_id, player_name, rpe, duration_minutes):
        """Registra una sesión de entrenamiento"""
        data = self.load()
        
        for team in data["teams"]:
            if team["id"] == team_id:
                session = {
                    "id": str(uuid.uuid4())[:8],
                    "player_id": player_id,
                    "player_name": player_name,
                    "date": datetime.now().isoformat(),
                    "rpe": rpe,
                    "duration_minutes": duration_minutes,
                    "session_load": rpe * duration_minutes
                }
                team["sessions"].append(session)
                break
        
        data["last_updated"] = datetime.now().isoformat()
        self.save(data)
    
    def get_player_sessions(self, team_id, player_id, days=28):
        """Obtiene las sesiones de un jugador en los últimos N días"""
        data = self.load()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        sessions = []
        for team in data["teams"]:
            if team["id"] == team_id:
                for session in team["sessions"]:
                    if session["player_id"] == player_id:
                        session_date = datetime.fromisoformat(session["date"])
                        if session_date >= cutoff_date:
                            sessions.append(session)
        
        return sorted(sessions, key=lambda x: x["date"])
    
    def add_anthropometry(self, team_id, player_id, data_point):
        """Añade datos antropométricos"""
        data = self.load()
        
        for team in data["teams"]:
            if team["id"] == team_id:
                for player in team["players"]:
                    if player["id"] == player_id:
                        anthro = {
                            "date": datetime.now().isoformat(),
                            "weight": data_point.get("weight"),
                            "height": data_point.get("height"),
                            "skinfolds": data_point.get("skinfolds"),  # dict
                            "notes": data_point.get("notes", "")
                        }
                        player["anthropometry"].append(anthro)
                break
        
        data["last_updated"] = datetime.now().isoformat()
        self.save(data)
    
    def add_performance_test(self, team_id, player_id, test_data):
        """Añade resultados de tests de rendimiento"""
        data = self.load()
        
        for team in data["teams"]:
            if team["id"] == team_id:
                for player in team["players"]:
                    if player["id"] == player_id:
                        test = {
                            "date": datetime.now().isoformat(),
                            "test_name": test_data.get("test_name"),
                            "value": test_data.get("value"),
                            "unit": test_data.get("unit"),
                            "notes": test_data.get("notes", "")
                        }
                        player["performance_tests"].append(test)
                break
        
        data["last_updated"] = datetime.now().isoformat()
        self.save(data)
