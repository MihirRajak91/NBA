"""
Player Performance Clustering Module

This module implements ML clustering to classify player game performances into:
- 🔥 Hot Game (exceptional performance)
- ❄️ Cold Game (below average performance)  
- 🟰 Average Game (typical performance)
"""

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class PlayerPerformanceClusterer:
    """Clusters player game performances using KMeans"""
    
    def __init__(self, n_clusters: int = 3, random_state: int = 42):
        """
        Initialize the clusterer
        
        Args:
            n_clusters: Number of clusters (default: 3 for Hot/Average/Cold)
            random_state: Random state for reproducibility
        """
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
        self.feature_columns = []
        self.cluster_labels = {}
        self.is_fitted = False
    
    def extract_features(self, game_log_df: pd.DataFrame) -> pd.DataFrame:
        """
        Extract relevant features for clustering
        
        Args:
            game_log_df: Player game log DataFrame from NBA API
            
        Returns:
            DataFrame with extracted features
        """
        # Core performance features
        features = pd.DataFrame()
        
        # Basic stats
        features['PTS'] = game_log_df['PTS']
        features['REB'] = game_log_df['REB'] 
        features['AST'] = game_log_df['AST']
        features['STL'] = game_log_df['STL']
        features['BLK'] = game_log_df['BLK']
        features['TOV'] = game_log_df['TOV']
        
        # Shooting efficiency
        features['FG_PCT'] = game_log_df['FG_PCT'].fillna(0)
        features['FG3_PCT'] = game_log_df['FG3_PCT'].fillna(0)
        features['FT_PCT'] = game_log_df['FT_PCT'].fillna(0)
        
        # Advanced metrics
        features['PLUS_MINUS'] = game_log_df['PLUS_MINUS']
        
        # Game impact score (custom metric)
        features['GAME_IMPACT'] = (
            features['PTS'] * 1.0 +
            features['REB'] * 1.2 +
            features['AST'] * 1.5 +
            features['STL'] * 2.0 +
            features['BLK'] * 2.0 -
            features['TOV'] * 1.0 +
            features['PLUS_MINUS'] * 0.5
        )
        
        # Efficiency metrics
        features['TRUE_SHOOTING'] = features['PTS'] / (2 * (game_log_df['FGA'] + 0.44 * game_log_df['FTA']))
        features['TRUE_SHOOTING'] = features['TRUE_SHOOTING'].fillna(0)
        
        # Store feature columns for later use
        self.feature_columns = features.columns.tolist()
        
        # Add game metadata
        features['GAME_ID'] = game_log_df['Game_ID']
        features['GAME_DATE'] = game_log_df['GAME_DATE']
        features['MATCHUP'] = game_log_df['MATCHUP']
        features['WL'] = game_log_df['WL']
        
        return features
    
    def fit_predict(self, features_df: pd.DataFrame) -> pd.DataFrame:
        """
        Fit the clustering model and predict clusters
        
        Args:
            features_df: DataFrame with extracted features
            
        Returns:
            DataFrame with cluster assignments
        """
        # Separate features from metadata
        feature_data = features_df[self.feature_columns]
        metadata = features_df[['GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL']]
        
        # Handle missing values
        feature_data = feature_data.fillna(feature_data.mean())
        
        # Scale features
        scaled_features = self.scaler.fit_transform(feature_data)
        
        # Fit KMeans
        cluster_labels = self.kmeans.fit_predict(scaled_features)
        
        # Calculate silhouette score
        if len(np.unique(cluster_labels)) > 1:
            silhouette_avg = silhouette_score(scaled_features, cluster_labels)
            logger.info(f"Silhouette Score: {silhouette_avg:.3f}")
        
        # Assign meaningful labels based on cluster centers
        self._assign_cluster_meanings(scaled_features, cluster_labels, feature_data)
        
        # Create results DataFrame
        results_df = metadata.copy()
        results_df['cluster'] = cluster_labels
        results_df['performance_label'] = [self.cluster_labels[c] for c in cluster_labels]
        
        # Add key stats for interpretation
        results_df['PTS'] = features_df['PTS']
        results_df['REB'] = features_df['REB']
        results_df['AST'] = features_df['AST']
        results_df['GAME_IMPACT'] = features_df['GAME_IMPACT']
        results_df['PLUS_MINUS'] = features_df['PLUS_MINUS']
        
        self.is_fitted = True
        return results_df
    
    def _assign_cluster_meanings(self, scaled_features: np.ndarray, cluster_labels: np.ndarray, 
                                original_features: pd.DataFrame):
        """
        Assign meaningful labels to clusters based on performance levels
        """
        cluster_centers = self.kmeans.cluster_centers_
        
        # Calculate average game impact for each cluster
        cluster_impacts = {}
        for i in range(self.n_clusters):
            cluster_mask = cluster_labels == i
            avg_impact = original_features.loc[cluster_mask, 'GAME_IMPACT'].mean()
            cluster_impacts[i] = avg_impact
        
        # Sort clusters by impact score
        sorted_clusters = sorted(cluster_impacts.items(), key=lambda x: x[1])
        
        # Assign labels based on performance level
        if self.n_clusters == 3:
            self.cluster_labels = {
                sorted_clusters[0][0]: "❄️ Cold Game",    # Lowest impact
                sorted_clusters[1][0]: "🟰 Average Game", # Middle impact  
                sorted_clusters[2][0]: "🔥 Hot Game"      # Highest impact
            }
        else:
            # For other cluster numbers, use generic labels
            for i, (cluster_id, _) in enumerate(sorted_clusters):
                self.cluster_labels[cluster_id] = f"Cluster {i+1}"
    
    def analyze_clusters(self, results_df: pd.DataFrame) -> Dict:
        """
        Analyze cluster characteristics and provide insights
        
        Args:
            results_df: DataFrame with cluster assignments
            
        Returns:
            Dictionary with cluster analysis
        """
        analysis = {}
        
        for cluster_id, label in self.cluster_labels.items():
            cluster_data = results_df[results_df['cluster'] == cluster_id]
            
            analysis[label] = {
                'count': len(cluster_data),
                'percentage': len(cluster_data) / len(results_df) * 100,
                'avg_stats': {
                    'PTS': cluster_data['PTS'].mean(),
                    'REB': cluster_data['REB'].mean(),
                    'AST': cluster_data['AST'].mean(),
                    'PLUS_MINUS': cluster_data['PLUS_MINUS'].mean(),
                    'GAME_IMPACT': cluster_data['GAME_IMPACT'].mean()
                },
                'win_rate': (cluster_data['WL'] == 'W').mean() * 100,
                'sample_games': cluster_data.head(3)[['GAME_DATE', 'MATCHUP', 'PTS', 'REB', 'AST']].to_dict('records')
            }
        
        return analysis
    
    def get_performance_summary(self, results_df: pd.DataFrame, player_name: str = "Player") -> str:
        """
        Generate a text summary of player performance clustering
        
        Args:
            results_df: DataFrame with cluster assignments
            player_name: Name of the player
            
        Returns:
            Formatted summary string
        """
        analysis = self.analyze_clusters(results_df)
        
        summary = f"\n🏀 {player_name} Performance Analysis ({len(results_df)} games)\n"
        summary += "=" * 60 + "\n\n"
        
        for label, stats in analysis.items():
            summary += f"{label}:\n"
            summary += f"  📊 {stats['count']} games ({stats['percentage']:.1f}%)\n"
            summary += f"  📈 Avg: {stats['avg_stats']['PTS']:.1f} pts, {stats['avg_stats']['REB']:.1f} reb, {stats['avg_stats']['AST']:.1f} ast\n"
            summary += f"  📈 +/-: {stats['avg_stats']['PLUS_MINUS']:.1f}, Impact: {stats['avg_stats']['GAME_IMPACT']:.1f}\n"
            summary += f"  🏆 Win Rate: {stats['win_rate']:.1f}%\n\n"
        
        return summary


