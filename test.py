from nba_api.stats.endpoints import playergamelog

# Nikola Jokić - 2024-25 season game logs
game_log = playergamelog.PlayerGameLog(player_id='203999', season='2024-25')

# Get game log data
game_data = game_log.get_dict()

print("=== Nikola Jokić 2024-25 Season Game-by-Game Stats ===")
print()

# The API returns game log data
if 'resultSets' in game_data and len(game_data['resultSets']) > 0:
    headers = game_data['resultSets'][0]['headers']
    rows = game_data['resultSets'][0]['rowSet']
    
    print(f"{'Date':<12} {'Opp':<5} {'MIN':<5} {'PTS':<4} {'REB':<4} {'AST':<4} {'FG%':<6} {'Result':<6}")
    print("-" * 60)
    
    for row in rows:
        game_date = row[2][:10]  # Game date (first 10 chars)
        matchup = row[3][-3:]    # Opponent (last 3 chars)
        minutes = row[8]         # Minutes played
        points = row[24]         # Points
        rebounds = row[18]       # Total rebounds
        assists = row[19]        # Assists
        fg_pct = f"{row[11]:.1%}" if row[11] else "0.0%"  # FG%
        wl = row[4]              # Win/Loss
        
        print(f"{game_date:<12} {matchup:<5} {minutes:<5} {points:<4} {rebounds:<4} {assists:<4} {fg_pct:<6} {wl:<6}")
        
    print(f"\nTotal games played: {len(rows)}")
else:
    print("No data found")