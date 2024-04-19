import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import HistGradientBoostingClassifier

# Load the data
customers_df = pd.read_csv('enhanced_hsb_clients.csv')
orders_df = pd.read_csv('orders_data_competition.csv')  # Adjust the filename to your orders data CSV

# Define churn - this is just a placeholder, you'll need to define churn based on your data
# For example, customers with no executed orders might be considered churned
customers_df['Churn'] = customers_df['Account ID'].apply(
    lambda x: 0 if any(orders_df[orders_df['Account ID'] == x]['Execution Status'] == 'Executed') else 1
)

# Merge the customer data with the orders data
# This will depend on how you want to incorporate orders data into the features. 
# This is an example where we might count the number of executed orders for each customer.
executed_orders_count = orders_df[orders_df['Execution Status'] == 'Executed'].groupby('Account ID').size()
customers_df['Executed Orders Count'] = customers_df['Account ID'].map(executed_orders_count).fillna(0)

# Preprocess the data: encode categorical variables, scale numerical variables, fill in missing values
categorical_cols = customers_df.select_dtypes(include=['object', 'category']).columns
numerical_cols = customers_df.select_dtypes(include=['int64', 'float64']).columns.drop('Churn')

preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='median'), numerical_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough',  # Include columns not specified in transformers
    sparse_threshold=0  # Ensure the output is a dense array
)

# Prepare features and target
X = customers_df.drop('Churn', axis=1)
y = customers_df['Churn']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model pipeline
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', HistGradientBoostingClassifier(random_state=42))
])

# Train the model
pipeline.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))


