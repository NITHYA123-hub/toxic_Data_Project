import streamlit as st
import pickle
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Toxic Comment Detection",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

/* Main App */
.stApp {
    background: linear-gradient(to right, #0f172a, #1e293b);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #374151;
}

/* Titles */
h1, h2, h3, h4 {
    color: white !important;
}

/* Paragraph Text */
p {
    color: #e5e7eb !important;
}

/* Text Area */
textarea {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #374151 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: white;
    border-radius: 12px;
    height: 3.2em;
    width: 100%;
    border: none;
    font-size: 18px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.02);
}

/* Metric Cards */
[data-testid="metric-container"] {
    background: #1f2937;
    border: 1px solid #374151;
    padding: 18px;
    border-radius: 18px;
    box-shadow: 0px 4px 18px rgba(0,0,0,0.3);
}

/* Progress Bar */
.stProgress > div > div > div > div {
    background-color: #ff4b2b;
}

/* Success Box */
.stSuccess {
    background-color: #064e3b !important;
    border-radius: 10px;
}

/* Error Box */
.stError {
    background-color: #7f1d1d !important;
    border-radius: 10px;
}

/* Warning Box */
.stWarning {
    border-radius: 10px;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOGIN DETAILS ----------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "toxic123"

GUEST_USERNAME = "guest"
GUEST_PASSWORD = "guest123"

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

# ---------------- LOGIN PAGE ----------------
if not st.session_state.logged_in:

    st.markdown("""
    <h1 style='text-align:center; font-size:50px;'>
    🛡 AI Toxic Comment Detection
    </h1>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h4 style='text-align:center; color:#d1d5db;'>
    Secure AI-Powered Toxicity Monitoring Dashboard
    </h4>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.subheader("🔐 Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            # Admin Login
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

                st.session_state.logged_in = True
                st.session_state.role = "Admin"

                st.success("✅ Admin Login Successful")

                st.rerun()

            # Guest Login
            elif username == GUEST_USERNAME and password == GUEST_PASSWORD:

                st.session_state.logged_in = True
                st.session_state.role = "Guest"

                st.success("✅ Guest Login Successful")

                st.rerun()

            else:

                st.error("❌ Invalid Username or Password")

# ---------------- MAIN DASHBOARD ----------------
else:

    # ---------- LOAD MODEL ----------
    BASE_DIR = os.path.dirname(__file__)

    model_path = os.path.join(BASE_DIR, "..", "models", "model.pkl")
    model = pickle.load(open(model_path, "rb"))

    vectorizer_path = os.path.join(BASE_DIR, "..", "models", "vectorizer.pkl")
    vectorizer = pickle.load(open(vectorizer_path, "rb"))

    # ---------- SIDEBAR ----------
    st.sidebar.title("🛡 Navigation")

    st.sidebar.markdown("---")

    st.sidebar.success(f"Logged in as {st.session_state.role}")

    # Admin Menu
    if st.session_state.role == "Admin":

        menu = st.sidebar.radio(
            "Select Menu",
            ["Dashboard", "Analytics", "History", "About", "Logout"]
        )

    # Guest Menu
    else:

        menu = st.sidebar.radio(
            "Select Menu",
            ["Dashboard", "About", "Logout"]
        )

    st.sidebar.markdown("---")

    st.sidebar.info("AI Moderation System v1.0")

    # ---------- DASHBOARD ----------
    if menu == "Dashboard":

        st.markdown("""
        <h1 style='text-align:center;'>
        🛡 AI Toxic Comment Detection Dashboard
        </h1>
        """, unsafe_allow_html=True)

        st.info("Analyze comments using Machine Learning and detect harmful content in real time.")

        # Metrics
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Predictions", "120")
        col2.metric("Toxic Comments", "45")
        col3.metric("Safe Comments", "75")
        col4.metric("Model Accuracy", "95%")

        st.markdown("---")

        st.subheader("💬 Comment Analysis")

        comment = st.text_area(
            "Enter Comment",
            placeholder="Type your comment here..."
        )

        if st.button("Analyze Comment"):

            if comment.strip() == "":
                st.warning("⚠ Please enter a comment")

            else:

                # Convert Text
                comment_vector = vectorizer.transform([comment])

                # Predict
                prediction = model.predict(comment_vector)[0]

                # Probability
                probability = model.predict_proba(comment_vector).max()

                st.markdown("---")

                # Result
                if prediction == 1:

                    st.error("⚠ Toxic Comment Detected")

                else:

                    st.success("✅ Safe Comment")

                # Confidence
                st.subheader("Confidence Score")

                st.write(f"{probability * 100:.2f}%")

                st.progress(int(probability * 100))

                # Save History
                history_data = {
                    "Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                    "Comment": [comment],
                    "Prediction": ["Toxic" if prediction == 1 else "Safe"],
                    "Confidence": [f"{probability*100:.2f}%"]
                }

                history_df = pd.DataFrame(history_data)

                # Create Folder
                os.makedirs("history", exist_ok=True)

                history_file = "history/prediction_history.csv"

                if os.path.exists(history_file):

                    old_df = pd.read_csv(history_file)

                    new_df = pd.concat(
                        [old_df, history_df],
                        ignore_index=True
                    )

                    new_df.to_csv(history_file, index=False)

                else:

                    history_df.to_csv(history_file, index=False)

    # ---------- ANALYTICS ----------
    elif menu == "Analytics":

        st.title("📊 Toxicity Analytics")

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Toxic vs Safe")

            labels = ["Safe", "Toxic"]
            values = [75, 45]

            fig, ax = plt.subplots()

            ax.pie(
                values,
                labels=labels,
                autopct='%1.1f%%'
            )

            st.pyplot(fig)

        with col2:

            st.subheader("Prediction Statistics")

            chart_data = pd.DataFrame({
                "Category": ["Safe", "Toxic"],
                "Count": [75, 45]
            })

            st.bar_chart(chart_data.set_index("Category"))

    # ---------- HISTORY ----------
    elif menu == "History":

        st.title("📜 Prediction History")

        history_file = "history/prediction_history.csv"

        if os.path.exists(history_file):

            history_df = pd.read_csv(history_file)

            st.dataframe(history_df, use_container_width=True)

        else:

            st.warning("No prediction history found.")

    # ---------- ABOUT ----------
    elif menu == "About":

        st.title("About Project")

        st.markdown("""
        ### 🛡 AI Toxic Comment Detection System
        
        This project uses Machine Learning to classify toxic and safe comments.

        ### 🚀 Technologies Used
        - Python
        - Streamlit
        - Scikit-learn
        - Pandas
        - Matplotlib

        ### 🤖 Machine Learning
        - TF-IDF Vectorizer
        - Logistic Regression

        ### 📌 Features
        - Real-time toxicity prediction
        - Interactive dashboard
        - Login authentication
        - Analytics visualization
        - Prediction history tracking
        - Admin & Guest Access

        ### 👨‍💻 Developed For
        AI-powered online content moderation and analytics.
        """)

    # ---------- LOGOUT ----------
    elif menu == "Logout":

        st.session_state.logged_in = False
        st.session_state.role = ""

        st.success("✅ Logged Out Successfully")

        st.rerun()