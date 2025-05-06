# ☕ Coffee Yield Forecast Web App Prototype

This is a demo web application that helps coffee farmers forecast their yield using image analysis, location-based weather data, and basic farm information. The prototype is built using Python, Supabase, Docker, and AI models.

---

## ✅ Features

- 👤 User authentication via Supabase Auth (email + password)
- 🧾 Chat interface for collecting:
  - Image of coffee trees
  - Farm area (hectares)
  - Number of coffee trees
  - Farm location
- 📷 Image analyzed using a pretrained AI model to assess plant health
- ☁️ Weather data fetched via Weather API (based on farm location)
- 🧠 Yield is forecasted using a custom logic combining image health, weather, and planting density
- 🗃️ Full chat and forecast history stored in Supabase DB
- 🌐 Basic frontend with Streamlit (or your choice)
- 🧱 Dockerized setup for local development

---

## 🛠️ Tech Stack

| Layer       | Tool/Service              |
|------------|----------------------------|
| Frontend   | Streamlit (Python)         |
| Backend    | Python AI Models           |
| Auth       | Supabase Auth              |
| Database   | Supabase PostgreSQL        |
| File Store | Supabase Storage (image)   |
| Weather    | OpenWeatherMap API         |
| AI Model   | Custom pretrained model    |
| DevOps     | Docker, WSL2               |

---

## 🧩 Entity Relationship Diagram (ERD)

See Miro link: [ERD on Miro](https://miro.com/app/board/uXjVI6Mz6WQ=/?share_link_id=134966694701)

Main tables:
- `profiles` (extra info)
- `conversations_state`
- `conversation_history`
---

## 🔄 Sequence Diagram

See Miro link: [Sequence Diagram on Miro](https://miro.com/app/board/uXjVI5yIqQM=/?share_link_id=407793621933)

---

## 🧠 Yield Forecast Logic

1. Analyze uploaded image to assess plant health score
2. Retrieve weather at farm location (rainfall, temperature)
3. Combine:
   - Health score
   - Weather data
   - Planting density (`trees / area`)
4. Estimate `yield (kg/hectare)` based on heuristic formula

Note: Exact model and weights chosen based on real-world agronomy heuristics and AI intuition.

---

## 🚀 How to Run Locally

### 1. Prerequisites

- Docker + Docker Desktop
- Supabase CLI
- Python 3.10+
- WSL2 (if on Windows)

### 2. Setup Supabase

```bash
supabase start
```

### 3. Run App

```bash
git clone https://github.com/tantran1011/CoffeeBeanOnTrees.git
pip install requirements.txt
streamlit run src/main.py --server.fileWatcherType none
```

## 📌 Notes
This is a demo, not production-ready

Authentication, image upload, and yield logic all work end-to-end

You can test with sample images provided in /models/test1.jpg

Contact me at: tantran1011@gmail.com

## 📎 Submission Info
GitHub Repo: https://github.com/tantran1011/CoffeeBeanOnTrees.git

Miro Board (ERD + Sequence): Miro Link

Assignment by: RegenX (AI Agvisory Internship)


