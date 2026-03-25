import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import os
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Civic AI Platform",
    page_icon="🏙️",
    layout="wide"
)

# ================================
# CUSTOM CSS (UI DESIGN)
# ================================

st.markdown("""
<style>

.main {
background-color: #0E1117;
}

h1, h2, h3 {
color: #38bdf8;
}

.stButton>button{
background: linear-gradient(90deg,#06b6d4,#3b82f6);
color:white;
border-radius:8px;
border:none;
padding:10px 20px;
font-weight:bold;
}

.stButton>button:hover{
background: linear-gradient(90deg,#3b82f6,#06b6d4);
}

</style>
""", unsafe_allow_html=True)
# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.title("🏙️ Civic AI System")

page = st.sidebar.radio(
    "Navigate",
    ["Issue Detection", "Verification", "Issues Dashboard", "Analytics"]
)

# ======================================================
# PAGE 1 — DETECTION
# ======================================================

if page == "Issue Detection":

    st.markdown('<p class="big-title">📍 Civic Issue Detection</p>', unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload Civic Image", type=["jpg","jpeg","png"])

    if uploaded:

        st.image(uploaded, caption="Uploaded Image", use_container_width=True)

        if st.button("🚀 Detect Issue"):

            with st.spinner("Running AI detection..."):

                res = requests.post(
                    f"{API_URL}/detect",
                    files={"file":(uploaded.name, uploaded.getvalue(), uploaded.type)}
                )

            if res.status_code == 200:

                data = res.json()

                st.success("Detection Completed")

                if data.get("annotated_image"):

                    st.image(
                        data["annotated_image"],
                        caption="Detected Issue",
                        use_container_width=True
                    )

                col1,col2 = st.columns(2)

                with col1:
                    st.metric("Issue Type", data.get("issue_type"))
                    st.metric("Priority", data.get("priority"))

                with col2:
                    st.metric("Department", data.get("department"))
                    st.metric("Status", data.get("status"))

                st.subheader("Detection Details")

                conf = data.get("confidence")

                if conf:
                    st.metric("Confidence", f"{conf*100:.2f}%")

                if data.get("bbox"):
                    st.code(data["bbox"])

                lat = data.get("lat")
                lon = data.get("lon")

                st.subheader("Location")

                st.write("Latitude:",lat)
                st.write("Longitude:",lon)

                if lat and lon:
                    map_df = pd.DataFrame({"lat":[lat],"lon":[lon]})
                    st.map(map_df)

            else:
                st.error("Detection failed")


# ======================================================
# PAGE 2 — VERIFICATION
# ======================================================

# ======================================================
# PAGE 2 — VERIFICATION
# ======================================================

elif page == "Verification":

    st.markdown('<p class="big-title">✅ Issue Verification</p>', unsafe_allow_html=True)

    # 1. Add a text input so the user can specify which issue they are resolving
    issue_id = st.text_input("Enter the Issue ID to verify (e.g., from the Dashboard):")

    uploaded = st.file_uploader("Upload Repair Image", type=["jpg","jpeg","png"])

    # 2. Only proceed if BOTH the ID and the image are provided
    if uploaded and issue_id:

        st.image(uploaded, caption="Repair Image Uploaded", use_container_width=True)

        if st.button("Verify Resolution"):

            with st.spinner("Verifying repair..."):

                # 3. Send BOTH the file and the issue_id to the backend
                res = requests.post(
                    f"{API_URL}/verify",
                    files={"file": (uploaded.name, uploaded.getvalue(), uploaded.type)},
                    data={"issue_id": issue_id}  # <--- THIS IS THE MAGIC LINE
                )

            if res.status_code == 200:

                data = res.json()

                st.success("Verification Completed")

                # =========================
                # SHOW ORIGINAL + RESOLVED
                # =========================

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Original Issue")
                    if data.get("original_image"):
                        # Get the folder where app.py lives (frontend/)
                        current_dir = os.path.dirname(os.path.abspath(__file__))

                        # Go up one level to the main project folder
                        parent_dir = os.path.dirname(current_dir)

                        # Combine it with the 'uploads/...' path from the database
                        full_image_path = os.path.join(parent_dir, data["original_image"])

                        # Force forward slashes for the web browser
                        clean_original = full_image_path.replace("\\", "/")

                        # Display it!
                        try:
                            st.image(clean_original, use_container_width=True)
                        except Exception as e:
                            st.error(f"Image found in DB, but missing from folder: {clean_original}")

                with col2:
                    st.subheader("Resolved Image")
                    st.image(uploaded, use_container_width=True)

                st.divider()

                col3, col4 = st.columns(2)

                with col3:
                    st.metric("Status", data.get("status"))

                with col4:
                    st.metric("Verification Result", data.get("verification"))

            else:
                st.error(f"Verification failed: {res.text}")

# ======================================================
# PAGE 3 — DASHBOARD
# ======================================================

elif page == "Issues Dashboard":

    st.markdown('<p class="big-title">📊 Issues Dashboard</p>', unsafe_allow_html=True)

    try:

        res = requests.get(f"{API_URL}/issues")

        if res.status_code == 200:

            issues = res.json()

            if len(issues)==0:

                st.info("No issues recorded yet")

            else:

                df = pd.DataFrame(issues)

                st.dataframe(df,use_container_width=True)

        else:
            st.error("Failed to fetch issues")

    except Exception:
        st.warning("Backend not reachable")


# ======================================================
# PAGE 4 — ANALYTICS
# ======================================================

elif page == "Analytics":

    st.markdown('<p class="big-title">📈 Civic Intelligence Analytics</p>', unsafe_allow_html=True)

    try:

        res = requests.get(f"{API_URL}/issues")

        if res.status_code != 200:
            st.error("Failed to load data")

        else:

            issues = res.json()

            if len(issues)==0:

                st.info("No data available")

            else:

                df = pd.DataFrame(issues)

                # =========================
                # KPI METRIC CARDS
                # =========================

                col1,col2,col3,col4 = st.columns(4)

                with col1:
                    st.metric("Total Issues",len(df))

                with col2:
                    st.metric("High Priority",len(df[df["priority"]=="HIGH"]))

                with col3:
                    st.metric("Departments",df["department"].nunique())

                with col4:
                    st.metric("Resolved",len(df[df["status"]=="CLOSED"]))

                st.divider()

                # =========================
                # CHARTS
                # =========================

                col1,col2 = st.columns(2)

                with col1:

                    fig = px.pie(
                        df,
                        names="priority",
                        color="priority",
                        color_discrete_map={
                            "HIGH":"red",
                            "MEDIUM":"orange",
                            "LOW":"green"
                        }
                    )

                    st.plotly_chart(fig,use_container_width=True)

                with col2:

                    fig = px.bar(
                        df,
                        x="department",
                        color="department",
                        title="Department Workload"
                    )

                    st.plotly_chart(fig,use_container_width=True)

                st.divider()

                fig = px.histogram(
                    df,
                    x="status",
                    color="status",
                    title="Issue Status"
                )

                st.plotly_chart(fig,use_container_width=True)

    except Exception:

        st.warning("Backend not reachable")