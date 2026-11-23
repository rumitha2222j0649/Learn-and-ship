# 🎓 StudyPulse: Smart Student Academic & Attendance Dashboard

> A beginner-friendly, visually attractive, and functional web application built with **Python**, **Streamlit**, and **Plotly**. Designed to help students monitor attendance thresholds, forecast semester GPA, and stay ahead of assignment deadlines.

---

## 📌 1. Project Overview

- **Project Title:** StudyPulse – Intelligent Student Academic & Attendance Planner
- **Tool Selected:** **Streamlit** (Python Framework for Interactive Web Apps)
- **Time to Build:** ~2 to 3 hours (easily completed in a single afternoon/evening)
- **Target Audience:** College / University students and Faculty Evaluators

### Why Streamlit?
Streamlit is one of the fastest-growing tools in the Python ecosystem for turning raw scripts into polished, interactive web dashboards without needing to write HTML, CSS, or JavaScript. It provides:
1. **Zero Frontend Overhead:** Pure Python widgets (`st.metric`, `st.slider`, `st.dataframe`, `st.form`).
2. **Instant Visual Polish:** Professional modern styling, dark/light theme support, and responsive layouts out of the box.
3. **Data Science Ready:** Native integration with Pandas, Plotly, Altair, and Matplotlib.
4. **Beginner-Friendly:** A complete functional app can be built in less than 200 lines of readable code.

---

## 💡 2. The Core Idea & Features

Most students juggle attendance percentages, course grade targets, and assignment deadlines across separate apps or scribbled notes. **StudyPulse** unifies these into an executive dashboard with three core problem-solvers:

1. **Attendance Shortage & Safe Bunk Predictor:**
   - Automatically computes real-time attendance percentage for each subject.
   - **Predictive Algorithm:**
     - If attendance is $\ge 75\%$, it calculates exactly how many classes you can **safely miss** without falling below the 75% university threshold.
     - If attendance is $< 75\%$, it calculates exactly how many **consecutive classes** you must attend to restore eligibility.
2. **SGPA & Grade Point Calculator:**
   - Implements standard 10-point credit grading ($O, A+, A, B+, B, C, F$).
   - Calculates overall weighted SGPA based on course credits and exam/internal marks.
   - Visualizes grade credit distribution using an interactive donut chart.
3. **Assignment & Task Planner:**
   - Tracks coursework deadlines, submission dates, and priority levels (High, Medium, Low).
   - Allows instant status changes (*Pending*, *In Progress*, *Completed*) with persistent updates.
4. **Local Data Persistence:**
   - Stores data cleanly in `student_data.json` so customizations persist between sessions.
   - Includes a **1-click "Reset to Sample Data"** button to quickly demonstrate features to evaluators.

---

## 🛠️ 3. Technologies Used

| Technology | Purpose |
| :--- | :--- |
| **Python 3.x** | Core backend logic, calculation algorithms, and data structures. |
| **Streamlit (v1.60+)** | Rapid web framework, interactive UI components, reactive state management. |
| **Plotly Express** | Interactive charts (threshold-marked horizontal bar chart & donut chart). |
| **Pandas** | Tabular data manipulation and dynamic dataframe rendering. |
| **JSON** | Lightweight local database for saving records. |

---

## 🚀 4. How to Run the Project

### Prerequisites
Make sure Python 3.10+ is installed on your computer.

### Step 1: Open Terminal / Command Prompt
Navigate to the project folder:
```bash
cd "c:\Learn and ship"
```

### Step 2: Install Dependencies (if not already installed)
```bash
pip install -r requirements.txt
```
*(Or individually: `pip install streamlit pandas plotly`)*

### Step 3: Run the Application
Launch the Streamlit app:
```bash
streamlit run app.py
```

### Step 4: Access the Dashboard
Streamlit will automatically launch your default browser and open:
```text
http://localhost:8501
```

---

## 📋 5. Step-by-Step Implementation Breakdown

