import streamlit as st
import google.generativeai as genai
import json
from datetime import datetime

# Configure API Key (replace with your valid API key)
API_KEY = "AIzaSyDX-UyxgsUZZiVBjfe4GFPxXOXEVjx_igQ"
genai.configure(api_key=API_KEY)

# Custom CSS for a sleek UI
st.markdown(
    """
    <style>
        .stApp {
            background: url("https://img.freepik.com/free-photo/abstract-luxury-gradient-blue-background-smooth-dark-blue-with-black-vignette-studio-banner_1258-88591.jpg?t=st=1740720028~exp=1740723628~hmac=9eeeeebee486cdafc07066d65bcc2753235900156857f43c67e60ff652b5eca5&w=1060");
            background-size: cover;
            background-attachment: fixed;
        }
        .main-title {
            color: #2b6777;
            font-size: 36px;
            text-align: center;
            font-weight: bold;
        }
        .sub-title {
            color: #2b6777;
            font-size: 24px;
            text-align: center;
        }
        .stButton button {
            background-color: #2b6777;
            color: white;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stButton button:hover {
            background-color: #2b6777;
            color: grey;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

def get_travel_recommendations(source, destination, travel_date):
    """
    Fetches travel recommendations using Gemini AI and returns structured JSON data.
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    query = f"""
    You are a smart travel assistant. Suggest travel options from {source} to {destination} for {travel_date}.
    Respond ONLY in JSON format as follows:
    {{
        "flights": [{{"airline": "Airline Name", "departure": "Time", "arrival": "Time", "duration": "Time", "cost": Amount}}],
        "trains": [{{"name": "Train Name", "departure": "Time", "arrival": "Time", "duration": "Time", "cost": Amount}}],
        "buses": [{{"operator": "Bus Operator", "departure": "Time", "arrival": "Time", "duration": "Time", "cost": Amount}}],
        "cabs": [{{"cost": Amount, "duration": "Time"}}]
    }}
    """
    try:
        response = model.generate_content(query)
        response_text = response.text.strip() if hasattr(response, 'text') else ""
        
        json_start = response_text.find("{")
        json_end = response_text.rfind("}")
        
        if json_start != -1 and json_end != -1:
            return json.loads(response_text[json_start:json_end+1])
        return {"error": "Invalid AI response format."}
    except json.JSONDecodeError:
        return {"error": "Error processing JSON response."}
    except Exception as e:
        return {"error": str(e)}

def generate_travel_summary(travel_info):
    """
    Generates a summary highlighting the best travel options.
    """
    summary = "### 🔹 Top Travel Options:\n"
    choices = []
    
    for mode in ["flights", "trains", "buses", "cabs"]:
        if mode in travel_info:
            choices.extend([(mode.capitalize(), option["cost"]) for option in travel_info[mode]])
    
    if choices:
        cheapest = min(choices, key=lambda x: x[1])
        summary += f"✔ Most Affordable: {cheapest[0]} at ₹{cheapest[1]}\n"
    
    if "flights" in travel_info:
        summary += "⚡ Fastest: Flights (usually 1-2 hours).\n"
    
    return summary

# Streamlit UI
st.markdown("<div class='main-title'>🌍 AI Travel Planner</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Plan your trip with real-time recommendations</div>", unsafe_allow_html=True)

origin = st.text_input("Enter Departure City")
destination = st.text_input("Enter Destination City")
date = st.date_input("Select Travel Date", min_value=datetime.today())

if st.button("Find Travel Options", use_container_width=True):
    if origin and destination:
        with st.spinner("Fetching travel options... 🚀"):
            travel_data = get_travel_recommendations(origin, destination, date.strftime("%Y-%m-%d"))
        
        if "error" in travel_data:
            st.error(travel_data["error"])
        else:
            st.success("Travel options loaded successfully! ✅")
            st.write(f"### Travel Options from {origin} to {destination} on {date.strftime('%B %d, %Y')}")
            st.write("---")
            st.markdown(generate_travel_summary(travel_data))
            
            for mode, emoji in zip(["flights", "trains", "buses", "cabs"], ["✈", "🚆", "🚌", "🚖"]):
                if travel_data.get(mode):
                    st.subheader(f"{emoji} {mode.capitalize()}")
                    for option in travel_data[mode]:
                        st.markdown(
                            f"""
                            <div style="border: 2px solid #52ab98; border-radius: 12px; padding: 15px; margin: 10px; background-color: #e3f6f5;">
                                <b>{mode.capitalize()} Details:</b><br>
                                {'<br>'.join([f'{key.capitalize()}: {value}' for key, value in option.items()])}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
    else:
        st.error("Please enter both departure and destination cities.")


# Let me know if you want me to add anything else or fine-tune the design further! 🚀
