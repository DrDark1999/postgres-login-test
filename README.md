# PostgreSQL Default Login Test

This is a Python script designed to brute force test default PostgreSQL logins using a list of common usernames, passwords, and database names. It attempts to connect to a PostgreSQL server with and without specifying a database. The script displays success and failure results with color coding and provides a summary of successful login attempts.

## Features

- Brute force login testing with common PostgreSQL usernames and passwords.
- Tests connections with default databases such as `postgres`, `template1`, etc.
- Option to test connections without specifying a database.
- Color-coded results for successful and failed attempts.
- Displays a summary of successful logins and provides an example `psql` command for manual testing.

## Requirements

- Python 3.x
- `psycopg2` for connecting to PostgreSQL
- `colorama` for color coding the output

### Installing PostgreSQL Client

#### On Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install postgresql-client
```

#### On CentOS/RHEL:

```bash
sudo yum install postgresql
```

#### On macOS:

```bash
brew install postgresql
```

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DrDark1999/postgres-login-test.git
    cd postgres-login-test
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script using Python and provide the target PostgreSQL server's IP address and port (optional).

```bash
python postgres_login_test.py --host <target_ip> --port <target_port>
