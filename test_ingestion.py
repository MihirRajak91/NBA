"""
Test script for NBA data ingestion
Run this to verify the data pipeline is working
"""

import sys
import os
sys.path.append('src')

from data.ingestion import NBADataIngestion

def test_data_ingestion():
    """Test the basic data ingestion functionality"""
    print("🏀 Testing NBA Data Ingestion...")
    
    # Initialize ingestion
    ingestion = NBADataIngestion()
    
    # Test 1: Get recent games (try longer period)
    print("\n1. Fetching recent games...")
    recent_games = ingestion.get_recent_games(days=30)  # Extended to 30 days
    
    if not recent_games.empty:
        print(f"✅ Found {len(recent_games)} recent games")
        
        # Show sample games
        print("\nRecent games:")
        for _, game in recent_games.head(3).iterrows():
            print(f"  {game['GAME_DATE'].strftime('%Y-%m-%d')}: {game['TEAM_NAME']} vs {game['MATCHUP']}")
        
        # Test 2: Get play-by-play for most recent game
        print(f"\n2. Testing play-by-play data...")
        latest_game_id = recent_games.iloc[0]['GAME_ID']
        print(f"Fetching data for game: {latest_game_id}")
        
        pbp_data = ingestion.get_play_by_play(latest_game_id)
        
        if not pbp_data.empty:
            print(f"✅ Successfully fetched {len(pbp_data)} play-by-play events")
            
            # Show sample events
            print("\nSample play-by-play events:")
            for _, event in pbp_data.head(5).iterrows():
                period = event.get('PERIOD', 'N/A')
                time_remaining = event.get('PCTIMESTRING', 'N/A')
                description = event.get('HOMEDESCRIPTION', '') or event.get('VISITORDESCRIPTION', '') or event.get('NEUTRALDESCRIPTION', '')
                if description:
                    print(f"  Q{period} {time_remaining}: {description}")
        else:
            print("❌ No play-by-play data found")
        
        # Test 3: Get advanced box score
        print(f"\n3. Testing advanced box score...")
        player_stats, team_stats = ingestion.get_box_score_advanced(latest_game_id)
        
        if not player_stats.empty:
            print(f"✅ Successfully fetched advanced stats for {len(player_stats)} players")
            
            # Show top performers
            if 'PTS' in player_stats.columns:
                top_scorers = player_stats.nlargest(3, 'PTS')[['PLAYER_NAME', 'PTS', 'REB', 'AST']]
                print("\nTop scorers:")
                for _, player in top_scorers.iterrows():
                    print(f"  {player['PLAYER_NAME']}: {player['PTS']} pts, {player['REB']} reb, {player['AST']} ast")
        else:
            print("❌ No advanced box score data found")
            
    else:
        print("❌ No recent games found in the last 30 days")
        print("🔄 Testing with a known game ID instead...")
        
        # Fallback: Test with a known game ID from earlier this season
        # This is a Lakers vs Celtics game from earlier in the season
        test_game_id = "0022400001"  # Example game ID
        
        print(f"\n2. Testing play-by-play data with game {test_game_id}...")
        pbp_data = ingestion.get_play_by_play(test_game_id)
        
        if not pbp_data.empty:
            print(f"✅ Successfully fetched {len(pbp_data)} play-by-play events")
            
            # Show sample events
            print("\nSample play-by-play events:")
            for _, event in pbp_data.head(5).iterrows():
                period = event.get('PERIOD', 'N/A')
                time_remaining = event.get('PCTIMESTRING', 'N/A')
                description = event.get('HOMEDESCRIPTION', '') or event.get('VISITORDESCRIPTION', '') or event.get('NEUTRALDESCRIPTION', '')
                if description:
                    print(f"  Q{period} {time_remaining}: {description}")
        else:
            print("❌ No play-by-play data found for test game")
    
    # Test 4: Player game log (this should work regardless)
    print(f"\n4. Testing player game log...")
    print("Fetching Nikola Jokić's season stats...")
    
    jokic_stats = ingestion.get_player_game_log('203999', '2024-25')
    
    if not jokic_stats.empty:
        print(f"✅ Successfully fetched {len(jokic_stats)} games for Jokić")
        
        # Show recent games
        print("\nJokić's recent games:")
        for _, game in jokic_stats.head(3).iterrows():
            print(f"  {game['GAME_DATE']}: {game['PTS']} pts, {game['REB']} reb, {game['AST']} ast vs {game['MATCHUP']}")
    else:
        print("❌ No player game log data found")
    
    print("\n🎯 Data ingestion test completed!")

if __name__ == "__main__":
    test_data_ingestion() 