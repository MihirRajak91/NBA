from nba_api.stats.endpoints import playercareerstats

# Nikola Jokić 
career = playercareerstats.PlayerCareerStats(player_id='203999')

# Get career totals (usually the first dataset)
career_data = career.get_dict()

print("=== Nikola Jokić NBA Career Stats ===")
print()

# The API returns multiple result sets, we want the career totals
if 'resultSets' in career_data and len(career_data['resultSets']) > 0:
    headers = career_data['resultSets'][0]['headers']
    rows = career_data['resultSets'][0]['rowSet']
    
    for row in rows:
        print(f"Season: {row[1]}")  # Season
        print(f"Team: {row[4]}")    # Team
        print(f"Games: {row[5]}")   # GP
        print(f"Points: {row[26]}")  # PTS
        print(f"Rebounds: {row[20]}")  # REB  
        print(f"Assists: {row[21]}")   # AST
        print("-" * 30)
else:
    print("No data found") 