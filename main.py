import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from backend import get_data

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Weather Forecast",
    page_icon="🌤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
        min-height: 100vh;
    }

    /* Hide default Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2.5rem; padding-bottom: 2rem; max-width: 1000px; }

    /* Title */
    .hero-title {
        font-family: 'DM Serif Display', serif;
        font-size: clamp(2.2rem, 5vw, 3.5rem);
        color: #f0ecff;
        letter-spacing: -0.02em;
        line-height: 1.1;
        margin-bottom: 0.2rem;
    }
    .hero-subtitle {
        font-size: 0.95rem;
        color: #8b84b8;
        font-weight: 300;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 2.5rem;
    }

    /* Input and widgets */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        color: #f0ecff !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.7rem 1rem !important;
        transition: border-color 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(138, 99, 255, 0.7) !important;
        box-shadow: 0 0 0 3px rgba(138, 99, 255, 0.15) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #5e5a85 !important; }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 12px !important;
        color: #f0ecff !important;
    }

    /* Slider */
    .stSlider > div > div > div > div { background: #8a63ff !important; }
    .stSlider [data-testid="stThumbValue"] { color: #f0ecff !important; }
    label, .stSlider label, .stSelectbox label, .stTextInput label {
        color: #8b84b8 !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.06em !important;
        text-transform: uppercase !important;
    }

    /* Section header */
    .section-label {
        font-family: 'DM Serif Display', serif;
        font-size: 1.4rem;
        color: #f0ecff;
        margin: 1.8rem 0 1rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    /* Metric cards */
    .metric-row { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 1.2rem; }
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 14px;
        padding: 1rem 1.4rem;
        flex: 1;
        min-width: 120px;
        backdrop-filter: blur(10px);
    }
    .metric-card .label {
        font-size: 0.72rem;
        color: #6e6a96;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-bottom: 0.3rem;
    }
    .metric-card .value {
        font-family: 'DM Serif Display', serif;
        font-size: 1.8rem;
        color: #f0ecff;
        line-height: 1;
    }
    .metric-card .unit {
        font-size: 0.85rem;
        color: #8b84b8;
        margin-left: 2px;
    }

    /* Sky condition grid */
    .sky-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(88px, 1fr));
        gap: 10px;
        margin-top: 0.5rem;
    }
    .sky-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 12px;
        padding: 0.7rem 0.5rem;
        text-align: center;
        transition: background 0.2s;
    }
    .sky-card:hover { background: rgba(138,99,255,0.12); }
    .sky-card .time {
        font-size: 0.68rem;
        color: #6e6a96;
        letter-spacing: 0.05em;
        margin-bottom: 4px;
    }
    .sky-card .condition {
        font-size: 0.78rem;
        color: #c4bfee;
        margin-top: 4px;
        font-weight: 500;
    }

    /* Error box */
    .error-box {
        background: rgba(255, 80, 80, 0.1);
        border: 1px solid rgba(255, 80, 80, 0.25);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        color: #ff9f9f;
        font-size: 0.92rem;
        margin-top: 1rem;
    }

    /* Plotly chart background fix */
    .js-plotly-plot { border-radius: 16px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">Weather Forecast</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">5-day outlook · Powered by OpenWeatherMap</div>', unsafe_allow_html=True)

# ── Controls ──────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    place = st.text_input("City", placeholder="e.g. Tokyo, London, New York…", label_visibility="visible")

with col2:
    days = st.slider("Days", min_value=1, max_value=5, value=3)

with col3:
    option = st.selectbox("View", ("Temperature", "Sky Conditions"))

# ── Data & Visualisation ──────────────────────────────────────────────────────
CONDITION_EMOJI = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Snow": "❄️",
    "Thunderstorm": "⛈️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️",
}

SKY_IMAGES = {
    "Clear": "images/clear.png",
    "Clouds": "images/cloud.png",
    "Rain": "images/rain.png",
    "Snow": "images/snow.png",
}

