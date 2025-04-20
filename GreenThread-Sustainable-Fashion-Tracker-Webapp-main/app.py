import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from functools import wraps

app = Flask(__name__)

# MongoDB connection
client = MongoClient('localhost', 27017)
db = client['sustainable_brands']
collection = db['brands']

def load_data_from_mongodb():
    cursor = collection.find({})
    df = pd.DataFrame(list(cursor))
    return df

# Load data
df = load_data_from_mongodb()

def with_brands(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # Get all brands for the navbar dropdown
            brands = list(collection.find({}, {'brand_name': 1, '_id': 0}).sort('brand_name', 1))
        except Exception as e:
            print(f"Error fetching brands: {str(e)}")
            brands = []
        
        # Add brands to kwargs
        kwargs['brands'] = brands
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@with_brands
def index(brands=[]):
    return render_template('index.html', brands=brands)

@app.route('/api/brand/<brand_name>')
def get_brand_api(brand_name):
    try:
        # Find brand by exact name match
        brand = collection.find_one({'brand_name': brand_name})
        
        if brand:
            # Convert ObjectId to string and clean up the data
            brand_data = {
                'brand_name': brand['brand_name'],
                'sustainability_score': float(brand['sustainability_score']),
                'carbon_footprint_mt': float(brand['carbon_footprint_mt']),
                'water_usage_liters': float(brand['water_usage_liters']),
                'product_lines': int(brand['product_lines']),
                'average_price_usd': float(brand['average_price_usd']),
                'market_trend': brand.get('market_trend', 'N/A'),
                'certifications': brand.get('certifications', 'N/A'),
                'material_type': brand.get('material_type', 'N/A')
            }
            return jsonify(brand_data)
        return jsonify({'error': 'Brand not found'}), 404
        
    except Exception as e:
        print(f"Error in get_brand_api: {str(e)}")  # Debug print
        return jsonify({'error': 'Error loading brand data'}), 500

@app.route('/api/similar-brands/<brand_name>')
def get_similar_brands_api(brand_name):
    try:
        features = [
            'sustainability_score',
            'carbon_footprint_mt',
            'water_usage_liters',
            'product_lines',
            'average_price_usd'
        ]
        
        brand_data = df[df['brand_name'] == brand_name][features].values
        all_brands_data = df[features].values
        
        similarities = cosine_similarity(brand_data, all_brands_data)[0]
        similar_indices = similarities.argsort()[::-1][1:6]
        
        similar_brands = []
        for idx in similar_indices:
            brand = df.iloc[idx]
            similar_brands.append({
                'brand_name': brand['brand_name'],
                'sustainability_score': float(brand['sustainability_score'])
            })
        
        return jsonify(similar_brands)
    except Exception as e:
        print(f"Error in get_similar_brands_api: {str(e)}")
        return jsonify([])

@app.route('/compare/<brand1>/<brand2>')
def compare_brands(brand1, brand2):
    try:
        brand1_data = collection.find_one({'brand_name': brand1})
        brand2_data = collection.find_one({'brand_name': brand2})
        
        if not brand1_data or not brand2_data:
            return "One or both brands not found", 404
            
        brand1_data['_id'] = str(brand1_data['_id'])
        brand2_data['_id'] = str(brand2_data['_id'])
        
        graphs = generate_comparison_graphs(brand1_data, brand2_data)
        
        return render_template('compare.html', 
                             brand1=brand1_data,
                             brand2=brand2_data,
                             graphs=graphs)
    except Exception as e:
        print(f"Error in compare_brands: {str(e)}")
        return f"Error comparing brands: {str(e)}", 500

def generate_comparison_graphs(brand1_data, brand2_data):
    graphs = {}
    fig_width = 8
    fig_height = 6
    
    plt.style.use('default')
    brand1_color = '#16a34a'  # green
    brand2_color = '#3b82f6'  # blue
    
    # 1. Sustainability Score Comparison
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    labels = ['Sustainability Score']
    x = np.arange(len(labels))
    width = 0.35
    
    ax.bar(x - width/2, [float(brand1_data['sustainability_score'])], width, 
          label=brand1_data['brand_name'], color=brand1_color)
    ax.bar(x + width/2, [float(brand2_data['sustainability_score'])], width, 
          label=brand2_data['brand_name'], color=brand2_color)
    
    ax.set_ylabel('Score')
    ax.set_title('Sustainability Score Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    graphs['sustainability_score'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    # 2. Environmental Impact
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_width, fig_height))
    
    brands = [brand1_data['brand_name'], brand2_data['brand_name']]
    carbon_values = [float(brand1_data['carbon_footprint_mt']), 
                    float(brand2_data['carbon_footprint_mt'])]
    
    ax1.bar(brands, carbon_values, color=[brand1_color, brand2_color])
    ax1.set_title('Carbon Footprint (MT)')
    ax1.set_ylabel('Metric Tons')
    ax1.tick_params(axis='x', rotation=45)
    
    water_values = [float(brand1_data['water_usage_liters']), 
                   float(brand2_data['water_usage_liters'])]
    
    ax2.bar(brands, water_values, color=[brand1_color, brand2_color])
    ax2.set_title('Water Usage (L)')
    ax2.set_ylabel('Liters')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    graphs['environmental_impact'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    # 3. Business Metrics
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(fig_width, fig_height))
    
    product_values = [int(brand1_data['product_lines']), 
                     int(brand2_data['product_lines'])]
    
    ax1.bar(brands, product_values, color=[brand1_color, brand2_color])
    ax1.set_title('Product Lines')
    ax1.set_ylabel('Number of Lines')
    ax1.tick_params(axis='x', rotation=45)
    
    price_values = [float(brand1_data['average_price_usd']), 
                   float(brand2_data['average_price_usd'])]
    
    ax2.bar(brands, price_values, color=[brand1_color, brand2_color])
    ax2.set_title('Average Price (USD)')
    ax2.set_ylabel('Price ($)')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    graphs['business_metrics'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    # 4. Radar Chart
    fig = plt.figure(figsize=(10, 10))
    
    # Categories for radar chart
    categories = ['Sustainability', 'Carbon Footprint', 'Water Usage', 
                 'Product Lines', 'Price']
    
    # Number of categories
    num_cats = len(categories)
    
    # Compute angle for each axis
    angles = np.linspace(0, 2*np.pi, num_cats, endpoint=False).tolist()
    
    # Complete the circle by appending the first value
    angles += angles[:1]
    
    # Initialize the spider plot
    ax = fig.add_subplot(111, polar=True)
    
    # Plot data
    def normalize_value(value, min_val, max_val):
        if max_val == min_val:
            return 0.5
        return (float(value) - min_val) / (max_val - min_val)
    
    # Get values
    values1 = [
        float(brand1_data['sustainability_score']),
        float(brand1_data['carbon_footprint_mt']),
        float(brand1_data['water_usage_liters']),
        float(brand1_data['product_lines']),
        float(brand1_data['average_price_usd'])
    ]
    
    values2 = [
        float(brand2_data['sustainability_score']),
        float(brand2_data['carbon_footprint_mt']),
        float(brand2_data['water_usage_liters']),
        float(brand2_data['product_lines']),
        float(brand2_data['average_price_usd'])
    ]
    
    # Normalize each metric
    normalized_values1 = []
    normalized_values2 = []
    
    for i in range(len(categories)):  # Use categories length to ensure consistency
        min_val = min(values1[i], values2[i])
        max_val = max(values1[i], values2[i])
        normalized_values1.append(normalize_value(values1[i], min_val, max_val))
        normalized_values2.append(normalize_value(values2[i], min_val, max_val))
    
    # Complete the circular plot by appending first value
    normalized_values1 += normalized_values1[:1]
    normalized_values2 += normalized_values2[:1]
    
    # Plot data
    ax.plot(angles, normalized_values1, 'o-', linewidth=2, 
           label=brand1_data['brand_name'], color=brand1_color)
    ax.fill(angles, normalized_values1, alpha=0.25, color=brand1_color)
    
    ax.plot(angles, normalized_values2, 'o-', linewidth=2, 
           label=brand2_data['brand_name'], color=brand2_color)
    ax.fill(angles, normalized_values2, alpha=0.25, color=brand2_color)
    
    # Set the labels
    ax.set_xticks(angles[:-1])  # Remove the last tick which is duplicate
    ax.set_xticklabels(categories)
    
    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    
    plt.title('Overall Brand Comparison', size=20, y=1.05)
    
    # Save radar chart
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=300, bbox_inches='tight')
    buf.seek(0)
    graphs['radar_chart'] = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close()
    
    return graphs

@app.route('/calculator')
def calculator():
    try:
        # Get all brands for the dropdown
        brands = list(collection.find({}, {'brand_name': 1, '_id': 0}))
        return render_template('calculator.html', brands=brands)
    except Exception as e:
        print(f"Error in calculator route: {str(e)}")
        return "Error loading calculator", 500

@app.route('/impact-calculator/<brand_name>')
@with_brands
def impact_calculator(brand_name, brands=[]):
    return render_template('impact_calculator.html', 
                         brands=brands, 
                         selected_brand=brand_name)

@app.route('/impact-calculator')
@with_brands
def impact_calculator_default(brands=[]):
    return render_template('impact_calculator.html', 
                         brands=brands, 
                         selected_brand=None)

if __name__ == '__main__':
    app.run(debug=True) 