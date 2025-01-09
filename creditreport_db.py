import sqlite3
import json

# Load JSON data
with open('smartcredit_3.json', 'r') as file:
    data = json.load(file)

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('credit_report3.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''CREATE TABLE IF NOT EXISTS credit_scores(
    id INTEGER PRIMARY KEY,
    status_id INTEGER,
    user_id INTEGER,
    user_type TEXT,
    credit_bureau_id INTEGER,
    credit_score TEXT,
    lender_rank TEXT,
    score_scale TEXT,
    type INTEGER,
    report_id INTEGER,
    created_at TEXT,
    updated_at TEXT,
    deleted_at TEXT,
    old_scores INTEGER,
    score_difference TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS credit_reporting_agencies (
    id INTEGER PRIMARY KEY,
    name TEXT,
    checkbox INTEGER,
    selected_address INTEGER,
    type INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS summary (
    credit_bureau_id INTEGER,
    total_accounts TEXT,
    open_accounts TEXT,
    closed_accounts TEXT,
    collection TEXT,
    delinquent TEXT,
    derogatory TEXT,
    balances TEXT,
    payments TEXT,
    public_records TEXT,
    inquiries TEXT,
    type INTEGER,
    agency_id INTEGER,
    FOREIGN KEY (agency_id) REFERENCES credit_reporting_agencies(id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS personal_information (
    credit_bureau_id INTEGER,
    name TEXT,
    dob TEXT,
    aka_name TEXT,
    former TEXT,
    current_addresses TEXT,
    previous_addresses TEXT,
    employers TEXT,
    type TEXT,
    agency_id INTEGER,
    FOREIGN KEY (agency_id) REFERENCES credit_reporting_agencies(id)
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS account_histories (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    credit_bureau_id INTEGER,
    furnisher_name TEXT,
    account_number TEXT,
    account_type TEXT,
    account_detail TEXT,
    bureau_code TEXT,
    account_status TEXT,
    monthly_payment TEXT,
    date_opened TEXT,
    balance TEXT,
    number_of_months TEXT,
    high_credit TEXT,
    credit_limit TEXT,
    past_due TEXT,
    payment_status TEXT,
    late_status TEXT,
    last_reported TEXT,
    comments TEXT,
    date_last_active TEXT,
    date_last_payment TEXT,
    type INTEGER,
    report_id INTEGER,
    created_at TEXT,
    updated_at TEXT,
    deleted_at TEXT
)''')

# Create the credit_contacts table
cursor.execute('''CREATE TABLE IF NOT EXISTS credit_contacts (
    id INTEGER PRIMARY KEY,
    creditor_name TEXT,
    address TEXT,
    type INTEGER,
    creditor_id INTEGER,
    FOREIGN KEY (creditor_id) REFERENCES account_histories(id)
)''')

# Insert data into credit_scores and credit_reporting_agencies
for score in data['report']['creditScores']:
    cursor.execute('''INSERT OR IGNORE INTO credit_scores (
        id, status_id, user_id, user_type, credit_bureau_id, credit_score, 
        lender_rank, score_scale, type, report_id, created_at, updated_at, 
        deleted_at, old_scores, score_difference
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        score['id'], score['status_id'], score['user_id'], score['user_type'],
        score['credit_bureau_id'], score['credit_score'], score['lender_rank'],
        score['score_scale'], score['type'], score['report_id'], score['created_at'],
        score['updated_at'], score['deleted_at'], score['old_scores'],
        score['score_difference']
    ))

    agency = score['credit_reporting_agency']
    cursor.execute('''INSERT OR IGNORE INTO credit_reporting_agencies (
        id, name, checkbox, selected_address, type
    ) VALUES (?, ?, ?, ?, ?)''', (
        agency['id'], agency['name'], agency['checkbox'],
        agency['selected_address'], agency['type']
    ))

# Insert data into summary
for summary in data['report']['summary']:
    agency = summary['credit_reporting_agency']
    cursor.execute('''INSERT INTO summary (
        credit_bureau_id, total_accounts, open_accounts, closed_accounts, 
        collection, delinquent, derogatory, balances, payments, public_records, 
        inquiries, type, agency_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        summary['credit_bureau_id'], summary['total_accounts'], summary['open_accounts'],
        summary['closed_accounts'], summary['collection'], summary['delinquent'],
        summary['derogatory'], summary['balances'], summary['payments'],
        summary['public_records'], summary['inquiries'], summary['type'], agency['id']
    ))

# Insert data into personal_information
for person in data['report']['personalInformation']:
    agency = person['credit_reporting_agency']
    cursor.execute('''INSERT INTO personal_information (
        credit_bureau_id, name, dob, aka_name, former, current_addresses, 
        previous_addresses, employers, type, agency_id
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        person['credit_bureau_id'], ', '.join(person['name']),
        ', '.join(person['dob']), ', '.join(person['aka_name']),
        person['former'], ', '.join(person['current_addresses']),
        ', '.join(person['previous_addresses']),
        json.dumps(person['employers']), person['type'], agency['id']
    ))

# Insert data into account_histories
for history in data['report']['accountHistories']:
    cursor.execute('''INSERT OR IGNORE INTO account_histories (
        id, user_id, credit_bureau_id, furnisher_name, account_number, 
        account_type, account_detail, bureau_code, account_status, 
        monthly_payment, date_opened, balance, number_of_months, 
        high_credit, credit_limit, past_due, payment_status, late_status, 
        last_reported, comments, date_last_active, date_last_payment, 
        type, report_id, created_at, updated_at, deleted_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        history['id'], history['user_id'], history['credit_bureau_id'],
        history['furnisher_name'], history['account_number'], history['account_type'],
        history['account_detail'], history['bureau_code'], history['account_status'],
        history['monthly_payment'], history['date_opened'], history['balance'],
        history['number_of_months'], history['high_credit'], history['credit_limit'],
        history['past_due'], history['payment_status'], history['late_status'],
        history['last_reported'], history['comments'], history['date_last_active'],
        history['date_last_payment'], history['type'], history['report_id'],
        history['created_at'], history['updated_at'], history['deleted_at']
    ))

    # Insert credit contacts for each account history
    for contact in history.get('credit_contact', []):
        cursor.execute('''INSERT OR IGNORE INTO credit_contacts (
            creditor_name, address, type, creditor_id
        ) VALUES (?, ?, ?, ?)''', (
            contact['creditor_name'], contact['address'], contact['type'], history['id']
        ))

# Commit and close connection
conn.commit()
conn.close()

print("All data has been successfully stored in SQLite!")