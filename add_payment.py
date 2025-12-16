from abstra.forms import MarkdownOutput, TextInput, TextOutput, run
from abstra.tasks import send_task

# Page 1: Personal Details
personal_details = [
    TextInput("👋 Hello there! What is your name?", key="name"),
]

# Page 2: Greeting Page (Reactive)
def greeting_page(state):
    name = state["name"]
    return [
        TextOutput(f"🎉 Welcome, {name}!"),
        MarkdownOutput(
            """
### 📌 Hackathon Registration Fee
- **Amount:** ₹299
- **Payment Method:** UPI / Bank Transfer

Proceed to the next page to complete payment 💳
"""
        ),
    ]

# Page 3: Payment Page
payment_page = [
    MarkdownOutput(
        """
## 💳 Payment Details

Please complete the payment using the details below:

**UPI ID:** `hackathon@upi`  
**Amount:** ₹299  

📸 After payment, enter the transaction details below.
"""
    ),
    TextInput("🧾 Transaction ID / UTR Number", key="transaction_id"),
    TextInput("📅 Payment Date (DD/MM/YYYY)", key="payment_date"),
]

# Page 4: Payment Confirmation (Reactive)
def confirmation_page(state):
    return [
        TextOutput(f"✅ Payment Successful, {state['name']}!"),
        MarkdownOutput(
            f"""
### 🧾 Payment Summary
- **Transaction ID:** {state['transaction_id']}
- **Payment Date:** {state['payment_date']}

🎉 Your hackathon registration is now complete!
We’ll contact you soon with further updates.
"""
        ),
    ]

# Run the multi-page form
state = run([
    personal_details,
    greeting_page,
    payment_page,
    confirmation_page
])

# Send all data to the workflow
send_task(
    "greeting",
    {
        "name": state["name"],
        "transaction_id": state["transaction_id"],
        "payment_date": state["payment_date"],
    }
)
