import streamlit as st
import re

# Page configuration
st.set_page_config(
    page_title="Alpha Restaurant AI",
    page_icon="🍽️",
    layout="centered"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .stButton button {
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
    }
    .order-summary {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# menus
veg_menu = {
    "paneer biryani": 180,
    "veg fried rice": 120,
    "veg noodles": 130
}

nonveg_menu = {
    "chicken biryani": 220,
    "mutton biryani": 280,
    "fish curry": 250,
    "chicken fried rice": 160
}

number_words = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
}

def get_quantity(text):
    num = re.search(r'\d+', text)
    if num:
        return int(num.group())
    
    text_lower = text.lower()
    for word, val in number_words.items():
        if word in text_lower:
            return val
    return 1

def process_order(sentence, menu):
    if not sentence:
        return []
    
    parts = re.split(r'and|,', sentence.lower())
    orders = []
    
    for part in parts:
        qty = get_quantity(part)
        for item in menu:
            if item in part:
                orders.append((item, qty))
                break
    
    return orders

# Main app
st.title("🍽️ Alpha Restaurant AI Ordering")
st.markdown("---")

# Get table number from query params
params = st.query_params
table = params.get("table", ["Unknown"])[0] if isinstance(params.get("table"), list) else params.get("table", "Unknown")

# Table info in sidebar
with st.sidebar:
    st.header("📋 Table Information")
    st.info(f"**Table Number:** {table}")
    st.markdown("---")
    st.header("ℹ️ How to Order")
    st.write("""
    1. Select menu type
    2. Type your order naturally
    3. Click 'Place Order'
    
    **Example:** "2 chicken biryani and 1 fish curry"
    """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    food_type = st.radio(
        "Choose Menu Type",
        ["Veg", "Non-Veg"],
        horizontal=True
    )

menu = veg_menu if food_type == "Veg" else nonveg_menu

# Display menu
with col2:
    st.subheader("📜 Today's Menu")
    for item, price in menu.items():
        st.write(f"• {item.title()} - ₹{price}")

st.markdown("---")

# Order input
order_text = st.text_input(
    "📝 Enter your order:",
    placeholder="Example: 2 chicken biryani and 1 fish curry",
    key="order_input"
)

# Place order button
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    place_order = st.button("🛎️ Place Order", use_container_width=True)

if place_order and order_text:
    order_list = process_order(order_text, menu)
    
    if order_list:
        total = 0
        
        st.markdown("---")
        st.subheader("📊 Order Summary")
        
        with st.container():
            st.markdown('<div class="order-summary">', unsafe_allow_html=True)
            
            for item, qty in order_list:
                price = menu[item] * qty
                total += price
                st.write(f"**{item.title()}** x {qty} = ₹{price}")
            
            st.markdown("---")
            
            # Calculate bill
            gst = total * 0.05
            final = total + gst
            
            # Display bill
            col1, col2 = st.columns(2)
            with col1:
                st.write("Subtotal:")
                st.write("GST (5%):")
                st.write("**Total Bill:**")
            with col2:
                st.write(f"₹{total}")
                st.write(f"₹{round(gst, 2)}")
                st.write(f"**₹{round(final, 2)}**")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.success(f"✅ Order received from Table {table}! Your food will be served soon.")
        
        # Add a reorder button
        if st.button("🔄 Place Another Order"):
            st.rerun()
    else:
        st.error("❌ No items recognized. Please check your order format.")
elif place_order and not order_text:
    st.warning("⚠️ Please enter your order first.")

# Footer
st.markdown("---")
st.markdown("🍳 *Happy Dining!*")
