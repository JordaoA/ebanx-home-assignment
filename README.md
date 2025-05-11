# Simple Banking API

This project implements a minimal banking service API using Flask and TinyDB. It supports account creation, deposits, withdrawals, balance queries, and transfers.

## Endpoints

### POST /reset

Resets all account data.

Request:
None

Response:
200 OK

---

### GET /balance?account\_id={id}

Retrieves the balance for the given account ID.

Example:
GET /balance?account\_id=100

Response:

* 200 OK with numeric body if account exists
* 404 with body 0 if not found

---

### POST /event

Processes deposit, withdraw, or transfer operations.

Request:
JSON object with one of the following formats:

Deposit:

```json
{
  "type": "deposit",
  "destination": "100",
  "amount": 10
}
```

Withdraw:

```json
{
  "type": "withdraw",
  "origin": "100",
  "amount": 5
}
```

Transfer:

```json
{
  "type": "transfer",
  "origin": "100",
  "amount": 15,
  "destination": "300"
}
```

Response:

* 201 Created with updated account(s) info
* 404 if account does not exist (for withdraw/transfer)
* 400 Bad Request if the payload is malformed

---

## How to Run

Ensure you have Python 3 and make installed.

1. Install dependencies and create virtualenv:

```bash
make venv
```

2. Start the application:

```bash
make run
```

3. To clean the environment:

```bash
make clean
```

The application runs on [http://localhost:5000](http://localhost:5000) by default.
