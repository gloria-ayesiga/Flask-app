import os
from flask import Flask, request, render_template_string
from pymongo import MongoClient
import certifi

app = Flask(__name__)

# MongoDB setup
try:
    client = MongoClient(
        "mongodb+srv://gloayesiga:ODyhsWYJLTlTlCG1@finalproject.ivwhchh.mongodb.net/?retryWrites=true&w=majority",
        tlsCAFile=certifi.where()
    )
    db = client["user_data_db"]
    collection = db["user_submissions"]
    print("✅ MongoDB connection successful")
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    warning = None

    if request.method == 'POST':
        age = request.form.get('age')
        gender = request.form.get('gender')
        monthly_income = request.form.get('monthly_income')

        try:
            if not age or int(age) < 18:
                error = "You must be at least 18 years old."
            else:
                income_val = float(monthly_income)
                if income_val <= 0:
                    error = "Total monthly income must be greater than zero."
        except (ValueError, TypeError):
            error = "Invalid age or income input."

        if not error:
            categories = ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']
            monthly_expenses = {}
            total_monthly_expenses = 0

            for category in categories:
                if request.form.get(category):
                    amount = request.form.get(f'{category}_amount')
                    try:
                        amount_val = float(amount)
                        if amount_val <= 0:
                            error = f"You checked '{category.replace('_', ' ').title()}' but didn't enter a valid amount."
                            break
                        monthly_expenses[category] = amount_val
                        total_monthly_expenses += amount_val
                    except (ValueError, TypeError):
                        error = f"Invalid amount entered for {category.replace('_', ' ').title()}."
                        break
                else:
                    monthly_expenses[category] = 0.0

        if not error:
            monthly_savings = income_val - total_monthly_expenses

            if total_monthly_expenses > income_val:
                warning = "Warning: Your expenses exceed your income."

            # Save to MongoDB
            doc = {
                'age': int(age),
                'gender': gender,
                'monthly_income': income_val,
                'total_monthly_expenses': total_monthly_expenses,
                'monthly_savings': monthly_savings,
                'monthly_expenses': monthly_expenses
            }
            collection.insert_one(doc)

            return render_template_string('''
                <h2>Submission Successful</h2>
                {% if warning %}
                    <p style="color:orange;"><strong>{{ warning }}</strong></p>
                {% endif %}
                <p><strong>Age:</strong> {{ age }}</p>
                <p><strong>Gender:</strong> {{ gender }}</p>
                <p><strong>Total Monthly Income:</strong> ${{ monthly_income }}</p>
                <p><strong>Total Monthly Expenses:</strong> ${{ total_monthly_expenses }}</p>
                <p><strong>Monthly Savings:</strong> ${{ monthly_savings }}</p>
                <ul>
                    {% for k, v in monthly_expenses.items() %}
                        {% if v > 0 %}
                            <li>{{ k.replace('_',' ').title() }}: ${{ v }}</li>
                        {% endif %}
                    {% endfor %}
                </ul>
                <a href="/">Back to form</a>
            ''', age=age, gender=gender, monthly_income=income_val, total_monthly_expenses=total_monthly_expenses, monthly_savings=monthly_savings, monthly_expenses=monthly_expenses, warning=warning)

    return render_template_string('''
        <h2>User Financial Form</h2>
        {% if error %}
            <p style="color:red;"><strong>{{ error }}</strong></p>
        {% endif %}
        <form method="POST" id="userForm">
            Age: <input type="number" name="age" required><br><br>
            Gender:
            <input type="radio" name="gender" value="Male" required> Male
            <input type="radio" name="gender" value="Female" required> Female
            <br><br>
            Total Monthly Income: <input type="number" name="monthly_income" placeholder="$" step="0.01" required><br><br>

            <h3>Total Monthly Expenses:</h3>
            <input type="checkbox" name="utilities"> Utilities
            Amount: <input type="number" name="utilities_amount" placeholder="$" step="0.01"><br><br>

            <input type="checkbox" name="entertainment"> Entertainment
            Amount: <input type="number" name="entertainment_amount" placeholder="$" step="0.01"><br><br>

            <input type="checkbox" name="school_fees"> School Fees
            Amount: <input type="number" name="school_fees_amount" placeholder="$" step="0.01"><br><br>

            <input type="checkbox" name="shopping"> Shopping
            Amount: <input type="number" name="shopping_amount" placeholder="$" step="0.01"><br><br>

            <input type="checkbox" name="healthcare"> Healthcare
            Amount: <input type="number" name="healthcare_amount" placeholder="$" step="0.01"><br><br>

            <input type="submit" value="Submit">
        </form>

        <script>
        document.addEventListener("DOMContentLoaded", function () {
            const ageInput = document.querySelector('input[name="age"]');
            ageInput.addEventListener("input", function () {
                if (ageInput.value < 18) {
                    ageInput.setCustomValidity("You must be at least 18 years old.");
                } else {
                    ageInput.setCustomValidity("");
                }
            });

            const categories = ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare'];
            categories.forEach(category => {
                const checkbox = document.querySelector(`input[name="${category}"]`);
                const amountInput = document.querySelector(`input[name="${category}_amount"]`);

                checkbox.addEventListener('change', function () {
                    amountInput.required = checkbox.checked;
                });

                amountInput.addEventListener('input', function () {
                    if (checkbox.checked && (!amountInput.value || parseFloat(amountInput.value) <= 0)) {
                        amountInput.setCustomValidity("Please enter a valid amount.");
                    } else {
                        amountInput.setCustomValidity("");
                    }
                });
            });
        });
        </script>
    ''', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
    #print("✅ App running at http://127.0.0.1:5000")
     
    # app.run(debug=True)

