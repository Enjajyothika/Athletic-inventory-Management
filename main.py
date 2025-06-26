import json
import streamlit as st
import os
import pandas as pd
import random
import time

# ------------------------------
# Helper Functions
# ------------------------------
def load_equipment_data():
    if not os.path.isfile("Eq_data.json"):
        return {}
    with open("Eq_data.json", 'r') as fd:
        return json.load(fd)

def save_equipment_data(data):
    with open("Eq_data.json", 'w') as fd:
        json.dump(data, fd)

def load_user_data():
    if not os.path.isfile("user_data.json"):
        return {}
    with open("user_data.json", 'r') as fd:
        return json.load(fd)

def save_user_data(data):
    with open("user_data.json", 'w') as fd:
        json.dump(data, fd)

def admin_login(username, password):
    return username == "admin" and password == "admin123"

def user_login(username, password):
    user_data = load_user_data()
    return username in user_data and user_data[username]["password"] == password

def user_register(username, password):
    user_data = load_user_data()
    if username in user_data:
        return False, "Username already exists. Please choose another one."
    user_data[username] = {"password": password, "equipment": {}}
    save_user_data(user_data)
    return True, "Registration successful. You can now login."

def display_equipment_data():
    equipment_data = load_equipment_data()
    if equipment_data:
        df = pd.DataFrame.from_dict(equipment_data, orient='index')
        df.index.name = "ID"
        st.dataframe(df)
    else:
        st.info("No equipment data found.")

def insert_equipment():
    eq_data = load_equipment_data()
    new_id = st.text_input("Enter New Equipment ID")
    if new_id and new_id not in eq_data:
        name = st.text_input("Equipment Name")
        category = st.text_input("Category")
        price = st.number_input("Price", min_value=0.0)
        qty = st.number_input("Quantity", min_value=0)
        date = st.date_input("Date").strftime("%d/%m/%Y")

        if st.button("Add Equipment"):
            eq_data[new_id] = {
                "Equipment_name": name,
                "Category": category,
                "Price": price,
                "Quantity": qty,
                "Date": date
            }
            save_equipment_data(eq_data)
            st.success("Equipment added successfully!")
    elif new_id in eq_data:
        st.warning("Equipment ID already exists.")

def delete_equipment():
    eq_data = load_equipment_data()
    del_id = st.text_input("Enter Equipment ID to Delete")
    if del_id and st.button("Delete"):
        if del_id in eq_data:
            del eq_data[del_id]
            save_equipment_data(eq_data)
            st.success("Deleted successfully!")
        else:
            st.error("Equipment ID not found.")

def user_collect_equipment():
    eq_data = load_equipment_data()
    user_data = load_user_data()
    username = st.session_state.username

    st.subheader("Collect Equipment")
    eq_ids = list(eq_data.keys())
    if eq_ids:
        selected_id = st.selectbox("Select Equipment ID", eq_ids)
        max_qty = eq_data[selected_id]["Quantity"]
        qty = st.number_input("Enter quantity to collect", min_value=1, max_value=int(max_qty))

        if st.button("Collect"):
            eq_data[selected_id]["Quantity"] -= qty
            user_equipment = user_data[username].get("equipment", {})
            if selected_id in user_equipment:
                user_equipment[selected_id]["Quantity"] += qty
            else:
                user_equipment[selected_id] = {
                    "Equipment_name": eq_data[selected_id]["Equipment_name"],
                    "Category": eq_data[selected_id]["Category"],
                    "Quantity": qty
                }
            user_data[username]["equipment"] = user_equipment
            save_equipment_data(eq_data)
            save_user_data(user_data)
            st.success("Equipment collected successfully!")
    else:
        st.warning("No equipment available.")

def user_replace_equipment():
    eq_data = load_equipment_data()
    user_data = load_user_data()
    username = st.session_state.username
    user_eq = user_data[username].get("equipment", {})

    st.subheader("Replace Equipment")
    if user_eq:
        old_id = st.selectbox("Select equipment to replace", list(user_eq.keys()))
        new_id = st.selectbox("Select new equipment to take", list(eq_data.keys()))

        if st.button("Replace"):
            qty = user_eq[old_id]["Quantity"]
            if eq_data[new_id]["Quantity"] >= qty:
                eq_data[new_id]["Quantity"] -= qty
                eq_data[old_id]["Quantity"] += qty
                del user_eq[old_id]
                user_eq[new_id] = {
                    "Equipment_name": eq_data[new_id]["Equipment_name"],
                    "Category": eq_data[new_id]["Category"],
                    "Quantity": qty
                }
                user_data[username]["equipment"] = user_eq
                save_equipment_data(eq_data)
                save_user_data(user_data)
                st.success("Equipment replaced successfully!")
            else:
                st.error("Not enough stock to replace with selected equipment.")
    else:
        st.info("You have no equipment to replace.")

def user_view_my_equipment():
    user_data = load_user_data()
    username = st.session_state.username
    user_eq = user_data[username].get("equipment", {})

    st.subheader("My Equipment")
    if user_eq:
        df = pd.DataFrame.from_dict(user_eq, orient='index')
        df.index.name = "Equipment ID"
        st.dataframe(df)
    else:
        st.info("You haven't collected any equipment yet.")

# ------------------------------
# Main Application
# ------------------------------
def main():
    st.set_page_config(page_title="Athletic Inventory System")
    st.title("🏋️ Athletic Equipment Inventory System")

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = ""

    if not st.session_state.logged_in:
        menu_choice = st.sidebar.selectbox("Choose Role", ["Admin", "User"])
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if menu_choice == "Admin" and admin_login(username, password):
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.session_state.username = username
                st.success("Logged in as Admin")
                st.experimental_rerun()
            elif menu_choice == "User" and user_login(username, password):
                st.session_state.logged_in = True
                st.session_state.role = "user"
                st.session_state.username = username
                st.success("Logged in as User")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

        if menu_choice == "User":
            st.subheader("New User? Register Below")
            new_username = st.text_input("New Username")
            new_password = st.text_input("New Password", type="password")
            if st.button("Register"):
                success, message = user_register(new_username, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)
    else:
        st.markdown(f"**👤 Logged in as:** `{st.session_state.username}` ({st.session_state.role})")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = None
            st.experimental_rerun()

        if st.session_state.role == "admin":
            st.subheader("Admin Panel")
            action = st.selectbox("Select Action", ["Display Equipment", "Insert Equipment", "Delete Equipment"])
            if action == "Display Equipment":
                display_equipment_data()
            elif action == "Insert Equipment":
                insert_equipment()
            elif action == "Delete Equipment":
                delete_equipment()

        elif st.session_state.role == "user":
            st.subheader("User Panel")
            action = st.selectbox("Select Action", ["View Equipment", "Collect Equipment", "Replace Equipment", "My Equipment"])
            if action == "View Equipment":
                display_equipment_data()
            elif action == "Collect Equipment":
                user_collect_equipment()
            elif action == "Replace Equipment":
                user_replace_equipment()
            elif action == "My Equipment":
                user_view_my_equipment()

if __name__ == "__main__":
    main()
