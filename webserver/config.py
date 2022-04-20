import os 

def get_postgres_uri():
    host = os.environ.get('DB_HOST', 'postgres') #host = "localhost"#"postgres"
    port = 54321 if host == 'localhost' else 5432
    password = os.environ.get('DB_PASSWORD', 'cardamom9867')
    user, db_name = 'cardamom', 'cardamom'
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005 if host == "localhost" else 80
    return f"http://{host}:{port}"


