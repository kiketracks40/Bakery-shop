# Bakery POS System Documentation

## Overview

The Bakery POS (Point of Sale) System is a Django-based application designed specifically for bakery shops that sell various types of bread and baked goods. This system manages inventory, processes sales, and provides reporting capabilities in a user-friendly interface.

## Features

- **Dashboard**: Overview of key metrics including total products, today's sales, and low stock alerts
- **Product Management**: Add, edit, view, and deactivate bakery products
- **Point of Sale (POS)**: Process customer transactions with an intuitive interface
- **Inventory Tracking**: Automatically update stock levels with each sale
- **Reporting**: View sales data and inventory status

## Technical Stack

- **Framework**: Django 5.1
- **Database**: SQLite (can be upgraded to PostgreSQL for production)
- **Frontend**: HTML, CSS (Bootstrap 5), JavaScript
- **Authentication**: Django's built-in authentication system

## Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/bakery-pos.git
   cd bakery-pos
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## System Architecture

### Models

1. **Product**
   - Core attributes: name, description, price, category
   - Inventory attributes: quantity, alert_threshold, active
   - Used to track bread products and their inventory levels

2. **Sale**
   - Tracks completed transactions
   - Attributes: date_time, cashier (user), payment_method, total

3. **SaleItem**
   - Links products to sales
   - Attributes: sale, product, quantity, price
   - Preserves price point at time of sale

### Views

The application follows a standard MVC (Model-View-Controller) pattern with the following key views:

1. **Dashboard View**
   - Displays key business metrics
   - Shows low stock products and recent sales

2. **Product Management View**
   - Lists all products with edit/delete capabilities
   - Includes modal forms for adding and editing products

3. **POS View**
   - Displays available products for selection
   - Creates and processes sales transactions

### API Endpoints

REST API endpoints are available for programmatic access:

- `/api/products/` - Product management
- `/api/sales/` - Sales data
- `/api/customers/` - Customer information (if implemented)

## User Guide

### Dashboard

The dashboard provides a snapshot of your bakery's current status, including:
- Total number of products in inventory
- Today's sales revenue
- Number of products with low stock
- Recent sales transactions
- Low stock products list

### Managing Products

1. **Viewing Products**
   - Navigate to Products page to see all bakery items
   - Products are displayed in a sortable table

2. **Adding Products**
   - Click "Add Product" button
   - Fill in the required fields:
     - Name
     - Description (optional)
     - Category
     - Price
     - Quantity in stock
     - Alert threshold

3. **Editing Products**
   - Click the "Edit" button next to a product
   - Update any fields as needed
   - Save changes

4. **Deactivating Products**
   - Click the "Delete" button next to a product
   - Confirm the deactivation
   - Note: Products used in previous sales are deactivated rather than deleted

### Using the POS System

1. **Processing a Sale**
   - Navigate to the POS page
   - Select products by clicking "Add" buttons
   - Adjust quantities if needed
   - Select payment method (Cash/Card)
   - Click "Checkout" to complete the transaction

2. **Managing the Cart**
   - Items appear in the cart on the right side
   - Total is automatically calculated
   - Clear cart option is available if needed

### Reports

1. **Daily Sales Report**
   - Navigate to Reports > Daily Sales
   - View sales totals and breakdowns by hour
   - Filter by specific dates

2. **Product Popularity Report**
   - Navigate to Reports > Product Popularity
   - See which products are selling the most
   - Filter by date range

## Security

- Authentication is required for all pages
- Different user roles can be implemented:
  - Cashier: Access to POS and basic product views
  - Manager: Full access including reports and product management
- CSRF protection is implemented on all forms

## Data Management

### Backup Recommendations

1. **Database Backup**
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Restore from Backup**
   ```bash
   python manage.py loaddata backup.json
   ```

### Data Retention

- Sales data is preserved indefinitely
- Products are soft-deleted (deactivated) rather than removed from the database

## Extending the System

The POS system can be extended in several ways:

1. **Customer Management**
   - Add customer profiles
   - Implement loyalty programs

2. **Enhanced Reporting**
   - Add export capabilities (PDF, Excel)
   - Create more detailed analytics

3. **Multiple Locations**
   - Add support for multiple bakery locations
   - Centralized inventory management

4. **Recipes and Production Planning**
   - Link products to ingredient requirements
   - Predict ingredient needs based on sales patterns

## Troubleshooting

### Common Issues

1. **Server won't start**
   - Check if another process is using port 8000
   - Verify virtual environment is activated

2. **Can't process sales**
   - Ensure products have quantity greater than zero
   - Check user permissions

3. **Products not appearing in POS**
   - Verify products are marked as active
   - Check that quantity is greater than zero

### Support

For technical support, please contact:
- Email: edgardopuentes406@hotmail.com
- Documentation: https://github.com/kiketracks40/Bakery-shop

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

*This documentation was last updated on February 28, 2025.*
