import csv

# Function to read a CSV file using the csv library
def read_csv_file(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

# Function to filter active accounts
def filter_active_accounts(accounts):
    return [account for account in accounts if (account['Is Dormant'] == '0.0' and
                                                account['Is Closed'] == '0' and
                                                account['Is Profile Suspended'] == '0' and
                                                account['Is Client Suspended'] == '0')]

# Load the data
clients_data = read_csv_file('clients_data_competition.csv')
orders_data = read_csv_file('orders_data_competition.csv')

# Filter clients data to find those related to "HSB"
filtered_clients = [client for client in clients_data if client['Company Name'].lower() == "hsb"]

# Filter the filtered clients for active accounts
active_accounts_hsb = filter_active_accounts(filtered_clients)


# Dictionary to store executed orders count for active and inactive accounts
executed_orders_count = {'active': {'total_orders': 0, 'executed_orders': 0},
                         'inactive': {'total_orders': 0, 'executed_orders': 0}}


# Count executed orders for each account
for order in orders_data:
    account_id = order['Account ID']
    if account_id in (account['Account ID'] for account in filtered_clients):
        executed_orders_count_key = 'active' if account_id in (account['Account ID'] for account in active_accounts_hsb) else 'inactive'
        if order['Execution Status'] == 'Executed':
            executed_orders_count[executed_orders_count_key]['executed_orders'] += 1
        executed_orders_count[executed_orders_count_key]['total_orders'] += 1

# Calculate and print percentage of executed orders for active and inactive accounts
total_active_orders = executed_orders_count['active']['total_orders']
total_executed_active_orders = executed_orders_count['active']['executed_orders']
percentage_executed_active = (total_executed_active_orders / total_active_orders) * 100 if total_active_orders > 0 else 0

total_inactive_orders = executed_orders_count['inactive']['total_orders']
total_executed_inactive_orders = executed_orders_count['inactive']['executed_orders']
percentage_executed_inactive = (total_executed_inactive_orders / total_inactive_orders) * 100 if total_inactive_orders > 0 else 0

print(f"Percentage of executed orders for active accounts: {percentage_executed_active:.2f}%")
print(f"Percentage of executed orders for inactive accounts: {percentage_executed_inactive:.2f}%")