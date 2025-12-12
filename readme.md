# Expense Tracker

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A comprehensive expense tracking application built with Streamlit that helps you record, analyze, and manage your financial expenses with data-driven insights and recommendations.

## Features

- **Expense Management**: Add, view, and delete expenses with date, amount, category, and description
- **Data Analytics**: Real-time statistics including total spending, averages, and category breakdowns
- **Visualizations**: Interactive charts showing spending trends, category distributions, and time-series analysis
- **Smart Insights**: Automated spending pattern analysis with budget recommendations and anomaly detection
- **Data Persistence**: CSV-based storage for reliable data management

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd expensetracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run expensetracker/main.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage

1. **Add Expenses**: Navigate to "Tambah Pengeluaran" to record new expenses
2. **View Records**: Check "Daftar Pengeluaran" to see all your expense entries
3. **Analyze Data**: Visit "Statistik" for comprehensive spending analytics and visualizations
4. **Get Insights**: Explore "Insights & Saran" for personalized recommendations and spending patterns

## Technology Stack

- **Streamlit** - Web application framework
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive data visualizations

## License

MIT License
