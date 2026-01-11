# 🚀 Quick Start Guide - InnSight

**Get InnSight running in 30 minutes!**

---

## ✅ **What You Need**

- Mac/Linux computer
- Python 3.9+
- MongoDB 7.0+
- Terminal access
- 5GB free disk space

---

## 📋 **Step-by-Step Setup**

### **1. Clone & Setup Python (5 mins)**

```bash
# Navigate to your projects folder
cd ~
git clone <repo-url> innsight-solo
cd innsight-solo/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (takes 2-3 minutes)
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"
```

---

### **2. Start MongoDB (2 mins)**

```bash
# Start MongoDB server
mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --fork

# Verify it's running
python test_mongodb.py
# Should output: "✅ MongoDB is running!"
```

---

### **3. Download Data (10 mins)**

**Option A: Browser Download (Easier)**
1. Go to: http://insideairbnb.com/get-the-data/
2. Find "London, England"
3. Download: `listings.csv.gz`, `reviews.csv.gz`, `neighbourhoods.geojson`
4. Move files to: `backend/data/raw/london/`
5. Unzip: `gunzip *.gz`

**Option B: Terminal Download**
```bash
cd backend/data/raw/london

curl -O http://data.insideairbnb.com/.../listings.csv.gz
curl -O http://data.insideairbnb.com/.../reviews.csv.gz
curl -O http://data.insideairbnb.com/.../neighbourhoods.geojson

gunzip *.gz
```

---

### **4. Process Data (8 mins)**

```bash
cd ~/innsight-solo/backend

# Clean the data (takes 5-8 minutes)
python -m data.etl_pipeline london --skip-calendar

# Expected output:
# ✅ Listings: 96,871 rows
# ✅ Reviews: 2,068,845 rows
```

---

### **5. Load MongoDB (5 mins)**

```bash
# Load cleaned data into database
python -m data.mongodb_loader london --drop

# Expected output:
# ✅ Inserted 96,871 listings
# ✅ Inserted 2,068,845 reviews
```

---

### **6. Add Sentiment (10-15 mins)**

```bash
cd ml

# Analyze all reviews (grab a coffee! ☕)
python add_sentiment_to_db.py london

# Progress bar will show:
# Processing reviews: 100%|████████| 2,068,845/2,068,845

# Expected output:
# ✅ Positive: 84.4%
# ✅ Neutral: 10.3%
# ✅ Negative: 5.3%
```

---

### **7. Start API Server**

```bash
cd ~/innsight-solo/backend
python run.py

# Output:
# 🚀 InnSight API Server Starting...
# API running at: http://localhost:5000
```

---

### **8. Test It! 🎉**

**Open a new terminal:**

```bash
# Test health
curl http://localhost:5000/health

# Test sentiment stats
curl http://localhost:5000/api/analytics/london/sentiment

# Test listings
curl http://localhost:5000/api/listings/london?limit=5
```

**Success!** If you see JSON data, you're done! ✅

---

## 🎯 **Try These Cool Endpoints**

```bash
# Happiest neighbourhoods
curl http://localhost:5000/api/analytics/london/sentiment/by-neighbourhood

# Price comparison
curl http://localhost:5000/api/analytics/london/price-stats

# Most common positive words
curl "http://localhost:5000/api/analytics/london/wordcloud?sentiment=positive&limit=10"

# Room type breakdown
curl http://localhost:5000/api/analytics/london/room-type-distribution

# Top hosts
curl http://localhost:5000/api/analytics/london/top-hosts
```

---

## 🐛 **Troubleshooting**

### **MongoDB won't start**
```bash
# Check if it's already running
ps aux | grep mongod

# Kill existing process
killall mongod

# Start fresh
mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --fork
```

### **Python package errors**
```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

### **"Module not found" errors**
```bash
# Make sure venv is activated
source venv/bin/activate

# You should see (venv) in your prompt
```

### **API returns empty data**
```bash
# Check if data was loaded
python test_mongo_query.py

# Should show: "Total London reviews: 2,068,845"
```

---

## 📊 **What You Built**

You now have:
- ✅ 96,871 London Airbnb listings in database
- ✅ 2,068,845 reviews with AI sentiment analysis
- ✅ RESTful API with 10+ endpoints
- ✅ Production-ready backend

**Total setup time: ~30-45 minutes**

---

## 🎨 **Next Steps**

### **Build the Frontend**
- React app with interactive map
- Dashboard with charts
- Filters and search
- Word cloud visualization

### **Add More Cities**
- Paris
- Amsterdam
- Barcelona

### **Deploy**
- Docker containerization
- Cloud hosting (AWS/Heroku)
- Domain & SSL certificate

---

## 💡 **Pro Tips**

1. **Keep MongoDB running** - It uses minimal resources
2. **Save API examples** - Bookmark working curl commands
3. **Monitor logs** - Check `run.py` output for errors
4. **Backup data** - MongoDB data in `/usr/local/var/mongodb`

---

## 🆘 **Need Help?**

1. Check the main README.md for detailed docs
2. Review error messages carefully
3. Verify each step completed successfully
4. Test components individually

---

**You're ready to explore 2 million Airbnb reviews with AI! 🚀**