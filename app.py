import pandas as pd
import plotly.express as px
import streamlit as st

# Page config
st.set_page_config(page_title="Vehicle Data Explorer", layout="wide")

# Load data
car_data = pd.read_csv("vehicles_us.csv")

# Title
st.title("🚗 Vehicle Data Explorer")
st.markdown(
    """
Explore used vehicle listings through interactive charts and filters.  
Analyze pricing trends, mileage, and vehicle market patterns.
"""
)

# Sidebar filters
st.sidebar.header("Filters")

filtered_data = car_data.copy()

# Manufacturer filter
if "manufacturer" in filtered_data.columns:
    manufacturers = sorted(filtered_data["manufacturer"].dropna().unique())
    selected_manufacturers = st.sidebar.multiselect(
        "Manufacturer",
        manufacturers,
        default=manufacturers[:5]
    )
    if selected_manufacturers:
        filtered_data = filtered_data[
            filtered_data["manufacturer"].isin(selected_manufacturers)
        ]

# Price filter
min_price = int(filtered_data["price"].min())
max_price = int(filtered_data["price"].max())

price_range = st.sidebar.slider(
    "Price Range",
    min_price,
    max_price,
    (min_price, min(max_price, 50000))
)

filtered_data = filtered_data[
    (filtered_data["price"] >= price_range[0]) &
    (filtered_data["price"] <= price_range[1])
]

# Metrics
col1, col2, col3 = st.columns(3)

col1.metric("Vehicles Listed", f"{len(filtered_data):,}")
col2.metric("Average Price", f"${filtered_data['price'].mean():,.0f}")
col3.metric("Average Mileage", f"{filtered_data['odometer'].mean():,.0f} mi")

st.markdown("---")

# Histogram
st.subheader("Mileage Distribution")

fig_hist = px.histogram(
    filtered_data,
    x="odometer",
    nbins=30,
    title="Vehicle Mileage Distribution",
    labels={"odometer": "Mileage (mi)"}
)

st.plotly_chart(fig_hist, use_container_width=True)

# Scatter plot
st.subheader("Price vs Mileage")

fig_scatter = px.scatter(
    filtered_data,
    x="odometer",
    y="price",
    color="manufacturer" if "manufacturer" in filtered_data.columns else None,
    title="Vehicle Price vs Mileage",
    labels={
        "odometer": "Mileage (mi)",
        "price": "Price (USD)"
    },
    opacity=0.7
)

st.plotly_chart(fig_scatter, use_container_width=True)

# Bar chart
if "manufacturer" in filtered_data.columns:
    st.subheader("Average Price by Manufacturer")

    avg_price = (
        filtered_data.groupby("manufacturer")["price"]
        .mean()
        .reset_index()
        .sort_values("price", ascending=False)
        .head(10)
    )

    fig_bar = px.bar(
        avg_price,
        x="manufacturer",
        y="price",
        title="Top 10 Manufacturers by Average Price",
        labels={
            "manufacturer": "Manufacturer",
            "price": "Average Price (USD)"
        }
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# Insights
st.markdown("---")
st.subheader("Key Insights")

st.markdown("""
- Higher mileage vehicles generally tend to have lower prices.  
- Some manufacturers maintain higher average resale values.  
- Filtering by price range helps identify better-value listings.  
""")

st.markdown("---")
st.markdown("Built by **Karen Cruz** | Data Scientist")
