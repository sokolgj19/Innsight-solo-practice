# InnSight - Smart Airbnb Explorer

> An intelligent data visualization platform for exploring Airbnb listings with ML-powered sentiment analysis

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-7.0+-brightgreen.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](LICENSE)

---

## 🎯 **Project Overview**

InnSight analyzes over **2 million Airbnb reviews** using natural language processing to help travelers make informed decisions. The platform combines geographic mapping, pricing analytics, and machine learning-powered sentiment analysis to transform raw data into actionable insights.

### **Key Features**

- 🗺️ **Interactive Map** - Visualize 96,871 London listings with geolocation
- 📊 **Analytics Dashboard** - Price trends, room types, occupancy rates
- 🤖 **ML Sentiment Analysis** - 2,068,845 reviews analyzed (84.4% positive!)
- 🏘️ **Neighborhood Insights** - Compare sentiment across 33 London neighborhoods
- ☁️ **Word Clouds** - Most common positive/negative review keywords
- 🏆 **Top Hosts** - Identify super-hosts with best reviews

---

## 📈 **Project Statistics**

| Metric | Count |
|--------|-------|
| **Listings Processed** | 96,871 |
| **Reviews Analyzed** | 2,068,845 |
| **Positive Reviews** | 1,745,163 (84.4%) |
| **Neutral Reviews** | 214,080 (10.3%) |
| **Negative Reviews** | 109,602 (5.3%) |
| **Neighborhoods Covered** | 33 |
| **API Endpoints** | 10+ |
| **Average Sentiment Score** | 0.843 / 1.0 |

---

## 🏗️ **Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                         FRONTEND                             │
│              React + Leaflet + Recharts                      │
│                    (To Be Built)                             │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP REST API
┌─────────────────────▼───────────────────────────────────────┐
│                    FLASK API SERVER                          │
│  - Listings endpoints (/api/listings/:city)                 │
│  - Analytics endpoints (/api/analytics/:city/...)           │
│  - Sentiment aggregation                                     │
│  - Word cloud generation                                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    MONGODB DATABASE                          │
│  Collections:                                                │
│  - listings (96,871 docs)                                   │
│  - reviews (2,068,845 docs with sentiment)                  │
│  - calendar (occupancy data)                                │
│  - neighbourhoods (GeoJSON boundaries)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    ETL PIPELINE                              │
│  1. Extract: Download CSV from InsideAirbnb                 │
│  2. Transform: Clean, validate, enrich                      │
│  3. Load: Insert into MongoDB with indexes                  │
└──────────────────────────────────────────────────────────────┘
```

---

## 🛠️ **Tech Stack**

### **Backend**
- **Python 3.9+** - Core language
- **Flask 3.0** - REST API framework
- **Flask-CORS** - Cross-origin resource sharing
- **PyMongo 4.6** - MongoDB driver
- **Pandas 2.0** - Data processing
- **NLTK 3.9** - Natural language processing
- **VADER** - Sentiment analysis model

### **Database**
- **MongoDB 7.0** - NoSQL document database
- **Indexes** - Optimized queries on city, sentiment, price

### **Machine Learning**
- **VADER SentimentIntensityAnalyzer** - Pre-trained sentiment model
- **Compound Score Thresholding** - Classification logic
  - Positive: score ≥ 0.05
  - Negative: score ≤ -0.05
  - Neutral: -0.05 < score < 0.05

### **Data Source**
- **Inside Airbnb** - http://insideairbnb.com/get-the-data/
- Dataset: London (December 2024)
- License: Creative Commons CC0 1.0 Universal

---

## 📂 **Project Structure**

```
innsight-solo/
├── backend/
│   ├── app/                      # Flask application
│   │   ├── __init__.py          # App factory
│   │   ├── config.py            # Configuration
│   │   ├── database.py          # MongoDB connection
│   │   └── routes/
│   │       ├── listings.py      # Listings API
│   │       └── analytics.py     # Analytics API
│   ├── data/                     # ETL pipeline
│   │   ├── config.py            # Data config
│   │   ├── utils.py             # Cleaning utilities
│   │   ├── data_cleaner.py      # Data cleaning logic
│   │   ├── etl_pipeline.py      # ETL orchestrator
│   │   └── mongodb_loader.py    # Database loader
│   ├── ml/                       # Machine learning
│   │   ├── sentiment_analyzer.py         # Sentiment analysis
│   │   └── add_sentiment_to_db.py       # Batch processing
│   ├── tests/                    # Unit tests
│   ├── requirements.txt         # Python dependencies
│   └── run.py                   # Server entry point
├── frontend/                     # React app (to be built)
├── docs/                         # Documentation
└── README.md                     # This file
```

---

## 🚀 **Getting Started**

### **Prerequisites**

- Python 3.9 or higher
- MongoDB 7.0 or higher
- 4GB RAM minimum
- 5GB free disk space

### **Installation**

#### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd innsight-solo
```

