# Service functions
from app import accounts, Account


def reset_accounts():
    accounts.truncate()


def get_account_balance(account_id: str):
    acc = accounts.get(Account.id == account_id)
    return acc['balance'] if acc else None


def process_deposit(data):
    dest = data.get('destination')
    amount = data.get('amount')
    acc = accounts.get(Account.id == dest)
    if acc:
        acc['balance'] += amount
        accounts.update({'balance': acc['balance']}, Account.id == dest)
    else:
        acc = {'id': dest, 'balance': amount}
        accounts.insert(acc)
    return acc


def process_withdraw(data):
    origin = data.get('origin')
    amount = data.get('amount')
    acc = accounts.get(Account.id == origin)
    if not acc or acc['balance'] < amount:
        return None
    acc['balance'] -= amount
    accounts.update({'balance': acc['balance']}, Account.id == origin)
    return acc


def process_transfer(data):
    origin = data.get('origin')
    dest = data.get('destination')
    amount = data.get('amount')

    acc_origin = accounts.get(Account.id == origin)
    if not acc_origin or acc_origin['balance'] < amount:
        return None
    acc_origin['balance'] -= amount
    accounts.update({'balance': acc_origin['balance']}, Account.id == origin)

    acc_dest = accounts.get(Account.id == dest)
    if acc_dest:
        acc_dest['balance'] += amount
        accounts.update({'balance': acc_dest['balance']}, Account.id == dest)
    else:
        acc_dest = {'id': dest, 'balance': amount}
        accounts.insert(acc_dest)

    return acc_origin, acc_dest