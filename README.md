# Coffee Shop Tracker

**Project 1 — Python Fundamentals**  
**Wejdan Ali**

Coffee Shop Tracker is a Streamlit app for managing a café menu, recording orders, and tracking daily sales in Bahraini dinars (BHD).

## Features

| Page | What you can do |
| --- | --- |
| Manage Menu | Add drinks with a name, size, price, and category. Upload or download the menu as a CSV file. |
| Point of Sale | Choose a drink and size, set the quantity, add items to an order, and remove items before confirming it. |
| Daily Dashboard | See how many cups were sold today, today's revenue, and a bar chart of drinks by quantity sold. |
| Sales Log | View confirmed sales and upload or download the sales history as a CSV file. |

**Student's choice feature — Daily Sales Goal.** Set a revenue target in BHD to see the percentage reached and the amount remaining. The dashboard displays a confirmation when revenue reaches the goal.

## Run the app

Install the dependencies from the project folder.

```bash
python -m pip install streamlit pandas matplotlib
```

Start Streamlit and open the local URL printed in the output.

```bash
python -m streamlit run app.py
```

To launch the app from a Jupyter code cell in the project folder, run the following command and open the local URL it prints.

```python
!streamlit run app.py --server.port 8502
```

## Save and reload data

1. In **Manage Menu** or **Sales Log**, upload a CSV and click the matching **Load** button.
2. Add drinks in **Manage Menu** or confirm orders in **Point of Sale**.
3. Download the updated CSV from its page to keep a copy. Loading a CSV replaces the corresponding menu or sales table in the current session.
4. To see an imported sale in **Daily Dashboard**, make sure its date matches today's date.

The app holds menu and sales data in Streamlit session state. Download CSV copies before ending the session if you want to keep the data.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit pages, order flow, and CSV handling. |
| `coffee_logic.py` | Functions for daily sales totals and best-seller counts. |
| `.streamlit/config.toml` | Theme settings for the café interface. |

## References

- General Assembly — *Python Fundamentals Project Guidelines*. Used to identify the project requirements.
- General Assembly — *Streamlit Guided Notebook*. Used as a reference for building the Streamlit app.
- General Assembly — `3-eda-with-pandas.ipynb`. Used as a reference for filtering DataFrames and working with CSV files.
- General Assembly — `6-exercise-descriptive-statistics-in-pandas.ipynb`. Used as a reference for grouping and sorting data with `groupby()` and `sort_values()`.
- General Assembly — `10-matplotlib-practice.ipynb`. Used as a reference for filtering records and creating bar charts.
