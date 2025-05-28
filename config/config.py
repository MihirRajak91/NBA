"""
Configuration settings for NBA Game Analyzer
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for NBA Game Analyzer"""
    
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # NBA API settings
    NBA_API_DELAY = float(os.getenv('NBA_API_DELAY', '0.6'))  # Delay between API calls
    
    # Data storage settings
    DATA_DIR = os.getenv('DATA_DIR', 'data')
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'True').lower() == 'true'
    
    # ML Model settings
    CLUSTERING_N_CLUSTERS = int(os.getenv('CLUSTERING_N_CLUSTERS', '3'))
    RANDOM_STATE = int(os.getenv('RANDOM_STATE', '42'))
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Current NBA season
    CURRENT_SEASON = os.getenv('CURRENT_SEASON', '2024-25')
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present"""
        if not cls.OPENAI_API_KEY:
            print("⚠️  Warning: OPENAI_API_KEY not set. LLM features will not work.")
            print("   Add your OpenAI API key to a .env file:")
            print("   OPENAI_API_KEY=your_api_key_here")
        
        return True

# Player IDs for common players (for testing)
PLAYER_IDS = {
    'nikola_jokic': '203999',
    'lebron_james': '2544',
    'stephen_curry': '201939',
    'kevin_durant': '201142',
    'giannis_antetokounmpo': '203507',
    'luka_doncic': '1629029',
    'jayson_tatum': '1628369',
    'joel_embiid': '203954'
}

# Team IDs for common teams
TEAM_IDS = {
    'lakers': '1610612747',
    'celtics': '1610612738',
    'warriors': '1610612744',
    'nuggets': '1610612743',
    'heat': '1610612748',
    'bucks': '1610612749'
} 