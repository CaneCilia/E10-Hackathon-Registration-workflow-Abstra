from abstra.tasks import get_trigger_task, send_task
from abstra.tables import insert

print("=== Processing Hackathon Registration ===")

# Get the registration task from the form
task = get_trigger_task()

print(f"Processing registration for: {task['name']}")
print(f"Email: {task['email']}")

# Store registration in database (assuming you have a 'registrations' table)
try:
    registration_result = insert(
        "registrations",
        {
            "name": task["name"],
            "email": task["email"],
            "phone": task["phone"],
            "organization": task["organization"],
            "role": task["role"],
            "team_name": task["team_name"],
            "tech_stack": task["tech_stack"],
            "portfolio": task["portfolio"],
            "status": "payment_pending"
        }
    )
    
    registration_id = registration_result["id"] if isinstance(registration_result, dict) else registration_result
    print(f"✅ Registration saved with ID: {registration_id}")
    
except Exception as e:
    print(f"⚠️ Could not save to database: {e}")
    print("Continuing with workflow...")
    registration_id = None

# Complete the current task
task.complete()
print("✅ Registration task completed")

# Send task to Payment Verification form
send_task("payment_pending", {
    "registration_id": str(registration_id) if registration_id else None,
    "name": task["name"],
    "email": task["email"],
    "phone": task["phone"],
    "organization": task["organization"],
    "team_name": task["team_name"]
})

print(f"✅ Payment pending task sent for {task['name']}")
print("=== Registration Processing Complete ===")
