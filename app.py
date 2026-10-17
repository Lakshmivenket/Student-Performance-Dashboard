
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Student Performance Dashboard",
    page_icon="🎓",
    layout="wide"
)

# Dashboard title
st.title("🎓 Student Performance Dashboard")
st.write("Analyze student marks and attendance.")


# Upload student data
st.sidebar.header("Upload Student Data")

uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV file",
    type=["csv"]
)


if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        required_columns = [
            "Student", "Maths", "Science",
            "English", "Attendance"
        ]

        if not all(column in df.columns for column in required_columns):
            st.error(
                "CSV file must contain: Student, Maths, Science, English, Attendance"
            )
            st.stop()

    except Exception:
        st.error("Unable to read this CSV file. Please upload a valid CSV.")
        st.stop()

else:

    # Sample student data
    data = {
        "Student": ["Arun", "Priya", "Kumar", "Divya", "Ravi"],
        "Maths": [85, 92, 25, 78, 55],
        "Science": [80, 88, 30, 90, 58],
        "English": [75, 95, 28, 85, 62],
        "Attendance": [90, 98, 60, 95, 65]
    }

    df = pd.DataFrame(data)


# Calculate average marks
df["Average Marks"] = df[
    ["Maths", "Science", "English"]
].mean(axis=1).round(1)

# Calculate Pass or Fail
df["Result"] = df["Average Marks"].apply(
    lambda mark: "Pass" if mark >= 35 else "Fail"
)

# Sidebar filter
st.sidebar.header("Dashboard Filters")

selected_students = st.sidebar.multiselect(
    "Select Students",
    options=df["Student"].tolist(),
    default=df["Student"].tolist()
)

filtered_df = df[
    df["Student"].isin(selected_students)
]

# Metric cards
if not filtered_df.empty:
    total_students = len(filtered_df)

    average_marks = round(
        filtered_df["Average Marks"].mean(), 1
    )

    pass_percentage = round(
        (filtered_df["Result"] == "Pass").mean() * 100, 1
    )

    average_attendance = round(
        filtered_df["Attendance"].mean(), 1
    )
else:
    total_students = 0
    average_marks = 0
    pass_percentage = 0
    average_attendance = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("👨‍🎓 Total Students", total_students)
col2.metric("📊 Average Marks", average_marks)
col3.metric("✅ Pass Percentage", f"{pass_percentage}%")
col4.metric("📅 Average Attendance", f"{average_attendance}%")

st.divider()

# Student details table
st.subheader("📋 Student Details")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# Charts
if not filtered_df.empty:

    # Subject-wise bar chart
    st.subheader("📊 Subject-wise Performance")

    subject_df = filtered_df.set_index("Student")[
        ["Maths", "Science", "English"]
    ]

    st.bar_chart(subject_df)

    # Attendance bar chart
    st.subheader("📅 Student Attendance")

    attendance_df = filtered_df.set_index("Student")[
        ["Attendance"]
    ]

    st.bar_chart(attendance_df)

    # Pass and Fail pie chart
    st.subheader("🥧 Pass and Fail Distribution")

    result_counts = filtered_df["Result"].value_counts()

    fig, ax = plt.subplots()

    ax.pie(
        result_counts.values,
        labels=result_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)

    plt.close(fig)

else:
    st.info("Please select at least one student from the sidebar.")

# Footer
st.caption(
    "Student Performance Dashboard | Python + Streamlit + Pandas"
)

