Financial Insights Dashboard and Scoring Model

This project involves building a Financial Insights Dashboard and scoring model that helps evaluate the financial health of a family based on their spending and income patterns. It includes data analysis, financial score calculation, interactive visualizations, and an API to expose the scoring model.
Project Overview

1. Data Analysis:
        The dataset includes family and member-level spending data.
        The analysis identifies spending patterns and correlations, such as income vs. expenses and savings vs. spending habits.

2. Financial Scoring Model:
        A score (0–100) evaluates family financial health.
        Factors considered include savings-to-income ratio, monthly expenses as a percentage of income, loan payments, credit card spending, and financial goals met.
        Weighting and scoring logic were designed to give importance to core financial health indicators (e.g., savings and loan payments).

3. Visualizations:
        Visualizations show key insights, such as spending distribution across categories, family financial scores, and member-wise spending trends.
        Plots were created using matplotlib, seaborn, and plotly for better interactivity.

4. Flask API:
        A Flask app serves the financial scoring model via an API, which takes family-level data as input and outputs their financial score and recommendations.

5. Interactive Dashboard:
        An interactive dashboard using Dash allows users to interact with the model, visualize their data, and receive recommendations for improving their financial scores.

Installation
Prerequisites

    Python 3.8+ is required.
    A virtual environment is recommended.

Setup Instructions

    Clone the repository:

git clone https://github.com/yourusername/financial-insights-dashboard.git
cd financial-insights-dashboard

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

Install dependencies:

pip install -r requirements.txt

Run the Flask App:

python app.py

The Flask app will start on http://127.0.0.1:5000.

Run the Dash Dashboard:

    python app.py

    Access the interactive dashboard at http://127.0.0.1:8050.

Model Logic

The financial scoring model is based on the following factors:

    Savings-to-Income Ratio: A higher savings rate improves the score.
    Monthly Expenses: Expenses as a percentage of income affect the score. Higher spending relative to income lowers the score.
    Loan Payments: High loan payments as a percentage of income reduce the score.
    Credit Card Spending: Trends in credit card spending indicate financial discipline. Excessive spending lowers the score.
    Spending Distribution: Categories such as entertainment and travel, when higher, reduce the score.
    Financial Goals Met: Meeting financial goals increases the score.

Justification:

Each factor is assigned a weight based on its impact on overall financial health. These weights are used to compute a normalized score between 0–100, with 0 being financially unhealthy and 100 being financially sound.
Contributing

Feel free to fork the repository and submit pull requests. Issues or improvements are welcome!
License

This project is licensed under the MIT License.
