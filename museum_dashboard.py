import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


import streamlit as st
import pandas as pd

# Sample data
df = pd.DataFrame({
    "Program Name": ["Robotics", "Math Games", "Eco Warriors"],
    "Rating": [4.5, 3.8, 4.2],
    "Participants": [35, 25, 30]
})

# Set background to light blue using CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #d6f0ff; /* Light blue */
    }
    .styled-table {
        background-color: #fffacd; /* Light yellow */
        border-collapse: collapse;
        width: 100%;
    }
    .styled-table th, .styled-table td {
        border: 1px solid #999;
        padding: 0.5rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Children's Museum Dashboard")

# Show styled table using HTML
st.subheader("Program Feedback Table")
st.markdown(df.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)




# Add logo
st.image(r"C:\Users\CDP USER\Downloads\New folder\PY code\Chat image.png", width=170)

# Section
st.markdown("### Jonga apha nkande patyutyu uhlomle")



# ------------------------
# Original Dataset
# ------------------------
original_data = {
    "Program Name": ["Robotics", "Math Games", "Eco Warriors", "Robotics", "Math Games"],
    "Program Rating (1-5)": [4.5, 3.8, 4.2, 4.0, 3.6],
    "No. of Participants": [35, 25, 30, 40, 20]
}
df_original = pd.DataFrame(original_data)

# ------------------------
# Load Feedback Data (if exists)
# ------------------------
if os.path.exists("feedback.csv"):
    feedback_raw = pd.read_csv("feedback.csv")
    
    # Only extract relevant columns and rename to match original data
    if not feedback_raw.empty:
        df_feedback = feedback_raw[["Program Name", "Rating (1-5)", "No. of Participants"]].copy()
        df_feedback.rename(columns={"Rating (1-5)": "Program Rating (1-5)"}, inplace=True)
        df_combined = pd.concat([df_original, df_feedback], ignore_index=True)
    else:
        df_combined = df_original.copy()
else:
    df_combined = df_original.copy()

# ------------------------
# Streamlit App Begins
# ------------------------
st.title("Children's Museum Program Dashboard")

# Show the raw data
st.subheader("Raw Data (Including Feedback)")
st.markdown(df_combined.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)


# Show average ratings by program
st.subheader("Average Rating by Program")
avg_ratings = df_combined.groupby("Program Name")["Program Rating (1-5)"].mean()
st.bar_chart(avg_ratings)

# Show boxplot of program ratings
st.subheader("Rating Distribution")
fig1, ax1 = plt.subplots()
sns.boxplot(data=df_combined, x="Program Name", y="Program Rating (1-5)", ax=ax1)
plt.xticks(rotation=45)
st.pyplot(fig1)

# ------------------------
# Feedback Form
# ------------------------
st.subheader("Give Us Feedback")

with st.form("feedback_form"):
    name = st.text_input("Your Name")
    program = st.selectbox("Which Program?", df_original["Program Name"].unique())
    rating = st.slider("Rating (1-5)", 1.0, 5.0, 3.0)
    participants = st.number_input("Number of Participants", min_value=1, step=1)
    comment = st.text_area("Any comments?")
    submitted = st.form_submit_button("Submit Feedback")

    if submitted:
        new_feedback = {
            "Name": name,
            "Program Name": program,
            "Rating (1-5)": rating,
            "No. of Participants": participants,
            "Comments": comment
        }
        feedback_df = pd.DataFrame([new_feedback])
        feedback_df.to_csv("feedback.csv", mode="a", header=not os.path.exists("feedback.csv"), index=False)
        st.success("Thanks for your feedback! Refresh the page to update graphs.")

# ------------------------
# Show Recent Feedback
# ------------------------
st.subheader("Recent Feedback")
if os.path.exists("feedback.csv"):
    fb_data = pd.read_csv("feedback.csv")
    st.markdown(fb_data.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)
else:
    st.info("No feedback submitted yet.")


# ------------------------
# Button to Clear Feedback
# ------------------------
if st.button("Clear All Feedback"):
    with open("feedback.csv", "w") as f:
        f.write("Name,Program Name,Rating (1-5),No. of Participants,Comments\n")
    st.success("All feedback has been cleared. Refresh the app to see updates.")





