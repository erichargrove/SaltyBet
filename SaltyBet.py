#!/usr/bin/env python3
"""
Salty Bet - A simple Python program for betting on fake wrestling matches.
Each user starts with $1000 (WrestleBucks) and can bet on wrestling matches.
"""

import json
import os
from pathlib import Path

class User:
    """Represents a user in the Salty Bet system."""
    
    def __init__(self, name):
        self.name = name
        self.wrestlebucks = 1000  # Starting amount
        self.wins = 0
        self.losses = 0
    
    def place_bet(self, amount):
        """Place a bet and deduct from WrestleBucks."""
        if amount > self.wrestlebucks:
            return False, "Insufficient WrestleBucks!"
        if amount <= 0:
            return False, "Bet amount must be positive!"
        
        self.wrestlebucks -= amount
        return True, f"Bet of {amount} WrestleBucks placed!"
    
    def win_bet(self, amount):
        """Process a winning bet (double the bet amount)."""
        winnings = amount * 2
        self.wrestlebucks += winnings
        self.wins += 1
        return winnings
    
    def lose_bet(self):
        """Process a losing bet (no payout)."""
        self.losses += 1
    
    
    def get_stats(self):
        """Get user statistics."""
        total_games = self.wins + self.losses
        win_rate = (self.wins / total_games * 100) if total_games > 0 else 0
        return {
            'name': self.name,
            'wrestlebucks': self.wrestlebucks,
            'wins': self.wins,
            'losses': self.losses,
            'win_rate': win_rate
        }
    
    def to_dict(self):
        """Convert user data to dictionary for JSON serialization."""
        return {
            'name': self.name,
            'wrestlebucks': self.wrestlebucks,
            'wins': self.wins,
            'losses': self.losses
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create User instance from dictionary data."""
        user = cls(data['name'])
        user.wrestlebucks = data['wrestlebucks']
        user.wins = data['wins']
        user.losses = data['losses']
        return user

class SaltyBet:
    """Main Salty Bet application."""
    
    def __init__(self, data_file=None):
        self.users = {}
        self.current_match = None
        self.bets = {}  # {user_name: {'wrestler': str, 'amount': int}}
        
        # Set up data file path with proper permissions handling
        if data_file is None:
            self.data_file = self._get_safe_data_file_path()
        else:
            self.data_file = data_file
            
        self.load_users_from_file()
    
    def _get_safe_data_file_path(self):
        """Get a safe path for the data file with proper permissions."""
        # Get the directory where the script is located
        script_dir = Path(__file__).parent
        
        # Try multiple locations in order of preference
        possible_paths = [
            # 1. Script directory (project root when run from File Explorer)
            script_dir / "saltybet_users.json",
            # 2. Current working directory (when run from terminal/Cursor)
            Path.cwd() / "saltybet_users.json",
            # 3. User's home directory (fallback)
            Path.home() / "saltybet_users.json",
            # 4. Temp file in script directory (last resort)
            script_dir / "temp_saltybet_users.json"
        ]
        
        for path in possible_paths:
            try:
                # Test if we can write to this location
                test_file = path.parent / f".test_write_{path.name}"
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)  # Clean up test file
                return str(path)
            except (PermissionError, OSError):
                continue
        
        # If all else fails, use script directory (will show error later)
        return str(script_dir / "saltybet_users.json")
    
    def save_users_to_file(self):
        """Save all users to JSON file."""
        try:
            users_data = {}
            for name, user in self.users.items():
                users_data[name] = user.to_dict()
            
            # Ensure directory exists
            data_path = Path(self.data_file)
            data_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.data_file, 'w') as f:
                json.dump(users_data, f, indent=2)
            print(f"User data saved to {self.data_file}")
            return True
        except PermissionError:
            print(f"Permission denied: Cannot write to {self.data_file}")
            print("Try running the application with appropriate permissions or choose a different location.")
            return False
        except OSError as e:
            print(f"File system error saving user data: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error saving user data: {e}")
            return False
    
    def load_users_from_file(self):
        """Load users from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    users_data = json.load(f)
                
                for name, user_data in users_data.items():
                    self.users[name] = User.from_dict(user_data)
                
                print(f"Loaded {len(self.users)} users from {self.data_file}")
            else:
                print(f"No existing user data found at {self.data_file}. Starting fresh!")
        except PermissionError:
            print(f"Permission denied: Cannot read from {self.data_file}")
            print("Starting with empty user list.")
        except FileNotFoundError:
            print(f"Data file not found: {self.data_file}")
            print("Starting with empty user list.")
        except json.JSONDecodeError as e:
            print(f"Invalid JSON format in {self.data_file}: {e}")
            print("Starting with empty user list.")
        except Exception as e:
            print(f"Error loading user data: {e}")
            print("Starting with empty user list.")
    
    def get_data_file_location(self):
        """Get the current data file location."""
        return self.data_file
    
    def add_user(self, name):
        """Add a new user to the system."""
        if name in self.users:
            print(f"User '{name}' already exists!")
            return False
        
        self.users[name] = User(name)
        print(f"User '{name}' added with 1000 WrestleBucks!")
        self.save_users_to_file()
        return True