def analyze_player_performance(game_log_df: pd.DataFrame, player_name: str = "Player") -> Tuple[pd.DataFrame, Dict, str]:
    """
    Complete player performance analysis pipeline
    
    Args:
        game_log_df: Player game log DataFrame
        player_name: Name of the player
        
    Returns:
        Tuple of (results_df, analysis_dict, summary_text)
    """
    # Initialize clusterer
    clusterer = PlayerPerformanceClusterer()
    
    # Extract features
    features_df = clusterer.extract_features(game_log_df)
    
    # Fit and predict
    results_df = clusterer.fit_predict(features_df)
    
    # Analyze results
    analysis = clusterer.analyze_clusters(results_df)
    summary = clusterer.get_performance_summary(results_df, player_name)
    
    return results_df, analysis, summary


# Example usage
if __name__ == "__main__":
    import sys
    import os
    sys.path.append('..')
    
    from data.ingestion import NBADataIngestion
    
    # Get Jokić's game log
    ingestion = NBADataIngestion()
    jokic_log = ingestion.get_player_game_log('203999', '2024-25')
    
    if not jokic_log.empty:
        # Analyze performance
        results, analysis, summary = analyze_player_performance(jokic_log, "Nikola Jokić")
        
        print(summary)
        
        # Show some hot and cold games
        hot_games = results[results['performance_label'] == '🔥 Hot Game'].head(3)
        cold_games = results[results['performance_label'] == '❄️ Cold Game'].head(3)
        
        print("🔥 Hottest Games:")
        for _, game in hot_games.iterrows():
            print(f"  {game['GAME_DATE']}: {game['PTS']} pts, {game['REB']} reb, {game['AST']} ast vs {game['MATCHUP']}")
        
        print("\n❄️ Coldest Games:")
        for _, game in cold_games.iterrows():
            print(f"  {game['GAME_DATE']}: {game['PTS']} pts, {game['REB']} reb, {game['AST']} ast vs {game['MATCHUP']}")
    else:
        print("No game log data available") 