Smart Expense Analyzer

 1. Project Overview

The **Smart Expense Analyzer** is a Python-based personal finance management project designed to help users analyze their spending habits, monitor budgets, visualize expense patterns, and estimate future monthly expenses using Machine Learning.

The project uses Python libraries for data processing and visualization, SQLite for database management, Scikit-learn for Machine Learning, and Streamlit to develop an interactive web dashboard.

The project is divided into two main parts:

- **Jupyter Notebook (`expense_analysis.ipynb`):** Used for data preprocessing, exploratory data analysis, visualization, budget analysis, database operations, and Machine Learning experimentation.
- **Streamlit Application (`app.py`):** Used to provide an interactive dashboard where users can view expense summaries, analyze spending patterns, monitor budgets, and explore expense predictions.

 2. Project Objectives

- Analyze personal expense records using Python.
- Clean and preprocess expense data before analysis.
- Calculate total, average, and category-wise expenses.
- Analyze monthly spending and payment methods.
- Visualize spending patterns through charts and graphs.
- Compare actual spending against predefined budgets.
- Store and retrieve expense records using SQLite.
- Implement a Linear Regression model to estimate future monthly expenses.
- Develop an interactive dashboard using Streamlit.

 3. Technologies and Libraries Used

| Technology | Purpose |
| Python | Main programming language |
| Jupyter Notebook | Data analysis, experimentation, and ML development |
| Pandas | Data loading, cleaning, grouping, and analysis |
| NumPy | Numerical calculations and ML evaluation |
| Matplotlib | Charts and graphical visualization |
| Scikit-learn | Linear Regression and model evaluation |
| SQLite | Persistent storage and retrieval of expense records |
| SQL | Database queries, filtering, insertion, and aggregation |
| Streamlit | Interactive web dashboard |
| Git and GitHub | Version control and project hosting |

4. Project Structure

```text
Smart-Expense-Analyzer/
│
├── app.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── expenses.csv
│   └── expenses.db
│
└── notebook/
    └── expense_analysis.ipynb
```

- `app.py`: Main Streamlit application.
- `README.md`: Project documentation.
- `requirements.txt`: Python dependencies required to run the project.
- `data/expenses.csv`: Expense dataset used for analysis and input.
- `data/expenses.db`: SQLite database used to store expense records.
- `notebook/expense_analysis.ipynb`: Notebook containing data analysis, visualizations, database experiments, and ML implementation.



 5. Dataset Description

The project uses expense records containing the following fields:

| Column | Description | Example |

| Date | Date of the transaction | 2026-01-02 |
| Category | Expense category | Food |
| Description | Details of the transaction | Breakfast |
| Amount | Amount spent | 80 |
| Payment_Method | Payment method used | UPI |

Example record:

```csv
Date,Category,Description,Amount,Payment_Method
2026-01-02,Food,Breakfast,80,UPI
2026-01-03,Travel,Bus,40,Cash
2026-01-04,Education,Books,650,UPI
```

The dataset is used to understand spending behavior, calculate summaries, generate charts, evaluate budgets, and prepare monthly data for expense forecasting.

6. Implementation in Jupyter Notebook

The Jupyter Notebook is the analysis and experimentation component of the project. It contains the following stages.

 6.1 Data Loading

Pandas is used to load expense records from a CSV file into a DataFrame.


df = pd.read_csv("../data/expenses.csv", sep="\t")


The separator should match the actual format of the CSV file. If the file uses commas, use the default comma separator instead of `sep="\t"`.

### 6.2 Data Cleaning and Preprocessing

The dataset is inspected and prepared for analysis by:

- Checking column names and data types.
- Identifying missing values and duplicate records.
- Converting the Date column into a datetime format.
- Converting Amount into a numeric format.
- Preparing consistent data for calculations and visualization.

Example:

python
df.columns = df.columns.str.strip()
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")


Data cleaning helps prevent incorrect calculations and makes the dataset more reliable.

 6.3 Exploratory Data Analysis (EDA)

Exploratory Data Analysis is used to understand the dataset and identify spending patterns.

The notebook calculates:

- Total expenses.
- Average transaction amount.
- Highest and lowest transactions.
- Number of transactions.
- Category-wise spending.
- Payment-method-wise spending.
- Monthly spending totals.
- Transaction counts and other spending patterns.

Example:


category_spending = (
    df.groupby("Category")["Amount"]
      .sum()
      .sort_values(ascending=False)
)


This groups transactions by category and calculates the total amount spent in each category.

 6.4 Data Visualization

Matplotlib is used to represent the analysis visually.

The notebook includes visualizations such as:

- Bar chart for category-wise spending.
- Pie chart for expense distribution.
- Line chart for monthly spending trends.
- Bar chart for payment-method analysis.
- Transaction-count charts.

These visualizations help identify major spending categories and changes in expenses over time.

### 6.5 Budget Analysis

The notebook compares predefined category budgets with actual spending.

For example, if the Food budget is ₹10,000 and actual spending is ₹12,000, the category is marked as over budget by ₹2,000.

The analysis calculates:

- Budget allocated to each category.
- Actual spending.
- Remaining budget.
- Budget status.
- Percentage of budget used.

This feature helps users identify categories where spending exceeds the planned limit.

### 6.6 SQLite Database Integration

SQLite is used to store and retrieve expense records in a structured database.

The notebook demonstrates database operations such as:

- Creating the expenses table.
- Inserting expense records.
- Reading records from the database.
- Filtering records using SQL.
- Aggregating expenses by category.

Example SQL query:


SELECT Category, SUM(Amount) AS Total_Expense
FROM expenses
GROUP BY Category;


SQLite provides persistent storage, allowing records to remain available after the notebook or application is closed. Care must be taken to avoid inserting the same records repeatedly.

### 6.7 Machine Learning: Linear Regression

The notebook implements **Linear Regression** to estimate future monthly expenses using historical monthly spending data.

**Input feature:** Month Number  
**Target variable:** Total Monthly Expense

The process involves:

1. Grouping transaction amounts by month.
2. Assigning a sequential number to each month.
3. Splitting the dataset into training and testing sets.
4. Training a Linear Regression model.
5. Predicting expenses for test data.
6. Evaluating the predictions.
7. Estimating the next month's expense.

The model learns a linear relationship represented by:


Expense = m × Month_Number + c


Here, `m` represents the slope and `c` represents the intercept learned by the model.

Example:

If a trained model learns the illustrative equation:


Expense = 100 × Month_Number + 8000


For Month 10, the estimated expense would be:


Expense = 100 × 10 + 8000
        = ₹9,000


This is an illustrative example, not the actual prediction from the project's trained model.

 6.8 Model Evaluation

The notebook uses the following evaluation metrics:

- **MAE (Mean Absolute Error):** Measures the average absolute difference between actual and predicted expenses.
- **RMSE (Root Mean Squared Error):** Measures prediction error while penalizing larger errors more heavily.
- **R² Score:** Indicates how well the model explains variation in the target values. A negative score means it performed worse than a constant-mean baseline on that test set.

These metrics help assess model performance. The reliability of the forecast depends on the amount of historical data, the selected features, and the suitability of Linear Regression for the spending pattern.

## 7. Implementation in `app.py`

The `app.py` file contains the Streamlit application that presents the project's features through a user-friendly web interface.

### 7.1 Application Setup

Streamlit is used to configure the page, display headings, organize the dashboard, and provide interactive components.

The application can be launched using:


python -m streamlit run app.py
```

### 7.2 Expense Data Input

The application supports CSV file upload. It can also attempt to load stored expense records from
