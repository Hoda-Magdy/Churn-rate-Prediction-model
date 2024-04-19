import csv
from datetime import datetime

def read_csv_file(filename):
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def write_to_csv_file(filename, data, fieldnames):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def calculate_age(birthdate_str, reference_date_str=None):
    birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d')
    if reference_date_str:
        reference_date = datetime.strptime(reference_date_str, '%Y-%m-%d')
    else:
        reference_date = datetime.today()
    return reference_date.year - birthdate.year - ((reference_date.month, reference_date.day) < (birthdate.month, birthdate.day))

clients_data = read_csv_file('clients_data_competition.csv')
orders_data = read_csv_file('orders_data_competition.csv')

hsb_clients = [client for client in clients_data if 'hsb' in client['Company Name'].lower()]
clients_latest_order = {client['Account ID']: {'Latest Order ID': None, 'Latest Order Date': None} for client in hsb_clients}

for order in orders_data:
    account_id = order['Account ID']
    if account_id in clients_latest_order:
        order_date = datetime.strptime(order['Order Time'], '%Y-%m-%d %H:%M:%S.%f')
        if clients_latest_order[account_id]['Latest Order Date'] is None or order_date > clients_latest_order[account_id]['Latest Order Date']:
            clients_latest_order[account_id]['Latest Order ID'] = order['Order ID']
            clients_latest_order[account_id]['Latest Order Date'] = order_date

# Check that the keys are added only once
base_client_fieldnames = clients_data[0].keys() if clients_data else []
additional_fields = ['Latest Order ID', 'Age', 'Age at Last Order']
extended_client_fieldnames = list(base_client_fieldnames) + additional_fields

for client in hsb_clients:
    account_id = client['Account ID']
    latest_order = clients_latest_order[account_id]
    client['Latest Order ID'] = latest_order['Latest Order ID']
    client['Age'] = calculate_age(client['BirthDate'])
    client['Age at Last Order'] = calculate_age(client['BirthDate'], latest_order['Latest Order Date'].strftime('%Y-%m-%d')) if latest_order['Latest Order ID'] else None

write_to_csv_file('enhanced_hsb_clients.csv', hsb_clients, extended_client_fieldnames)

hsb_orders = [order for order in orders_data if order['Account ID'] in clients_latest_order]
order_fieldnames = orders_data[0].keys() if orders_data else []
write_to_csv_file('hsb_client_orders.csv', hsb_orders, order_fieldnames)
