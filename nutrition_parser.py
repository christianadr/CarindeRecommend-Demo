import pandas as pd
import re
import plotly.graph_objects as go

def parse_nutrition(nutrition_string):
    nutrient_pattern = r"(\d+(\.\d+)?)(\s+)?(g)?\s+((?!Calories)\w+)"
    matches = re.findall(nutrient_pattern, nutrition_string)
    nutrition_dict = {}
    for match in matches:
        value, _, _, _, nutrient = match
        nutrition_dict[nutrient] = float(value)
    nutrition_df = pd.DataFrame.from_dict(nutrition_dict, orient='index', columns=['Value'])
    fig = plot_nutrition(nutrition_df)
    return fig

def plot_nutrition(nutrition_df):
    fig = go.Figure(data=[go.Pie(labels=nutrition_df.index, values=nutrition_df['Value'])])
    fig.update_layout(legend=dict(orientation="v", x=0, y=0))
    return fig