from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime

# In-memory storage for orders
orders = []
order_counter = 1

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.secret_key = 'college_cafeteria_secret_key'
    return app

app = create_app()

# Menu items with Iraqi currency
menu_items = {
    'breakfast': [
        {'id': 1, 'name': 'Pancakes', 'price': 5000, 'description': 'Stack of 3 fluffy pancakes with maple syrup'},
        {'id': 2, 'name': 'Omelette', 'price': 4500, 'description': 'Three-egg omelette with cheese and vegetables'},
        {'id': 3, 'name': 'Coffee', 'price': 2500, 'description': 'Fresh brewed coffee'},
        {'id': 4, 'name': 'Tea', 'price': 1500, 'description': 'Iraqi black tea'}
    ],
    'lunch': [
        {'id': 5, 'name': 'Burger', 'price': 6500, 'description': 'Quarter-pound beef patty with lettuce, tomato and cheese'},
        {'id': 6, 'name': 'Salad', 'price': 4000, 'description': 'Fresh garden salad with olive oil dressing'},
        {'id': 7, 'name': 'Pizza Slice', 'price': 3500, 'description': 'Cheese or pepperoni slice'},
        {'id': 8, 'name': 'Shawarma', 'price': 7000, 'description': 'Traditional Iraqi shawarma with garlic sauce and pickles'},
        {'id': 9, 'name': 'French Fries', 'price': 3000, 'description': 'Crispy golden fries with seasoning'}
    ]
}

# Cafeteria information
cafeteria_info = {
    'name': 'CS Cafeteria',
    'contact': 'cafeteria@college.edu',
    'phone number': '123456###',
    'hours': {
        'days': 'Sunday - Thursday',
        'time': '8:00 AM - 2:00 PM'
    },
    'location': 'Building CS, First Floor'
}

# Initialize cart in session
@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = []

# Home route
@app.route('/')
def home():
    return render_template('home.html', cafeteria_info=cafeteria_info)

# Menu route
@app.route('/menu/<category>')
def menu(category):
    if category not in menu_items:
        return redirect(url_for('menu', category='breakfast'))
    return render_template('menu.html', category=category, items=menu_items[category], categories=menu_items.keys())

# Add to cart route
@app.route('/add_to_cart/<int:item_id>', methods=['POST'])
def add_to_cart(item_id):
    # Find the item in menu_items
    item = None
    for category in menu_items:
        for menu_item in menu_items[category]:
            if menu_item['id'] == item_id:
                item = menu_item
                break
        if item:
            break
    
    if item:
        quantity = int(request.form.get('quantity', 1))
        cart_item = {
            'id': item['id'],
            'name': item['name'],
            'price': item['price'],
            'quantity': quantity,
            'total': item['price'] * quantity
        }
        session['cart'].append(cart_item)
        session.modified = True
        flash(f'Added {item["name"]} to cart!')
    
    return redirect(request.referrer or url_for('menu', category='breakfast'))

