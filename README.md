
## 📱 Jumia Phone Tracker — Web Scraping Project

A data extraction tool built with **Scrapy** to crawl and collect mobile phone listings from [Jumia Nigeria](https://www.jumia.com.ng/mobile-phones/). The spider extracts structured product data and stores it into **MongoDB** for easy analysis and tracking.

---

### 🧰 Tech Stack

* **Scrapy** (Core framework)
* **MongoDB** (Data storage)
* **Custom Middleware**

  * `RotateHeadersMiddleware` – Randomly rotates user agents and languages to avoid detection
* **AutoThrottle** – Manages crawl speed dynamically based on site response time

---

### 📦 Features

* ✅ Crawls up to 4 pages of mobile phone listings (configurable)
* ✅ Designed to **scale to more pages** — page limit set to 4 intentionally to:

  * Avoid hammering Jumia’s servers
  * Stay within ethical scraping limits
  * Keep test runs short during development
* ✅ Extracts:

  * Product title
  * Price
  * Rating
  * Stock availability
  * Product URL
* ✅ Skips products with missing data gracefully
* ✅ Saves data directly to MongoDB in a collection named after the spider
* ✅ Logs pagination progress and crawl status

---

### 📁 Folder Structure

```shell
jumia_phone_tracker/
├── spiders/
│   └── phone_spider.py       # Main spider logic
├── middlewares.py            # Downloader & spider middleware, header rotation
├── pipelines.py              # MongoDB storage logic
├── settings.py               # All project settings
```

---

### 🚀 How to Run the Spider

1. **Install requirements**

   ```shell
   pip install scrapy pymongo
   ```

2. **Start MongoDB** (locally or with Atlas)

3. **Run the spider**

   ```shell
   scrapy crawl phone_spider
   ```

4. **Check MongoDB**
   Your data will be in the `jumia_phone_tracker.phone_spider` collection.

---

### ✅ Sample Output

```json
{
  "titles": "Samsung Galaxy A15",
  "prices": "₦123,000",
  "ratings": "4.3 out of 5",
  "availability": "Only 3 units left",
  "links": "https://www.jumia.com.ng/samsung-a15-4gb-128gb..."
}
```

---

### 📌 Notes

* The page limit is **configurable** and can easily be increased or removed for broader crawls.
* Keeping it to 4 pages during development was a conscious choice to:

  * Avoid triggering anti-bot systems
  * Respect the server load
  * Speed up testing and iteration
* This approach demonstrates **scalability** and **scraper etiquette**.
* Respects ethical scraping principles by limiting crawl depth and using throttling.
* Does **not** obey `robots.txt` (for educational purposes only).

---

### 💼 Portfolio Use

This project is perfect for showcasing:

* Custom Scrapy middleware development
* Integration with MongoDB
* Smart pagination and data cleaning
* Scalable scraping architecture
