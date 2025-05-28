# 🏀 NBA Game Analyzer

AI-powered NBA game analyzer that provides quarter-wise summaries, player performance clustering, and momentum shift detection using play-by-play data.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Sync all dependencies
uv sync

# Or install manually
uv add nba_api pandas numpy scikit-learn openai sentence-transformers streamlit plotly jupyter python-dotenv
```

### 2. Set Up Environment Variables
Create a `.env` file in the root directory:
```bash
# OpenAI API Key (required for LLM features)
OPENAI_API_KEY=your_openai_api_key_here

# Optional settings
OPENAI_MODEL=gpt-3.5-turbo
NBA_API_DELAY=0.6
CLUSTERING_N_CLUSTERS=3
CURRENT_SEASON=2024-25
```

### 3. Test Data Ingestion
```bash
# Test the data pipeline
uv run python test_ingestion.py

# Or test individual player stats
uv run python test.py
```

## 📁 Project Structure

```
nba_analyzer/
├── src/
│   ├── data/
│   │   ├── ingestion.py      # NBA API data fetching
│   │   └── processing.py     # Data cleaning/transformation
│   ├── analysis/
│   │   ├── clustering.py     # Player performance clustering
│   │   └── momentum.py       # Momentum shift detection
│   ├── llm/
│   │   ├── summarizer.py     # Quarter summaries
│   │   └── commentary.py     # Player commentary
│   └── utils/
│       └── helpers.py
├── notebooks/               # Jupyter notebooks for exploration
├── data/                   # Raw and processed data
├── config/                 # Configuration files
├── tests/                  # Unit tests
└── test_ingestion.py       # Test script
```

## 🎯 Features

### ✅ Implemented
- **Data Ingestion**: Fetch play-by-play, player stats, and box scores from NBA API
- **Rate Limiting**: Respectful API usage with configurable delays
- **Error Handling**: Robust error handling and logging

### 🔄 In Progress
- **Player Performance Clustering**: KMeans clustering for Hot/Cold/Average games
- **Quarter Summarization**: LLM-powered game summaries
- **Momentum Detection**: ML-based momentum shift detection

### 📋 Planned
- **Interactive Dashboard**: Streamlit UI for game analysis
- **Advanced Analytics**: Player impact metrics and contextual insights
- **Real-time Analysis**: Live game monitoring and analysis

## 🛠 Usage Examples

### Basic Game Analysis
```python
from src.data.ingestion import NBADataIngestion

# Initialize data ingestion
ingestion = NBADataIngestion()

# Get recent games
recent_games = ingestion.get_recent_games(days=3)

# Analyze a specific game
game_id = recent_games.iloc[0]['GAME_ID']
game_data = ingestion.get_game_data_complete(game_id)

print(f"Play-by-play events: {len(game_data['play_by_play'])}")
print(f"Player stats: {len(game_data['player_advanced'])}")
```

### Player Season Analysis
```python
# Analyze Nikola Jokić's season
jokic_stats = ingestion.get_player_game_log('203999', '2024-25')
print(f"Games played: {len(jokic_stats)}")
```

## 🔧 Configuration

Key configuration options in `config/config.py`:

- `OPENAI_API_KEY`: Your OpenAI API key for LLM features
- `NBA_API_DELAY`: Delay between NBA API calls (default: 0.6s)
- `CLUSTERING_N_CLUSTERS`: Number of performance clusters (default: 3)
- `CURRENT_SEASON`: NBA season to analyze (default: 2024-25)

## 📊 Data Sources

- **NBA API**: Official NBA statistics and play-by-play data
- **Player IDs**: Pre-configured for popular players (Jokić, LeBron, Curry, etc.)
- **Team IDs**: Major teams included for quick analysis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🆘 Troubleshooting

### Common Issues

1. **"uv not found"**: Make sure uv is installed and in your PATH
2. **NBA API errors**: Check your internet connection and API rate limits
3. **OpenAI errors**: Verify your API key is set correctly in `.env`

### Getting Help

- Check the logs for detailed error messages
- Run `test_ingestion.py` to verify data pipeline
- Open an issue on GitHub for bugs or feature requests