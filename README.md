# 🌤 Skycast — Weather Forecast App

A clean, interactive weather forecast app built with **Python + Streamlit**. Search any city in the world and get a 5-day temperature and sky condition forecast powered by the OpenWeatherMap API.

## Features
- 🔍 Search weather for any city worldwide
- 🌡️ Temperature forecast chart with feels-like overlay
- ☁️ Sky condition view (Clear, Cloudy, Rain, Snow)
- 📅 Adjustable forecast range — 1 to 5 days
- ⚡ Lightweight and fast — runs locally or on Streamlit Cloud

## Tech Stack
- **Python** — core language
- **Streamlit** — web UI framework
- **Plotly** — interactive charts
- **OpenWeatherMap API** — live weather data
- **python-dotenv** — secure API key management

## Setup

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
pip install -r requirements.txt
streamlit run main.py
```

Create a `.env` file and add your API key:
```
OPENWEATHER_API_KEY=your_key_here
```
Get a free key at [openweathermap.org](https://openweathermap.org/api)
