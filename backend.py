import streamlit as st
import toml
import os

# Path to the TOML file
CONFIG_FILE = "config.toml"

# Load configuration from the TOML file
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return toml.load(file)
    return {}

# Save configuration to the TOML file
def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        toml.dump(config, file)

# Load existing configuration
config = load_config()

# Streamlit app for managing the token
st.title("Manage Configuration")
st.write("Add or update your configuration securely.")

# Display existing token (masked)
existing_token = config.get("github", {}).get("personal_access_token", None)
if existing_token:
    st.text_input("GitHub Personal Access Token (Existing)", value="********", disabled=True)

# Add or update token
with st.form("update_token_form"):
    new_token = st.text_input("Enter New GitHub Personal Access Token", type="password")
    submitted = st.form_submit_button("Save Token")

    if submitted:
        if new_token:
            config["github"] = {"personal_access_token": new_token}
            save_config(config)
            st.success("Token saved successfully!")
        else:
            st.error("Token cannot be empty.")
