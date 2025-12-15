# RetailPulse 📊

**RetailPulse** is a Django-based analytics dashboard designed for retail managers to visualize sales trends, monitor inventory health, and forecast peak shopping hours. It leverages **Pandas** for data aggregation and **Matplotlib** for generating server-side visualizations.

## 🚀 Features

  * **Interactive Dashboard:** A centralized view of key performance indicators (KPIs) like Total Revenue, Items Sold, and Top Selling Categories.
  * **Data Visualization:**
      * **Revenue by Category:** Bar chart comparing performance across product categories.
      * **Monthly Trend:** Line chart tracking revenue growth over the last 12 months.
      * **Peak Shopping Heatmap:** A heatmap displaying sales density by "Day of Week" vs. "Hour of Day" to identify busy periods.
  * **Inventory Management:** Real-time **Low Stock Alerts** that flag items falling below their reorder point.
  * **Data Export:** Download detailed sales reports as CSV files for offline analysis.
  * **Automated Data Seeding:** Includes a custom management command to populate the database with realistic dummy data for testing.

## 🛠️ Tech Stack

  * **Backend:** Python 3, Django 5.0+
  * **Data Analysis:** Pandas
  * **Visualization:** Matplotlib (Agg backend)
  * **Frontend:** HTML5, Bootstrap 5.3
  * **Database:** SQLite (Default)

## 📦 Installation Guide

Follow these steps to set up the project locally.

### 1\. Clone the Repository

```bash
git clone https://github.com/YourUsername/RetailPulse.git
cd RetailPulse
```

### 2\. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

Install the required packages listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 4\. Database Setup

Apply the migrations to set up the database schema.

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🌱 Data Seeding

This project includes a custom command to generate realistic test data (50 products and 600+ sales records). You **must** run this command to see data on the dashboard.

```bash
python manage.py seed_data
```

*Output: "Successfully created 50 products and 600 sales."*

## ▶️ Running the Application

Start the local development server:

```bash
python manage.py runserver
```

Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](https://www.google.com/search?q=http://127.0.0.1:8000/)**

## 📂 Project Structure

```text
RetailPulse/
├── manage.py                   # Django CLI utility
├── requirements.txt            # Project dependencies
├── db.sqlite3                  # Database file
│
├── RetailPulse/                # Project Configuration
│   ├── settings.py             # App registration & DB config
│   ├── urls.py                 # Main URL routing
│   └── wsgi.py
│
└── forecaster/                 # Main Application
    ├── admin.py                # Admin panel configuration
    ├── models.py               # Product & Sale database models
    ├── views.py                # Dashboard logic & Matplotlib plotting
    ├── urls.py                 # App-specific URLs
    ├── management/
    │   └── commands/
    │       └── seed_data.py    # Custom data population script
    └── templates/
        └── dashboard.html      # Frontend template
```

## 📸 Screenshots

> *Add screenshots of your dashboard here to showcase the KPI cards and charts.*

## 🤝 Contributing

Contributions are welcome\! Please follow these steps:

1.  Fork the project.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License

This project is open-source and available under the **MIT License**.



