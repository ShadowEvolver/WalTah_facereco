import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image
import datetime
import pandas as pd

from utils.recognition_utils import predict_identity
from utils.database import get_user_info
from utils.accounts import authenticate
from utils.schedule_utils import get_exams_for_examiner, get_schedule_entry

# Config
st.set_page_config(page_title="Exam Access System", layout="wide")

# Sidebar - login
st.sidebar.title("🔒 Examiner Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")
if st.sidebar.button("Log In"):
    if authenticate(username, password):
        st.sidebar.success("Logged in as %s" % username)
        st.session_state.logged_in = True
    else:
        st.sidebar.error("Invalid credentials")

def main_app(username):
    st.title(f"📝 Exam Session Dashboard ({username})")
    # Load exams
    exams = get_exams_for_examiner(username)
    if not exams:
        st.warning("No scheduled exams found for you.")
        return

    # Select exam
    halls = sorted({e['hall'] for e in exams})
    selected_hall = st.selectbox("Select Hall:", halls)
    timeslots = [e['timeslot'] for e in exams if e['hall']==selected_hall]
    selected_timeslot = st.selectbox("Select Timeslot:", timeslots)

    entry = get_schedule_entry(exams, selected_hall, selected_timeslot)
    if not entry:
        st.error("Schedule entry not found.")
        return

    st.write(f"**Examiner:** {username}  |  **Hall:** {selected_hall}  |  **Timeslot:** {selected_timeslot}")
    students = entry.get('students', [])
    scheduled_labels = {s['label']: s for s in students}

    st.markdown("---")
    st.header("🔍 Student Verification")
    # Initialize session state
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'verified' not in st.session_state:
        st.session_state.verified = False

    # Capture face
    img_file = st.camera_input("Place student face in front of the camera")
    if img_file is not None and not st.session_state.verified:
        image = Image.open(img_file)
        image_np = np.array(image)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        label, confidence = predict_identity(image_np)
        if label in scheduled_labels and confidence > 0.9:
            info = scheduled_labels[label]
            user_info = get_user_info(label)
            st.success(f"✅ {user_info['name']} verified (ID: {info['student_id']})")
            st.image(user_info['image'], width=150)
            st.write(f"**Hall:** {info['hall']}  |  **Seat #:** {info['number']}")
            # Log
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df = pd.DataFrame([[username, user_info['name'], label, confidence, ts]],
                               columns=["Examiner","Name","Label","Confidence","Timestamp"])
            os.makedirs('logs', exist_ok=True)
            df.to_csv('logs/access_log.csv', mode='a', header=False, index=False)
            st.session_state.verified = True
        else:
            st.session_state.attempts += 1
            st.warning(f"❌ Verification failed (Attempt {st.session_state.attempts}/3)")
            if st.session_state.attempts >= 3:
                st.error("🚨 Alert! Student could not be verified after 3 attempts.")
    
if st.session_state.get('logged_in'):
    main_app(username)
else:
    st.info("Please log in to continue.")