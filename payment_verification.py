from abstra.forms import (
    MarkdownOutput, FileInput, CheckboxInput, TextOutput, run, get_user
)
from abstra.tasks import get_tasks, send_task
from abstra.tables import update
from datetime import datetime

print("=== Payment Verification Form ===")

# Get authenticated user
user = get_user()
if not user or not user.email:
    run([[
        MarkdownOutput("⚠️ You need to be authenticated to access this page.")
    ]])
    exit()

user_email = user.email.lower()
print(f"User authenticated: {user_email}")

# Get pending payment tasks for this user
pending_tasks = [
    t for t in get_tasks() 
    if t.get("email", "").lower() == user_email
]

if not pending_tasks:
    run([[
        MarkdownOutput(f"ℹ️ No pending payments found for **{user_email}**.")
    ]])
    exit()

print(f"Found {len(pending_tasks)} pending payment(s)")

# Process the first pending payment
task = pending_tasks[0]

name = task.get("name", "Participant")
organization = task.get("organization", "N/A")
team_name = task.get("team_name", "N/A")
registration_id = task.get("registration_id")

print(f"Processing payment for: {name}")

# Payment verification page
payment_page = [
    MarkdownOutput(f"""
# 💳 Hackathon Payment Verification

**Participant:** {name}  
**Organization:** {organization}  
**Team:** {team_name}  
**Email:** {user_email}

---

💵 **Registration Fee:** $50.00

Please upload your payment proof and confirm your payment.
    """),
    FileInput(
        key="payment_proof",
        label="Upload Payment Proof (Receipt/Screenshot)",
        required=False,
        hint="Accepted formats: PDF, PNG, JPG"
    ),
    CheckboxInput(
        key="payment_confirmed",
        label="I confirm that I have completed the payment",
        required=True
    )
]

state = run([payment_page])

if not state.get("payment_confirmed"):
    run([[
        MarkdownOutput("⚠️ Payment not confirmed. Please try again.")
    ]])
    exit()

print(f"✅ Payment confirmed by {name}")

# Update registration status in database if registration_id exists
if registration_id:
    try:
        update(
            "registrations",
            where={"id": registration_id},
            set={"status": "payment_confirmed"}
        )
        print(f"✅ Registration {registration_id} updated to 'payment_confirmed'")
    except Exception as e:
        print(f"⚠️ Could not update database: {e}")

# Show confirmation
run([[
    MarkdownOutput(f"""
# ✅ Payment Confirmed!

Thank you, **{name}**! Your payment has been verified.

You will receive a confirmation email shortly with:
- Event details
- Schedule
- Venue information
- Team guidelines

See you at the hackathon! 🚀
    """)
]])

# Complete the current task
task.complete()
print("✅ Payment task completed")

# Send confirmation task to next stage
send_task("payment_confirmed", {
    "registration_id": registration_id,
    "name": name,
    "email": user_email,
    "organization": organization,
    "team_name": team_name,
    "payment_confirmed_at": datetime.now().isoformat()
})

print(f"✅ Confirmation task sent for {name}")
print("=== Payment Verification Complete ===")
