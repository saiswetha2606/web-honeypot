# Simple Web Honeypot

This is a basic web honeypot designed to trap and log malicious activity.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/saiswetha2606/web-honeypot.git
    cd web-honeypot
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the honeypot:**
    ```bash
    python your_honeypot_script.py
    ```

## Example Interactions and Output

When a potential attacker tries to access a non-existent administrative page (`/admin`), the honeypot might log the following: