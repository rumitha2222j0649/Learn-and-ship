import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from datetime import date, datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="StudyPulse | Student Academic Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom Styling ---
st.markdown("""
<style>
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.04);
    }
    div[data-testid="stMetric"]:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        border-color: #ced4da;
    }
    /* Section headers */
    .section-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    .badge-safe {
        background-color: #d1fae5;
        color: #065f46;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-warn {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "student_data.json"

# --- Default Sample Data ---
DEFAULT_DATA = {
    "attendance": [
        {"subject": "Data Structures & Algorithms", "attended": 28, "total": 32, "target": 75},
        {"subject": "Database Management Systems", "attended": 22, "total": 30, "target": 75},
        {"subject": "Computer Networks", "attended": 18, "total": 28, "target": 75},
        {"subject": "Operating Systems", "attended": 25, "total": 26, "target": 75},
        {"subject": "Mathematics for CS", "attended": 20, "total": 30, "target": 75},
    ],
    "grades": [
        {"subject": "Data Structures & Algorithms", "credits": 4, "marks": 88},
        {"subject": "Database Management Systems", "credits": 4, "marks": 82},
        {"subject": "Computer Networks", "credits": 3, "marks": 74},
        {"subject": "Operating Systems", "credits": 4, "marks": 91},
        {"subject": "Mathematics for CS", "credits": 3, "marks": 68},
    ],
    "tasks": [
        {"task": "DSA Assignment 3 - Binary Trees", "subject": "Data Structures & Algorithms", "due_date": "2026-11-26", "priority": "High", "status": "Pending"},
        {"task": "DBMS Mini Project Schema Design", "subject": "Database Management Systems", "due_date": "2026-11-28", "priority": "High", "status": "In Progress"},
        {"task": "CN Lab WireShark Packet Capture Report", "subject": "Computer Networks", "due_date": "2026-11-30", "priority": "Medium", "status": "Pending"},
        {"task": "OS Chapter 4 CPU Scheduling Notes", "subject": "Operating Systems", "due_date": "2026-11-25", "priority": "Low", "status": "Completed"},
    ]
}

# --- Data Helper Functions ---
def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_DATA.copy()

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def marks_to_grade(marks):
    if marks >= 90:
        return "O", 10
    elif marks >= 80:
        return "A+", 9
    elif marks >= 70:
        return "A", 8
    elif marks >= 60:
        return "B+", 7
    elif marks >= 50:
        return "B", 6
    elif marks >= 40:
        return "C", 5
    else:
        return "F", 0

# Initialize Session State
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# --- Sidebar ---
with st.sidebar:
    st.title("🎓 StudyPulse")
    st.caption("Smart Academic Performance & Attendance Hub")
    st.divider()

    menu = st.radio(
        "Navigation",
        [
            "📊 Executive Dashboard",
            "📅 Attendance & Bunk Predictor",
            "🎯 GPA & Performance Calculator",
            "📝 Task & Assignment Manager",
            "ℹ️ About the Project"
        ],
        index=0
    )

    st.divider()
    st.subheader("⚙️ Quick Actions")
    if st.button("🔄 Reset to Sample Data", use_container_width=True):
        st.session_state.data = DEFAULT_DATA.copy()
        save_data(DEFAULT_DATA)
        st.toast("Sample data restored successfully!", icon="✅")
        st.rerun()

    st.caption("Built with **Streamlit** & **Plotly**")


# ==========================================================
# PAGE 1: EXECUTIVE DASHBOARD
# ==========================================================
if menu == "📊 Executive Dashboard":
    st.title("📊 Academic Performance Dashboard")
    st.write("Welcome back! Here is a high-level overview of your attendance, grades, and upcoming deadlines.")

    # Calculations
    att_list = data["attendance"]
    total_attended = sum(item["attended"] for item in att_list)
    total_conducted = sum(item["total"] for item in att_list)
    overall_att_pct = round((total_attended / total_conducted * 100), 1) if total_conducted > 0 else 0.0

    # GPA Calculation
    grade_list = data["grades"]
    total_credits = sum(item["credits"] for item in grade_list)
    total_weighted_points = sum(item["credits"] * marks_to_grade(item["marks"])[1] for item in grade_list)
    current_gpa = round(total_weighted_points / total_credits, 2) if total_credits > 0 else 0.0

    # Task Stats
    task_list = data["tasks"]
    pending_tasks = len([t for t in task_list if t["status"] != "Completed"])
    completed_tasks = len([t for t in task_list if t["status"] == "Completed"])
    task_completion_pct = round((completed_tasks / len(task_list) * 100), 1) if len(task_list) > 0 else 0

    # Critical Attendance Count
    crit_count = sum(1 for item in att_list if (item["attended"] / item["total"] * 100) < item["target"])

    # Top KPI Metrics Row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        att_delta = f"{overall_att_pct - 75:.1f}% vs 75% req"
        c1.metric(
            label="Overall Attendance",
            value=f"{overall_att_pct}%",
            delta=att_delta,
            delta_color="normal" if overall_att_pct >= 75 else "inverse"
        )
    with c2:
        c2.metric(
            label="Projected SGPA",
            value=f"{current_gpa} / 10.0",
            delta="First Class with Distinction" if current_gpa >= 8.5 else "First Class"
        )
    with c3:
        c3.metric(
            label="Pending Tasks",
            value=f"{pending_tasks}",
            delta=f"{completed_tasks} completed",
            delta_color="off"
        )
    with c4:
        c4.metric(
            label="Subjects at Risk",
            value=f"{crit_count} / {len(att_list)}",
            delta="Attention required" if crit_count > 0 else "All Safe",
            delta_color="inverse" if crit_count > 0 else "normal"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Charts Row
    ch1, ch2 = st.columns([3, 2])

    with ch1:
        st.subheader("📈 Attendance per Subject vs 75% Target")
        att_df = pd.DataFrame([
            {
                "Subject": item["subject"],
                "Attendance %": round((item["attended"] / item["total"] * 100), 1) if item["total"] > 0 else 0,
                "Attended": item["attended"],
                "Total": item["total"]
            }
            for item in att_list
        ])

        fig_att = px.bar(
            att_df,
            x="Attendance %",
            y="Subject",
            orientation="h",
            text="Attendance %",
            color="Attendance %",
            color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
            range_color=[50, 100]
        )
        fig_att.add_vline(x=75, line_width=2, line_dash="dash", line_color="#dc2626", annotation_text="75% Min Req")
        fig_att.update_layout(
            height=320,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis_title="Attendance Percentage (%)",
            yaxis_title="",
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig_att, use_container_width=True)

    with ch2:
        st.subheader("🎯 Grade Distribution by Credits")
        grade_records = []
        for g in grade_list:
            grade_name, pt = marks_to_grade(g["marks"])
            grade_records.append({
                "Subject": g["subject"],
                "Credits": g["credits"],
                "Marks": g["marks"],
                "Grade": f"{grade_name} ({pt} pts)"
            })
        gdf = pd.DataFrame(grade_records)

        fig_pie = px.pie(
            gdf,
            names="Grade",
            values="Credits",
            hole=0.45,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_pie.update_layout(
            height=320,
            margin=dict(l=10, r=10, t=20, b=20),
            showlegend=True
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Active Deadlines Section
    st.subheader("⏰ Upcoming Deadlines")
    active_tasks = [t for t in task_list if t["status"] != "Completed"]
    if active_tasks:
        tdf = pd.DataFrame(active_tasks)
        st.dataframe(
            tdf[["due_date", "task", "subject", "priority", "status"]].rename(
                columns={"due_date": "Due Date", "task": "Task Name", "subject": "Subject", "priority": "Priority", "status": "Status"}
            ),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("🎉 All caught up! No pending deadlines.")


# ==========================================================
# PAGE 2: ATTENDANCE & BUNK PREDICTOR
# ==========================================================
elif menu == "📅 Attendance & Bunk Predictor":
    st.title("📅 Attendance Tracker & Safe Bunk Predictor")
    st.write("Keep your attendance safely above university regulations with automated mathematical predictions.")

    att_list = data["attendance"]

    # Subject Analysis Table
    rows = []
    for item in att_list:
        att = item["attended"]
        tot = item["total"]
        tgt = item["target"]
        cur_pct = round((att / tot * 100), 1) if tot > 0 else 0

        # Predictor Formula:
        # If current % >= target: safe to miss 'x' classes: (att / (tot + x)) >= (tgt / 100) => att*100 >= tgt*(tot+x) => x = floor((att*100 - tgt*tot)/tgt)
        # If current % < target: must attend 'y' classes: ((att + y) / (tot + y)) >= (tgt / 100) => y = ceil((tgt*tot - 100*att) / (100 - tgt))
        if cur_pct >= tgt:
            safe_bunks = int((att * 100 - tgt * tot) // tgt)
            status_text = f"Safe: Can miss {safe_bunks} class{'es' if safe_bunks != 1 else ''}"
            category = "🟢 Safe"
        else:
            needed = int(((tgt * tot - 100 * att) + (100 - tgt - 1)) // (100 - tgt))
            status_text = f"Shortage: Must attend {needed} consecutive class{'es' if needed != 1 else ''}"
            category = "🔴 Critical"

        rows.append({
            "Subject": item["subject"],
            "Attended": att,
            "Conducted": tot,
            "Percentage": f"{cur_pct}%",
            "Target": f"{tgt}%",
            "Status": category,
            "Recommendation": status_text
        })

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.divider()

    # Two columns: Add New Subject & Edit / Delete Existing
    col_add, col_edit = st.columns(2)

    with col_add:
        st.subheader("➕ Add New Subject")
        with st.form("add_subject_form", clear_on_submit=True):
            new_sub = st.text_input("Subject Name", placeholder="e.g. Machine Learning")
            c_att, c_tot = st.columns(2)
            with c_att:
                new_att = st.number_input("Classes Attended", min_value=0, max_value=200, value=15)
            with c_tot:
                new_tot = st.number_input("Total Classes Held", min_value=1, max_value=200, value=20)
            new_target = st.slider("Target Minimum %", min_value=50, max_value=95, value=75, step=5)

            submitted = st.form_submit_button("Add Subject", use_container_width=True)
            if submitted:
                if new_sub.strip():
                    if new_att > new_tot:
                        st.error("Attended classes cannot exceed total classes.")
                    else:
                        data["attendance"].append({
                            "subject": new_sub.strip(),
                            "attended": int(new_att),
                            "total": int(new_tot),
                            "target": int(new_target)
                        })
                        # Also add default to grades if not present
                        data["grades"].append({
                            "subject": new_sub.strip(),
                            "credits": 3,
                            "marks": 75
                        })
                        save_data(data)
                        st.success(f"Added {new_sub} successfully!")
                        st.rerun()
                else:
                    st.warning("Subject name cannot be empty.")

    with col_edit:
        st.subheader("✏️ Quick Update Subject Attendance")
        sub_names = [item["subject"] for item in data["attendance"]]
        if sub_names:
            selected_sub = st.selectbox("Select Subject", sub_names)
            curr_item = next(i for i in data["attendance"] if i["subject"] == selected_sub)

            with st.form("edit_subject_form"):
                e_att = st.number_input("Classes Attended", min_value=0, max_value=300, value=curr_item["attended"])
                e_tot = st.number_input("Total Classes Held", min_value=1, max_value=300, value=curr_item["total"])
                e_tgt = st.slider("Target Requirement %", 50, 95, value=curr_item["target"], step=5)

                b_update, b_delete = st.columns(2)
                with b_update:
                    update_btn = st.form_submit_button("💾 Save Update", use_container_width=True)
                with b_delete:
                    delete_btn = st.form_submit_button("🗑️ Delete Subject", use_container_width=True)

                if update_btn:
                    if e_att > e_tot:
                        st.error("Attended classes cannot exceed total classes.")
                    else:
                        curr_item["attended"] = int(e_att)
                        curr_item["total"] = int(e_tot)
                        curr_item["target"] = int(e_tgt)
                        save_data(data)
                        st.success(f"Updated {selected_sub}!")
                        st.rerun()

                if delete_btn:
                    data["attendance"] = [i for i in data["attendance"] if i["subject"] != selected_sub]
                    data["grades"] = [i for i in data["grades"] if i["subject"] != selected_sub]
                    save_data(data)
                    st.success(f"Deleted {selected_sub}!")
                    st.rerun()


# ==========================================================
# PAGE 3: GPA & GRADE CALCULATOR
# ==========================================================
elif menu == "🎯 GPA & Performance Calculator":
    st.title("🎯 GPA & Academic Grade Calculator")
    st.write("Calculate your Semester Grade Point Average (SGPA) based on course credits and internal/external marks.")

    grade_list = data["grades"]

    g_col1, g_col2 = st.columns([3, 2])

    with g_col1:
        st.subheader("📋 Subject Grades & Credits")
        calc_rows = []
        for g in grade_list:
            grade_name, pt = marks_to_grade(g["marks"])
            calc_rows.append({
                "Subject": g["subject"],
                "Credits": g["credits"],
                "Marks (/100)": g["marks"],
                "Letter Grade": grade_name,
                "Grade Points": pt,
                "Credit Points (Credit × Pt)": g["credits"] * pt
            })

        cdf = pd.DataFrame(calc_rows)
        st.dataframe(cdf, use_container_width=True, hide_index=True)

        total_cr = cdf["Credits"].sum()
        total_pts = cdf["Credit Points (Credit × Pt)"].sum()
        sgpa = round(total_pts / total_cr, 2) if total_cr > 0 else 0.0

        st.info(f"**Total Credits:** {total_cr} | **Total Credit Points:** {total_pts} | **Final SGPA:** **{sgpa}** / 10.0")

    with g_col2:
        st.subheader("💡 Grading Scheme Reference")
        ref_df = pd.DataFrame({
            "Marks Range": ["90 - 100", "80 - 89", "70 - 79", "60 - 69", "50 - 59", "40 - 49", "< 40"],
            "Grade": ["O (Outstanding)", "A+ (Excellent)", "A (Very Good)", "B+ (Good)", "B (Above Average)", "C (Pass)", "F (Fail)"],
            "Points": [10, 9, 8, 7, 6, 5, 0]
        })
        st.dataframe(ref_df, use_container_width=True, hide_index=True)

    st.divider()

    st.subheader("✏️ Modify Subject Credits & Marks")
    if grade_list:
        sub_to_edit = st.selectbox("Select Course", [g["subject"] for g in grade_list], key="grade_sub_select")
        sel_grade = next(g for g in grade_list if g["subject"] == sub_to_edit)

        with st.form("update_grade_form"):
            gc1, gc2 = st.columns(2)
            with gc1:
                new_credits = st.number_input("Course Credits", min_value=1, max_value=6, value=sel_grade["credits"])
            with gc2:
                new_marks = st.slider("Expected / Scored Marks (out of 100)", 0, 100, value=sel_grade["marks"])

            if st.form_submit_button("Update Grade"):
                sel_grade["credits"] = int(new_credits)
                sel_grade["marks"] = int(new_marks)
                save_data(data)
                st.success(f"Updated grades for {sub_to_edit}!")
                st.rerun()


# ==========================================================
# PAGE 4: TASK & ASSIGNMENT MANAGER
# ==========================================================
elif menu == "📝 Task & Assignment Manager":
    st.title("📝 Assignment & Study Task Planner")
    st.write("Never miss an assignment deadline or exam revision schedule.")

    tasks = data["tasks"]

    # Filter controls
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        status_filter = st.radio("Filter Tasks", ["All", "Pending", "In Progress", "Completed"], horizontal=True)

    filtered_tasks = tasks if status_filter == "All" else [t for t in tasks if t["status"] == status_filter]

    st.subheader(f"Task List ({len(filtered_tasks)})")
    if filtered_tasks:
        for idx, t in enumerate(filtered_tasks):
            t_box = st.container(border=True)
            with t_box:
                tc1, tc2, tc3, tc4 = st.columns([4, 2, 2, 2])
                with tc1:
                    st.markdown(f"**{t['task']}**")
                    st.caption(f"Course: {t['subject']}")
                with tc2:
                    st.write(f"📅 Due: {t['due_date']}")
                with tc3:
                    p_color = "red" if t['priority'] == 'High' else "orange" if t['priority'] == 'Medium' else "blue"
                    st.markdown(f"Priority: :{p_color}[**{t['priority']}**]")
                with tc4:
                    new_status = st.selectbox(
                        "Status",
                        ["Pending", "In Progress", "Completed"],
                        index=["Pending", "In Progress", "Completed"].index(t["status"]),
                        key=f"status_{idx}_{t['task']}"
                    )
                    if new_status != t["status"]:
                        t["status"] = new_status
                        save_data(data)
                        st.rerun()
    else:
        st.info("No tasks matching the selected filter.")

    st.divider()

    # Add Task Form
    st.subheader("➕ Create New Task")
    with st.form("create_task_form", clear_on_submit=True):
        t_name = st.text_input("Task Title", placeholder="e.g. Chapter 5 Practice Problems")
        available_courses = [item["subject"] for item in data["attendance"]]
        c_sub, c_due, c_pri = st.columns(3)
        with c_sub:
            t_sub = st.selectbox("Subject", available_courses if available_courses else ["General"])
        with c_due:
            t_due = st.date_input("Due Date", value=date.today())
        with c_pri:
            t_pri = st.selectbox("Priority", ["High", "Medium", "Low"])

        if st.form_submit_button("Add Task", use_container_width=True):
            if t_name.strip():
                data["tasks"].append({
                    "task": t_name.strip(),
                    "subject": t_sub,
                    "due_date": str(t_due),
                    "priority": t_pri,
                    "status": "Pending"
                })
                save_data(data)
                st.success("Task added!")
                st.rerun()
            else:
                st.warning("Task title cannot be empty.")


# ==========================================================
# PAGE 5: ABOUT THE PROJECT
# ==========================================================
elif menu == "ℹ️ About the Project":
    st.title("ℹ️ About StudyPulse")
    st.write("A lightweight, practical, and beginner-friendly web application designed for students and educators.")

    st.markdown("""
    ### 🎯 Motivation & Problem Statement
    College students often struggle with three frequent problems:
    1. **Attendance Shortage Anxiety:** Not knowing exactly how many classes they can afford to miss or how many they must attend consecutively to hit the mandatory 75% threshold.
    2. **GPA Uncertainty:** Lack of clarity on how individual course marks and credit weightages translate into their final SGPA.
    3. **Missed Deadlines:** Fragmented management of lab submissions, homework, and assignment due dates.

    **StudyPulse** solves all three in a unified, interactive dashboard.

    ---

    ### 🛠️ Key Technical Highlights
    - **Interactive Frontend:** Built with **Streamlit**, eliminating frontend boilerplate while maintaining clean aesthetics.
    - **Dynamic Visualizations:** Integrated with **Plotly** for real-time interactive bar, gauge, and donut charts.
    - **Persistence:** Local JSON data layer enabling state preservation across sessions.
    - **Zero-Friction Deployment:** Pure Python codebase running locally or hostable on Streamlit Community Cloud with 1 click.

    ---

    ### 🎓 Presentation Script (For Faculty)
    > *"Good morning/afternoon Professors. Today I am presenting **StudyPulse**, a smart academic productivity and attendance dashboard built using Python and Streamlit. The tool addresses the everyday challenges students face in tracking university compliance and semester performance. It features a predictive algorithm that calculates safe bunks or required attendances for a 75% threshold, an automated SGPA calculator based on standard university credit grading, and a task management board. The entire application runs natively in Python with reactive data visualizations using Plotly."*
    """)
