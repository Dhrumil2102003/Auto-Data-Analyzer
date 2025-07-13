import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    mean_squared_error, r2_score
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, SVR
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd

def run_models(df):
    st.header("🧠 Machine Learning Models")

    all_columns = df.columns.tolist()
    target_column = st.selectbox("🎯 Select Target Column (skip for clustering)", ["None (Clustering)"] + all_columns)

    task_type = st.radio("🧪 Select Task Type", ["Classification", "Regression", "Clustering"])

    # Set X and y
    if task_type == "Clustering":
        X = df.copy()
        y = None
    else:
        if target_column == "None (Clustering)":
            st.error("❌ Please select a valid target column for classification/regression.")
            return
        X = df.drop(columns=[target_column])
        y = df[target_column]

    # Encode categorical features
    cat_cols = X.select_dtypes(include=['object']).columns.tolist()
    if cat_cols:
        encoding = st.radio("🔤 Feature Encoding", ["Label Encoding", "One-Hot Encoding"], horizontal=True)
        try:
            if encoding == "One-Hot Encoding":
                X = pd.get_dummies(X)
            else:
                for col in cat_cols:
                    X[col] = LabelEncoder().fit_transform(X[col].astype(str))
        except Exception as e:
            st.error(f"⚠️ Feature Encoding Error: {e}")
            return

    # Encode target if classification
    if task_type == "Classification" and y.dtype == 'object':
        y = LabelEncoder().fit_transform(y)

    # Train-test split
    if task_type != "Clustering":
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            st.info(f"📊 Train/Test Split: {X_train.shape[0]} train rows, {X_test.shape[0]} test rows")
        except Exception as e:
            st.error(f"❌ Train-Test Split Error: {e}")
            return

    # ------------------------ MODEL CHOICE ------------------------
    if task_type == "Classification":
        model_name = st.selectbox("🤖 Choose Classifier", ["Decision Tree", "KNN", "SVM"])
        if model_name == "Decision Tree":
            model = DecisionTreeClassifier()
        elif model_name == "KNN":
            model = KNeighborsClassifier()
        elif model_name == "SVM":
            model = SVC(probability=True)

    elif task_type == "Regression":
        model_name = st.selectbox("📈 Choose Regressor", ["Linear Regression", "Decision Tree Regressor", "SVR"])
        if model_name == "Linear Regression":
            model = LinearRegression()
        elif model_name == "Decision Tree Regressor":
            model = DecisionTreeRegressor()
        elif model_name == "SVR":
            model = SVR()

    elif task_type == "Clustering":
        cluster_model = st.selectbox("🔗 Select Clustering Algorithm", ["KMeans", "Agglomerative Clustering", "DBSCAN"])
        if cluster_model == "KMeans":
            n_clusters = st.slider("Number of Clusters (k)", 2, 10, 3)
            model = KMeans(n_clusters=n_clusters)
        elif cluster_model == "Agglomerative Clustering":
            n_clusters = st.slider("Number of Clusters", 2, 10, 3)
            model = AgglomerativeClustering(n_clusters=n_clusters)
        elif cluster_model == "DBSCAN":
            eps = st.slider("Epsilon (eps)", 0.1, 5.0, 0.5)
            min_samples = st.slider("Min Samples", 1, 10, 5)
            model = DBSCAN(eps=eps, min_samples=min_samples)
        else:
            st.error("❌ Unsupported clustering method.")
            return

    # ------------------------ TRAIN & EVALUATE ------------------------
    try:
        if task_type == "Clustering":
            model.fit(X)
            labels = model.labels_
            st.subheader("🧮 Clustering Results")
            st.write("📊 Unique Cluster Labels:", np.unique(labels))
            df["Cluster"] = labels
            st.dataframe(df)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            train_pred = model.predict(X_train)

            st.subheader("📊 Model Evaluation")

            if task_type == "Classification":
                st.write("✅ Test Accuracy:", accuracy_score(y_test, y_pred))
                st.write("🏋️ Train Accuracy:", accuracy_score(y_train, train_pred))
                st.write("📘 Confusion Matrix:")
                st.write(confusion_matrix(y_test, y_pred))
                st.text(classification_report(y_test, y_pred))

            elif task_type == "Regression":
                st.write("🔢 Test RMSE:", mean_squared_error(y_test, y_pred, squared=False))
                st.write("📈 Test R² Score:", r2_score(y_test, y_pred))
                st.write("🏋️ Train RMSE:", mean_squared_error(y_train, train_pred, squared=False))
                st.write("🏋️ Train R² Score:", r2_score(y_train, train_pred))

    except Exception as e:
        st.error(f"❌ Error during model training or evaluation: {e}")
        return

    # ------------------------ CUSTOM PREDICTION ------------------------
    if task_type != "Clustering" and st.checkbox("🔮 Predict on Custom Input"):
        input_values = st.text_input(f"Enter {X.shape[1]} comma-separated values")
        if input_values:
            try:
                user_input = np.array([float(i) for i in input_values.split(',')]).reshape(1, -1)
                st.success(f"Prediction: {model.predict(user_input)[0]}")
            except Exception as e:
                st.error(f"⚠️ Prediction Error: {e}")
