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

# Output filtered active accounts with company name "HSB"
print("Active Accounts with Company Name HSB:")
for account in active_accounts_hsb:
    print(account)

# Find orders for each active account with company name "HSB"
for account in active_accounts_hsb:
    account_id = account['Account ID']
    # Print orders corresponding to the current account's Account ID
    print(f"Orders found for Account ID {account_id}:")
    for order in orders_data:
        if order['Account ID'] == account_id:  # Using order['Account ID'] to access the Account ID
            print(order)

