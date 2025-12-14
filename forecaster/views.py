import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import F
from .models import Product, Sale

# Use Agg backend to prevent GUI errors
matplotlib.use('Agg')

# --- CONFIGURATION FOR DARK MODE CHARTS ---
# This sets the base style for all plots to match a dark dashboard
plt.style.use('dark_background')
plt.rcParams.update({
    'figure.facecolor': 'none',  # Transparent outer background
    'axes.facecolor': 'none',  # Transparent inner background
    'axes.edgecolor': '#444444',  # Subtle borders
    'axes.labelcolor': '#ffffff',  # White labels
    'text.color': '#ffffff',  # White text
    'xtick.color': '#cccccc',  # Light gray ticks
    'ytick.color': '#cccccc',  # Light gray ticks
    'grid.color': '#444444',  # Dark grid lines
    'grid.alpha': 0.3  # Subtle grid
})


def get_graph():
    """Helper: Renders current plot to base64 string"""
    buffer = io.BytesIO()
    # Save with transparent background
    plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')


def dashboard_view(request):
    # 1. Load Data
    sales_qs = Sale.objects.select_related('product').all().values(
        'sale_date', 'quantity_sold', 'total_revenue', 'product__category'
    )

    if not sales_qs.exists():
        return render(request, 'dashboard.html', {'no_data': True})

    df = pd.DataFrame(sales_qs)

    # 2. Data Cleaning
    df['sale_date'] = pd.to_datetime(df['sale_date'])
    df['total_revenue'] = pd.to_numeric(df['total_revenue'])

    # 3. KPI Calculations
    total_revenue = df['total_revenue'].sum()
    total_items_sold = df['quantity_sold'].sum()

    cat_sales = df.groupby('product__category')['total_revenue'].sum()
    top_category = cat_sales.idxmax() if not cat_sales.empty else "N/A"

    # Low Stock Logic
    low_stock_products = Product.objects.filter(current_stock_level__lt=F('reorder_point'))

    # --- VISUALIZATIONS ---

    # Chart 1: Revenue by Category (Bar Chart)
    plt.figure(figsize=(8, 5))
    # Using a vibrant color map for dark mode contrast
    colors = plt.cm.plasma(range(len(cat_sales)))
    bars = plt.bar(cat_sales.index, cat_sales.values, color=colors)
    plt.title('Revenue by Category', fontsize=14, pad=20)
    plt.ylabel('Revenue ($)')
    plt.xlabel('Category')
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.tight_layout()
    chart_category = get_graph()
    plt.close()

    # Chart 2: Monthly Trend (Line Chart)
    df.set_index('sale_date', inplace=True)
    monthly_sales = df['total_revenue'].resample('ME').sum()

    plt.figure(figsize=(8, 5))
    # Neon Cyan line with glow effect simulation (thick line + marker)
    plt.plot(monthly_sales.index, monthly_sales.values, marker='o', color='#00f2ff', linewidth=3, markersize=8)
    plt.fill_between(monthly_sales.index, monthly_sales.values, color='#00f2ff', alpha=0.1)  # Glow under line
    plt.title('Monthly Revenue Trend', fontsize=14, pad=20)
    plt.ylabel('Revenue ($)')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    chart_trend = get_graph()
    plt.close()

    # Chart 3: Heatmap (Hour vs Day)
    df.reset_index(inplace=True)
    df['hour'] = df['sale_date'].dt.hour
    df['day'] = df['sale_date'].dt.day_name()

    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot = df.pivot_table(index='hour', columns='day', values='quantity_sold', aggfunc='count', fill_value=0)
    pivot = pivot.reindex(columns=days_order, fill_value=0)

    plt.figure(figsize=(8, 5))
    # 'inferno' colormap looks great on dark backgrounds (Black -> Red -> Yellow)
    plt.imshow(pivot, cmap='inferno', interpolation='nearest', aspect='auto')
    cbar = plt.colorbar(label='Sales Count')
    cbar.outline.set_edgecolor('#444')  # Dark border for colorbar
    plt.title('Peak Shopping Hours Heatmap', fontsize=14, pad=20)
    plt.xticks(range(len(pivot.columns)), pivot.columns, rotation=45)
    plt.yticks(range(24), range(24))
    plt.tight_layout()
    chart_heatmap = get_graph()
    plt.close()

    context = {
        'total_revenue': f"{total_revenue:,.2f}",  # Added comma formatting
        'total_items_sold': f"{total_items_sold:,}",
        'top_category': top_category,
        'low_stock_products': low_stock_products,
        'chart_category': chart_category,
        'chart_trend': chart_trend,
        'chart_heatmap': chart_heatmap,
    }
    return render(request, 'dashboard.html', context)


def export_csv(request):
    """Generates CSV report"""
    sales_qs = Sale.objects.all().values('sale_date', 'product__name', 'product__category', 'quantity_sold',
                                         'total_revenue')
    df = pd.DataFrame(sales_qs)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    df.to_csv(path_or_buf=response, index=False)

    return response