import pandas as pd

def auto_rename_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('[^A-Za-z0-9_]+', '')
    return df

def remove_outliers(df, cols):
    for col in cols:
        if pd.api.types.is_numeric_dtype(df[col]):
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            df = df[(df[col] >= lower) & (df[col] <= upper)]
    return df
