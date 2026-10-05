import streamlit as st
import pandas as pd
import sqlite3
from sklearn.linear_model import LinearRegression


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Smart Expense Analyzer",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Smart Expense Analyzer")
st.write(
    "Analyze your expenses, monitor your budget, "
    "and predict future spending using Machine Learning."
)


# =========================================================
# CSV UPLOAD
# =========================================================

st.sidebar.header("📂 Upload Expense Data")

uploaded_file = st.sidebar.file_uploader(
    "Choose an expense CSV file",
    type=["csv"]
)


# =========================================================
# LOAD DATA
# =========================================================

data = None

if uploaded_file is not None:

    try:

        # Try normal CSV
        data = pd.read_csv(uploaded_file)

        # If only one column is detected,
        # try tab-separated format
        if len(data.columns) == 1:

            uploaded_file.seek(0)

            data = pd.read_csv(
                uploaded_file,
                sep="\t"
            )

        st.sidebar.success(
            "CSV uploaded successfully!"
        )

    except Exception as error:

        st.error(
            f"Unable to read CSV: {error}"
        )

        st.stop()


else:

    # Try database first
    try:

        connection = sqlite3.connect(
            "data/expenses.db"
        )

        data = pd.read_sql(
            "SELECT * FROM expenses",
            connection
        )

        connection.close()

        if data.empty:

            data = pd.read_csv(
                "data/expenses.csv",
                sep="\t"
            )

            st.sidebar.info(
                "Using default expenses.csv"
            )

        else:

            st.sidebar.info(
                "Using SQLite database"
            )

    except Exception:

        # If database fails, use CSV
        try:

            data = pd.read_csv(
                "data/expenses.csv",
                sep="\t"
            )

            st.sidebar.info(
                "Using default expenses.csv"
            )

        except Exception:

            st.error(
                "No expense data found. "
                "Please upload a CSV file."
            )

            st.stop()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

data.columns = [
    str(column)
    .strip()
    .lower()
    .replace(" ", "_")
    for column in data.columns
]


# Handle possible column variations

data = data.rename(
    columns={
        "paymentmethod": "payment_method",
        "payment": "payment_method"
    }
)


# =========================================================
# CHECK REQUIRED COLUMNS
# =========================================================

required_columns = [
    "date",
    "category",
    "amount",
    "payment_method"
]

missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]


if missing_columns:

    st.error(
        "Missing required columns: "
        + ", ".join(missing_columns)
    )

    st.info(
        "Required columns are: "
        "Date, Category, Description, "
        "Amount, Payment_Method"
    )

    st.stop()


# =========================================================
# DATA CLEANING
# =========================================================

data["date"] = pd.to_datetime(
    data["date"],
    errors="coerce"
)

data["amount"] = pd.to_numeric(
    data["amount"],
    errors="coerce"
)

data["category"] = (
    data["category"]
    .astype(str)
    .str.strip()
)

data["payment_method"] = (
    data["payment_method"]
    .astype(str)
    .str.strip()
)


# Remove invalid records

data = data.dropna(
    subset=[
        "date",
        "amount"
    ]
)


if data.empty:

    st.error(
        "No valid expense records were found."
    )

    st.stop()


# =========================================================
# SIDEBAR FILTER
# =========================================================

st.sidebar.header("🎛️ Filters")

categories = sorted(
    data["category"].unique()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + categories
)


if selected_category == "All":

    view = data.copy()

else:

    view = data[
        data["category"] == selected_category
    ].copy()


# =========================================================
# SUMMARY METRICS
# =========================================================

st.subheader("📊 Expense Summary")

total_spending = view["amount"].sum()

transaction_count = len(view)

average_expense = view["amount"].mean()


col1, col2, col3 = st.columns(3)


col1.metric(
    "💰 Total Spending",
    f"₹{total_spending:,.2f}"
)


col2.metric(
    "🧾 Transactions",
    transaction_count
)


col3.metric(
    "📊 Average Expense",
    f"₹{average_expense:,.2f}"
)


# =========================================================
# EXPENSE RECORDS
# =========================================================

st.subheader("📋 Expense Records")