# View cart route
@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(item['total'] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

# Remove from cart route
@app.route('/remove_from_cart/<int:index>', methods=['POST'])
def remove_from_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        removed_item = cart.pop(index)
        session.modified = True
        flash(f'Removed {removed_item["name"]} from cart!')
    return redirect(url_for('view_cart'))

# Checkout route
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    global order_counter
    
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        pickup_time = request.form.get('pickup_time')
        cart = session.get('cart', [])
        total = sum(item['total'] for item in cart)

        # Create order in memory
        order = {
            'id': order_counter,
            'student_id': student_id,
            'pickup_time': pickup_time,
            'total': total,
            'timestamp': datetime.now(),
            'items': [item.copy() for item in cart]
        }
        
        # Add order to in-memory storage
        orders.append(order)
        order_counter += 1

        # Clear cart after checkout
        session['cart'] = []
        flash('Order placed successfully! Please pick up your order at the specified time and bring cash for payment.')
        return redirect(url_for('home'))
    
    cart = session.get('cart', [])
    total = sum(item['total'] for item in cart)
    current_time = datetime.now().strftime('%H:%M')
    return render_template('checkout.html', cart=cart, total=total, current_time=current_time)

# Admin route to view all orders
@app.route('/admin/orders')
def view_orders():
    return render_template('orders.html', order_details=[{'order': order, 'items': order['items']} for order in orders])

# Create directory structure and HTML templates
def create_templates():
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Base template
    with open('templates/base.html', 'w') as f:
        f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}College Cafeteria{% endblock %}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* Animation Keyframes */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes glowPulse {
            0% { text-shadow: 0 0 10px rgba(206, 147, 216, 0.5); }
            50% { text-shadow: 0 0 20px rgba(206, 147, 216, 0.8), 0 0 30px rgba(106, 27, 154, 0.5); }
            100% { text-shadow: 0 0 10px rgba(206, 147, 216, 0.5); }
        }

        @keyframes borderGlow {
            0% { box-shadow: 0 0 10px rgba(156, 39, 176, 0.3); }
            50% { box-shadow: 0 0 20px rgba(156, 39, 176, 0.6); }
            100% { box-shadow: 0 0 10px rgba(156, 39, 176, 0.3); }
        }

        :root {
            --primary-color: #6a1b9a;
            --secondary-color: #9c27b0;
            --accent-color: #ce93d8;
            --background-color: #1a1a1a;
            --text-color: #ffffff;
            --card-bg: #2d2d2d;
            --border-color: #444444;
            --nav-bg: rgba(106, 27, 154, 0.2);
            --header-font: 'Poppins', sans-serif;
            --body-font: 'Segoe UI', system-ui, -apple-system, sans-serif;
        }

        body {
            background-color: var(--background-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
        }

        nav {
            background: var(--nav-bg);
            padding: 1rem 0;
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
        }

        nav ul {
            display: flex;
            justify-content: center;
            gap: 2rem;
            list-style: none;
            padding: 0;
            margin: 0;
        }

        nav ul li a {
            color: var(--text-color);
            text-decoration: none;
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            background: rgba(106, 27, 154, 0.3);
            transition: all 0.3s ease;
            font-weight: 500;
        }

        nav ul li a:hover {
            background: var(--primary-color);
            border-color: var(--accent-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(106, 27, 154, 0.3);
        }

        nav ul li {
            animation: fadeInDown 0.5s ease-out;
            animation-fill-mode: both;
        }

        nav ul li:nth-child(1) { animation-delay: 0.2s; }
        nav ul li:nth-child(2) { animation-delay: 0.4s; }
        nav ul li:nth-child(3) { animation-delay: 0.6s; }

        .menu-categories {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .menu-categories a {
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            background: var(--nav-bg);
            color: var(--text-color);
            text-decoration: none;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .menu-categories a:hover {
            background: var(--primary-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(106, 27, 154, 0.3);
        }

        .menu-item {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 2rem;
            margin-bottom: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .menu-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(156, 39, 176, 0.2);
        }

        .menu-item h3 {
            color: var(--accent-color);
            margin-bottom: 1rem;
        }

        .info-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 2rem;
            margin-bottom: 2rem;
            border-radius: 12px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }

        header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            padding: 2rem;
            text-align: center;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
            animation: borderGlow 3s infinite;
        }

        header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at center, rgba(206, 147, 216, 0.2), transparent);
            animation: glowPulse 3s infinite;
        }

        header h1 {
            margin: 0;
            font-size: 2.8rem;
            font-family: var(--header-font);
            font-weight: 700;
            color: #ffffff;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            animation: fadeInDown 1s ease-out, glowPulse 3s infinite;
            letter-spacing: 2px;
        }

        .btn {
            background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
            color: var(--text-color);
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
        }

        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(106, 27, 154, 0.3);
        }

        .quantity-selector {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin: 1rem 0;
        }

        .quantity-input {
            display: flex;
            align-items: center;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.5rem;
            gap: 0.5rem;
        }

        .quantity-btn {
            background: var(--primary-color);
            color: var(--text-color);
            border: none;
            border-radius: 4px;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .quantity-btn:hover {
            background: var(--secondary-color);
            transform: scale(1.1);
        }

        .quantity-input input {
            width: 50px;
            background: transparent;
            border: none;
            color: var(--text-color);
            font-size: 1rem;
            text-align: center;
            -moz-appearance: textfield;
        }

        .quantity-input input::-webkit-outer-spin-button,
        .quantity-input input::-webkit-inner-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }
    </style>
