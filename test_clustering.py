"""
Test script for Player Performance Clustering
Run this to see Jokić's games classified as Hot/Cold/Average
"""

import sys
import os
sys.path.append('src')

from data.ingestion import NBADataIngestion
from analysis.clustering import analyze_player_performance

def test_player_clustering():
    """Test the player performance clustering system"""
    print("🔥 Testing Player Performance Clustering...")
    
    # Initialize data ingestion
    ingestion = NBADataIngestion()
    
    # Get Jokić's game log
    print("\n📊 Fetching Nikola Jokić's 2024-25 season data...")
    jokic_log = ingestion.get_player_game_log('203999', '2024-25')
    
    if not jokic_log.empty:
        print(f"✅ Found {len(jokic_log)} games for Jokić")
        
        # Run clustering analysis
        print("\n🤖 Running ML clustering analysis...")
        results, analysis, summary = analyze_player_performance(jokic_log, "Nikola Jokić")
        
        # Print the summary
        print(summary)
        
        # Show examples of each performance type
        print("🔥 HOTTEST GAMES:")
        print("-" * 50)
        hot_games = results[results['performance_label'] == '🔥 Hot Game'].nlargest(5, 'GAME_IMPACT')
        for _, game in hot_games.iterrows():
            print(f"  {game['GAME_DATE']}: {game['PTS']} pts, {game['REB']} reb, {game['AST']} ast")
            print(f"    vs {game['MATCHUP']} | Impact: {game['GAME_IMPACT']:.1f} | +/-: {game['PLUS_MINUS']}")
        
        print("\n❄️ COLDEST GAMES:")
        print("-" * 50)
        cold_games = results[results['performance_label'] == '❄️ Cold Game'].nsmallest(5, 'GAME_IMPACT')
        for _, game in cold_games.iterrows():
            print(f"  {game['GAME_DATE']}: {game['PTS']} pts, {game['REB']} reb, {game['AST']} ast")
            print(f"    vs {game['MATCHUP']} | Impact: {game['GAME_IMPACT']:.1f} | +/-: {game['PLUS_MINUS']}")
        
        print("\n🟰 AVERAGE GAMES (Sample):")
        print("-" * 50)
        avg_games = results[results['performance_label'] == '🟰 Average Game'].head(5)
        for _, game in avg_games.iterrows():
            print(f"  {game['GAME_DATE']}: {game['PTS']} pts, {game['REB']} reb, {game['AST']} ast")
            print(f"    vs {game['MATCHUP']} | Impact: {game['GAME_IMPACT']:.1f} | +/-: {game['PLUS_MINUS']}")
        
        # Performance insights
        print("\n📈 KEY INSIGHTS:")
        print("-" * 50)
        
        # Win rate by performance type
        for label in ['🔥 Hot Game', '🟰 Average Game', '❄️ Cold Game']:
            cluster_data = results[results['performance_label'] == label]
            win_rate = (cluster_data['WL'] == 'W').mean() * 100
            print(f"  {label}: {win_rate:.1f}% win rate ({len(cluster_data)} games)")
        
        # Best and worst months
        results['MONTH'] = pd.to_datetime(results['GAME_DATE']).dt.strftime('%B')
        monthly_performance = results.groupby('MONTH')['GAME_IMPACT'].mean().sort_values(ascending=False)
        print(f"\n  🏆 Best month: {monthly_performance.index[0]} (avg impact: {monthly_performance.iloc[0]:.1f})")
        print(f"  📉 Worst month: {monthly_performance.index[-1]} (avg impact: {monthly_performance.iloc[-1]:.1f})")
        
        # Save results for further analysis
        results.to_csv('data/jokic_performance_clusters.csv', index=False)
        print(f"\n💾 Results saved to 'data/jokic_performance_clusters.csv'")
        
    else:
        print("❌ No game log data found for Jokić")
    
    print("\n🎯 Clustering analysis completed!")

if __name__ == "__main__":
    import pandas as pd
    test_player_clustering() 