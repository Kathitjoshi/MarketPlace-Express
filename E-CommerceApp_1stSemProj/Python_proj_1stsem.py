import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import json
import os
import re
from datetime import datetime
import bcrypt
import logging

# --- Constants, Data & State Management ---

# Get the absolute path of the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Configure logging (Moved after SCRIPT_DIR definition)
log_file_path = os.path.join(SCRIPT_DIR, "app_log.log")
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Centralized style configuration
STYLE = {
    "font_normal": ("Helvetica", 10),
    "font_bold": ("Helvetica", 12, "bold"),
    "font_title": ("Helvetica", 16, "bold"),
    "bg_color": "#F0F0F0",
    "frame_bg": "#FFFFFF",
    "primary_color": "#0078D7",
    "text_color": "#333333",
    "button_color": "#0078D7",
    "button_fg": "#FFFFFF",
}

# --- Data models and persistence ---
def load_user_data():
    """Loads user data from users.json, creating a more detailed structure."""
    path = os.path.join(SCRIPT_DIR, "users.json")
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                logging.info("User data loaded successfully.")
                # Ensure admin password is hashed if it's plaintext
                if "admin" in data and not data["admin"]["password"].startswith("$2b$"):
                    logging.warning("Admin password is plaintext, hashing it now.")
                    data["admin"]["password"] = bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    # Optionally save immediately if you want to ensure admin is always hashed
                    # with open(path, "w") as fw:
                    #     json.dump(data, fw, indent=4)
                return data
        else:
            logging.info("users.json not found, initializing with default admin.")
            # Ensure the initial admin password is hashed
            return {
                "admin": {"password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), 
                          "email": "admin@example.com", "wishlist": [], "orders": []}
            }
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding users.json: {e}. Initializing with default admin.")
        messagebox.showerror("Data Error", "Could not read user data. File might be corrupted. Initializing new data.")
        return {
            "admin": {"password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), 
                      "email": "admin@example.com", "wishlist": [], "orders": []}
        }
    except Exception as e:
        logging.error(f"An unexpected error occurred loading user data: {e}. Initializing with default admin.")
        messagebox.showerror("Error", "An unexpected error occurred while loading user data.")
        return {
            "admin": {"password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), 
                      "email": "admin@example.com", "wishlist": [], "orders": []}
        }

def save_user_data():
    """Saves the current user data to a JSON file."""
    path = os.path.join(SCRIPT_DIR, "users.json")
    try:
        with open(path, "w") as f:
            json.dump(user_data, f, indent=4)
            logging.info("User data saved successfully.")
    except IOError as e:
        logging.error(f"Error saving user data to {path}: {e}")
        messagebox.showerror("Save Error", f"Could not save user data: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred saving user data: {e}")
        messagebox.showerror("Error", "An unexpected error occurred while saving user data.")

# Mapping for uploaded image filenames (assuming they are in the 'images' subdirectory)
IMAGE_MAP = {
    "levis_pants.png": "levis_pants.png",
    "vanheusen_shirt.png": "vanheusen_shirt.png",
    "arrow_shirt.png": "arrow_shirt.png",
    "pepe_jeans_pants.png": "pepe_jeans_pants.png"
}

def get_image_path(filename_in_items_dict):
    """
    Creates a reliable, absolute path to an image, considering it's in an 'images' subdirectory.
    """
    actual_filename = IMAGE_MAP.get(filename_in_items_dict, filename_in_items_dict)
    return os.path.join(SCRIPT_DIR, "images", actual_filename)

# --- Global State Variables ---
user_data = load_user_data() # Load data after defining load_user_data
current_user = None
items = {
    "Levis Pants": {"price": 39, "product": "Pants", "style": "Daily", "desc": "Classic straight-fit denim jeans.", "image": "levis_pants.png"},
    "Van Heusen Shirt": {"price": 89, "product": "Shirts", "style": "Party", "desc": "A premium formal shirt for parties.", "image": "vanheusen_shirt.png"},
    "Arrow Polo": {"price": 59, "product": "Shirts", "style": "Daily", "desc": "A smart casual polo shirt.", "image": "arrow_shirt.png"},
    "Pepe Jeans": {"price": 79, "product": "Pants", "style": "Party", "desc": "Stylish slim-fit jeans.", "image": "pepe_jeans_pants.png"}
}
cart_items = {}
applied_discount = 1.0

