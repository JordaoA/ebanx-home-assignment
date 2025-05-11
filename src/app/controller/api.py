from app import app
from flask import request, jsonify
from app.service import (reset_accounts, get_account_balance, process_deposit, process_withdraw, process_transfer)


@app.route('/reset', methods=['POST'])
def reset():
    """
    Reset state: clear all account data.
    """
    reset_accounts()
    return '', 200


@app.route('/balance', methods=['GET'])
def get_balance():
    """
    Get balance for a given account_id query parameter.
    """
    account_id = request.args.get('account_id')
    if not account_id:
        return 'Missing account_id parameter', 400
    balance = get_account_balance(account_id)
    if balance is not None:
        return str(balance), 200
    return str(0), 404


@app.route('/event', methods=['POST'])
def handle_event():
    """
    Handle deposit, withdraw, and transfer events.
    - deposit: create or update destination account
    - withdraw: deduct from origin if exists and sufficient funds
    - transfer: move funds from origin to destination
    """
    data = request.get_json()
    if not data or 'type' not in data:
        return '', 400

    t = data['type']

    if t == 'deposit':
        if 'destination' not in data or 'amount' not in data:
            return '', 400
        acc = process_deposit(data)
        return jsonify({"destination": acc}), 201

    if t == 'withdraw':
        if 'origin' not in data or 'amount' not in data:
            return '', 400
        acc = process_withdraw(data)
        if not acc:
            return str(0), 404
        return jsonify({"origin": acc}), 201

    if t == 'transfer':
        if 'origin' not in data or 'destination' not in data or 'amount' not in data:
            return '', 400
        result = process_transfer(data)
        if not result:
            return str(0), 404
        acc_origin, acc_dest = result
        return jsonify({"origin": acc_origin, "destination": acc_dest}), 201

    return '', 400
