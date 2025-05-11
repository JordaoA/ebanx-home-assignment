from app import accounts, Account

# Event Objects
class Event:
    def __init__(self,data):
        self.data = data

    
    def perform(self):
        return "performed!"


class Deposit(Event):
    def __init__(self, data):
        super().__init__(data)


    def perform(self):
        dest = self.data['destination']
        amount = self.data['amount']
        acc = accounts.get(Account.id == dest)
        
        if acc:
            acc['balance'] += amount
            accounts.update({'balance': acc['balance']}, Account.id == dest)
        
        else:
            acc = {'id': dest, 'balance': amount}
            accounts.insert(acc)
        
        return {"destination": acc}
    

class Withdraw(Event):
    def __init__(self, data):
        super().__init__(data)

    
    def perform(self):
        origin = self.data['origin']
        amount = self.data['amount']
        acc = accounts.get(Account.id == origin)
    
        if not acc or acc['balance'] < amount:
            return None
        
        acc['balance'] -= amount
        accounts.update({'balance': acc['balance']}, Account.id == origin)
    
        return {"origin": acc}


class Transfer(Event):
    def __init__(self, data):
        super().__init__(data)

    
    def perform(self):
        origin = self.data['origin']
        dest = self.data['destination']
        amount = self.data['amount']
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
        
        return {"origin": acc_origin, "destination": acc_dest}


# Service functions
def create_event(data):
    t = data['type']

    if t == 'deposit':
        return Deposit(data)

    if t == 'withdraw':
        return Withdraw(data)

    if t == 'transfer':
        return Transfer(data)

    return None


def reset_accounts():
    accounts.truncate()


def get_account_balance(account_id: str):
    acc = accounts.get(Account.id == account_id)
    return acc['balance'] if acc else None
