import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from .models import Product, Sale

# Set Matplotlib backend to 'Agg' to prevent GUI errors in server environment
matplotlib.use('Agg')


def get_graph():
    """Helper to convert the current plt figure to a base64 string"""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    plt.close()  # Important: Close plot to free memory
    return graphic


def dashboard_view(request):
    # 1. Fetch Data
    sales_qs = Sale.objects.select_related('product').all().values(
        'sale_date', 'quantity_sold', 'total_revenue', 'product__category'
    )

    # Check if we have data
    if not sales_qs.exists():
        return render(request, 'dashboard.html', {'no_data': True})

    df = pd.DataFrame(sales_qs)

    # Ensure datatypes
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['total_revenue'] = pd.to_numeric(df['total_revenue'])

    # --- KPI CALCULATIONS ---
    total_revenue = df['total_revenue'].sum()
    total_items_sold = df['quantity_sold'].sum()

    # Top Category
    category_sales = df.groupby('product__category')['total_revenue'].sum()
    top_category = category_sales.idxmax() if not category_sales.empty else "N/A"

    # Low Stock Alert (Direct DB Query is faster for this)
    low_stock_products = Product.objects.filter(current_stock_level__lt=F('reorder_point'))

    # --- VISUALIZATIONS ---

    # Chart 1: Sales per Category (Bar Chart)
    plt.figure(figsize=(6, 4))
    category_sales.plot(kind='bar', color='#4e73df')
    plt.title('Revenue by Category')
    plt.xlabel('Category')
    plt.ylabel('Revenue ($)')
    plt.tight_layout()
    chart_category = get_graph()

    # Chart 2: Monthly Revenue Trend (Line Chart)
    # Resample by Month ('ME' is Month End in newer Pandas, use 'M' for older)
    df.set_index('sale_date', inplace=True)
    monthly_sales = df['total_revenue'].resample('ME').sum()

    plt.figure(figsize=(6, 4))
    plt.plot(monthly_sales.index, monthly_sales.values, marker='o', linestyle='-', color='#1cc88a')
    plt.title('Monthly Revenue Trend')
    plt.xlabel('Date')
    plt.ylabel('Revenue ($)')
    plt.grid(True)
    plt.tight_layout()
    chart_trend = get_graph()

    # Chart 3: Heatmap (Day of Week vs Hour)
    # Restore index to column
    df.reset_index(inplace=True)
    df['hour'] = df['sale_date'].dt.hour
    df['day_of_week'] = df['sale_date'].dt.day_name()

    # Order of days
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = df.pivot_table(index='hour', columns='day_of_week', values='quantity_sold', aggfunc='count',
                                 fill_value=0)

    # Reindex to ensure all days are present
    pivot_table = pivot_table.reindex(columns=days_order, fill_value=0)

    plt.figure(figsize=(7, 5))
    plt.imshow(pivot_table, cmap='hot', interpolation='nearest', aspect='auto')
    plt.colorbar(label='Sales Count')
    plt.title('Sales Heatmap (Day vs Hour)')
    plt.xlabel('Day of Week')
    plt.ylabel('Hour of Day')
    plt.xticks(range(len(pivot_table.columns)), pivot_table.columns, rotation=45)
    plt.yticks(range(24), range(24))  # 0-23 hours
    plt.tight_layout()
    chart_heatmap = get_graph()

    context = {
        'total_revenue': round(total_revenue, 2),
        'total_items_sold': total_items_sold,
        'top_category': top_category,
        'low_stock_products': low_stock_products,
        'chart_category': chart_category,
        'chart_trend': chart_trend,
        'chart_heatmap': chart_heatmap,
    }

    return render(request, 'dashboard.html', context)


def export_csv(request):
    """Generates a CSV report of monthly sales"""
    sales_qs = Sale.objects.all().values('sale_date', 'product__name', 'product__category', 'quantity_sold',
                                         'total_revenue')
    df = pd.DataFrame(sales_qs)

    if df.empty:
        return HttpResponse("No data to export", content_type='text/plain')

    # Prep data for report
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    df.to_csv(path_or_buf=response, index=False)
    return response