import pandas as pd
import os

# Load dataset
def load_data(uploaded_file):
    try:
        file_extension = os.path.splitext(uploaded_file.name)[1].lower()
        if file_extension == ".csv":
            df = pd.read_csv(uploaded_file)
        elif file_extension in [".xls", ".xlsx"]:
            df = pd.read_excel(uploaded_file)
        else:
            raise ValueError("Unsupported file format.")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Check and clean data
def check_and_clean_data(df):
    df.dropna(axis=1, how="all", inplace=True)  # Drop columns with all NaN values
    df.drop_duplicates(inplace=True)
    return df

# Identify date column
def get_date_column(df):
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]) or "date" in col.lower():
            return col
    return None

# Save uploaded file to a temporary directory
def save_dataset_to_database(uploaded_file):
    folder_path = "uploaded_datasets"
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path