#### 2. Set Up Python Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"
```

#### 3. Start MongoDB

```bash
# Option A: Local installation
mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --fork

# Option B: Docker
docker run -d -p 27017:27017 --name innsight-mongo mongo:7.0
```

#### 4. Configure Environment

```bash
# Create .env file
cat > .env << EOF
MONGO_URI=mongodb://localhost:27017/
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
API_PORT=5000
EOF
```

---

## 📥 **Data Setup**

### **Download Data**

1. Go to http://insideairbnb.com/get-the-data/
2. Find "London, England, United Kingdom"
3. Download these 4 files:
   - `listings.csv.gz`
   - `reviews.csv.gz`
   - `calendar.csv.gz`
   - `neighbourhoods.geojson`

4. Place files in: `backend/data/raw/london/`

### **Run ETL Pipeline**

```bash
cd backend

# Process listings and reviews (skip large calendar file)
python -m data.etl_pipeline london --skip-calendar
```

**Expected output:**
```
✅ Listings: 96,871 rows
✅ Reviews: 2,068,845 rows
```

### **Load into MongoDB**

```bash
# Load cleaned data into database
python -m data.mongodb_loader london --drop
```

**Expected output:**
```
✅ Inserted 96,871 listings
✅ Inserted 2,068,845 reviews
✅ Indexes created
```

### **Add Sentiment Analysis**

```bash
cd ml

# Analyze all 2M reviews (takes 10-15 minutes)
python add_sentiment_to_db.py london
```

**Expected output:**
```
✅ Processed: 2,068,845 reviews
✅ Positive: 84.4%
✅ Neutral: 10.3%
✅ Negative: 5.3%
```

---

## 🖥️ **Running the Application**

### **Start API Server**

```bash
cd backend
source venv/bin/activate
python run.py
```

Server runs at: **http://localhost:5000**

### **Test Endpoints**

```bash
# Health check
curl http://localhost:5000/health

# Get sentiment statistics
curl http://localhost:5000/api/analytics/london/sentiment

# Get listings
curl http://localhost:5000/api/listings/london?limit=10

# Get sentiment by neighbourhood
curl http://localhost:5000/api/analytics/london/sentiment/by-neighbourhood

# Get word cloud data (positive words)
curl "http://localhost:5000/api/analytics/london/wordcloud?sentiment=positive&limit=20"
```

---

## 📡 **API Documentation**

### **Base URL**
```
http://localhost:5000/api
```

### **Endpoints**

#### **Listings**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/listings/:city` | Get all listings with filters |
| GET | `/listings/:city/:id` | Get single listing detail |
| GET | `/listings/:city/neighbourhoods` | List all neighbourhoods |
| GET | `/listings/:city/room-types` | List all room types |

**Query Parameters for `/listings/:city`:**
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter
- `room_type` - Room type filter
- `neighbourhood` - Neighbourhood filter
- `limit` - Max results (default: 1000, max: 5000)

#### **Analytics**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/:city/price-stats` | Price statistics |
| GET | `/analytics/:city/room-type-distribution` | Room type breakdown |
| GET | `/analytics/:city/occupancy` | Monthly occupancy rates |
| GET | `/analytics/:city/top-hosts` | Top 10 hosts by listings |
| GET | `/analytics/:city/sentiment` | Overall sentiment stats |
| GET | `/analytics/:city/sentiment/by-neighbourhood` | Sentiment by area |
| GET | `/analytics/:city/wordcloud` | Word frequency data |

**Query Parameters for `/wordcloud`:**
- `sentiment` - Filter by sentiment (positive/negative/neutral)
- `neighbourhood` - Filter by neighbourhood
- `limit` - Number of words (default: 100)

