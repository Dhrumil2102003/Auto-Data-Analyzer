# gamma3.py - Uses Google Gemini API to explain charts
import google.generativeai as genai
import os

GEMINI_API_KEY = "AIzaSyAYQi3X9u3Sf7Iwryalw6jGpP2ycGYhEag"
genai.configure(api_key=GEMINI_API_KEY)

def explain_chart(chart_type, x_col=None, y_col=None, name_col=None, date_col=None, value_col=None):
    try:
        if chart_type.lower() == "pie chart":
            if name_col and value_col:
                prompt = f"""
                I have a Pie Chart that visualizes data with categories as {name_col} and their corresponding values as {value_col}. 
                Can you explain what insights this chart might provide?
                """
            else:
                return "Pie chart explanation requires category and value columns."

        elif chart_type.lower() == "time series":
          if date_col and y_col:
            prompt = f"""
            I have a Time Series chart that visualizes data with dates as {date_col} and values as {y_col}.
            Can you explain what insights this chart might provide?
            """
          else:
            return "Time Series Chart explanation requires date and value columns"
        elif x_col and y_col:
            prompt = f"""
            I have a {chart_type} that visualizes data with X-axis as {x_col} and Y-axis as {y_col}. 
            Can you explain what insights this chart might provide?
            """
        elif name_col:
            prompt = f"""
            I have a {chart_type} that visualizes data with X-axis as {name_col}. 
            Can you explain what insights this chart might provide?
            """
        elif date_col:
            prompt = f"""
            I have a {chart_type} that visualizes data with X-axis as {date_col}. 
            Can you explain what insights this chart might provide?
            """
        else:
            return "Insufficient information to explain the chart."

        model = genai.GenerativeModel("gemini-2.0-flash") #or gemini-2.0-flash, or gemini-pro-vision, etc.
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"Error fetching explanation: {str(e)}"
