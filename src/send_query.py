import requests
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    "dbname": "Adventureworks",
    "user": "postgres",
    "password": "postgres",
    "host": "172.18.206.109",
    "port": 5435,
}

# Webhook URL for Teams
webhook_url = os.getenv("WEBHOOK_URL")

def fetch_query_results():
    """
    Fetches query results from the PostgreSQL database.
    """
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Execute the query
        query = "SELECT * FROM humanresources.department"
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        conn.close()
        return results
    
    except Exception as e:
        print(f"Error fetching query results: {e}")
        return None

def send_to_teams(message):
    """
    Sends a message to the Teams channel via a webhook.
    """
    if not webhook_url:
        print("Error: WEBHOOK_URL is not defined in the environment variables.")
        return
    
    response = requests.post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(message)
    )
    
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)

def main():
    # Fetch query results
    results = fetch_query_results()
    
    if results is None or len(results) == 0:
        print("No data found or failed to fetch data.")
        return
    
    # Format results for Teams message
    formatted_results = "\n".join(
        [f"- ID: {row['departmentid']}, Name: {row['name']}, Group: {row['groupname']}" for row in results]
    )
    
    message = {
        "title": "Query Results",
        "text": f"Here are the results of your query:\n\n{formatted_results}"
    }
    
    # Send the message to Teams
    send_to_teams(message)

if __name__ == "__main__":
    main()
