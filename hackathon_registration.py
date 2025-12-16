from abstra.forms import MarkdownOutput, TextInput, TextOutput, run
from abstra.tasks import send_task

# Page 1: Personal & Hackathon Details
registration_details = [
    TextInput("👋 Hello! What is your full name?", key="name"),
    TextInput("📧 Email Address", key="email"),
    TextInput("📱 Phone Number", key="phone"),
    TextInput("🏫 College / Organization Name", key="organization"),
    TextInput("🎓 Current Year / Role (e.g., 3rd Year, Developer)", key="role"),
    TextInput("💡 Hackathon Team Name (if any)", key="team_name"),
    TextInput("🛠️ Primary Tech Stack (e.g., Python, Flutter, React)", key="tech_stack"),
    TextInput("🔗 GitHub / Portfolio Link", key="portfolio"),
]

# Page 2: Greeting & Confirmation (Reactive Page)
def confirmation_page(state):
    return [
        TextOutput(f"🎉 Thank you for registering, {state['name']}!"),
        MarkdownOutput(
            f"""
### 📋 Registration Summary
- **Email:** {state['email']}
- **Phone:** {state['phone']}
- **Organization:** {state['organization']}
- **Role:** {state['role']}
- **Team Name:** {state['team_name']}
- **Tech Stack:** {state['tech_stack']}
- **Portfolio:** {state['portfolio']}

🚀 We’ll reach out to you soon with further updates!
"""
        ),
    ]

# Run the form(validate option)
state = run([registration_details, confirmation_page])

# Send task to Process Registration tasklet
send_task("new_registration", {
    "name": state["name"],
    "email": state["email"],
    "phone": state["phone"],
    "organization": state["organization"],
    "role": state["role"],
    "team_name": state["team_name"],
    "tech_stack": state["tech_stack"],
    "portfolio": state["portfolio"],
})

print(f"✅ Registration task sent for {state['name']}")
