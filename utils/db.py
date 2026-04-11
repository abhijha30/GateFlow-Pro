from supabase import create_client

SUPABASE_URL = "https://kamgkwfkzvofkwexhrvn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImthbWdrd2ZrenZvZmt3ZXhocnZuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU4NzA3MjAsImV4cCI6MjA5MTQ0NjcyMH0.8I3OgpamJBjw65ifO9djPKwFv0SwgO92UYvrXTYq5U0"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# EVENTS
def create_event(data):
    return supabase.table("events").insert(data).execute()

def get_events():
    return supabase.table("events").select("*").execute()

def delete_event(event_id):
    return supabase.table("events").delete().eq("id", event_id).execute()

# USERS
def create_user(data):
    return supabase.table("users").insert(data).execute()

def get_users():
    return supabase.table("users").select("*").execute()

# APPLICATIONS
def apply_event(data):
    return supabase.table("applications").insert(data).execute()

def get_applications():
    return supabase.table("applications").select("*").execute()

def update_status(id, status, qr=None):
    return supabase.table("applications").update({
        "status": status,
        "qr_code": qr
    }).eq("id", id).execute()
