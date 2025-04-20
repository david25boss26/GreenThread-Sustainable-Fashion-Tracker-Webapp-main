# GreenThread-Sustainable-Fashion-Tracker-Webapp-main
Based on your uploaded files, here’s a comprehensive and updated **README** for your project:

---

# 🌿 GreenThread: Sustainable Fashion Tracker

**GreenThread** is an open-source web application that empowers consumers to make eco-conscious fashion choices. By aggregating and analyzing data from thousands of fashion brands, it provides detailed sustainability insights and intelligent recommendations.

---

## 🧩 Problem Statement

The fashion industry is a major contributor to environmental degradation, including:
- High carbon emissions  
- Excessive water usage  
- Waste production  

**GreenThread** addresses this by offering transparency and actionable insights into the environmental impact of fashion brands.

---

## 🌱 Sustainability Vision

Aligned with the **UN Sustainable Development Goal (SDG) 12** — _Responsible Consumption and Production_ — GreenThread promotes sustainable fashion through education and data-driven tools.

---

## 🚀 Features

### ✅ Sustainable Brand Dashboard
- 4,999+ brand entries
- Metrics include:
  - Carbon footprint (MT)
  - Water usage (liters)
  - Product lines & price
  - Sustainability score
  - Certifications & materials

### 🔍 Brand Insights
- Individual pages per brand with visualized sustainability data
- View trends and raw environmental metrics

### 🧠 Smart Recommendations
- Uses **KMeans clustering** and **Euclidean distance**
- Suggests similar brands based on scaled sustainability metrics

### ⚖️ Brand Comparison
- Side-by-side brand analysis with:
  - Bar charts
  - Radar/spider visualizations
  - Breakdown of sustainability, water/carbon metrics, and pricing

### 📊 Impact Calculator
- Calculates user consumption impact
- Personalized estimates based on brand selection and usage

---

## 🛠 Tech Stack

| Component      | Stack                                                                 |
|----------------|----------------------------------------------------------------------|
| **Backend**     | Python, Flask, Pandas, Scikit-learn, MongoDB (pymongo)               |
| **Frontend**    | HTML, CSS, JavaScript (with Flask templates)                         |
| **Database**    | MongoDB                                                              |
| **Visualization** | matplotlib, seaborn                                                 |
| **Clustering & Similarity** | KMeans, Euclidean distance, cosine similarity           |

---

## 🧪 File Structure

- `app.py` – Flask web app with routes, rendering, and MongoDB interactions
- `brand_recom.py` – Clustering and recommendation logic
- `datafetch.py` / `upload_to_mongodb.py` – Load Excel data into MongoDB
- `oss_dataset_features.xlsx` – Dataset containing sustainability features
- `templates/` – HTML templates for dashboard, comparison, calculator
- `static/` – CSS, JS, and image assets

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/GreenThread.git
cd GreenThread
```

### 2. Install Dependencies

Make sure Python 3.7+ is installed, then run:

```bash
pip install -r requirements.txt
```

> _Note: Add your `requirements.txt` with libraries like `Flask`, `pymongo`, `matplotlib`, `pandas`, `scikit-learn`, etc._

### 3. Start MongoDB

Ensure MongoDB is running locally:
```bash
sudo service mongod start
```

### 4. Load the Dataset

```bash
python upload_to_mongodb.py
```

### 5. Run the Application

```bash
python app.py
```

Open in browser: [http://localhost:5000](http://localhost:5000)

---

## 🧠 Future Improvements

- Integrate real-time data sources (e.g., APIs from brands)
- Add user account system for tracking personal carbon impact
- Support sentiment analysis of user reviews
- Deploy to cloud (Heroku, AWS, etc.)

---

## 🤝 Contributing

Contributions are welcome! Open an issue or submit a PR with enhancements, fixes, or new features.

---

## 📄 License

MIT License. See `LICENSE` for details.

---

