import streamlit as st
import pandas as pd
from datetime import date
from coffee_logic import calculate_daily_totals, calculate_best_sellers

st.title("Coffee Shop Tracker")

page = st.sidebar.radio(
    "Navigation",
    ["Manage Menu", "Point of Sale", "Daily Dashboard", "Sales Log"]
)

if "menu" not in st.session_state:
    st.session_state["menu"] = pd.DataFrame(
        columns=["Name", "Size", "Price", "Category"]
    )
if "sales" not in st.session_state:
    st.session_state["sales"] = pd.DataFrame(
        columns=["Date", "Name", "Size", "Unit Price", "Quantity", "Line Total"]
    )
if page == "Manage Menu":
    st.subheader("Manage Menu")
    uploaded_menu = st.file_uploader("Upload Menu CSV", type="csv")

    if uploaded_menu is not None:
        if st.button("Load Menu from CSV"):
            menu_columns = ["Name", "Size", "Price", "Category"]

            try:
                imported_menu = pd.read_csv(
                    uploaded_menu,
                    usecols=menu_columns,
                    dtype={"Name": str, "Size": str, "Price": float, "Category": str}
                )

                if imported_menu.isna().any().any() or (imported_menu["Price"] <= 0).any():
                    st.error("Fill in every field and use prices greater than zero.")
                else:
                    st.session_state["menu"] = imported_menu[menu_columns]
                    st.success("Menu loaded.")
            except ValueError:
                st.error("Use a CSV with Name, Size, Price, and Category columns and numeric prices.")

    with st.form("add_drink_form"):
        drink_name = st.text_input("Drink name")

        size_col, price_col = st.columns(2)
        with size_col:
            drink_size = st.selectbox("Size", ["Large", "Medium", "Small"])
        with price_col:
            drink_price = st.number_input("Price (BHD)", min_value=0.0, step=0.1)

        drink_category = st.selectbox(
            "Category", ["Hot Coffee", "Cold Coffee", "Tea", "Other"]
        )
        submitted = st.form_submit_button("Add Drink")

    if submitted:
        if drink_name.strip() == "" or drink_price <= 0:
            st.error("Enter a drink name and a price greater than zero.")
        else:
            new_drink = pd.DataFrame({
                "Name": [drink_name.strip()],
                "Size": [drink_size],
                "Price": [drink_price],
                "Category": [drink_category]
            })

            st.session_state["menu"] = pd.concat(
                [st.session_state["menu"], new_drink],
                ignore_index=True
            )
            st.success("Drink added to the menu.")

    st.dataframe(st.session_state["menu"])
    menu_csv = st.session_state["menu"].to_csv(index=False)

    st.download_button(
        label="Download Menu CSV",
        data=menu_csv,
        file_name="menu.csv",
        mime="text/csv"
    )

elif page == "Point of Sale":
    st.subheader("Point of Sale")
    menu = st.session_state["menu"]

    if len(menu) == 0:
        st.info("Add a drink in Manage Menu first.")
    else:
        drink_names = menu["Name"].unique()
        selected_drink = st.selectbox("Select a drink", drink_names)
        matching_drinks = menu[menu["Name"] == selected_drink]
        available_sizes = matching_drinks["Size"].unique()
        selected_size = st.selectbox("Select a size", available_sizes)
        quantity = st.number_input("Quantity", min_value=1, step=1)
        matching_size = matching_drinks[matching_drinks["Size"] == selected_size]
        unit_price = list(matching_size["Price"])[0]
        line_total = unit_price * quantity
        st.write("Total (BHD):", line_total)
        if "order" not in st.session_state:
            st.session_state["order"] = pd.DataFrame(
                columns=["Name", "Size", "Unit Price", "Quantity", "Line Total"]
            )

        if st.button("Add to Order"):
            new_item = pd.DataFrame({
                "Name": [selected_drink],
                "Size": [selected_size],
                "Unit Price": [unit_price],
                "Quantity": [quantity],
                "Line Total": [line_total]
            })

            st.session_state["order"] = pd.concat(
                [st.session_state["order"], new_item],
                ignore_index=True
            )
            st.subheader("Current Order")
        order = st.session_state["order"]

        if len(order) > 0:
            row_to_remove = st.selectbox("Select a row to remove", order.index)

            if st.button("Remove from Order"):
                st.session_state["order"] = order.drop(row_to_remove)

        if len(st.session_state["order"]) > 0:
            if st.button("Confirm Order"):
                confirmed_order = st.session_state["order"].copy()
                confirmed_order["Date"] = str(date.today())

                st.session_state["sales"] = pd.concat(
                    [st.session_state["sales"], confirmed_order],
                    ignore_index=True
                )

                st.session_state["order"] = pd.DataFrame(
                    columns=["Name", "Size", "Unit Price", "Quantity", "Line Total"]
                )
                st.success("Order confirmed.")

        st.dataframe(st.session_state["order"])
elif page == "Sales Log":
    st.subheader("Sales Log")
    uploaded_sales = st.file_uploader("Upload Sales CSV", type="csv")

    if uploaded_sales is not None:
        if st.button("Load Sales from CSV"):
            sales_columns = ["Date", "Name", "Size", "Unit Price", "Quantity", "Line Total"]

            try:
                imported_sales = pd.read_csv(
                    uploaded_sales,
                    usecols=sales_columns,
                    dtype={
                        "Name": str,
                        "Size": str,
                        "Unit Price": float,
                        "Quantity": int,
                        "Line Total": float
                    }
                )

                if imported_sales.isna().any().any():
                    st.error("Fill in all fields in the sales CSV.")
                else:
                    imported_sales["Date"] = pd.to_datetime(
                        imported_sales["Date"]
                    ).dt.strftime("%Y-%m-%d")

                    st.session_state["sales"] = imported_sales[sales_columns]
                    st.success("Sales loaded.")
            except ValueError:
                st.error("Check the sales CSV columns, dates, and numbers.")
    st.dataframe(st.session_state["sales"])
    sales_csv = st.session_state["sales"].to_csv(index=False)

    st.download_button(
        label="Download Sales CSV",
        data=sales_csv,
        file_name="sales.csv",
        mime="text/csv"
    )
elif page == "Daily Dashboard":
    st.subheader("Daily Dashboard")

    sales = st.session_state["sales"]
    today = str(date.today())
    today_sales = sales[sales["Date"] == today]

    total_cups, total_revenue = calculate_daily_totals(today_sales)

    cups_col, revenue_col = st.columns(2)
    cups_col.metric("Cups Sold Today", int(total_cups))
    revenue_col.metric("Today's Revenue", f"{total_revenue:.2f} BHD")
    st.subheader("Daily Sales Goal")

    daily_goal = st.number_input(
        "Sales goal (BHD)",
        min_value=0.01,
        value=20.0,
        step=1.0
    )

    goal_percent = (total_revenue / daily_goal) * 100
    st.write(f"Goal achieved: {goal_percent:.1f}%")

    if total_revenue >= daily_goal:
        st.success("Goal reached!")
    else:
        remaining = daily_goal - total_revenue
        st.write(f"Remaining to reach goal: {remaining:.2f} BHD")
    if len(today_sales) > 0:
        cups_by_drink = calculate_best_sellers(today_sales)

        ax = cups_by_drink.plot(
            kind="bar",
            color="#875333",
            title="Best Sellers Today",
            xlabel="Drink",
            ylabel="Cups Sold",
            rot=0
        )
        st.pyplot(ax.figure)
