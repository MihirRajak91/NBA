"""
NBA Data Ingestion Module

This module handles fetching data from the NBA API including:
- Play-by-play data
- Player game logs
- Box scores and advanced stats
"""

from typing import Dict, List, Optional, Tuple
import pandas as pd
from nba_api.stats.endpoints import (
    playbyplayv2, 
    playergamelog, 
    boxscoreadvancedv2,
    leaguegamefinder
)
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NBADataIngestion:
    """Main class for fetching NBA data from the API"""
    
    def __init__(self, delay: float = 0.6):
        """
        Initialize the data ingestion class
        
        Args:
            delay: Delay between API calls to respect rate limits
        """
        self.delay = delay
    
    def get_recent_games(self, team_id: Optional[str] = None, days: int = 7) -> pd.DataFrame:
        """
        Get recent games from the last N days
        
        Args:
            team_id: Specific team ID (optional)
            days: Number of days to look back
            
        Returns:
            DataFrame with recent games
        """
        try:
            finder = leaguegamefinder.LeagueGameFinder(
                team_id_nullable=team_id,
                season_nullable='2024-25',
                season_type_nullable='Regular Season'
            )
            games_df = finder.get_data_frames()[0]
            
            # Convert game date and filter recent games
            games_df['GAME_DATE'] = pd.to_datetime(games_df['GAME_DATE'])
            recent_date = pd.Timestamp.now() - pd.Timedelta(days=days)
            recent_games = games_df[games_df['GAME_DATE'] >= recent_date]
            
            logger.info(f"Found {len(recent_games)} recent games")
            return recent_games
            
        except Exception as e:
            logger.error(f"Error fetching recent games: {e}")
            return pd.DataFrame()
    
    def get_play_by_play(self, game_id: str) -> pd.DataFrame:
        """
        Get play-by-play data for a specific game
        
        Args:
            game_id: NBA game ID
            
        Returns:
            DataFrame with play-by-play data
        """
        try:
            time.sleep(self.delay)  # Rate limiting
            
            pbp = playbyplayv2.PlayByPlayV2(game_id=game_id)
            pbp_df = pbp.get_data_frames()[0]
            
            logger.info(f"Fetched {len(pbp_df)} play-by-play events for game {game_id}")
            return pbp_df
            
        except Exception as e:
            logger.error(f"Error fetching play-by-play for game {game_id}: {e}")
            return pd.DataFrame()
    
    def get_player_game_log(self, player_id: str, season: str = '2024-25') -> pd.DataFrame:
        """
        Get player game log for a season
        
        Args:
            player_id: NBA player ID
            season: Season in format 'YYYY-YY'
            
        Returns:
            DataFrame with player game logs
        """
        try:
            time.sleep(self.delay)  # Rate limiting
            
            game_log = playergamelog.PlayerGameLog(
                player_id=player_id,
                season=season
            )
            log_df = game_log.get_data_frames()[0]
            
            logger.info(f"Fetched {len(log_df)} games for player {player_id}")
            return log_df
            
        except Exception as e:
            logger.error(f"Error fetching game log for player {player_id}: {e}")
            return pd.DataFrame()
    
    def get_box_score_advanced(self, game_id: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Get advanced box score data for a game
        
        Args:
            game_id: NBA game ID
            
        Returns:
            Tuple of (player_stats, team_stats) DataFrames
        """
        try:
            time.sleep(self.delay)  # Rate limiting
            
            box_score = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id)
            data_frames = box_score.get_data_frames()
            
            player_stats = data_frames[0]  # Player advanced stats
            team_stats = data_frames[1]    # Team advanced stats
            
            logger.info(f"Fetched advanced box score for game {game_id}")
            return player_stats, team_stats
            
        except Exception as e:
            logger.error(f"Error fetching advanced box score for game {game_id}: {e}")
            return pd.DataFrame(), pd.DataFrame()
    
    def get_game_data_complete(self, game_id: str) -> Dict[str, pd.DataFrame]:
        """
        Get complete game data including play-by-play and advanced stats
        
        Args:
            game_id: NBA game ID
            
        Returns:
            Dictionary with all game data
        """
        logger.info(f"Fetching complete data for game {game_id}")
        
        # Get all data
        pbp_df = self.get_play_by_play(game_id)
        player_advanced, team_advanced = self.get_box_score_advanced(game_id)
        
        return {
            'play_by_play': pbp_df,
            'player_advanced': player_advanced,
            'team_advanced': team_advanced,
            'game_id': game_id
        }


# Example usage and testing
if __name__ == "__main__":
    # Initialize ingestion
    ingestion = NBADataIngestion()
    
    # Get recent games
    recent_games = ingestion.get_recent_games(days=3)
    
    if not recent_games.empty:
        # Get data for the most recent game
        latest_game_id = recent_games.iloc[0]['GAME_ID']
        print(f"Analyzing game: {latest_game_id}")
        
        # Get complete game data
        game_data = ingestion.get_game_data_complete(latest_game_id)
        
        print(f"Play-by-play events: {len(game_data['play_by_play'])}")
        print(f"Player stats: {len(game_data['player_advanced'])}")
    else:
        print("No recent games found") 