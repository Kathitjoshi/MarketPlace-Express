import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageTk
import json
import os
import re # Imported for email validation
from datetime import datetime

# --- Constants, Data & State Management ---

# Get the absolute path of the directory where the script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

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
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {
        "admin": {"password": "password", "email": "admin@example.com", "wishlist": [], "orders": []}
    }

def save_user_data():
    """Saves the current user data to a JSON file."""
    path = os.path.join(SCRIPT_DIR, "users.json")
    with open(path, "w") as f:
        json.dump(user_data, f, indent=4)

def get_image_path(filename):
    """Creates a reliable, absolute path to an image."""
    return os.path.join(SCRIPT_DIR, "images", filename)

# --- Global State Variables ---
user_data = load_user_data()
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

    if username in user_data and user_data[username]['password'] == password:
        current_user = username
        messagebox.showinfo("Login Successful", f"Welcome, {current_user}!")
        notebook.select(frame_home)
        update_all_dynamic_displays()
    else:
        current_user = None
        messagebox.showerror("Login Failed", "Invalid username or password")

def logout():
    global current_user, cart_items, applied_discount
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
        return
    if not re.match(email_regex, email):
        messagebox.showerror("Error", "Invalid email format. Please enter a valid email address.")
        return
    if username in user_data:
        messagebox.showerror("Error", "Username already exists. Please choose another.")
        return

    user_data[username] = {"password": password, "email": email, "wishlist": [], "orders": []}
    save_user_data()
    messagebox.showinfo("Success", f"Sign-up successful for {username}!")
    
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    notebook.select(frame_login)