---

## 🔬 **Sentiment Analysis Details**

### **Model: VADER (Valence Aware Dictionary and sEntiment Reasoner)**

VADER is a lexicon and rule-based sentiment analysis tool specifically attuned to social media text. It's included in NLTK.

### **How It Works**

1. **Analyze Text** - Extract sentiment indicators
2. **Calculate Scores**:
   - `positive` (0-1): Proportion of positive words
   - `neutral` (0-1): Proportion of neutral words
   - `negative` (0-1): Proportion of negative words
   - `compound` (-1 to 1): Overall sentiment score

3. **Classify**:
   ```python
   if compound >= 0.05:  sentiment = "positive"
   elif compound <= -0.05:  sentiment = "negative"
   else:  sentiment = "neutral"
   ```

### **Example Analysis**

**Review:** *"Amazing host! The location was perfect and the apartment was very clean. Highly recommend!"*

```json
{
  "sentiment": "positive",
  "sentiment_score": 0.9342,
  "scores": {
    "positive": 0.68,
    "neutral": 0.32,
    "negative": 0.00
  }
}
```

---

## 📊 **Key Insights from Data**

### **Top 5 Happiest Neighbourhoods** (by % positive reviews)

1. **Richmond upon Thames** - 94.1% positive (avg score: 0.812)
2. **Kingston upon Thames** - 91.6% positive (avg score: 0.776)
3. **Havering** - 91.0% positive (avg score: 0.727)
4. **Hounslow** - 90.2% positive (avg score: 0.743)
5. **Hillingdon** - 89.9% positive (avg score: 0.709)

### **Most Expensive Neighbourhoods** (avg price/night)

1. **Tower Hamlets** - £431
2. **City of London** - £354
3. **Lambeth** - £346
4. **Westminster** - £342
5. **Kensington and Chelsea** - £336

### **Most Common Positive Words**

1. stay (5,698 mentions)
2. great (5,468)
3. london (4,901)
4. place (4,078)
5. room (3,404)
6. location (3,179)
7. clean (2,925)
8. host (2,802)
9. nice (2,751)
10. lovely (2,327)

### **Room Type Distribution**

- Entire home/apt: 64.9%
- Private room: 34.7%
- Shared room: 0.2%
- Hotel room: 0.1%

---

## 🧪 **Testing**

### **Run Test Scripts**

```bash
# Test MongoDB connection
python test_mongodb.py

# Test sentiment analyzer
python ml/sentiment_analyzer.py

# Test data cleaning (sample)
python test_cleaning.py
```

---

## 🚧 **Roadmap / TODO**

### **Phase 1: Backend (COMPLETE)** ✅
- [x] ETL pipeline
- [x] MongoDB integration
- [x] Sentiment analysis
- [x] Flask API
- [x] Analytics endpoints

### **Phase 2: Frontend (TODO)**
- [ ] React app setup
- [ ] Interactive Leaflet map
- [ ] Dashboard with Recharts
- [ ] Filters component
- [ ] Neighbourhood comparison
- [ ] Word cloud visualization

### **Phase 3: Deployment (TODO)**
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/Heroku)
- [ ] CI/CD pipeline
- [ ] API documentation (Swagger)

### **Phase 4: Enhancements (TODO)**
- [ ] Add Paris and Amsterdam data
- [ ] User authentication
- [ ] Saved searches
- [ ] Email alerts for price drops
- [ ] Advanced ML (topic modeling)

---

## 🤝 **Contributing**

This is an educational project. Contributions, issues, and feature requests are welcome!

---

## 📄 **License**

This project is for educational purposes as part of the Holberton School curriculum.

---

## 👥 **Author**

**Sokol** - Solo Development Project
- GitHub: [@your-username](https://github.com/your-username)

---

## 🙏 **Acknowledgments**

- **Inside Airbnb** - For providing open data
- **Holberton School** - Educational support
- **NLTK/VADER** - Sentiment analysis tools
- **MongoDB** - Database platform
- **Flask** - Web framework

---

## 📞 **Support**

For questions or issues:
1. Check existing documentation
2. Review API endpoint examples
3. Test with provided curl commands
4. Check MongoDB connection

---

**Built with ❤️ in Tirana, Albania - January 2026**