</head>
<body>
    <header>
        <h1>CS Cafeteria</h1>
    </header>
    <nav>
        <ul>
            <li><a href="{{ url_for('home') }}">Home</a></li>
            <li><a href="{{ url_for('menu', category='breakfast') }}">Menu</a></li>
            <li><a href="{{ url_for('view_cart') }}">Cart</a></li>
        </ul>
    </nav>
    <div class="container">
        {% if session.get('flash', []) %}
            <div class="flash-messages">
                {% for message in session.get('flash', []) %}
                    <p>{{ message }}</p>
                {% endfor %}
            </div>
        {% endif %}
        {% block content %}{% endblock %}
    </div>
    <script>
        function incrementQuantity(itemId) {
            const input = document.getElementById(`quantity-${itemId}`);
            if (input.value < 10) {
                input.value = parseInt(input.value) + 1;
            }
        }

        function decrementQuantity(itemId) {
            const input = document.getElementById(`quantity-${itemId}`);
            if (input.value > 1) {
                input.value = parseInt(input.value) - 1;
            }
        }
    </script>
</body>
</html>''')
    
    # Home template
    with open('templates/home.html', 'w') as f:
        f.write('''{% extends 'base.html' %}

{% block content %}
    <h2>Welcome to {{ cafeteria_info.name }}!</h2>
    
    <div class="info-card">
        <h3>Hours of Operation</h3>
        <p>Days: {{ cafeteria_info.hours.days }}</p>
        <p>Time: {{ cafeteria_info.hours.time }}</p>
        
        <h3>Location</h3>
        <p>{{ cafeteria_info.location }}</p>
        
        <h3>Contact</h3>
        <p>{{ cafeteria_info.contact }}</p>
    </div>
    
    <div class="quick-links">
        <h3>Quick Links</h3>
        <p><a href="{{ url_for('menu', category='breakfast') }}" class="btn">View Breakfast Menu</a></p>
        <p><a href="{{ url_for('menu', category='lunch') }}" class="btn">View Lunch Menu</a></p>
        <p><a href="{{ url_for('menu', category='dinner') }}" class="btn">View Dinner Menu</a></p>
    </div>
{% endblock %}''')
    
    # Menu template
    with open('templates/menu.html', 'w') as f:
        f.write('''{% extends 'base.html' %}

{% block title %}{{ category|capitalize }} Menu - College Cafeteria{% endblock %}

{% block content %}
    <h2>{{ category|capitalize }} Menu</h2>
    
    <div class="menu-categories">
        {% for cat in categories %}
            <a href="{{ url_for('menu', category=cat) }}" {% if cat == category %}style="background-color: #2980b9;"{% endif %}>{{ cat|capitalize }}</a>
        {% endfor %}
    </div>
    
    <div class="menu-items">
        {% for item in items %}
            <div class="menu-item">
                <h3>{{ item.name }} - {{ "%.0f"|format(item.price) }} IQD</h3>
                <p>{{ item.description }}</p>
                <form action="{{ url_for('add_to_cart', item_id=item.id) }}" method="post">
                    <div class="quantity-selector">
                        <label for="quantity-{{ item.id }}">Quantity:</label>
                        <div class="quantity-input">
                            <button type="button" class="quantity-btn" onclick="decrementQuantity({{ item.id }})">-</button>
                            <input type="number" id="quantity-{{ item.id }}" name="quantity" value="1" min="1" max="10" readonly>
                            <button type="button" class="quantity-btn" onclick="incrementQuantity({{ item.id }})">+</button>
                        </div>
                    </div>
                    <button type="submit" class="btn">Add to Cart</button>
                </form>
            </div>
        {% endfor %}
    </div>
{% endblock %}''')
    
    # Cart template
    with open('templates/cart.html', 'w') as f:
        f.write('''{% extends 'base.html' %}

{% block title %}Cart - College Cafeteria{% endblock %}