def update_product_display():
    for widget in product_display_frame.winfo_children():
        widget.destroy()

    product_type = product_var.get()
    style_type = style_var.get()
    search_query = search_var.get().lower()

    filtered_items = {
        name: data for name, data in items.items()
        if (product_type == "All" or data["product"] == product_type) and
           (style_type == "All" or data["style"] == style_type) and
           (search_query in name.lower())
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
            img_label = tk.Label(card, text="No Image", width=12, height=6, bg="#CCC")
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
    if not current_user: messagebox.showwarning("Not Logged In", "Please log in to add items to your cart."); return
    cart_items[item_name] = cart_items.get(item_name, 0) + 1
    update_cart_display()
    messagebox.showinfo("Added to Cart", f"Added {item_name} to your cart.")

def remove_from_cart(item_name):
    if item_name in cart_items:
        cart_items[item_name] -= 1
        if cart_items[item_name] <= 0: del cart_items[item_name]
    update_cart_display()

def add_to_wishlist(item_name):
    if not current_user: messagebox.showwarning("Not Logged In", "Please log in to add items to your wishlist."); return
    wishlist = user_data[current_user]['wishlist']
    if item_name not in wishlist:
        wishlist.append(item_name)
        save_user_data()
        messagebox.showinfo("Wishlist", f"Added {item_name} to your wishlist.")
        update_profile_display()
    else:
        messagebox.showinfo("Wishlist", f"{item_name} is already in your wishlist.")

def remove_from_wishlist(item_name):
    if current_user and item_name in user_data[current_user]['wishlist']:
        user_data[current_user]['wishlist'].remove(item_name)
        save_user_data()
        update_profile_display()

def update_cart_display():
    for widget in cart_display_frame.winfo_children(): widget.destroy()
    if not cart_items:
        ttk.Label(cart_display_frame, text="Your cart is empty.", style="TLabel").pack(pady=20)
        total_price_label.config(text="Total: $0.00")
        return
    subtotal = sum(items[name]['price'] * qty for name, qty in cart_items.items())
    for name, quantity in cart_items.items():
        price = items[name]['price']
        item_frame = ttk.Frame(cart_display_frame); item_frame.pack(fill=tk.X, pady=2)
        ttk.Label(item_frame, text=f"{name} (x{quantity}) - ${price * quantity:.2f}").pack(side=tk.LEFT, padx=5)
        ttk.Button(item_frame, text="Remove", command=lambda n=name: remove_from_cart(n)).pack(side=tk.RIGHT)
    final_total = subtotal * applied_discount
    subtotal_text = f"Subtotal: ${subtotal:.2f}"; discount_text = ""
    if applied_discount < 1.0: discount_text = f"Discount: -${subtotal * (1 - applied_discount):.2f}"
    total_price_label.config(text=f"{subtotal_text}\n{discount_text}\nTotal: ${final_total:.2f}")

def apply_coupon():
    global applied_discount
    coupon_code = entry_coupon.get().upper()
    if coupon_code == "DISCOUNT20":
        applied_discount = 0.80
        messagebox.showinfo("Coupon Applied", "20% discount has been applied to your cart!")
    else:
        applied_discount = 1.0
        messagebox.showerror("Invalid Coupon", "The entered coupon code is not valid.")
    update_cart_display()
    update_checkout_display() # Also update checkout view

def show_checkout():
    if not current_user: messagebox.showwarning("Not Logged In", "Please log in to proceed."); return
    if not cart_items: messagebox.showerror("Empty Cart", "Your cart is empty."); return
    update_checkout_display()
    notebook.select(frame_checkout)

def update_checkout_display():
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
    global cart_items, applied_discount
    new_order = {
        "order_id": f"ORD-{int(datetime.now().timestamp())}",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": cart_items.copy(),
        "total": sum(items[name]['price'] * qty for name, qty in cart_items.items()) * applied_discount
    }
    user_data[current_user]['orders'].append(new_order); save_user_data()
    messagebox.showinfo("Payment Successful", f"Your order {new_order['order_id']} has been placed!")
    cart_items = {}; applied_discount = 1.0
    update_all_dynamic_displays()
    notebook.select(frame_profile)

def update_profile_display():
    for widget in profile_display_frame.winfo_children(): widget.destroy()
    if not current_user: ttk.Label(profile_display_frame, text="Please log in to view your profile.", style="TLabel").pack(pady=20); return
    user_info = user_data[current_user]
    header_frame = ttk.Frame(profile_display_frame); header_frame.pack(fill=tk.X, pady=10)
    ttk.Label(header_frame, text=f"Welcome, {current_user}!", style="Title.TLabel").pack(side=tk.LEFT)
    ttk.Button(header_frame, text="Logout", command=logout).pack(side=tk.RIGHT)
    ttk.Label(profile_display_frame, text=f"Email: {user_info['email']}", style="Bold.TLabel").pack(anchor="w", padx=10)
    ttk.Separator(profile_display_frame, orient='horizontal').pack(fill='x', pady=15)
    ttk.Label(profile_display_frame, text="Your Wishlist", style="Bold.TLabel").pack(anchor="w", padx=10)
    wishlist_frame = ttk.Frame(profile_display_frame); wishlist_frame.pack(fill=tk.X, padx=10)
    if not user_info['wishlist']: ttk.Label(wishlist_frame, text="Your wishlist is empty.").pack(pady=5)
    else:
        for item_name in user_info['wishlist']:
            item_frame = ttk.Frame(wishlist_frame); item_frame.pack(fill=tk.X, pady=2)
            ttk.Label(item_frame, text=f"- {item_name}").pack(side=tk.LEFT)
            ttk.Button(item_frame, text="Remove", command=lambda n=item_name: remove_from_wishlist(n)).pack(side=tk.RIGHT)
    ttk.Separator(profile_display_frame, orient='horizontal').pack(fill='x', pady=15)
    ttk.Label(profile_display_frame, text="Order History", style="Bold.TLabel").pack(anchor="w", padx=10)
    history_frame = ttk.Frame(profile_display_frame); history_frame.pack(fill=tk.BOTH, expand=True, padx=10)
    if not user_info['orders']: ttk.Label(history_frame, text="You have no past orders.").pack(pady=5)
    else:
        for order in reversed(user_info['orders']):
            order_frame = ttk.LabelFrame(history_frame, text=f"Order {order['order_id']} ({order['date']})", padding=10)
            order_frame.pack(fill=tk.X, pady=5)
            for name, qty in order['items'].items(): ttk.Label(order_frame, text=f"- {name} (x{qty})").pack(anchor="w")
            ttk.Label(order_frame, text=f"Total: ${order['total']:.2f}", style="Bold.TLabel").pack(anchor="e")

def update_all_dynamic_displays():
    update_profile_display(); update_cart_display(); update_home_display(); update_checkout_display()

def on_tab_changed(event):
    selected_tab = notebook.tab(notebook.select(), "text")
    if selected_tab == "Profile": update_profile_display()
    elif selected_tab == "Shopping Cart": update_cart_display()
    elif selected_tab == "Home": update_home_display()
    elif selected_tab == "Checkout": update_checkout_display()

def update_home_display():
    for widget in frame_home.winfo_children(): widget.destroy()
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
root = tk.Tk(); root.title("MarketPlace Express"); root.geometry("650x700"); root.configure(bg=STYLE['bg_color'])
s = ttk.Style(); s.theme_use('clam'); s.configure("TNotebook", background=STYLE['bg_color'], borderwidth=0)
s.configure("TNotebook.Tab", background="#E1E1E1", padding=[10, 5], font=STYLE['font_bold'])
s.map("TNotebook.Tab", background=[("selected", STYLE['primary_color'])], foreground=[("selected", STYLE['button_fg'])])
s.configure("TFrame", background=STYLE['frame_bg']); s.configure("TLabel", background=STYLE['frame_bg'], foreground=STYLE['text_color'], font=STYLE['font_normal'])
s.configure("Bold.TLabel", font=STYLE['font_bold'], background=STYLE['frame_bg']); s.configure("Title.TLabel", font=STYLE['font_title'], background=STYLE['frame_bg'])
s.configure("TButton", background=STYLE['button_color'], foreground=STYLE['button_fg'], font=STYLE['font_normal'], padding=5)
s.map("TButton", background=[('active', '#005a9e')])

notebook = ttk.Notebook(root, style="TNotebook"); notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

# --- Tab Frames ---
frame_home = ttk.Frame(notebook, padding=20)
frame_products = ttk.Frame(notebook, padding=10)
frame_cart = ttk.Frame(notebook, padding=20)
frame_checkout = ttk.Frame(notebook, padding=20) # RESTORED
frame_profile = ttk.Frame(notebook, padding=10)
frame_coupons = ttk.Frame(notebook, padding=20)   # RESTORED
frame_login = ttk.Frame(notebook, padding=20)
frame_signup = ttk.Frame(notebook, padding=20)

notebook.add(frame_home, text='Home'); notebook.add(frame_products, text='Products'); notebook.add(frame_cart, text='Shopping Cart')
notebook.add(frame_checkout, text='Checkout'); notebook.add(frame_profile, text='Profile'); notebook.add(frame_coupons, text='Coupons')
notebook.add(frame_login, text='Login'); notebook.add(frame_signup, text='Sign Up')

# --- Home, Signup, Login Frames (Content) ---
update_home_display()
ttk.Label(frame_signup, text="Create a New Account", style="Title.TLabel").pack(pady=10)
entry_username = ttk.Entry(frame_signup, width=30); entry_username.pack(pady=2); ttk.Label(frame_signup, text="Username").pack()
entry_password = ttk.Entry(frame_signup, show="*", width=30); entry_password.pack(pady=2); ttk.Label(frame_signup, text="Password").pack()
entry_email = ttk.Entry(frame_signup, width=30); entry_email.pack(pady=2); ttk.Label(frame_signup, text="Email").pack()
ttk.Button(frame_signup, text="Submit", command=submit_signup).pack(pady=20)
ttk.Label(frame_login, text="Welcome Back!", style="Title.TLabel").pack(pady=10)
entry_login_username = ttk.Entry(frame_login, width=30); entry_login_username.pack(pady=2); ttk.Label(frame_login, text="Username").pack()
entry_login_password = ttk.Entry(frame_login, show="*", width=30); entry_login_password.pack(pady=2); ttk.Label(frame_login, text="Password").pack()
ttk.Button(frame_login, text="Login", command=login).pack(pady=20)

# --- Products Frame (Content) ---
filter_frame = ttk.Frame(frame_products, padding=10); filter_frame.pack(fill=tk.X)
ttk.Label(filter_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
search_var = tk.StringVar(); ttk.Entry(filter_frame, textvariable=search_var).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
product_var = tk.StringVar(value="All"); ttk.Combobox(filter_frame, textvariable=product_var, values=["All"] + list(set(d['product'] for d in items.values())), state="readonly", width=10).pack(side=tk.LEFT, padx=5)
style_var = tk.StringVar(value="All"); ttk.Combobox(filter_frame, textvariable=style_var, values=["All"] + list(set(d['style'] for d in items.values())), state="readonly", width=10).pack(side=tk.LEFT, padx=5)
ttk.Button(filter_frame, text="Search/Filter", command=update_product_display).pack(side=tk.LEFT, padx=5)
canvas = tk.Canvas(frame_products, bg=STYLE['frame_bg']); scrollbar = ttk.Scrollbar(frame_products, orient="vertical", command=canvas.yview)
product_display_frame = ttk.Frame(canvas); product_display_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=product_display_frame, anchor="nw"); canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True); scrollbar.pack(side="right", fill="y")

