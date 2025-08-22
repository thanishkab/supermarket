import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Supermarket Daily Sales", layout="wide")
st.title("🛒 Supermarket Daily Sales Tracker")

# Initialize session state for storing sales data
if "sales" not in st.session_state:
    st.session_state.sales = pd.DataFrame(columns=["Product", "Quantity", "Price", "Revenue"])

# --- Sales Input Form ---
st.subheader("Enter Today's Sales")
with st.form("sales_form", clear_on_submit=True):
    product = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1, step=1)
    price = st.number_input("Price per Unit (₹)", min_value=0.0, step=0.5)
    submitted = st.form_submit_button("➕ Add Sale")

    if submitted:
        if product.strip() != "":
            revenue = quantity * price
            new_row = {"Product": product, "Quantity": quantity, "Price": price, "Revenue": revenue}
            st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"✅ Added {product} - Revenue: ₹{revenue:.2f}")
        else:
            st.warning("⚠️ Please enter a valid product name.")

# --- Display Sales Records ---
st.subheader("📋 Sales Records")
if st.session_state.sales.empty:
    st.info("No sales records yet. Add sales using the form above 👆")
else:
    st.dataframe(st.session_state.sales, use_container_width=True)

    # --- Total Revenue ---
    total_revenue = st.session_state.sales["Revenue"].sum()
    st.metric("💰 Total Revenue Today", f"₹{total_revenue:.2f}")

    # --- Revenue by Product Chart ---
    fig = px.bar(
        st.session_state.sales,
        x="Product",
        y="Revenue",
        title="Revenue by Product",
        color="Product",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- Download Option ---
    csv = st.session_state.sales.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Sales Data (CSV)",
        data=csv,
        file_name="daily_sales.csv",
        mime="text/csv",
    )
