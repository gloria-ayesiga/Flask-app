# Budget Tracker Web App
Web app URL: https://flask-app-2wbi.onrender.com/

This is a simple Flask-based web application that allows users to input their **age**, **gender**, **monthly income**, and **expense breakdown** to calculate savings. The app validates inputs, provides warnings if expenses exceed income, and stores submissions in a **MongoDB Atlas** database.

It also includes a Jupyter notebook component for **data analysis and export**.

## Features

- Form-based user input
- Real-time validation and error handling
- Auto-calculated total expenses and monthly savings
- Stores user submissions in MongoDB
- CSV export for offline analysis
- Visualizations (e.g. top earners by age, gender-based spending)
- Ready for cloud deployment (tested on Render.com)

## Technologies Used

- **Python 3**
- **Flask** for the web framework
- **MongoDB Atlas** for data storage
- **Jinja2** for templating
- **Pandas & Matplotlib** (in Jupyter) for analysis
- **Render.com** for deployment


## Setup Instructions

### 1. Clone the Repository


git clone https://github.com/your-username/budget-tracker-app.git

### 2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Configure MongoDB

Update the MongoDB connection string inside `app.py`:

client = MongoClient("your_mongodb_uri")

You can get this from [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).

### 5. Run the App Locally

python app.py


Then visit: `http://localhost:5000`


## Deployment on Render

### Files needed for Render:
- `app.py`
- `requirements.txt`
- `render.yaml`
- `runtime.txt`

### Example `render.yaml`:

services:
  - type: web
    name: budget-tracker
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py


Push your code to GitHub and [connect to Render](https://render.com/docs/deploy-python).

## Data Analysis (Jupyter)

- Use `export_to_csv()` function in the notebook to extract submissions from MongoDB
- Analyze top earners, expense categories, and savings trends
- Export visuals as PNGs for presentations

## To-Do / Enhancements

- Add user authentication (login/signup)
- Support for multi-currency income/expenses
- Dashboard with interactive graphs (Plotly/Dash)
- PDF export of user summary


## Author
Gloria Eden Zion Ayesiga for the fulfiment of the BAN6420 course Final Project assignment
