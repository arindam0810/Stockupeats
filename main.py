import streamlit as st
import base64
import random

# Custom CSS for styling
main_page_style = """
<style>
body {
    background-color: #e6f3ff;
}

.stButton>button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.stButton>button:hover {
    background-color: #45a049;
}

.stTextInput>div>div>input {
    border-radius: 4px;
}
</style>
"""

st.set_page_config(layout="wide")

# Apply custom CSS
st.markdown(main_page_style, unsafe_allow_html=True)

# Registered usernames and passwords (for demonstration purposes)
registered_users = {"user1": "password1", "user2": "password2", "user3": "password3"}

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'cart' not in st.session_state:
    st.session_state.cart = {}

# Page title and header
st.title("StockUpEats")
st.header("Welcome to StockUpEats - Your Favorite Food Ordering App!")

# Login form
st.subheader("Login")
username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_button = st.button("Login")

if login_button:
    if username in registered_users:
        if password == registered_users[username]:
            st.session_state.logged_in = True
            st.success(f"Welcome back, {username}!")
            st.write("Redirecting to the main interface...")
            # Add a redirect or load the main interface here
        else:
            st.error("Incorrect password. Please try again.")
    else:
        st.error("User not found. Please check your username.")

# Check if user is logged in before displaying content
if st.session_state.logged_in:
    # Continue with your existing code

    # Example menu items structured by categories
    menu_items = {
        "Snacks": {
            "Vada Pav": {"price": 25.00, "image": "data:image/png;base64," + base64.b64encode(open("vadapav.png", "rb").read()).decode()},
            "Pizza": {"price": 150.00, "image": "data:image/png;base64," + base64.b64encode(open("pizza.png", "rb").read()).decode()},
            "Burger": {"price": 55.00, "image": "data:image/png;base64," + base64.b64encode(open("burger.png", "rb").read()).decode()},
        },
        "Desserts": {
            "Ice Cream": {"price": 40.00, "image": "data:image/png;base64," + base64.b64encode(open("icecream.png", "rb").read()).decode()},
            "Cake": {"price": 55.00, "image": "data:image/png;base64," + base64.b64encode(open("cake.png", "rb").read()).decode()},
        },
        # Add more categories and items as needed
    }

    if 'order' not in st.session_state:
        st.session_state.order = {}

    # Function to add items to the order
    def add_to_order(category, item_name):
        item_key = f"{category} - {item_name}"
        if item_key in st.session_state.order:
            st.session_state.order[item_key]['quantity'] += 1
        else:
            st.session_state.order[item_key] = {"name": item_name, "category": category, "quantity": 1, "price": menu_items[category][item_name]['price']}

    # Title of the app
    st.title('StockUpEats')

    # Option menu for choosing between sections
    selected_option = st.sidebar.selectbox("Choose an option:", ["Menu", "Meet Our Team", "Give Feedback", "Cart"])

    if selected_option == "Meet Our Team":
        # Meet Our Team section
        st.header("Meet Our Team")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image("arindam.png", width=150)
            st.write("Arindam Pandey")

        with col2:
            st.image("sankalp.png", width=150)
            st.write("Sankalp Hargode")

        with col3:
            st.image("vinayak.png", width=150)
            st.write("Vinayak Punj")

        with col4:
            st.image("sagar.png", width=150)
            st.write("Sagar Tarachandani")

    elif selected_option == "Give Feedback":
        # Give Feedback section
        st.header("Give Feedback")
        feedback = st.text_area("Please provide your feedback here:", "")
        if st.button("Submit Feedback"):
            # Process feedback here (e.g., save to database)
            st.success("Thank you for your feedback!")

    elif selected_option == "Cart":
        st.header("Your Cart")
        for item, details in st.session_state.cart.items():
            st.write(f"{item}: {details['quantity']}")

        if st.button("Proceed to Checkout"):
            # Add code to proceed to checkout
            payment_option = st.radio("Choose a payment option:", ["Pay at Counter", "Pay Online"])
            if payment_option == "Pay at Counter":
                st.success("Redirecting you to pay at the counter.")
                order_number = random.randint(100, 999)
                st.success(f"Order placed! Your order number is {order_number}.")
            elif payment_option == "Pay Online":
                st.success("Redirecting you to pay online.")
                order_number = random.randint(100, 999)
                st.success(f"Order placed! Your order number is {order_number}.")

    else:
        # Menu section
        st.header("Menu")
        search_query = st.text_input("Search", "").lower()

        # Display menu items based on search query
        for category, items in menu_items.items():
            with st.expander(category, expanded=True):
                for item_name, details in items.items():
                    if search_query in item_name.lower():
                        st.image(details['image'], width=150, caption=item_name)
                        st.write(f"Price: ₹{details['price']:.2f}")
                        # Use item_name and category as part of the key to ensure uniqueness
                        button_key = f"add_{category}_{item_name}".replace(" ", "_").lower()
                        if st.button(f"Add to Order", key=button_key):
                            add_to_order(category, item_name)
                            if item_name in st.session_state.cart:
                                st.session_state.cart[item_name]['quantity'] += 1
                            else:
                                st.session_state.cart[item_name] = {"name": item_name, "quantity": 1, "price": details['price']}
                        st.text("")
else:
    st.info("Please login to access StockUpEats.")