if place:
    try:
        data = get_data(place, days)
        df = pd.DataFrame(
            [
                {
                    "datetime": entry["dt_txt"],
                    "temp": entry["main"]["temp"],
                    "feels_like": entry["main"]["feels_like"],
                    "humidity": entry["main"]["humidity"],
                    "condition": entry["weather"][0]["main"],
                    "description": entry["weather"][0]["description"].title(),
                }
                for entry in data
            ]
        )
        df["datetime"] = pd.to_datetime(df["datetime"])
        df["time_label"] = df["datetime"].dt.strftime("%-d %b %H:%M")

        # ── Summary metrics ──────────────────────────────────────────────────
        st.markdown(f'<div class="section-label">{place.title()} · Next {days} day{"s" if days > 1 else ""}</div>', unsafe_allow_html=True)

        avg_temp = df["temp"].mean()
        max_temp = df["temp"].max()
        min_temp = df["temp"].min()
        avg_humidity = df["humidity"].mean()

        st.markdown(
            f"""
            <div class="metric-row">
                <div class="metric-card">
                    <div class="label">Avg Temp</div>
                    <div class="value">{avg_temp:.0f}<span class="unit">°C</span></div>
                </div>
                <div class="metric-card">
                    <div class="label">High</div>
                    <div class="value">{max_temp:.0f}<span class="unit">°C</span></div>
                </div>
                <div class="metric-card">
                    <div class="label">Low</div>
                    <div class="value">{min_temp:.0f}<span class="unit">°C</span></div>
                </div>
                <div class="metric-card">
                    <div class="label">Humidity</div>
                    <div class="value">{avg_humidity:.0f}<span class="unit">%</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Temperature chart ────────────────────────────────────────────────
        if option == "Temperature":
            fig = go.Figure()

            # Feels-like area
            fig.add_trace(
                go.Scatter(
                    x=df["datetime"],
                    y=df["feels_like"],
                    mode="lines",
                    name="Feels Like",
                    line=dict(color="rgba(138,99,255,0.4)", width=1.5, dash="dot"),
                    fill=None,
                )
            )

            # Temp fill area
            fig.add_trace(
                go.Scatter(
                    x=df["datetime"],
                    y=df["temp"],
                    mode="lines+markers",
                    name="Temperature",
                    line=dict(color="#a78bfa", width=2.5, shape="spline"),
                    marker=dict(
                        size=7,
                        color=df["temp"],
                        colorscale=[[0, "#6366f1"], [0.5, "#a78bfa"], [1, "#f472b6"]],
                        line=dict(color="#1a1a3e", width=1.5),
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(138,99,255,0.07)",
                    hovertemplate="<b>%{x|%a %-d %b, %H:%M}</b><br>Temp: %{y:.1f}°C<extra></extra>",
                )
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans, sans-serif", color="#8b84b8", size=12),
                xaxis=dict(
                    showgrid=False,
                    showline=False,
                    tickfont=dict(color="#6e6a96", size=11),
                    tickformat="%a %-d",
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="rgba(255,255,255,0.05)",
                    showline=False,
                    ticksuffix="°C",
                    tickfont=dict(color="#6e6a96", size=11),
                    zeroline=False,
                ),
                legend=dict(
                    bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#8b84b8"),
                    orientation="h",
                    x=0,
                    y=1.08,
                ),
                margin=dict(l=10, r=10, t=30, b=10),
                height=320,
                hovermode="x unified",
                hoverlabel=dict(
                    bgcolor="#1a1a3e",
                    bordercolor="#8a63ff",
                    font=dict(color="#f0ecff", family="DM Sans"),
                ),
            )

            st.plotly_chart(fig, use_container_width=True)

        # ── Sky conditions grid ──────────────────────────────────────────────
        elif option == "Sky Conditions":
            # Try image display first, fall back to emoji grid
            image_map = {
                "Clear": "images/clear.png",
                "Clouds": "images/cloud.png",
                "Rain": "images/rain.png",
                "Snow": "images/snow.png",
            }

            # Build emoji cards for every 3-hour slot
            cards_html = '<div class="sky-grid">'
            for _, row in df.iterrows():
                emoji = CONDITION_EMOJI.get(row["condition"], "🌡️")
                cards_html += f"""
                <div class="sky-card">
                    <div class="time">{row['datetime'].strftime('%-d %b')}<br>{row['datetime'].strftime('%H:%M')}</div>
                    <div style="font-size:1.8rem">{emoji}</div>
                    <div class="condition">{row['condition']}</div>
                </div>"""
            cards_html += "</div>"
            st.markdown(cards_html, unsafe_allow_html=True)

            # Attempt to show images if they exist
            available = [r for r in df["condition"] if r in image_map]
            if available:
                st.markdown("---")
                try:
                    image_paths = [image_map[c] for c in df["condition"] if c in image_map]
                    st.image(image_paths, width=100)
                except Exception:
                    pass  # images folder not present, emoji grid is enough

    except (ValueError, ConnectionError) as e:
        st.markdown(f'<div class="error-box">⚠️ {e}</div>', unsafe_allow_html=True)
    except Exception as e:
        st.markdown(
            f'<div class="error-box">⚠️ Something went wrong. Please try again.<br><small>{e}</small></div>',
            unsafe_allow_html=True,
        )

elif not place:
    st.markdown(
        '<p style="color:#5e5a85;font-size:0.95rem;margin-top:1.5rem;">Enter a city name above to get started.</p>',
        unsafe_allow_html=True,
    )
