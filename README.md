# 🌌 Delusion Search Engine

![Delusion Banner](file:///C:/Users/Home%20PC/.gemini/antigravity/brain/fc9b0f80-df34-4aba-bfd7-74d31823bdcd/delusion_search_banner_1775750082979.png)

**Delusion** is a high-performance, full-text search engine built from the ground up. It features a custom indexing pipeline, an optimized ranking algorithm, and a modern, responsive web interface. Designed to scrape, index, and search through Medium articles with lightning-fast autocomplete suggestions.

---

## 🚀 Key Features

- **Custom Indexing Engine**: Implements both Forward and Inverted indexing using a "barrel" system for efficient storage and retrieval.
- **Medium Article Scraper**: Automatically extract and index content, thumbnails, and metadata from Medium URLs.
- **Intelligent Ranking**: Proprietary ranking algorithm (`ranking.py`) that handles term frequency, proximity, and section weighting.
- **Blazing Fast Autocomplete**: Powered by a Trie-based algorithm for real-time word suggestions as you type.
- **Modern UI/UX**: Built with React, Vite, and Tailwind CSS, featuring smooth transitions, pagination, and a premium aesthetic.
- **State Management**: Robust state handling using Redux Toolkit for a seamless user experience.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Server**: Uvicorn
- **Data Processing**: NLTK, Regex
- **Index Storage**: Custom Binary/CSV Barrel System
- **API**: RESTful endpoints for Search, Scraping, and Autocomplete

### Frontend
- **Framework**: React.js (Vite)
- **Styling**: Tailwind CSS, Shadcn UI, Radix UI
- **State Management**: Redux Toolkit
- **Icons**: Lucide React, React Icons
- **HTTP Client**: Axios

---

## 📂 Project Structure

```text
Delusion/
├── client/                # React Vite Frontend
│   ├── src/               # React components, hooks, redux slices
│   ├── public/            # Static assets
│   └── tailwind.config.js # CSS System
├── src/                   # Python Backend
│   ├── server.py          # FastAPI Server entry point
│   ├── indexer.py         # Forward/Inverted indexing logic
│   ├── scraper.py         # Medium content extractor
│   ├── search_util.py     # Search query processor
│   ├── autocomplete.py    # Trie-based suggestion engine
│   └── word_processing.py # Text normalization and tagging
├── indexes/               # Storage for generated search barrels (binary/csv)
└── README.md              # Project Documentation
```

---

## ⚙️ Local Setup

### 1. Prerequisite
- Python 3.8+
- Node.js 18+
- npm or yarn

### 2. Backend Setup
```bash
cd src
pip install -r requirements.txt  # Ensure you create one if missing
python server.py
```
*The server will start at `http://localhost:8000`*

### 3. Frontend Setup
```bash
cd client
npm install
npm run dev
```
*The client will start at `http://localhost:5173`*

---

## 🧠 Behind the Scenes: How it Works

1. **Scraping**: `scraper.py` fetches the HTML from a Medium URL and extracts relevant content.
2. **Indexing**: The text is passed through `word_processing.py` (tagging, stemming, stop-word removal). `indexer.py` then assigns a `doc_id` and distributes term counts into respective barrels.
3. **Searching**: When a user queries, `search_util.py` retrieves matching `doc_ids` from the inverted barrels, and `ranking.py` computes the relevance score to return the top results.
4. **Suggestions**: Each keystroke in the search bar queries the Trie built from the `lexicon.csv` to provide instant suggestions.

---
