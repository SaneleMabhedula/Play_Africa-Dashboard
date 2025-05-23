import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Sample data
df = pd.DataFrame({
    "Program Name": ["I am scientist", "Design thinking", "Creative Arts"],
    "Rating": [4.5, 4.8, 4.2],
    "No. of Children": [35, 25, 30]
})

# Set navy blue background with white text
st.markdown(
    """
    <style>
    .stApp {
        background-color: #001f3f; /* Navy blue */
        color: white;
    }
    .metric-box {
        background-color: #0a2d5a;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        color: white;
    }
    .css-1aumxhk {
        background-color: #003366;
        color: white;
    }
    /* Make all text white */
    body, h1, h2, h3, h4, h5, h6, p, div, span {
        color: white !important;
    }
    /* Style tables */
    .dataframe {
        background-color: #0a2d5a !important;
        color: white !important;
    }
    table {
        background-color: #0a2d5a !important;
        color: white !important;
    }
    th, td {
        background-color: #0a2d5a !important;
        color: white !important;
        border-color: #2a4a7a !important;
    }
    /* Style input fields */
    .stTextInput>div>div>input, 
    .stSelectbox>div>div>select, 
    .stTextArea>div>div>textarea,
    .stSlider>div>div>div>div {
        color: black !important;
        background-color: white !important;
    }
    /* Style buttons */
    .stButton>button {
        background-color: #003366 !important;
        color: white !important;
        border: 1px solid #2a4a7a !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and logo in same row
col1, col2 = st.columns([4, 1])
with col1:
    st.title("Play Africa Dashboard")
with col2:
    st.image("play_africa_logo.png", width= 120)

# Horizontal line divider
st.markdown("---")

# ------------------------
# Original Dataset
# ------------------------
original_data = {
    "Program Name": ["I am scientist", "Design thinking", "Creative Arts", "Design thinking","I am scientist"],
    "Program Rating (1-5)": [4.5, 4.8, 4.2, 4.0, 3.6],
    "No. of Children": [35, 25, 30, 40, 20]
}
df_original = pd.DataFrame(original_data)

# ------------------------
# Load Feedback Data (if exists)
# ------------------------
if os.path.exists("feedback.csv"):
    feedback_raw = pd.read_csv("feedback.csv")
    
    if not feedback_raw.empty:
        df_feedback = feedback_raw[["Program Name", "Rating (1-5)", "No. of Children"]].copy()
        df_feedback.rename(columns={"Rating (1-5)": "Program Rating (1-5)"}, inplace=True)
        df_combined = pd.concat([df_original, df_feedback], ignore_index=True)
    else:
        df_combined = df_original.copy()
else:
    df_combined = df_original.copy()

# ------------------------
# Key Metrics Section
# ------------------------
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_children = df_combined["No. of Children"].sum()
    st.markdown(
        f"""
        <div class="metric-box">
            <h3 style="color: #7fbfff; margin-top: 0;">Children Impacted</h3>
            <h2 style="color: white; text-align: center;">{total_children:,}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    avg_rating = df_combined["Program Rating (1-5)"].mean()
    st.markdown(
        f"""
        <div class="metric-box">
            <h3 style="color: #7fbfff; margin-top: 0;">Average Rating</h3>
            <h2 style="color: white; text-align: center;">{avg_rating:.1f}/5</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    num_programs = df_combined["Program Name"].nunique()
    st.markdown(
        f"""
        <div class="metric-box">
            <h3 style="color: #7fbfff; margin-top: 0;">Active Programs</h3>
            <h2 style="color: white; text-align: center;">{num_programs}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------
# Main Content with Tabs
# ------------------------
tab1, tab2, tab3 = st.tabs(["📊 Data & Visualizations", "📝 Feedback Form", "🗃️ Raw Data"])

with tab1:
    st.subheader("Program Performance")
    
    # Two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Average Rating by Program**")
        avg_ratings = df_combined.groupby("Program Name")["Program Rating (1-5)"].mean()
        st.bar_chart(avg_ratings, color="#7fbfff")
    
    with col2:
        st.markdown("**Program Participation**")
        participation = df_combined.groupby("Program Name")["No. of Children"].sum()
        
        # Create pie chart with navy blue theme
        fig, ax = plt.subplots(figsize=(6, 6))
        colors = ['#7fbfff', '#50c878', '#ffa07a']  # Blue, Green, Orange
        participation.plot.pie(autopct='%1.1f%%', startangle=90, 
                             colors=colors, ax=ax, wedgeprops={'edgecolor': '#001f3f'})
        
        # Set background color and text color
        fig.patch.set_facecolor('#001f3f')
        ax.set_facecolor('#001f3f')
        plt.setp(ax.texts, color='white')
        ax.set_ylabel('')  # Remove default ylabel
        
        st.pyplot(fig)
    
    st.markdown("---")
    st.subheader("Program Participation Data")
    participation_data = df_combined.groupby("Program Name")["No. of Children"].sum().reset_index()
    st.dataframe(participation_data.style.format({"No. of Children": "{:,}"}))

with tab2:
    st.subheader("Give Us Feedback")
    
    with st.form("feedback_form", clear_on_submit=True):
        name = st.text_input("Your Name")
        program = st.selectbox("Which Program?", df_original["Program Name"].unique())
        rating = st.slider("Rating (1-5)", 1.0, 5.0, 3.0, step=0.1)
        participants = st.number_input("No. of Children", min_value=1, step=1)
        comment = st.text_area("Any comments?")
        submitted = st.form_submit_button("Submit Feedback")

        if submitted:
            new_feedback = {
                "Name": name,
                "Program Name": program,
                "Rating (1-5)": rating,
                "No. of Children": participants,
                "Comments": comment
            }
            feedback_df = pd.DataFrame([new_feedback])
            feedback_df.to_csv("feedback.csv", mode="a", 
                             header=not os.path.exists("feedback.csv"), 
                             index=False)
            st.success("Thanks for your feedback! Refresh the page to update graphs.")
    
    st.markdown("---")
    st.subheader("Recent Feedback")
    if os.path.exists("feedback.csv"):
        fb_data = pd.read_csv("feedback.csv")
        st.dataframe(fb_data)
    else:
        st.info("No feedback submitted yet.")

with tab3:
    st.subheader("All Program Data")
    st.dataframe(df_combined)
    
    st.download_button(
        label="Download Data as CSV",
        data=df_combined.to_csv(index=False).encode('utf-8'),
        file_name='museum_programs_data.csv',
        mime='text/csv',
    )

# ------------------------
# Footer with Clear Button
# ------------------------
st.markdown("---")
if st.button("🗑️ Clear All Feedback"):
    if os.path.exists("feedback.csv"):
        os.remove("feedback.csv")
        st.success("All feedback has been cleared. Refresh the app to see updates.")
    else:
        st.warning("No feedback file exists to clear.")