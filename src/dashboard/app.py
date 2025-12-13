import os
import requests
import streamlit as st
import pandas as pd
import logging

# Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dashboard")

st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("🎓 Student Performance Dashboard")
st.caption("UI → FastAPI → PostgreSQL")

# Você pode definir por env var, ou manter default local
API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
print("API_BASE_URL", API_BASE_URL)

@st.cache_data(ttl=10)
def fetch_students():
    logger.info("[DASHBOARD] GET /students")
    try:
        resp = requests.get(f"{API_BASE_URL}/students", timeout=5)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API connection error: {e}")
        st.info("Make sure the FastAPI server is running and the API Base URL is correct.")
        return []

def create_student(payload: dict):
    logger.info(f"[DASHBOARD] POST /students (id={payload['student_id']})")
    resp = requests.post(f"{API_BASE_URL}/students", json=payload, timeout=5)
    if resp.status_code >= 400:
        return False, resp.text
    return True, resp.json()

def update_student(student_id: int, payload: dict):
    resp = requests.put(f"{API_BASE_URL}/students/{student_id}", json=payload, timeout=5)
    if resp.status_code >= 400:
        return False, resp.text
    return True, resp.json()

def delete_student(student_id: int):
    resp = requests.delete(f"{API_BASE_URL}/students/{student_id}", timeout=5)
    if resp.status_code >= 400:
        return False, resp.text
    return True, resp.json()

# Sidebar
st.sidebar.header("⚙️ Config")
api_url_input = st.sidebar.text_input("API Base URL", API_BASE_URL)
if api_url_input and api_url_input != API_BASE_URL:
    API_BASE_URL = api_url_input

st.sidebar.divider()

st.sidebar.header("➕ Add Student")
with st.sidebar.form("add_student_form"):
    student_id = st.number_input("student_id", min_value=1, step=1)
    name = st.text_input("name")
    age = st.number_input("age", min_value=0, step=1)
    gender = st.text_input("gender (e.g., Male/Female)")
    subject = st.text_input("subject (e.g., Math)")
    marks = st.number_input("marks", min_value=0, max_value=100, step=1)

    submitted = st.form_submit_button("Create")
    if submitted:
        payload = {
            "student_id": int(student_id),
            "name": name.strip(),
            "age": int(age),
            "gender": gender.strip(),
            "subject": subject.strip(),
            "marks": int(marks),
        }
        ok, data = create_student(payload)
        if ok:
            st.success("Student created!")
            st.cache_data.clear()
        else:
            st.error(f"Failed to create student: {data}")

# Main: Load data
try:
    students = fetch_students()
except Exception as e:
    st.error(f"Could not fetch students from API: {e}")
    st.stop()

df = pd.DataFrame(students)
if df.empty:
    st.info("No students found. Add one using the sidebar.")
    st.stop()

# Filters
col1, col2, col3 = st.columns(3)
with col1:
    subjects = ["All"] + sorted(df["subject"].dropna().unique().tolist())
    selected_subject = st.selectbox("Filter by subject", subjects)

with col2:
    genders = ["All"] + sorted(df["gender"].dropna().unique().tolist())
    selected_gender = st.selectbox("Filter by gender", genders)

with col3:
    top_n = st.slider("Top N students", min_value=3, max_value=20, value=5, step=1)

filtered = df.copy()
filtered = filtered[['student_id'] + [col for col in filtered.columns if col != 'student_id']]
if selected_subject != "All":
    filtered = filtered[filtered["subject"] == selected_subject]
if selected_gender != "All":
    filtered = filtered[filtered["gender"] == selected_gender]

# KPIs
k1, k2, k3, k4 = st.columns(4)
k1.metric("Students", len(filtered))
k2.metric("Avg marks", round(filtered["marks"].mean(), 2))
k3.metric("Min marks", int(filtered["marks"].min()))
k4.metric("Max marks", int(filtered["marks"].max()))

st.divider()

left, right = st.columns([2, 1])

with left:
    st.subheader("📋 Students")
    st.dataframe(filtered.sort_values(["student_id"], ascending=True), use_container_width=True)

with right:
    st.subheader("📈 Average marks by subject")
    avg_by_subject = df.groupby("subject")["marks"].mean().sort_values(ascending=False)
    st.bar_chart(avg_by_subject)

st.divider()

center = st.columns(1)[0]
with center:
    st.subheader(f"🏅 Top {top_n}")
    top_df = df.sort_values("marks", ascending=False).head(top_n)[
        ["student_id", "name", "subject", "marks"]
    ]
    st.table(top_df)

st.divider()

st.subheader("🛠️ Manage Student")
student_ids = ["None"] + sorted(df["student_id"].tolist())
selected_id = st.selectbox("Select student_id", student_ids)

action_col1, action_col2 = st.columns(2)

with action_col1:
    st.write("Update selected student (partial)")
    with st.form("update_student_form"):
        new_name = st.text_input("name (optional)")
        new_age = st.text_input("age (optional)")
        new_gender = st.text_input("gender (optional)")
        new_subject = st.text_input("subject (optional)")
        new_marks = st.text_input("marks (optional)")

        update_submit = st.form_submit_button("Update")
        if update_submit:
            payload = {}
            if new_name.strip():
                payload["name"] = new_name.strip()
            if new_age.strip():
                payload["age"] = int(new_age)
            if new_gender.strip():
                payload["gender"] = new_gender.strip()
            if new_subject.strip():
                payload["subject"] = new_subject.strip()
            if new_marks.strip():
                payload["marks"] = int(new_marks)

            if not payload:
                st.warning("No fields provided.")
            else:
                ok, data = update_student(int(selected_id), payload)
                if ok:
                    st.success("Student updated!")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Failed to update: {data}")

with action_col2:
    st.write("Delete selected student")
    if st.button("Delete", type="primary"):
        ok, data = delete_student(int(selected_id))
        if ok:
            st.success("Student deleted!")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error(f"Failed to delete: {data}")