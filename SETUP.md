# 🚀 InnSight Setup Guide

Complete setup instructions for running InnSight on a new computer.

---

## ⏱️ Estimated Setup Time: 45-60 minutes

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.9+** installed
- **MongoDB 7.0+** installed and running
- **Git** installed
- **4GB RAM** minimum
- **5GB free disk space**
- **Internet connection** (for downloading data)

---

## 🔧 Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/innsight-solo.git
cd innsight-solo
```

---

## 🐍 Step 2: Set Up Python Environment

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies (takes 2-3 minutes)
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"
```

**Verify installation:**
```bash
python test_setup.py
```

You should see: `🎉 SUCCESS! All packages installed!`

---

## 🗄️ Step 3: Start MongoDB

### Mac (Homebrew):
```bash
brew services start mongodb-community
```

### Linux:
```bash
sudo systemctl start mongod
```

### Docker:
```bash
docker run -d -p 27017:27017 --name innsight-mongo mongo:7.0
```

**Verify MongoDB is running:**
```bash
python test_mongodb.py
```

You should see: `✅ MongoDB is running!`

---

## 📥 Step 4: Download Data

### Option A: Manual Download (Recommended)

1. Go to: **http://insideairbnb.com/get-the-data/**
2. Find **"London, England, United Kingdom"**
3. Download these 3 files:
   - `listings.csv.gz`
   - `reviews.csv.gz`
   - `neighbourhoods.geojson`
4. Extract the `.gz` files:
   ```bash
   gunzip listings.csv.gz
   gunzip reviews.csv.gz
   ```
5. Move files to: `backend/data/raw/london/`

### Option B: Command Line Download

```bash
cd backend/data/raw
mkdir -p london
cd london

# Download files (replace URLs with latest from insideairbnb.com)
curl -O http://data.insideairbnb.com/united-kingdom/england/london/[DATE]/data/listings.csv.gz
curl -O http://data.insideairbnb.com/united-kingdom/england/london/[DATE]/data/reviews.csv.gz
curl -O http://data.insideairbnb.com/united-kingdom/england/london/[DATE]/visualisations/neighbourhoods.geojson

# Extract
gunzip *.gz
```

**Verify files exist:**
```bash
ls -lh backend/data/raw/london/
```

You should see:
- `listings.csv` (~50-60 MB)
- `reviews.csv` (~300-400 MB)
- `neighbourhoods.geojson` (~1 MB)

---

## 🧹 Step 5: Process Data

```bash
cd ~/innsight-solo/backend

# Clean and process data (takes 5-10 minutes)
python -m data.etl_pipeline london --skip-calendar
```

**Expected output:**
```
✅ Listings: ~96,000 rows
✅ Reviews: ~2,000,000 rows
```

**Verify processed files:**
```bash
ls -lh backend/data/processed/
```

You should see:
- `london_listings_clean.csv`
- `london_reviews_clean.csv`

---

## 💾 Step 6: Load into MongoDB

```bash
# Load data into MongoDB (takes 5-8 minutes)
python -m data.mongodb_loader london --drop
```

**Expected output:**
```
✅ Inserted ~96,000 listings
✅ Inserted ~2,000,000 reviews
✅ Indexes created
```

**Verify data loaded:**
```bash
python test_mongo_query.py
```

You should see: `Total London reviews: 2,068,845`

---

## 🤖 Step 7: Run Sentiment Analysis

```bash
cd ml

# Analyze all reviews (takes 10-15 minutes)
# This is the longest step - grab a coffee! ☕
python add_sentiment_to_db.py london
```

**Expected output:**
```
Processing reviews: 100%|████████| 2,068,845/2,068,845

✅ Processed: 2,068,845 reviews
✅ Positive: 84.4%
✅ Neutral: 10.3%
✅ Negative: 5.3%
```

---

## 🚀 Step 8: Run the Application

### Start Backend API (Terminal 1)

```bash
cd ~/innsight-solo/backend
source venv/bin/activate  # Make sure venv is activated
python run.py
```

