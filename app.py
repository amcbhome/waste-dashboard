import streamlit as st
from fetch_and_store import update_database
from database import get_upcoming_collections

st.set_page_config(page_title="Bin Collection Dashboard", layout="centered")

st.title("♻️ Bin Collection Dashboard")

# --- Input ---
uprn = st.text_input("Enter UPRN", value="127072473")

# --- Button ---
if st.button("Access current information"):
    try:
        count = update_database(uprn)
        st.success(f"Retrieved and stored {count} events")
    except Exception as e:
        st.error(str(e))

# --- Display Data ---
st.subheader("Upcoming Collections")

rows = get_upcoming_collections()

if rows:
    for date, type_ in rows:
        st.write(f"📅 {date} — {type_}")
else:
    st.info("No data available. Click the button above.")