1. **Architecture & State Management (`app.py`):**
   - Configured page metadata (`st.set_page_config`) for a responsive wide layout.
   - Implemented `load_data()` and `save_data()` functions interfacing with `student_data.json`.
   - Initialized `st.session_state` to keep UI changes reactive and persistent.
2. **Multi-Page Sidebar Navigation:**
   - Built a sleek navigation panel utilizing `st.sidebar.radio` dividing the app into:
     - 📊 Executive Dashboard
     - 📅 Attendance & Bunk Predictor
     - 🎯 GPA & Performance Calculator
     - 📝 Task & Assignment Manager
     - ℹ️ About the Project
3. **Mathematical Predictor Logic:**
   - **Safe Miss Formula:**
     $$\text{Safe Bunks} = \left\lfloor \frac{(\text{Attended} \times 100) - (\text{Target} \times \text{Total})}{\text{Target}} \right\rfloor$$
   - **Recovery Formula:**
     $$\text{Required Classes} = \left\lceil \frac{(\text{Target} \times \text{Total}) - (100 \times \text{Attended})}{100 - \text{Target}} \right\rceil$$
4. **Data Visualizations:**
   - Placed Plotly horizontal bar charts featuring a red dashed vertical reference line at $75\%$ to immediately flag subjects at risk.
   - Built a grade distribution donut chart displaying credit weights.

---

## 🖥️ 6. Final Output Description

When launched, the user is greeted by:
- **Header KPI Metric Cards:** Showing real-time Overall Attendance (with $+/-$ delta compared to 75%), Projected SGPA, Total Pending Tasks, and Number of Subjects at Risk.
- **Interactive Visuals:** Hoverable bar graphs showing subject-wise attendance with colored alerts, plus credit distribution charts.
- **Dynamic Tables:** Clean tables with status badges (🟢 Safe, 🔴 Critical) and personalized natural-language recommendations.
- **Actionable Forms:** Easy modal-like forms to add new subjects, tweak internal scores, or check off homework assignments.

---

## 🎓 7. Short Explanation for Faculty / Viva Presentation

When presenting this project to your professor or viva examiner, use this structured 1-minute pitch:

> *"Good morning Professors. For this project, I explored **Streamlit**, a Python framework used across industry and data science to build reactive, data-centric web interfaces rapidly.*
>
> *Using Streamlit, I built **StudyPulse**—an academic productivity dashboard that solves three concrete student challenges:*
> 1. *First, attendance management: rather than simply calculating percentages, the system includes a predictive algorithm that informs students either how many classes they can safely skip or how many consecutive lectures they must attend to meet the mandatory 75% university cutoff.*
> 2. *Second, an automated SGPA predictor that weights subject credits and grades according to standard academic 10-point scale.*
> 3. *Third, an assignment tracking workflow for deadline management.*
>
> *The frontend is completely powered by Python with reactive Plotly visualizations and JSON-backed data persistence. It demonstrates how rapid UI prototyping tools like Streamlit eliminate frontend complexity while delivering clean, functional software."*

### Anticipated Viva Questions & Answers:
- **Q1: Why choose Streamlit over Flask or Django?**
  *Answer:* Flask and Django require configuring HTML templates, CSS styles, routing, and JavaScript state handling. Streamlit allows you to declare UI directly from Python data structures, reducing development time by 80% while natively integrating interactive data visualizations.
- **Q2: How does the application handle data persistence?**
  *Answer:* The application uses a local JSON serialization layer coupled with Streamlit's `st.session_state`. Any edits, additions, or deletions immediately write back to the JSON file and re-render the UI reactively.
- **Q3: What happens if attendance falls below 75%?**
  *Answer:* The algorithm detects the deficit and calculates the ceiling value: $\lceil(\text{Target} \times \text{Total} - 100 \times \text{Attended}) / (100 - \text{Target})\rceil$, providing the exact number of consecutive classes required to regain good standing.
