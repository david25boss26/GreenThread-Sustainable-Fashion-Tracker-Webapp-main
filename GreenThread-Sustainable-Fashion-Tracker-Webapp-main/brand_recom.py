import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

# Load data
def load_data(input_file):
    df = pd.read_excel(input_file)
    return df

# Preprocess data: select features, scale them, and perform clustering
def preprocess_and_cluster(df, num_clusters=5):
    feature_columns = ['carbon_footprint_mt_scaled', 'water_usage_liters_scaled', 
                       'waste_production_kg_scaled', 'product_lines_scaled', 
                       'average_price_usd_scaled', 'sustainability_score_scaled']
    
    # Ensure the columns are numeric and handle missing values
    df[feature_columns] = df[feature_columns].apply(pd.to_numeric, errors='coerce')
    df = df.dropna(subset=feature_columns)  # Drop rows with missing values in relevant columns
    
    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df['cluster'] = kmeans.fit_predict(df[feature_columns])
    
    return df, kmeans

# Find similar brands within the same cluster
def get_similar_brands(df, selected_brand, kmeans, num_similar=5):
    # Get the selected brand's data
    selected_brand_data = df[df['brand_name'] == selected_brand].iloc[0]
    selected_cluster = selected_brand_data['cluster']
    
    # Filter to only the brands in the same cluster
    same_cluster = df[df['cluster'] == selected_cluster]
    
    # Extract relevant scaled features for distance calculation
    selected_brand_features = np.array(selected_brand_data[['carbon_footprint_mt_scaled', 
                                                            'water_usage_liters_scaled', 
                                                            'waste_production_kg_scaled', 
                                                            'product_lines_scaled', 
                                                            'average_price_usd_scaled', 
                                                            'sustainability_score_scaled']])
    
    # Ensure the selected brand features are numeric and reshaped properly
    selected_brand_features = selected_brand_features.astype(np.float64).reshape(1, -1)
    
    # Calculate pairwise distances within the cluster
    distances = cdist(selected_brand_features, same_cluster[['carbon_footprint_mt_scaled', 
                                                             'water_usage_liters_scaled', 
                                                             'waste_production_kg_scaled', 
                                                             'product_lines_scaled', 
                                                             'average_price_usd_scaled', 
                                                             'sustainability_score_scaled']], 
                      metric='euclidean').flatten()
    
    # Get the indices of the closest brands
    similar_brands_indices = np.argsort(distances)[1:num_similar + 1]  # Exclude the selected brand itself
    similar_brands = same_cluster.iloc[similar_brands_indices][['brand_name']]
    similar_brands['distance'] = distances[similar_brands_indices]
    
    return similar_brands

# Visualize similar brands
def plot_similar_brands(similar_brands, selected_brand):
    plt.figure(figsize=(10, 6))
    plt.bar(similar_brands['brand_name'], similar_brands['distance'], color='skyblue')
    plt.xlabel('Brand')
    plt.ylabel('Distance')
    plt.title(f'Similar Brands to {selected_brand} in the Same Cluster')
    plt.xticks(rotation=45)
    plt.show()

# Main function to execute
if _name_ == "_main_":
    input_file = "oss_dataset_features.xlsx"
    
    # Load and preprocess data
    df = load_data(input_file)
    df, kmeans = preprocess_and_cluster(df, num_clusters=5)
    
    # Get similar brands for a selected brand
    selected_brand = "20Dresses"  # Example: Replace with the brand you're interested in
    similar_brands = get_similar_brands(df, selected_brand, kmeans, num_similar=5)
    print(f"Top similar brands to {selected_brand}:")
    print(similar_brands)
    
    # Plot similar brands
    plot_similar_brands(similar_brands, selected_brand)