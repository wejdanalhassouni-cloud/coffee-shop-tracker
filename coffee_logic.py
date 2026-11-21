def calculate_daily_totals(today_sales):
    total_cups = today_sales["Quantity"].sum()
    total_revenue = today_sales["Line Total"].sum()
    return total_cups, total_revenue
def calculate_best_sellers(today_sales):
    cups_by_drink = today_sales.groupby("Name")["Quantity"].sum()
    return cups_by_drink.astype(int).sort_values(ascending=False)
