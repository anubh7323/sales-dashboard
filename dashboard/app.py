import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# Page Config
st.set_page_config(page_title="Sales Dashboard", layout="wide")

# Constants
DB_PATH = "sales_dashboard.db"


# Helper Functions
@st.cache_data
def load_data():
    if not os.path.exists(DB_PATH):
        st.error(
            f"Database not found at {DB_PATH}. Please run setup_db.py first."
        )
        return None, None

    conn = sqlite3.connect(DB_PATH)

    # Load Sales with Product info
    query = """
        SELECT
            s.sales_id,
            s.date,
            s.region,
            s.quantity,
            s.revenue,
            p.product_name,
            p.category
        FROM Sales s
        JOIN Product p ON s.product_id = p.product_id
    """

    df = pd.read_sql_query(query, conn)

    # Ensure date column is datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Load Inventory
    inventory_query = """
        SELECT
            i.warehouse_location,
            i.stock_level,
            p.product_name,
            p.category
        FROM Inventory i
        JOIN Product p ON i.product_id = p.product_id
    """

    df_inv = pd.read_sql_query(inventory_query, conn)

    conn.close()

    return df, df_inv


# Main App
def main():
    st.title("📊 Sales Performance Dashboard")

    df, df_inv = load_data()

    if df is None:
        return

    # Debug Info (remove later if not needed)
    st.sidebar.caption(f"Pandas Version: {pd.__version__}")

    # Remove invalid dates if any
    df = df.dropna(subset=["date"])

    if df.empty:
        st.error("No valid sales data found.")
        return

    # Sidebar Filters
    st.sidebar.header("Filters")

    # Date Filter
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()

    date_range = st.sidebar.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )

    # Handle single-date selection
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = end_date = date_range[0]

    # Region Filter
    regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
    selected_region = st.sidebar.selectbox("Region", regions)

    # Category Filter
    categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
    selected_category = st.sidebar.selectbox("Category", categories)

    # Apply Filters
    mask = (
        (df["date"] >= pd.to_datetime(start_date))
        & (df["date"] <= pd.to_datetime(end_date))
    )

    if selected_region != "All":
        mask &= df["region"] == selected_region

    if selected_category != "All":
        mask &= df["category"] == selected_category

    filtered_df = df.loc[mask].copy()

    # Empty dataset protection
    if filtered_df.empty:
        st.warning("No data found for the selected filters.")
        return

    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)

    total_revenue = filtered_df["revenue"].sum()
    total_sales = filtered_df["sales_id"].count()
    avg_order_value = filtered_df["revenue"].mean()
    total_units = filtered_df["quantity"].sum()

    col1.metric("Total Revenue", f"${total_revenue:,.2f}")
    col2.metric("Total Transactions", f"{total_sales:,}")
    col3.metric("Avg Order Value", f"${avg_order_value:,.2f}")
    col4.metric("Units Sold", f"{total_units:,}")

    st.markdown("---")

    # Charts Row 1
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Revenue over Time")

        filtered_df["date"] = pd.to_datetime(filtered_df["date"])

        # Use ME (Month End) for newer pandas compatibility
        daily_sales = (
            filtered_df.groupby(
                pd.Grouper(key="date", freq="ME")
            )["revenue"]
            .sum()
            .reset_index()
        )

        fig_line = px.line(
            daily_sales,
            x="date",
            y="revenue",
            markers=True,
            title="Monthly Revenue",
        )

        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.subheader("Sales by Region")

        region_sales = (
            filtered_df.groupby("region")["revenue"]
            .sum()
            .reset_index()
        )

        fig_bar = px.bar(
            region_sales,
            x="region",
            y="revenue",
            color="region",
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    # Charts Row 2
    c3, c4 = st.columns(2)

    with c3:
        st.subheader("Top 5 Products")

        top_products = (
            filtered_df.groupby("product_name")["revenue"]
            .sum()
            .nlargest(5)
            .reset_index()
        )

        fig_prod = px.bar(
            top_products,
            x="revenue",
            y="product_name",
            orientation="h",
        )

        st.plotly_chart(fig_prod, use_container_width=True)

    with c4:
        st.subheader("Sales by Category")

        cat_sales = (
            filtered_df.groupby("category")["revenue"]
            .sum()
            .reset_index()
        )

        fig_pie = px.pie(
            cat_sales,
            values="revenue",
            names="category",
        )

        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # Inventory Section
    st.subheader("Current Inventory Levels (Low Stock Warning)")

    low_stock = (
        df_inv[df_inv["stock_level"] < 50]
        .sort_values("stock_level")
    )

    if not low_stock.empty:
        st.dataframe(low_stock, use_container_width=True)
    else:
        st.success("No low stock items found.")

    # Raw Data
    with st.expander("View Raw Sales Data"):
        st.dataframe(
            filtered_df.sort_values(
                "date",
                ascending=False
            ),
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
