# GreenThread: Sustainable Fashion Tracker

**GreenThread** is an open-source platform designed to promote sustainability in the fashion industry. By providing consumers with data-driven insights into the environmental practices of fashion brands, it empowers them to make eco-conscious purchasing decisions.

---

## 📜 **Problem Statement**
The fashion industry contributes significantly to carbon emissions, excessive water usage, and waste production. Consumers lack accessible tools to identify eco-friendly brands. **GreenThread** bridges this gap by offering:
- Transparent data on sustainable brands.
- Tools to encourage responsible consumption patterns.

---

## 🌍 **Sustainability Goals**
GreenThread aligns with **United Nations Sustainable Development Goal (SDG) 12**: Responsible Consumption and Production. It fosters eco-friendly habits by tracking and promoting sustainable fashion brands.

---

## 🎯 **Key Features**
1. **Sustainable Brand Database**  
   - Over 4,999 entries with detailed sustainability metrics such as:
     - Carbon footprint
     - Water usage
     - Sustainability score
     - Recycling initiatives and certifications  

2. **Individual Brand Pages**  
   - Visualize sustainability metrics like carbon footprint, water usage, and waste production.  

3. **Recommendation System**  
   - Uses **KMeans clustering** and **Euclidean distance** to suggest similar sustainable brands.  

4. **Impact Calculator**  
   - Estimate environmental impacts (e.g., emissions, water use, and waste) based on user inputs.  

5. **Data Visualizations**  
   - Interactive charts for comparing sustainability trends across brands.

---

## 🛠 **Tools & Technologies**
- **Backend**: Python (Flask, pandas, scikit-learn, pymongo)
- **Frontend**: HTML, CSS, JavaScript
- **Database**: MongoDB
- **Libraries**:  
   - `pandas` for data preprocessing  
   - `scikit-learn` for clustering and recommendations  
   - `scipy` for similarity calculations  
   - `matplotlib` & `seaborn` for visualizations  

---

## 🚀 **How to Use**
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-repo/GreenThread.git
   cd GreenThread
   ```

2. **Setup the Database**  
   - Ensure MongoDB is running locally or remotely.
   - Load the preprocessed dataset:
     ```python
     python load_data_to_mongo.py
     ```

3. **Run the Application**  
   ```bash
   python app.py
   ```
