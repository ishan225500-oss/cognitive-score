import streamlit as st
import numpy as np
import pickle
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- DATABASE ----------------
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS history(
            username TEXT,
            sleep REAL, stress REAL, sleep_quality REAL,
            exercise REAL, screen REAL, work REAL,
            heart REAL, caffeine REAL, prediction REAL)''')

conn.commit()

# ---------------- MODEL ----------------
model = pickle.load(open("model.pkl", "rb"))

# ---------------- AUTH ----------------
def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()

def signup_user(username, password):
    c.execute("INSERT INTO users VALUES(?, ?)", (username, password))
    conn.commit()

def save_history(data):
    c.execute("INSERT INTO history VALUES(?,?,?,?,?,?,?,?,?,?)", data)
    conn.commit()

def get_history(username):
    c.execute("SELECT * FROM history WHERE username=?", (username,))
    return c.fetchall()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- LOGIN ----------------
if not st.session_state.logged_in:

    st.title("🔐 Login / Signup")

    choice = st.radio("Select Option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            try:
                signup_user(username, password)
                st.success("Account created! Please login.")
            except:
                st.error("Username already exists")

    else:
        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully")
            else:
                st.error("Invalid credentials")

# ---------------- MAIN APP ----------------
else:

    st.title("🧠 Cognitive Performance Analyzer")
    st.write(f"Welcome, **{st.session_state.username}**")

    # ---------------- EXPLANATION ----------------
    with st.expander("🧠 What is Cognitive Score?"):
        st.write("""
        Cognitive Score is a predicted measure of your mental performance.

        It estimates:
        - Focus and concentration  
        - Memory efficiency  
        - Decision-making ability  

        ### 📊 Score Meaning:
        - **80+ → High Performance**
        - **60–79 → Moderate**
        - **<60 → Needs Improvement**

        ⚠️ This is an ML-based estimate, not a medical diagnosis.
        """)

    # ---------------- INPUT ----------------
    st.header("📥 Enter Your Lifestyle Data")

    sleep = st.slider("Sleep Duration (hrs)", 0.0, 12.0, 7.0)

    st.info("Stress Guide: 1–3 Low | 4–6 Moderate | 7–10 High")
    stress = st.slider("Stress Score", 1, 10, 5)

    sleep_quality = st.slider("Sleep Quality (1–10)", 1, 10, 7)
    exercise = st.slider("Exercise (days/week)", 0, 7, 3)
    screen = st.slider("Screen Time Before Bed (mins)", 0, 180, 60)
    work = st.slider("Work Hours", 0, 16, 8)

    st.info("Heart Rate: 60–80 Normal")
    heart = st.slider("Resting Heart Rate", 40, 120, 70)

    caffeine = st.slider("Caffeine Before Bed (mg)", 0, 500, 100)

    # ---------------- PREDICT ----------------
    if st.button("Predict"):

        input_data = np.array([[sleep, stress, sleep_quality,
                                exercise, screen, work,
                                heart, caffeine]])

        prediction = model.predict(input_data)[0]

        st.header("🎯 Result")

        if prediction >= 80:
            level = "High 🟢"
        elif prediction >= 60:
            level = "Moderate 🟡"
        else:
            level = "Low 🔴"

        st.metric("Cognitive Score", round(prediction, 2))
        st.write(f"Performance Level: **{level}**")

        # Save history
        save_history((
            st.session_state.username,
            sleep, stress, sleep_quality,
            exercise, screen, work,
            heart, caffeine, prediction
        ))

        # ---------------- GRAPH ----------------
        fig, ax = plt.subplots()
        ax.bar(["Your Score", "Average"], [prediction, 70])
        st.pyplot(fig)

        # ---------------- WHY RESULT ----------------
        st.subheader("🔍 Why did you get this score?")

        reasons = []

        if sleep < 6:
            reasons.append("Low sleep reduces focus")
        if stress > 7:
            reasons.append("High stress affects decision-making")
        if sleep_quality < 5:
            reasons.append("Poor sleep quality reduces brain recovery")
        if exercise < 2:
            reasons.append("Low activity impacts brain health")
        if screen > 90:
            reasons.append("High screen time affects sleep cycle")
        if caffeine > 300:
            reasons.append("Excess caffeine disrupts sleep")

        if reasons:
            for r in reasons:
                st.write("•", r)
        else:
            st.write("Your habits are well balanced 👍")

        # ---------------- SUGGESTIONS ----------------
        st.subheader("💡 Improvement Tips")

        if sleep < 6:
            st.write("• Sleep 7–8 hours")
        if stress > 7:
            st.write("• Practice meditation")
        if exercise < 2:
            st.write("• Add physical activity")
        if screen > 90:
            st.write("• Reduce screen time before bed")
        if caffeine > 300:
            st.write("• Limit caffeine intake")

    # ---------------- HISTORY ----------------
    st.subheader("📜 Your Past Records")

    history = get_history(st.session_state.username)

    if history:
        df = pd.DataFrame(history, columns=[
            "User","Sleep","Stress","SleepQ","Exercise",
            "Screen","Work","Heart","Caffeine","Score"
        ])
        st.dataframe(df)

        st.write("📈 Average Score:", round(df["Score"].mean(), 2))
    else:
        st.write("No history available")

    # ---------------- FAQ ----------------
    st.header("❓ FAQs")

    with st.expander("Is this medically accurate?"):
        st.write("No, this is a predictive ML model, not a clinical tool.")

    with st.expander("Why is my score low?"):
        st.write("Usually due to poor sleep, high stress, or lifestyle imbalance.")

    with st.expander("Can I improve my score?"):
        st.write("Yes, improving sleep, reducing stress, and exercising helps.")

    with st.expander("Why ensemble model?"):
        st.write("Multiple models improve accuracy and reduce errors.")

    with st.expander("Is my data safe?"):
        st.write("Data is stored locally per user for history tracking.")

    # ---------------- LOGOUT ----------------
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
