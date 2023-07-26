import sqlite3


conn = sqlite3.connect('terminals.db')
c = conn.cursor()
c.execute('DROP TABLE IF EXISTS terminals;')
c.execute('''
    CREATE TABLE terminals (
        userTerminalId TEXT,
        kitSerialNumber TEXT,
        dishSerialNumber TEXT,
        serviceLineNumber TEXT,
        active INTEGER,
        accountNumber TEXT,
        accountName TEXT
    )
''')

c.execute('DROP TABLE IF EXISTS service_accounts;')
c.execute('''
    CREATE TABLE SERVICE_ACCOUNTS
    (SERVICE_ACCOUNT_NUMBER TEXT PRIMARY KEY NOT NULL,
    SECRET                  TEXT NOT NULL); 
''')



# insert each service account into the database
c.execute("INSERT INTO SERVICE_ACCOUNTS VALUES (?, ?)", ('aaa-aaaa-aaaa', 'a_secret'))
c.execute("INSERT INTO SERVICE_ACCOUNTS VALUES (?, ?)", ('bbb-bbbb-bbbb', 'b_secret'))
c.execute("INSERT INTO SERVICE_ACCOUNTS VALUES (?, ?)", ('ccc-cccc-cccc', 'c_secret'))
conn.commit()



# the array for terminals
terminals = [
    ('010000000-00000000-1', 'KIT1', 'HCPCP1', 'AST-1', 1, 'ACC-1', 'DUDECENT'),
    ('010000000-00000000-2', 'KIT2', 'HCPCP2', 'AST-2', 0, 'ACC-2', 'BROCENT'),
    ('010000000-00000000-3', 'KIT3', 'HCPCP3', 'AST-3', 1, 'ACC-3', 'SISCENT')
]

# insert each terminal into the database
for terminal in terminals:
    c.execute('''
        INSERT INTO terminals (userTerminalId, kitSerialNumber, dishSerialNumber, serviceLineNumber, active, accountNumber, accountName)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', terminal)

conn.commit()
conn.close()