st.dataframe(
    view,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# CATEGORY ANALYSIS
# =========================================================

st.subheader("📊 Spending by Category")

category_data = (
    view
    .groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_data)


# =========================================================
# MONTHLY ANALYSIS
# =========================================================

st.subheader("📈 Monthly Spending")

monthly_view = view.copy()

monthly_view["month"] = (
    monthly_view["date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_data = (
    monthly_view
    .groupby("month")["amount"]
    .sum()
    .sort_index()
)

st.line_chart(monthly_data)


# =========================================================
# PAYMENT METHOD ANALYSIS
# =========================================================

st.subheader("💳 Spending by Payment Method")

payment_data = (
    view
    .groupby("payment_method")["amount"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(payment_data)


# =========================================================
# BUDGET ANALYSIS
# =========================================================

st.subheader("💰 Budget Analysis")


budgets = {

    "Food": 10000,

    "Travel": 5000,

    "Education": 8000,

    "Shopping": 7000,

    "Entertainment": 4000,

    "Bills": 12000,

    "Health": 5000

}


budget_rows = []


for category, budget in budgets.items():

    spent = category_data.get(
        category,
        0
    )

    remaining = budget - spent

    percentage_used = (
        (spent / budget) * 100
        if budget > 0
        else 0
    )

    if spent > budget:

        status = "🔴 Over Budget"

    else:

        status = "🟢 Within Budget"


    budget_rows.append({

        "Category": category,

        "Budget": budget,

        "Spent": spent,

        "Remaining": remaining,

        "Used %": round(
            percentage_used,
            2
        ),

        "Status": status

    })


budget_table = pd.DataFrame(
    budget_rows
)


st.dataframe(
    budget_table,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# BUDGET ALERT
# =========================================================

over_budget = budget_table[
    budget_table["Spent"]
    >
    budget_table["Budget"]
]


if not over_budget.empty:

    st.warning(
        "⚠️ One or more categories "
        "are over budget."
    )

    for _, row in over_budget.iterrows():

        excess = (
            row["Spent"]
            -
            row["Budget"]
        )

        st.error(
            f"{row['Category']} is "
            f"₹{excess:,.2f} over budget."
        )

else:

    st.success(
        "✅ All categories are within budget."
    )


# =========================================================
# MACHINE LEARNING
# =========================================================

st.divider()

st.subheader(
    "🤖 Machine Learning - "
    "Future Expense Prediction"
)


# Create monthly dataset

ml_data = view.copy()

ml_data["month_period"] = (
    ml_data["date"]
    .dt.to_period("M")
)


monthly_ml = (
    ml_data
    .groupby("month_period")["amount"]
    .sum()
    .reset_index()
)


# =========================================================
# CHECK DATA FOR ML
# =========================================================

if len(monthly_ml) < 3:

    st.warning(
        "⚠️ At least 3 months of expense "
        "data are required for ML prediction."
    )

else:

    # Create numerical month feature

    monthly_ml["month_number"] = range(
        1,
        len(monthly_ml) + 1
    )


    # Input and target

    X = monthly_ml[
        ["month_number"]
    ]

    y = monthly_ml[
        "amount"
    ]


    # =====================================================
    # TRAIN MODEL
    # =====================================================

    model = LinearRegression()

    model.fit(
        X,
        y
    )


    # =====================================================
    # PREDICT EXISTING MONTHS
    # =====================================================

    monthly_ml["predicted_amount"] = (
        model.predict(X)
    )


    # =====================================================
    # NEXT MONTH PREDICTION
    # =====================================================

    next_month = (
        len(monthly_ml) + 1
    )


    predicted_next_month = model.predict(
        [[next_month]]
    )[0]


    # =====================================================
    # DISPLAY PREDICTION
    # =====================================================

    st.metric(
        "🔮 Predicted Next Month Expense",
        f"₹{predicted_next_month:,.2f}"
    )


    st.info(
        "The prediction is based on the "
        "historical monthly spending pattern "
        "in the selected data."
    )


    # =====================================================
    # ACTUAL VS PREDICTED TABLE
    # =====================================================

    st.write(
        "### 📋 Actual vs Predicted Expenses"
    )


    prediction_table = monthly_ml[
        [
            "month_period",
            "amount",
            "predicted_amount"
        ]
    ].copy()


    prediction_table.columns = [
        "Month",
        "Actual Expense",
        "Predicted Expense"
    ]


    prediction_table[
        "Actual Expense"
    ] = prediction_table[
        "Actual Expense"
    ].round(2)


    prediction_table[
        "Predicted Expense"
    ] = prediction_table[
        "Predicted Expense"
    ].round(2)


    st.dataframe(
        prediction_table,
        use_container_width=True,
        hide_index=True
    )


    # =====================================================
    # ACTUAL VS PREDICTED CHART
    # =====================================================

    st.write(
        "### 📈 Actual vs Predicted"
    )


    prediction_chart = (
        prediction_table
        .set_index("Month")
    )


    st.line_chart(
        prediction_chart
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Smart Expense Analyzer | "
    "Python + Pandas + SQLite + "
    "Scikit-learn + Streamlit"
)