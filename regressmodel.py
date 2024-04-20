import numpy as np
from sklearn.linear_model import LinearRegression

# Provided x and y values
years = [1998, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
churn_rates = [0.171717, 0.213004, 0.164345, 0.17452, 0.158065, 0.168803, 0.161184, 0.113949, 0.135638, 0.118421, 0.190476, 0.147287, 0.176991, 0.207207, 0.211462, 0.21087, 0.178303, 0.245902, 0.201139, 0.011106]

# Convert lists to numpy arrays
X = np.array(years).reshape(-1, 1)  # Reshape to a single feature matrix
y = np.array(churn_rates)

# Initialize and fit the linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict churn rates for future years (e.g., 2025, 2026, etc.)
future_years = np.array([2024, 2025]).reshape(-1, 1)
future_churn_rates = model.predict(future_years)

print("Predicted churn rates for future years:")
for year, churn_rate in zip(future_years.flatten(), future_churn_rates):
    print(f"Year {year}: Churn rate {churn_rate:.6f}")
