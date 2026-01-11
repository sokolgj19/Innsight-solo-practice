# 📡 API Examples - InnSight

Complete examples for all API endpoints with sample responses.

**Base URL:** `http://localhost:5000/api`

---

## 🏠 **Listings Endpoints**

### **1. Get Listings for a City**

```bash
curl http://localhost:5000/api/listings/london?limit=5
```

**Response:**
```json
{
  "city": "london",
  "count": 5,
  "listings": [
    {
      "id": 13913,
      "name": "Holiday London DB Room",
      "latitude": 51.56861,
      "longitude": -0.1127,
      "price": 70.0,
      "room_type": "Private room",
      "neighbourhood_cleansed": "Islington",
      "review_scores_rating": 4.85
    }
  ]
}
```

### **2. Filter by Price**

```bash
curl "http://localhost:5000/api/listings/london?min_price=50&max_price=150&limit=10"
```

### **3. Filter by Room Type**

```bash
curl "http://localhost:5000/api/listings/london?room_type=Entire home/apt&limit=10"
```

### **4. Filter by Neighbourhood**

```bash
curl "http://localhost:5000/api/listings/london?neighbourhood=Westminster&limit=10"
```

### **5. Get Single Listing Detail**

```bash
curl http://localhost:5000/api/listings/london/13913
```

**Response:**
```json
{
  "id": 13913,
  "name": "Holiday London DB Room",
  "description": "My bright double bedroom...",
  "host_name": "John",
  "price": 70.0,
  "sentiment": {
    "positive": 45,
    "neutral": 8,
    "negative": 2
  }
}
```

### **6. Get Neighbourhoods List**

```bash
curl http://localhost:5000/api/listings/london/neighbourhoods
```

**Response:**
```json
{
  "city": "london",
  "neighbourhoods": [
    "Barking and Dagenham",
    "Barnet",
    "Bexley",
    "Brent",
    "Bromley",
    "Camden",
    ...
  ]
}
```

### **7. Get Room Types**

```bash
curl http://localhost:5000/api/listings/london/room-types
```

**Response:**
```json
{
  "city": "london",
  "room_types": [
    "Entire home/apt",
    "Hotel room",
    "Private room",
    "Shared room"
  ]
}
```

---

## 📊 **Analytics Endpoints**

### **1. Price Statistics**

```bash
curl http://localhost:5000/api/analytics/london/price-stats
```

**Response:**
```json
{
  "city": "london",
  "overall": {
    "avg_price": 229.92,
    "min_price": 7.0,
    "max_price": 1085147.0,
    "count": 61963
  },
  "by_neighbourhood": [
    {
      "_id": "Tower Hamlets",
      "avg_price": 430.91,
      "min_price": 10.0,
      "max_price": 1085147.0,
      "count": 4275
    },
    {
      "_id": "Westminster",
      "avg_price": 342.14,
      "count": 8443
    }
  ]
}
```

### **2. Room Type Distribution**

```bash
curl http://localhost:5000/api/analytics/london/room-type-distribution
```

**Response:**
```json
{
  "city": "london",
  "total_listings": 96871,
  "distribution": [
    {
      "_id": "Entire home/apt",
      "count": 62907,
      "percentage": 64.9,
      "avg_price": 279.35
    },
    {
      "_id": "Private room",
      "count": 33643,
      "percentage": 34.7,
      "avg_price": 121.71
    }
  ]
}
```

### **3. Top Hosts**

```bash
curl http://localhost:5000/api/analytics/london/top-hosts
```

**Response:**
```json
{
  "city": "london",
  "top_hosts": [
    {
      "_id": 446820235,
      "host_name": "LuxurybookingsFZE",
      "listing_count": 500,
      "avg_price": 485.26,
      "avg_rating": 4.53
    },
    {
      "_id": 314162972,
      "host_name": "Blueground",
      "listing_count": 405,
      "avg_price": 348.20,
      "avg_rating": 4.35
    }
  ]
}
```

### **4. Overall Sentiment Statistics**

```bash
curl http://localhost:5000/api/analytics/london/sentiment
```

**Response:**
```json
{
  "city": "london",
  "total_reviews": 2068845,
  "sentiment": {
    "positive": {
      "count": 1745163,
      "percentage": 84.4,
      "avg_score": 0.843
    },
    "neutral": {
      "count": 214080,
      "percentage": 10.3,
      "avg_score": 0.0
    },
    "negative": {
      "count": 109602,
      "percentage": 5.3,
      "avg_score": -0.571
    }
  }
}
```

### **5. Sentiment by Neighbourhood**

```bash
curl http://localhost:5000/api/analytics/london/sentiment/by-neighbourhood
```

**Response:**
```json
{
  "city": "london",
  "neighbourhoods": [
    {
      "neighbourhood": "Richmond upon Thames",
      "total_reviews": 36260,
      "positive": 34122,
      "positive_pct": 94.1,
      "neutral": 1399,
      "neutral_pct": 3.9,
      "negative": 739,
      "negative_pct": 2.0,
      "avg_sentiment_score": 0.812
    },
    {
      "neighbourhood": "Westminster",
      "total_reviews": 283989,
      "positive": 232062,
      "positive_pct": 81.7,
      "neutral": 35198,
      "neutral_pct": 12.4,
      "negative": 16729,
      "negative_pct": 5.9,
      "avg_sentiment_score": 0.649
    }
  ]
}
```