# --- Cart, Checkout, Coupons Frames (Content) ---
ttk.Label(frame_cart, text="Your Shopping Cart", style="Title.TLabel").pack(pady=10)
cart_display_frame = ttk.Frame(frame_cart, padding=10); cart_display_frame.pack(fill=tk.BOTH, expand=True)
total_price_label = ttk.Label(frame_cart, text="Total: $0.00", style="Bold.TLabel", justify=tk.RIGHT); total_price_label.pack(pady=10, anchor="e")
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
canvas_profile = tk.Canvas(frame_profile, bg=STYLE['frame_bg']); scrollbar_profile = ttk.Scrollbar(frame_profile, orient="vertical", command=canvas_profile.yview)
profile_display_frame = ttk.Frame(canvas_profile, padding=10); profile_display_frame.bind("<Configure>", lambda e: canvas_profile.configure(scrollregion=canvas_profile.bbox("all")))
canvas_profile.create_window((0, 0), window=profile_display_frame, anchor="nw", width=600); canvas_profile.configure(yscrollcommand=scrollbar_profile.set)
canvas_profile.pack(side="left", fill="both", expand=True); scrollbar_profile.pack(side="right", fill="y")

# --- Finalize ---
notebook.pack(expand=True, fill='both', padx=10, pady=10)
update_all_dynamic_displays()
root.mainloop()
save_user_data()