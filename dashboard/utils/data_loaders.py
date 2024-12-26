import pandas as pd

def load_user_data():
    return pd.read_csv("data/user_data.csv")

def load_engagement_data():
    return pd.read_csv("data/load_engagement_data.csv")

def load_experience_data():
    return pd.read_csv("data/experience_data.csv")

def load_combined_data():
    return pd.read_csv("data/combined_data.csv")