# --- Core Application Logic ---

def login():
    global current_user
    username = entry_login_username.get()
    password = entry_login_password.get()

    if username in user_data:
        stored_password_value = user_data[username]['password']

        # Attempt to check if the stored password is a bcrypt hash
        if stored_password_value.startswith('$2b$'):
            try:
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_value.encode('utf-8')):
                    current_user = username
                    messagebox.showinfo("Login Successful", f"Welcome, {current_user}!")
                    logging.info(f"User '{username}' logged in successfully (bcrypt).")
                    notebook.select(frame_home)
                    update_all_dynamic_displays()
                else:
                    current_user = None
                    messagebox.showerror("Login Failed", "Invalid username or password")
                    logging.warning(f"Failed login attempt for '{username}': Incorrect bcrypt password.")
            except ValueError:
                # This could happen if a malformed bcrypt hash is stored
                messagebox.showerror("Login Failed", "An error occurred with your password. Please contact support or try resetting.")
                logging.error(f"ValueError: Invalid salt for user '{username}'. Stored: '{stored_password_value}'.")
                current_user = None
        else:
            # Handle plaintext passwords (migration step)
            if stored_password_value == password:
                current_user = username
                # Hash the password and update in user_data for future logins
                new_hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user_data[username]['password'] = new_hashed_password
                save_user_data()
                messagebox.showinfo("Login Successful", f"Welcome, {current_user}! Your password has been updated for security.")
                logging.info(f"User '{username}' logged in successfully (plaintext migration). Password hashed and saved.")
                notebook.select(frame_home)
                update_all_dynamic_displays()
            else:
                current_user = None
                messagebox.showerror("Login Failed", "Invalid username or password")
                logging.warning(f"Failed login attempt for '{username}': Incorrect plaintext password.")
    else:
        current_user = None
        messagebox.showerror("Login Failed", "Invalid username or password")
        logging.warning(f"Failed login attempt for non-existent username '{username}'.")

def logout():
    global current_user, cart_items, applied_discount
    if current_user:
        logging.info(f"User '{current_user}' logged out.")
    current_user = None
    cart_items = {}
    applied_discount = 1.0
    messagebox.showinfo("Logout", "You have been successfully logged out.")
    notebook.select(frame_home)
    update_all_dynamic_displays()

def submit_signup():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()

    # Define a regular expression for basic email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not all([username, password, email]):
        messagebox.showerror("Error", "All fields must be filled")
        logging.warning("Sign-up failed: All fields not filled.")
        return
    if not re.match(email_regex, email):
        messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
        logging.warning(f"Sign-up failed for '{username}': Invalid email format.")
        return
    if username in user_data:
        messagebox.showerror("Error", "Username already exists. Please choose another.")
        logging.warning(f"Sign-up failed for '{username}': Username already exists.")
        return

    # Hash the password before saving
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data[username] = {"password": hashed_password, "email": email, "wishlist": [], "orders": []}
    save_user_data()
    messagebox.showinfo("Success", f"Sign-up successful for {username}!")
    logging.info(f"New user '{username}' signed up successfully.")
    
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    notebook.select(frame_login)

def clear_product_filters():
    """Resets all product search and filter criteria."""
    search_var.set("")
    product_var.set("All")
    style_var.set("All")
    update_product_display()
    logging.info("Product filters cleared.")

