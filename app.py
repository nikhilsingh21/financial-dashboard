import os
import base64
from io import BytesIO
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Financial Dashboard"),
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Button('Upload Excel File'),
            multiple=False
        ),
        html.Div(id='file-error', style={'color': 'red'})
    ]),
    html.Div(id='data-table'),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Spending by Category', value='tab-1'),
        dcc.Tab(label='Family Financial Scores', value='tab-2'),
        dcc.Tab(label='Member Spending Trends', value='tab-3'),
        dcc.Tab(label='Income vs Savings', value='tab-4'),
    ]),
    html.Div(id='tabs-content')
])

def load_and_preprocess_data(file_path):
    try:
        df = pd.read_excel(file_path)
        df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], format='%d-%m-%Y')
        return df, None
    except Exception as e:
        return None, f"Error loading and preprocessing data: {str(e)}"

def calculate_financial_score(df):
    try:
        df['Savings-to-Income Ratio'] = df['Savings'] / df['Income'] * 100
        df['Expenses-to-Income Ratio'] = df['Monthly Expenses'] / df['Income'] * 100
        df['Loan-to-Income Ratio'] = df['Loan Payments'] / df['Income'] * 100
        df['Credit Card Spending'] = df['Credit Card Spending'] / df['Income'] * 100
        df['Financial Score'] = 100 - df['Expenses-to-Income Ratio'] - df['Loan-to-Income Ratio'] + df['Savings-to-Income Ratio']
        df['Financial Score'] = df['Financial Score'].clip(0, 100)
        return df, None
    except Exception as e:
        return None, f"Error calculating financial scores: {str(e)}"

def generate_plots(df):
    try:
        category_spending = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        fig_category = go.Figure(data=[go.Bar(x=category_spending.index, y=category_spending.values)])
        fig_category.update_layout(title='Spending Distribution by Category', xaxis_title='Category', yaxis_title='Amount')
        family_scores = df.groupby('Family ID')['Financial Score'].mean()
        fig_family = go.Figure(data=[go.Bar(x=family_scores.index, y=family_scores.values)])
        fig_family.update_layout(title='Family Financial Scores', xaxis_title='Family ID', yaxis_title='Financial Score')
        member_spending = df.groupby('Member ID')['Amount'].sum().sort_values(ascending=False)
        fig_trends = go.Figure(data=[go.Scatter(x=member_spending.index, y=member_spending.values, mode='lines+markers')])
        fig_trends.update_layout(title='Member Spending Trends', xaxis_title='Member ID', yaxis_title='Amount')
        fig_income_savings = px.scatter(df, x='Income', y='Savings', color='Family ID', title="Income vs Savings")
        fig_income_savings.update_layout(xaxis_title='Income', yaxis_title='Savings')
        return fig_category, fig_family, fig_trends, fig_income_savings, None
    except Exception as e:
        return None, None, None, None, f"Error generating visualizations: {str(e)}"

@app.callback(
    [Output('data-table', 'children'),
     Output('tabs-content', 'children'),
     Output('file-error', 'children')],
    [Input('upload-data', 'contents')]
)
def update_output(contents):
    if contents is None:
        return None, None, None
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        upload_path = os.path.join('uploads', 'uploaded_data.xlsx')
        with open(upload_path, 'wb') as f:
            f.write(decoded)
        df, error_message = load_and_preprocess_data(upload_path)
        if df is None:
            return None, None, error_message
        df, error_message = calculate_financial_score(df)
        if df is None:
            return None, None, error_message
        fig_category, fig_family, fig_trends, fig_income_savings, error_message = generate_plots(df)
        if error_message:
            return None, None, error_message
        tabs_content = html.Div([
            dcc.Graph(figure=fig_category),
            dcc.Graph(figure=fig_family),
            dcc.Graph(figure=fig_trends),
            dcc.Graph(figure=fig_income_savings)
        ])
        return None, tabs_content, None
    except Exception as e:
        return None, None, f"Error: {str(e)}"

if __name__ == '__main__':
    app.run_server(debug=True)