### **6. Word Cloud - Positive Words**

```bash
curl "http://localhost:5000/api/analytics/london/wordcloud?sentiment=positive&limit=20"
```

**Response:**
```json
{
  "city": "london",
  "sentiment": "positive",
  "neighbourhood": null,
  "words": [
    {"word": "stay", "count": 5698},
    {"word": "great", "count": 5468},
    {"word": "london", "count": 4901},
    {"word": "place", "count": 4078},
    {"word": "room", "count": 3404},
    {"word": "location", "count": 3179},
    {"word": "clean", "count": 2925},
    {"word": "host", "count": 2802},
    {"word": "nice", "count": 2751},
    {"word": "lovely", "count": 2327}
  ]
}
```

### **7. Word Cloud - Negative Words**

```bash
curl "http://localhost:5000/api/analytics/london/wordcloud?sentiment=negative&limit=10"
```

### **8. Word Cloud for Specific Neighbourhood**

```bash
curl "http://localhost:5000/api/analytics/london/wordcloud?sentiment=positive&neighbourhood=Camden&limit=15"
```

### **9. Occupancy Statistics**

```bash
curl http://localhost:5000/api/analytics/london/occupancy
```

**Response:**
```json
{
  "city": "london",
  "by_month": [
    {
      "_id": "2024-12",
      "total_days": 850000,
      "booked_days": 425000,
      "occupancy_rate": 50.0
    },
    {
      "_id": "2025-01",
      "total_days": 900000,
      "booked_days": 495000,
      "occupancy_rate": 55.0
    }
  ]
}
```

---

## 🔥 **Advanced Query Examples**

### **Find Cheap Listings in Happy Neighbourhoods**

```bash
# 1. Get happiest neighbourhoods
curl http://localhost:5000/api/analytics/london/sentiment/by-neighbourhood | jq '.neighbourhoods[0:5]'

# 2. Find cheap listings in Richmond upon Thames
curl "http://localhost:5000/api/listings/london?neighbourhood=Richmond upon Thames&max_price=100&limit=20"
```

### **Compare Price vs Sentiment**

```bash
# Get both datasets
curl http://localhost:5000/api/analytics/london/price-stats > prices.json
curl http://localhost:5000/api/analytics/london/sentiment/by-neighbourhood > sentiment.json
```

### **Find Most Positive Reviews for a Neighbourhood**

```bash
# Step 1: Get listings in Camden
curl "http://localhost:5000/api/listings/london?neighbourhood=Camden&limit=100" > camden_listings.json

# Step 2: Check sentiment for each listing
curl http://localhost:5000/api/listings/london/13913
```

### **Export Data to CSV**

```bash
# Get listings and convert to CSV
curl "http://localhost:5000/api/listings/london?limit=1000" | \
  jq -r '.listings[] | [.id, .name, .price, .neighbourhood_cleansed] | @csv' > listings.csv
```

---

## 🎨 **Frontend Integration Examples**

### **JavaScript/Fetch**

```javascript
// Get sentiment stats
fetch('http://localhost:5000/api/analytics/london/sentiment')
  .then(res => res.json())
  .then(data => {
    console.log(`Positive: ${data.sentiment.positive.percentage}%`);
  });
```

### **React/Axios**

```javascript
import axios from 'axios';

const API_BASE = 'http://localhost:5000/api';

// Get listings with filters
const fetchListings = async (filters) => {
  const params = new URLSearchParams(filters);
  const response = await axios.get(`${API_BASE}/listings/london?${params}`);
  return response.data.listings;
};

// Get sentiment by neighbourhood
const fetchSentiment = async () => {
  const response = await axios.get(`${API_BASE}/analytics/london/sentiment/by-neighbourhood`);
  return response.data.neighbourhoods;
};
```

### **Python/Requests**

```python
import requests

API_BASE = 'http://localhost:5000/api'

# Get price statistics
response = requests.get(f'{API_BASE}/analytics/london/price-stats')
data = response.json()

print(f"Average price: £{data['overall']['avg_price']:.2f}")
```

---

## 📈 **Performance Notes**

- Most endpoints return in **< 100ms**
- `sentiment/by-neighbourhood` takes **~2-3 seconds** (processes all reviews)
- `wordcloud` takes **~1-2 seconds** (processes text)
- Use `limit` parameter to reduce response size
- Responses are not cached (add Redis for production)

---

## 🔒 **Error Responses**

### **404 Not Found**
```json
{
  "error": "Listing not found"
}
```

### **400 Bad Request**
```json
{
  "error": "Invalid parameter: limit must be between 1 and 5000"
}
```

### **500 Internal Server Error**
```json
{
  "error": "Database connection failed"
}
```

---

## 💡 **Tips**

1. **Use `jq` for pretty JSON**: `curl ... | jq`
2. **Save responses**: `curl ... > output.json`
3. **Test incrementally**: Start with simple queries
4. **Check server logs**: Look at `run.py` output for errors
5. **URL encode special characters**: Use `%20` for spaces

---

**All endpoints tested and working! ✅**