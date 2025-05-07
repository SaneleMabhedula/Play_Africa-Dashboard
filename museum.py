import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Dummy data
data = {
    "Program Name": ["Robotics", "Math Games", "Eco Warriors", "Robotics", "Math Games"],
    "Program Rating (1-5)": [4.5, 3.8, 4.2, 4.0, 3.6],
    "No. of Participants": [35, 25, 30, 40, 20]
}

df = pd.DataFrame(data)

# App title
st.title("Children's Museum Program Dashboard")

# Show the raw data
st.subheader("Raw Data")
st.dataframe(df)

# Show average ratings
st.subheader("Average Rating by Program")
avg_ratings = df.groupby("Program Name")["Program Rating (1-5)"].mean()
st.bar_chart(avg_ratings)

# Show boxplot
st.subheader("Rating Distribution")
fig, ax = plt.subplots()
sns.boxplot(data=df, x="Program Name", y="Program Rating (1-5)", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)





#KEEP

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create feedback.csv if it doesn't exist yet
if not os.path.exists("feedback.csv"):
    pd.DataFrame(columns=["Name", "Program", "Rating", "Comment"]).to_csv("feedback.csv", index=False)


# Set page layout
st.set_page_config(page_title="Museum Dashboard", layout="centered")

# Dummy data
data = {
    "Program Name": ["Robotics", "Math Games", "Eco Warriors", "Robotics", "Math Games"],
    "Program Rating (1-5)": [4.5, 3.8, 4.2, 4.0, 3.6],
    "No. of Participants": [35, 25, 30, 40, 20]
}

df = pd.DataFrame(data)

# App title
st.title("🤖 Play Africa Dashboard")

# Sidebar filters
st.sidebar.header("🔍 Filter Data")

# Program filter
programs = df["Program Name"].unique()
selected_programs = st.sidebar.multiselect("Select Program(s)", programs, default=programs)

# Rating range slider
rating_min, rating_max = st.sidebar.slider("Select Rating Range", 1.0, 5.0, (3.0, 5.0))

# Filter the DataFrame
filtered_df = df[
    (df["Program Name"].isin(selected_programs)) &
    (df["Program Rating (1-5)"] >= rating_min) &
    (df["Program Rating (1-5)"] <= rating_max)
]

# Show the filtered raw data
st.subheader("📋 Filtered Data")
st.dataframe(filtered_df)

# Show average ratings
st.subheader("📊 Average Rating by Program")
if not filtered_df.empty:
    avg_ratings = filtered_df.groupby("Program Name")["Program Rating (1-5)"].mean()
    st.bar_chart(avg_ratings)
else:
    st.warning("No data to show for selected filters.")

# Show boxplot
st.subheader("🎯 Rating Distribution (Boxplot)")
if not filtered_df.empty:
    fig, ax = plt.subplots()
    sns.boxplot(data=filtered_df, x="Program Name", y="Program Rating (1-5)", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)
else:
    st.warning("Boxplot not available for empty selection.")

st.subheader("📋 Submit Feedback")

# Feedback form
with st.form("feedback_form"):
    name = st.text_input("Your Name")
    selected_program = st.selectbox("Program", df["Program Name"].unique())
    rating = st.slider("Rate the program (1-5)", 1, 5)
    comment = st.text_area("Any comments?")
    submit = st.form_submit_button("Submit")

    if submit:
        new_feedback = {
            "Name": name,
            "Program": selected_program,
            "Rating": rating,
            "Comment": comment
        }

        # Save feedback to CSV
        feedback_df = pd.DataFrame([new_feedback])
        feedback_df.to_csv("feedback.csv", mode='a', header=not pd.read_csv("feedback.csv").empty, index=False)
        st.success("Thank you for your feedback!")

st.subheader("🗣 Recent Feedback")
all_feedback = pd.read_csv("feedback.csv")
st.dataframe(all_feedback.tail(10))


#KEEP 2


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Children's Museum Dashboard", layout="wide")

# 🔧 Step 1: Create feedback.csv if it doesn’t exist
if not os.path.exists("feedback.csv"):
    pd.DataFrame(columns=["Name", "Program", "Rating", "Comment"]).to_csv("feedback.csv", index=False)

# 📊 Step 2: Base data
base_data = pd.DataFrame({
    "Program Name": ["Robotics", "Math Games", "Eco Warriors", "Robotics", "Math Games"],
    "Program Rating (1-5)": [4.5, 3.8, 4.2, 4.0, 3.6],
    "No. of Participants": [35, 25, 30, 40, 20]
})

# 📥 Step 3: Load feedback and combine with base data
feedback_file = "feedback.csv"
if os.path.exists(feedback_file):
    feedback_data = pd.read_csv(feedback_file)

    if not feedback_data.empty:
        feedback_data.rename(columns={
            "Program": "Program Name",
            "Rating": "Program Rating (1-5)"
        }, inplace=True)

        feedback_data["No. of Participants"] = 1  # Each feedback = 1 participant

        combined_df = pd.concat([
            base_data,
            feedback_data[["Program Name", "Program Rating (1-5)", "No. of Participants"]]
        ], ignore_index=True)
    else:
        combined_df = base_data
else:
    combined_df = base_data

# 🎨 Step 4: Dashboard Layout
st.title("🎨 Children's Museum Program Dashboard")

# 📋 Show data
st.subheader("🔍 Raw Data")
st.dataframe(combined_df)

# 📊 Average rating by program
st.subheader("⭐ Average Rating by Program")
avg_ratings = combined_df.groupby("Program Name")["Program Rating (1-5)"].mean()
st.bar_chart(avg_ratings)

# 📦 Boxplot
st.subheader("🎯 Rating Distribution by Program")
fig, ax = plt.subplots()
sns.boxplot(data=combined_df, x="Program Name", y="Program Rating (1-5)", ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# 📝 Feedback Section
st.subheader("🗣 Submit Your Feedback")

with st.form("feedback_form"):
    name = st.text_input("Your Name")
    selected_program = st.selectbox("Program", base_data["Program Name"].unique())
    rating = st.slider("Rate the program (1-5)", 1, 5)
    comment = st.text_area("Any comments?")
    submit = st.form_submit_button("Submit")

    if submit:
        new_feedback = {
            "Name": name,
            "Program": selected_program,
            "Rating": rating,
            "Comment": comment
        }
        feedback_df = pd.DataFrame([new_feedback])
        feedback_df.to_csv("feedback.csv", mode='a', header=False, index=False)
        st.success("Thank you for your feedback!")

# 👁️ View Recent Feedback
st.subheader("📖 Recent Feedback")
show_feedback = pd.read_csv("feedback.csv")
if not show_feedback.empty:
    st.dataframe(show_feedback.tail(10))
else:
    st.info("No feedback submitted yet.")

# Display existing feedback
st.subheader("Recent Feedback")
st.dataframe(pd.read_csv("feedback.csv"))

# Clear feedback button (put this after showing the feedback)
if st.button("Clear All Feedback"):
    with open("feedback.csv", "w") as f:
        f.write("Name,Program Name,Rating (1-5),Comments\n")
    st.success("All feedback has been cleared.")