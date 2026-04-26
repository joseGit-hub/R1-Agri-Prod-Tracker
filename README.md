# 🌾 Region I Agricultural Production Dashboard
> **Project Overview**

An interactive tool designed to analyze and simulate agricultural volume production output in **Region I (Ilocos Region), Philippines**. 

### 🛠 Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

# Description
Using Palay and Corn production data from **2020 to 2025**, the application transforms raw government statistics (PSA) into actionable insights for food security and regional policy planning.

I first downloaded real government data from PSA OpenSTAT to get the info I needed as raw data. I then cleaned the data and was put into a database to have a more organized view of the data. Then, the app pulled this data to be used in the system.

# Key Features

# **A. Unified Executive Dashboard**
* **Automated Metrics:** Displays real-time production totals with Year-over-Year (YoY) growth indicators and percentage deltas.
* **Data Integrity Logic:** Implemented a backend filtering system to prevent the double-counting of aggregate rows (e.g., separating "Palay Total" from "Irrigated vs. Rainfed" sub-categories).

# **B. Semestral & Quarterly Breakdown**
* Visualizes production shifts across Quarters 1-4 or Semester 1-2, identifying peak harvest periods trends.

# **C. Predictive Simulator**
* A scenario prediction tool that allows users to simulate yield improvements and land expansion.
* Calculates projected Metric Tons (MT) and net gains dynamically to assist in hypothetical policy evaluations.