def update_product_display():
    """Updates the display of products based on current filters and search query."""
    for widget in product_display_frame.winfo_children():
        widget.destroy()

    product_type = product_var.get()
    style_type = style_var.get()
    search_query = search_var.get().lower()

    filtered_items = {
        name: data for name, data in items.items()
        if (product_type == "All" or data["product"] == product_type) and
           (style_type == "All" or data["style"] == style_type) and
           (search_query in name.lower() or search_query in data.get('desc', '').lower()) # Search in name and description
    }

    if not filtered_items:
        ttk.Label(product_display_frame, text="No items match your search/filter.", style="TLabel").pack(pady=20)
        return

    for name, data in filtered_items.items():
        card = tk.Frame(product_display_frame, relief=tk.RAISED, borderwidth=1, bg=STYLE['frame_bg'])
        card.pack(fill=tk.X, padx=10, pady=5)
        
        try:
            full_path = get_image_path(data['image'])
            img = Image.open(full_path).resize((100, 100), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = tk.Label(card, image=photo, bg=STYLE['frame_bg'])
            img_label.image = photo
            img_label.pack(side=tk.LEFT, padx=10, pady=10)
        except FileNotFoundError:
            logging.warning(f"Image file not found: {full_path}. Displaying placeholder.")
            img_label = tk.Label(card, text="No Image", width=12, height=6, bg="#CCC")
            img_label.pack(side=tk.LEFT, padx=10, pady=10)
        except Exception as e:
            logging.error(f"Error loading image {full_path}: {e}. Displaying placeholder.")
            img_label = tk.Label(card, text="Image Error", width=12, height=6, bg="#F00")
            img_label.pack(side=tk.LEFT, padx=10, pady=10)

        info_frame = tk.Frame(card, bg=STYLE['frame_bg'])
        info_frame.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
        ttk.Label(info_frame, text=name, style="Bold.TLabel").pack(anchor="w")
        ttk.Label(info_frame, text=f"${data['price']}", style="TLabel").pack(anchor="w")
        btn_frame = tk.Frame(card, bg=STYLE['frame_bg'])
        btn_frame.pack(side=tk.RIGHT, padx=10)
        ttk.Button(btn_frame, text="Add to Cart", command=lambda n=name: add_to_cart(n)).pack(fill=tk.X, pady=2)
        ttk.Button(btn_frame, text="Add to Wishlist", command=lambda n=name: add_to_wishlist(n)).pack(fill=tk.X, pady=2)

def add_to_cart(item_name):
    """Adds an item to the cart or increments its quantity."""
    if not current_user: 
        messagebox.showwarning("Not Logged In", "Please log in to add items to your cart.")
        logging.info(f"Attempted to add '{item_name}' to cart without login.")
        return
    cart_items[item_name] = cart_items.get(item_name, 0) + 1
    update_cart_display()
    messagebox.showinfo("Added to Cart", f"Added {item_name} to your cart.")
    logging.info(f"User '{current_user}' added '{item_name}' to cart. Current quantity: {cart_items[item_name]}.")

def increase_cart_item(item_name):
    """Increases the quantity of a specific item in the cart."""
    if item_name in cart_items:
        cart_items[item_name] += 1
        update_cart_display()
        logging.info(f"User '{current_user}' increased quantity of '{item_name}' to {cart_items[item_name]}.")

def decrease_cart_item(item_name):
    """Decreases the quantity of a specific item in the cart, removing if quantity becomes zero."""
    if item_name in cart_items:
        cart_items[item_name] -= 1
        if cart_items[item_name] <= 0:
            del cart_items[item_name]
            logging.info(f"User '{current_user}' removed '{item_name}' from cart (quantity reached 0).")
        else:
            logging.info(f"User '{current_user}' decreased quantity of '{item_name}' to {cart_items[item_name]}.")
    update_cart_display()

def add_to_wishlist(item_name):
    """Adds an item to the current user's wishlist."""
    if not current_user: 
        messagebox.showwarning("Not Logged In", "Please log in to add items to your wishlist.")
        logging.info(f"Attempted to add '{item_name}' to wishlist without login.")
        return
    wishlist = user_data[current_user]['wishlist']
    if item_name not in wishlist:
        wishlist.append(item_name)
        save_user_data()
        messagebox.showinfo("Wishlist", f"Added {item_name} to your wishlist.")
        logging.info(f"User '{current_user}' added '{item_name}' to wishlist.")
        update_profile_display()
    else:
        messagebox.showinfo("Wishlist", f"{item_name} is already in your wishlist.")
        logging.info(f"User '{current_user}' attempted to add '{item_name}' to wishlist, but it was already there.")

def remove_from_wishlist(item_name):
    """Removes an item from the current user's wishlist."""
    if current_user and item_name in user_data[current_user]['wishlist']:
        user_data[current_user]['wishlist'].remove(item_name)
        save_user_data()
        messagebox.showinfo("Wishlist", f"Removed {item_name} from your wishlist.")
        logging.info(f"User '{current_user}' removed '{item_name}' from wishlist.")
        update_profile_display()
    else:
        logging.warning(f"Attempted to remove '{item_name}' from wishlist, but it was not found or user not logged in.")

def update_cart_display():
    """Updates the shopping cart display with current items and total price."""
    for widget in cart_display_frame.winfo_children(): 
        widget.destroy()
    
    if not cart_items:
        ttk.Label(cart_display_frame, text="Your cart is empty.", style="TLabel").pack(pady=20)
        total_price_label.config(text="Total: $0.00")
        return

    subtotal = sum(items[name]['price'] * qty for name, qty in cart_items.items())
    for name, quantity in cart_items.items():
        price = items[name]['price']
        item_frame = ttk.Frame(cart_display_frame); 
        item_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(item_frame, text=f"{name}").pack(side=tk.LEFT, padx=5)
        
        qty_frame = ttk.Frame(item_frame)
        qty_frame.pack(side=tk.LEFT, padx=5)
        ttk.Button(qty_frame, text="-", width=2, command=lambda n=name: decrease_cart_item(n)).pack(side=tk.LEFT)
        ttk.Label(qty_frame, text=f"x{quantity}", width=4, anchor="center").pack(side=tk.LEFT)
        ttk.Button(qty_frame, text="+", width=2, command=lambda n=name: increase_cart_item(n)).pack(side=tk.LEFT)

        ttk.Label(item_frame, text=f"${price * quantity:.2f}").pack(side=tk.RIGHT, padx=5)
        ttk.Button(item_frame, text="Remove", command=lambda n=name: decrease_cart_item(n)).pack(side=tk.RIGHT) # Use decrease for single item removal

    final_total = subtotal * applied_discount
    subtotal_text = f"Subtotal: ${subtotal:.2f}"
    discount_text = ""
    if applied_discount < 1.0: 
        discount_amount = subtotal * (1 - applied_discount)
        discount_text = f"Discount: -${discount_amount:.2f}"
    
    total_price_label.config(text=f"{subtotal_text}\n{discount_text}\nTotal: ${final_total:.2f}")

def apply_coupon():
    """Applies a coupon code to the cart total."""
    global applied_discount
    coupon_code = entry_coupon.get().upper()
    if coupon_code == "DISCOUNT20":
        applied_discount = 0.80
        messagebox.showinfo("Coupon Applied", "20% discount has been applied to your cart!")
        logging.info(f"User '{current_user}' applied 'DISCOUNT20' coupon.")
    else:
        applied_discount = 1.0
        messagebox.showerror("Invalid Coupon", "The entered coupon code is not valid.")
        logging.warning(f"User '{current_user}' attempted to apply invalid coupon: '{coupon_code}'.")
    update_cart_display()
    update_checkout_display() # Also update checkout view

def show_checkout():
    """Navigates to the checkout tab if conditions are met."""
    if not current_user: 
        messagebox.showwarning("Not Logged In", "Please log in to proceed.")
        return
    if not cart_items: 
        messagebox.showerror("Empty Cart", "Your cart is empty.")
        return
    update_checkout_display()
    notebook.select(frame_checkout)

def update_checkout_display():
    """Updates the order summary in the checkout tab."""
    checkout_summary_text.config(state=tk.NORMAL)
    checkout_summary_text.delete(1.0, tk.END)
    if not cart_items:
        checkout_summary_text.insert(tk.END, "Your cart is empty.")
    else:
        checkout_summary_text.insert(tk.END, "Order Summary:\n\n")
        for name, qty in cart_items.items():
            checkout_summary_text.insert(tk.END, f"- {name} (x{qty}): ${items[name]['price'] * qty:.2f}\n")
        checkout_summary_text.insert(tk.END, f"\n{total_price_label.cget('text')}")
    checkout_summary_text.config(state=tk.DISABLED)

def proceed_to_payment():
    """Processes the payment, saves the order, and clears the cart."""
    global cart_items, applied_discount
    if not current_user: # Should not happen if show_checkout is used, but for robustness
        messagebox.showerror("Error", "No user logged in to place order.")
        return

    if not cart_items: # Should not happen if show_checkout is used
        messagebox.showerror("Error", "Cart is empty, cannot proceed with payment.")
        return

    new_order = {
        "order_id": f"ORD-{int(datetime.now().timestamp())}",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": cart_items.copy(),
        "total": sum(items[name]['price'] * qty for name, qty in cart_items.items()) * applied_discount
    }
    user_data[current_user]['orders'].append(new_order); 
    save_user_data()
    messagebox.showinfo("Payment Successful", f"Your order {new_order['order_id']} has been placed!")
    logging.info(f"User '{current_user}' placed order {new_order['order_id']} for total ${new_order['total']:.2f}.")
    cart_items = {}; 
    applied_discount = 1.0
    update_all_dynamic_displays()
    notebook.select(frame_profile)

def update_profile_display():
    """Updates the user profile display with personal info, wishlist, and order history."""
    for widget in profile_display_frame.winfo_children(): 
        widget.destroy()
    
    if not current_user: 
        ttk.Label(profile_display_frame, text="Please log in to view your profile.", style="TLabel").pack(pady=20)
        return
    
    user_info = user_data[current_user]
    header_frame = ttk.Frame(profile_display_frame); 
    header_frame.pack(fill=tk.X, pady=10)
    
    ttk.Label(header_frame, text=f"Welcome, {current_user}!", style="Title.TLabel").pack(side=tk.LEFT)
    ttk.Button(header_frame, text="Logout", command=logout).pack(side=tk.RIGHT)
    
    ttk.Label(profile_display_frame, text=f"Email: {user_info['email']}", style="Bold.TLabel").pack(anchor="w", padx=10)
    
    # --- Wishlist Section ---
    ttk.Separator(profile_display_frame, orient='horizontal').pack(fill='x', pady=15)
    ttk.Label(profile_display_frame, text="Your Wishlist", style="Bold.TLabel").pack(anchor="w", padx=10)
    wishlist_frame = ttk.Frame(profile_display_frame); 
    wishlist_frame.pack(fill=tk.X, padx=10)
    
    if not user_info['wishlist']: 
        ttk.Label(wishlist_frame, text="Your wishlist is empty.").pack(pady=5)
    else:
        for item_name in user_info['wishlist']:
            item_frame = ttk.Frame(wishlist_frame); 
            item_frame.pack(fill=tk.X, pady=2)
            ttk.Label(item_frame, text=f"- {item_name}").pack(side=tk.LEFT)
            ttk.Button(item_frame, text="Remove", command=lambda n=item_name: remove_from_wishlist(n)).pack(side=tk.RIGHT)
    
    # --- Order History Section ---
    ttk.Separator(profile_display_frame, orient='horizontal').pack(fill='x', pady=15)
    ttk.Label(profile_display_frame, text="Order History", style="Bold.TLabel").pack(anchor="w", padx=10)
    history_frame = ttk.Frame(profile_display_frame); 
    history_frame.pack(fill=tk.BOTH, expand=True, padx=10)
    
    if not user_info['orders']: 
        ttk.Label(history_frame, text="You have no past orders.").pack(pady=5)
    else:
        for order in reversed(user_info['orders']): # Display most recent orders first
            order_frame = ttk.LabelFrame(history_frame, text=f"Order {order['order_id']} ({order['date']})", padding=10)
            order_frame.pack(fill=tk.X, pady=5)
            for name, qty in order['items'].items(): 
                ttk.Label(order_frame, text=f"- {name} (x{qty})").pack(anchor="w")
            ttk.Label(order_frame, text=f"Total: ${order['total']:.2f}", style="Bold.TLabel").pack(anchor="e")

    # This is important for the scrollbar to work correctly with dynamically added content
    profile_display_frame.update_idletasks()
    canvas_profile.config(scrollregion=canvas_profile.bbox("all"))


def update_all_dynamic_displays():
    """Calls all functions that update dynamic content across tabs."""
    update_profile_display()
    update_cart_display()
    update_home_display()
    update_checkout_display() # Ensure checkout summary is refreshed

def on_tab_changed(event):
    """Event handler for notebook tab changes to update content."""
    selected_tab = notebook.tab(notebook.select(), "text")
    logging.info(f"Tab changed to: {selected_tab}")
    if selected_tab == "Profile": 
        update_profile_display()
    elif selected_tab == "Shopping Cart": 
        update_cart_display()
    elif selected_tab == "Home": 
        update_home_display()
    elif selected_tab == "Checkout": 
        update_checkout_display()
    elif selected_tab == "Products":
        update_product_display() # Ensure products are always refreshed on tab switch

def update_home_display():
    """Updates the home tab content based on login status."""
    for widget in frame_home.winfo_children(): 
        widget.destroy() # Clear existing widgets
    
    if current_user:
        ttk.Label(frame_home, text=f"Welcome back, {current_user}!", style="Title.TLabel").pack(pady=20)
        ttk.Label(frame_home, text="Check out our latest products or view your profile.", wraplength=400).pack(pady=10)
        ttk.Button(frame_home, text="Go to Products", command=lambda: notebook.select(frame_products)).pack(pady=5)
        ttk.Button(frame_home, text="View My Profile", command=lambda: notebook.select(frame_profile)).pack(pady=5)
    else:
        ttk.Label(frame_home, text="Welcome to MarketPlace Express", style="Title.TLabel").pack(pady=20)
        ttk.Label(frame_home, text="Your one-stop shop for fashion. Please sign up or log in to continue.", wraplength=400).pack(pady=10)
        ttk.Button(frame_home, text="Login", command=lambda: notebook.select(frame_login)).pack(pady=5)
        ttk.Button(frame_home, text="Sign Up", command=lambda: notebook.select(frame_signup)).pack(pady=5)

# --- GUI Setup ---
root = tk.Tk()
root.title("MarketPlace Express")
root.geometry("650x700")
root.configure(bg=STYLE['bg_color'])

# Configure ttk styles
s = ttk.Style()
s.theme_use('clam') # 'clam' or 'alt' or 'default'
s.configure("TNotebook", background=STYLE['bg_color'], borderwidth=0)
s.configure("TNotebook.Tab", background="#E1E1E1", padding=[10, 5], font=STYLE['font_bold'])
s.map("TNotebook.Tab", background=[("selected", STYLE['primary_color'])], foreground=[("selected", STYLE['button_fg'])])
s.configure("TFrame", background=STYLE['frame_bg'])
s.configure("TLabel", background=STYLE['frame_bg'], foreground=STYLE['text_color'], font=STYLE['font_normal'])
s.configure("Bold.TLabel", font=STYLE['font_bold'], background=STYLE['frame_bg'])
s.configure("Title.TLabel", font=STYLE['font_title'], background=STYLE['frame_bg'])
s.configure("TButton", background=STYLE['button_color'], foreground=STYLE['button_fg'], font=STYLE['font_normal'], padding=5)
s.map("TButton", background=[('active', '#005a9e')])

# Create Notebook (tabs container)
notebook = ttk.Notebook(root, style="TNotebook")
notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# --- Tab Frames ---
frame_home = ttk.Frame(notebook, padding=20)
frame_products = ttk.Frame(notebook, padding=10)
frame_cart = ttk.Frame(notebook, padding=20)
frame_checkout = ttk.Frame(notebook, padding=20)
frame_profile = ttk.Frame(notebook, padding=10)
frame_coupons = ttk.Frame(notebook, padding=20)
frame_login = ttk.Frame(notebook, padding=20)
frame_signup = ttk.Frame(notebook, padding=20)

# Add tabs to the notebook
notebook.add(frame_home, text='Home')
notebook.add(frame_products, text='Products')
notebook.add(frame_cart, text='Shopping Cart')
notebook.add(frame_checkout, text='Checkout')
notebook.add(frame_profile, text='Profile')
notebook.add(frame_coupons, text='Coupons')
notebook.add(frame_login, text='Login')
notebook.add(frame_signup, text='Sign Up')

# --- Home, Signup, Login Frames (Content) ---
update_home_display() # Initialize home display

# Signup Frame
ttk.Label(frame_signup, text="Create a New Account", style="Title.TLabel").pack(pady=10)
ttk.Label(frame_signup, text="Username").pack()
entry_username = ttk.Entry(frame_signup, width=30); entry_username.pack(pady=2)
ttk.Label(frame_signup, text="Password").pack()
entry_password = ttk.Entry(frame_signup, show="*", width=30); entry_password.pack(pady=2)
ttk.Label(frame_signup, text="Email").pack()
entry_email = ttk.Entry(frame_signup, width=30); entry_email.pack(pady=2)
ttk.Button(frame_signup, text="Submit", command=submit_signup).pack(pady=20)

# Login Frame
ttk.Label(frame_login, text="Welcome Back!", style="Title.TLabel").pack(pady=10)
ttk.Label(frame_login, text="Username").pack()
entry_login_username = ttk.Entry(frame_login, width=30); entry_login_username.pack(pady=2)
ttk.Label(frame_login, text="Password").pack()
entry_login_password = ttk.Entry(frame_login, show="*", width=30); entry_login_password.pack(pady=2)
ttk.Button(frame_login, text="Login", command=login).pack(pady=20)

# --- Products Frame (Content) ---
filter_frame = ttk.Frame(frame_products, padding=10); filter_frame.pack(fill=tk.X)
ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
search_var = tk.StringVar()
search_entry = ttk.Entry(filter_frame, textvariable=search_var)
search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
search_entry.bind("<KeyRelease>", lambda event: update_product_display()) # Live search

product_var = tk.StringVar(value="All")
ttk.Combobox(filter_frame, textvariable=product_var, values=["All"] + list(set(d['product'] for d in items.values())), state="readonly", width=10).pack(side=tk.LEFT, padx=5)
product_var.trace_add("write", lambda *args: update_product_display()) # Update on combobox change

style_var = tk.StringVar(value="All")
ttk.Combobox(filter_frame, textvariable=style_var, values=["All"] + list(set(d['style'] for d in items.values())), state="readonly", width=10).pack(side=tk.LEFT, padx=5)
style_var.trace_add("write", lambda *args: update_product_display()) # Update on combobox change

ttk.Button(filter_frame, text="Clear Filters", command=clear_product_filters).pack(side=tk.LEFT, padx=5)

# Product display area with scrollbar
canvas = tk.Canvas(frame_products, bg=STYLE['frame_bg']); 
scrollbar = ttk.Scrollbar(frame_products, orient="vertical", command=canvas.yview)
product_display_frame = ttk.Frame(canvas); 
product_display_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=product_display_frame, anchor="nw"); 
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True); 
scrollbar.pack(side="right", fill="y")

