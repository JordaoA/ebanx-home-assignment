from app import app
from flask import request, jsonify
from app.service import (
                         create_event, 
                         reset_accounts, 
                         get_account_balance, 
                         )

@app.route('/reset', methods=['POST'])
def reset():
    """
    Reset state: clear all account data.
    """
    reset_accounts()
    return 'OK', 200


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
        return 'Invalid Data', 400

    event = create_event(data)
    
    result = event.perform()

    if result:
        return result, 201
    else:
        return str(0), 404