Region I Agricultural Production Dashboard

Data Analytics 
Tech Stack: Python, Pandas, Plotly, Streamlit, SQLite

Project Overview
This is an interactive tool designed to analyze and simulate agricultural output in Region I (Ilocos Region), Philippines. Using Palay and Corn production data from 2020 to 2025, the application transforms raw government statistics (PSA) into actionable insights for food security and regional policy planning.

I first downloaded real government data from PSA OpenSTAT to get the info I needed as raw data. I then cleaned the data and 
was put into a database to have a more organized view of the data. Then, the app pulled this data to be used in the system.

Key Features
A. Unified Executive Dashboard
-Automated Metrics: Displays real-time production totals with Year-over-Year (YoY) growth indicators and percentage deltas.

-Data Integrity Logic: Implemented a backend filtering system to prevent the double-counting of aggregate rows. (e.g., separating "Palay Total" from "Irrigated vs. Rainfed" sub-categories).

B. Semestral & Quarterly Breakdown
-Visualizes production shifts across Quarters 1-4 or Semester 1-2, identifying peak harvest periods trends.

C. Predictive Simulator
-A scenario prediction tool that allows users to simulate yield improvements and land expansion.
-Calculates projected Metric Tons (MT) and net gains dynamically to assist in hypothetical policy evaluations.

Database Schema
The system then pulls from a relational SQLite database (production.db) with the following structure:

-Ecosystem/Croptype: Categorical (Palay, Corn, Irrigated, etc.)
-Geolocation: Spatial (Region I)
-Period: Quarterly and Semester-based timeframes
-Volume_Metric_Tons: Numeric output
-Year: Time-series component (2020-2025)