# --- Cart, Checkout, Coupons Frames (Content) ---
ttk.Label(frame_cart, text="Your Shopping Cart", style="Title.TLabel").pack(pady=10)
cart_display_frame = ttk.Frame(frame_cart, padding=10); 
cart_display_frame.pack(fill=tk.BOTH, expand=True)
total_price_label = ttk.Label(frame_cart, text="Total: $0.00", style="Bold.TLabel", justify=tk.RIGHT); 
total_price_label.pack(pady=10, anchor="e")
ttk.Button(frame_cart, text="Proceed to Checkout", command=show_checkout).pack(pady=10)

ttk.Label(frame_checkout, text="Confirm Your Order", style="Title.TLabel").pack(pady=10)
checkout_summary_text = tk.Text(frame_checkout, height=15, width=60, wrap=tk.WORD, state=tk.DISABLED, font=STYLE['font_normal'], relief=tk.FLAT, bg=STYLE['frame_bg'])
checkout_summary_text.pack(pady=10, padx=10)
ttk.Button(frame_checkout, text="Confirm and Pay", command=proceed_to_payment).pack(pady=20)

ttk.Label(frame_coupons, text="Apply a Coupon", style="Title.TLabel").pack(pady=10)
ttk.Label(frame_coupons, text="Enter Coupon Code: (Hint: DISCOUNT20)").pack(pady=5)
entry_coupon = ttk.Entry(frame_coupons, width=30); entry_coupon.pack(pady=5)
ttk.Button(frame_coupons, text="Apply Coupon", command=apply_coupon).pack(pady=10)

# --- Profile Frame (Content) ---
canvas_profile = tk.Canvas(frame_profile, bg=STYLE['frame_bg']); 
scrollbar_profile = ttk.Scrollbar(frame_profile, orient="vertical", command=canvas_profile.yview)
profile_display_frame = ttk.Frame(canvas_profile, padding=10); 
profile_display_frame.bind("<Configure>", lambda e: canvas_profile.configure(scrollregion=canvas_profile.bbox("all")))
canvas_profile.create_window((0, 0), window=profile_display_frame, anchor="nw", width=600); 
canvas_profile.configure(yscrollcommand=scrollbar_profile.set)
canvas_profile.pack(side="left", fill="both", expand=True); 
scrollbar_profile.pack(side="right", fill="y")

# --- Finalize ---
notebook.pack(expand=True, fill='both', padx=10, pady=10)
update_all_dynamic_displays() # Initial update for all dynamic content
update_product_display() # Initial display of products

# Ensure data is saved on application close
def on_closing():
    save_user_data()
    root.destroy()
    logging.info("Application closed.")

root.protocol("WM_DELETE_WINDOW", on_closing) # Bind closing event
root.mainloop()