You should see:
```
🚀 InnSight API Server Starting...
API running at: http://localhost:5000
```

**Test API:**
```bash
# In a new terminal
curl http://localhost:5000/health
# Should return: {"status": "healthy"}
```

### Start Frontend Server (Terminal 2)

```bash
cd ~/innsight-solo/frontend
python3 -m http.server 8000
```

You should see:
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

---

## 🌐 Step 9: Open in Browser

Navigate to: **http://localhost:8000**

**You should see:**
- ✅ Blue navbar with "InnSight" logo
- ✅ Interactive map with colored markers
- ✅ Sidebar filters
- ✅ Dashboard with 4 charts

---

## ✅ Verification Checklist

Test these features:

- [ ] Map loads with markers (green, orange, red dots)
- [ ] Click a marker - popup shows listing details
- [ ] Select a neighbourhood - filters work
- [ ] Sidebar shows average price
- [ ] Charts display data
- [ ] No console errors (press F12)

---

## 🐛 Troubleshooting

### MongoDB Connection Failed
```bash
# Check if MongoDB is running
ps aux | grep mongod

# Restart MongoDB
brew services restart mongodb-community  # Mac
sudo systemctl restart mongod            # Linux
```

### Port 5000 Already in Use
```bash
# Find what's using port 5000
lsof -i :5000

# Kill it
kill -9 <PID>

# Or use a different port in backend/app/config.py
```

### "Module not found" Errors
```bash
# Make sure venv is activated (you should see "(venv)" in prompt)
source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

### No Data Showing
```bash
# Check MongoDB has data
python test_mongo_query.py

# Check API returns data
curl http://localhost:5000/api/listings/london?limit=5
```

### Frontend Shows Blank Page
- Check browser console (F12) for errors
- Verify Flask API is running on port 5000
- Check CORS is enabled in Flask

---

## 📊 Data Summary

After setup, you'll have:

| Collection | Documents | Description |
|------------|-----------|-------------|
| listings | ~96,871 | London Airbnb properties |
| reviews | ~2,068,845 | Guest reviews with sentiment |
| neighbourhoods | ~33 | London boroughs/areas |

---

## 🔄 Daily Usage

After initial setup, to run the app:

```bash
# Terminal 1: Start MongoDB (if not auto-started)
brew services start mongodb-community

# Terminal 2: Start Flask API
cd ~/innsight-solo/backend
source venv/bin/activate
python run.py

# Terminal 3: Start Frontend
cd ~/innsight-solo/frontend
python3 -m http.server 8000
```

Then open: **http://localhost:8000**

---

## 🗑️ Cleanup

To stop everything:

```bash
# Stop servers: Press CTRL+C in each terminal

# Stop MongoDB
brew services stop mongodb-community  # Mac
sudo systemctl stop mongod            # Linux
```

To completely remove and start fresh:

```bash
# Delete MongoDB data
mongo
> use innsight_db
> db.dropDatabase()

# Delete processed files
rm -rf backend/data/processed/*

# Keep raw data and re-run from Step 5
```

---

## 💡 Tips

1. **Keep MongoDB running** - It uses minimal resources
2. **MongoDB data location** - `/usr/local/var/mongodb` (Mac)
3. **Backup MongoDB** - `mongodump --db=innsight_db`
4. **Update data** - Download new CSV files and re-run ETL
5. **Performance** - On slower machines, reduce `limit` in API calls

---

## 🆘 Getting Help

If you encounter issues:

1. Check the main **README.md** for details
2. Review **API_EXAMPLES.md** for endpoint testing
3. Check server logs in terminal output
4. Verify each step completed successfully

---

## 📈 Next Steps

After successful setup:

- Explore different neighbourhoods
- Compare prices and sentiment
- Add more cities (Paris, Amsterdam)
- Customize the frontend
- Deploy to the cloud

---

**Setup complete! Enjoy exploring Airbnb data with InnSight! 🎉**