{% block content %}
    <h2>Your Cart</h2>
    
    {% if cart %}
        <table class="cart-table">
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for item in cart %}
                    <tr>
                        <td>{{ item.name }}</td>
                        <td>{{ "%.0f"|format(item.price) }} IQD</td>
                        <td>{{ item.quantity }}</td>
                        <td>{{ "%.0f"|format(item.total) }} IQD</td>
                        <td>
                            <form action="{{ url_for('remove_from_cart', index=loop.index0) }}" method="post">
                                <button type="submit" class="btn btn-danger">Remove</button>
                            </form>
                        </td>
                    </tr>
                {% endfor %}
                <tr>
                    <td colspan="3" style="text-align: right;"><strong>Total:</strong></td>
                    <td><strong>{{ "%.0f"|format(total) }} IQD</strong></td>
                    <td></td>
                </tr>
            </tbody>
        </table>
        
        <div style="margin-top: 20px; text-align: right;">
            <a href="{{ url_for('checkout') }}" class="btn">Proceed to Checkout</a>
        </div>
    {% else %}
        <p>Your cart is empty. <a href="{{ url_for('menu', category='breakfast') }}">Browse our menu</a> to add items.</p>
    {% endif %}
{% endblock %}''')
    
    # Checkout template
    with open('templates/checkout.html', 'w') as f:
        f.write('''{% extends 'base.html' %}
 
{% block title %}Checkout - College Cafeteria{% endblock %}
 
{% block content %}
    <h2>Checkout</h2>
    
    {% if cart %}
        <div class="info-card">
            <h3>Order Summary</h3>
            <table class="cart-table">
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Price</th>
                        <th>Quantity</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in cart %}
                        <tr>
                            <td>{{ item.name }}</td>
                            <td>{{ "%.0f"|format(item.price) }} IQD</td>
                            <td>{{ item.quantity }}</td>
                            <td>{{ "%.0f"|format(item.total) }} IQD</td>
                        </tr>
                    {% endfor %}
                    <tr>
                        <td colspan="3" style="text-align: right;"><strong>Total:</strong></td>
                        <td><strong>{{ "%.0f"|format(total) }} IQD</strong></td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="info-card">
            <h3>Order Details</h3>
            <form action="{{ url_for('checkout') }}" method="post">
                <div class="form-group">
                    <label for="student_id">Student ID:</label>
                    <input type="text" id="student_id" name="student_id" required>
                </div>
                
                <div class="form-group">
                    <label for="pickup_time">Pickup Time:</label>
                    <input type="time" id="pickup_time" name="pickup_time" value="{{ current_time }}" required>
                </div>
                
                <div class="form-group">
                    <p class="payment-note">Payment Method: <strong>Pay on Pickup (Cash only)</strong></p>
                </div>
                
                <div class="form-actions">
                    <button type="submit" class="btn">Place Order</button>
                    <a href="{{ url_for('view_cart') }}" class="btn btn-secondary">Back to Cart</a>
                </div>
            </form>
        </div>
    {% else %}
        <div class="info-card">
            <p>Your cart is empty. <a href="{{ url_for('menu', category='breakfast') }}">Browse our menu</a> to add items.</p>
        </div>
    {% endif %}
{% endblock %}''')

    # Orders template
    with open('templates/orders.html', 'w') as f:
        f.write('''{% extends 'base.html' %}

{% block title %}All Orders - Admin{% endblock %}

{% block content %}
    <h2>All Orders</h2>
    {% for entry in order_details %}
        <div class="info-card">
            <h3>Order #{{ entry.order.id }}</h3>
            <p><strong>Student ID:</strong> {{ entry.order.student_id }}</p>
            <p><strong>Pickup Time:</strong> {{ entry.order.pickup_time }}</p>
            <p><strong>Total:</strong> {{ "%.0f"|format(entry.order.total) }} IQD</p>
            <p><strong>Timestamp:</strong> {{ entry.order.timestamp.strftime('%Y-%m-%d %H:%M:%S') }}</p>
            <table class="cart-table">
                <thead>
                    <tr>
                        <th>Item</th>http://127.0.0.1:5000/
                        <th>Qty</th>
                        <th>Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in entry.items %}
                        <tr>
                            <td>{{ item.name }}</td>
                            <td>{{ item.quantity }}</td>
                            <td>{{ "%.0f"|format(item.price) }} IQD</td>
                            <td>{{ "%.0f"|format(item.total) }} IQD</td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% endfor %}
{% endblock %}''')

# Create templates when running the app
def init():
    """Initialize the application by creating necessary templates"""
    create_templates()
    return app

def run_app():
    """Run the Flask application with production settings"""
    app.run(debug=False, host='0.0.0.0', port=5000)

# Initialize the app when this module is imported
init()

if __name__ == '__main__':
    run_app()
