from app import app, spec, accounts, Account
from flask import request, jsonify
from flask_pydantic_spec import (Response, Request)


@app.post('/reset')
@spec.validate(tags=["EBANX-API"])
def reset():
    """
    Reset state: clear all account data.
    """
    accounts.truncate()
    return '', 200


@app.get('/balance/<int:account_id>')
@spec.validate(tags=["EBANX-API"])
def get_balance(account_id):
    """
    Get balance for a given account_id query parameter.
    """
    if account_id:
        acc = accounts.get(Account.id == account_id)
        if acc:
            return str(acc['balance']), 200
    
    return str(0), 404


@app.post('/event')
@spec.validate(tags=["EBANX-API"])
def handle_event():
    """
    Handle deposit, withdraw, and transfer events.
    - deposit: create or update destination account
    - withdraw: deduct from origin if exists and sufficient funds
    - transfer: move funds from origin to destination
    """
    data = request.get_json()
    t = data.get('type')

    if t == 'deposit':
        dest = data['destination']
        amount = data['amount']
        acc = accounts.get(Account.id == dest)
        if acc:
            acc['balance'] += amount
            accounts.update({'balance': acc['balance']}, Account.id == dest)
        else:
            acc = {'id': dest, 'balance': amount}
            accounts.insert(acc)
        return jsonify({"destination": acc}), 201

    if t == 'withdraw':
        origin = data['origin']
        amount = data['amount']
        acc = accounts.get(Account.id == origin)
        if not acc or acc['balance'] < amount:
            return str(0), 404
        acc['balance'] -= amount
        accounts.update({'balance': acc['balance']}, Account.id == origin)
        return jsonify({"origin": acc}), 201

    if t == 'transfer':
        origin = data['origin']
        dest = data['destination']
        amount = data['amount']

        acc_origin = accounts.get(Account.id == origin)
        if not acc_origin or acc_origin['balance'] < amount:
            return str(0), 404

        acc_origin['balance'] -= amount
        accounts.update({'balance': acc_origin['balance']}, Account.id == origin)

        acc_dest = accounts.get(Account.id == dest)
        if acc_dest:
            acc_dest['balance'] += amount
            accounts.update({'balance': acc_dest['balance']}, Account.id == dest)
        else:
            acc_dest = {'id': dest, 'balance': amount}
            accounts.insert(acc_dest)

        return jsonify({"origin": acc_origin, "destination": acc_dest}), 201

    return '', 400