import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.simpledialog import askstring

user_credentials = {"admin": "password"}
items = {
    "Levis": {"price": "$39", "product": "Pants", "style": "Daily"},
    "Van Heusen": {"price": "$89", "product": "Shirts", "style": "Party"},
    "Arrow": {"price": "$59", "product": "Shirts", "style": "Daily"},
    "Pepe Jeans": {"price": "$79", "product": "Pants", "style": "Party"}
}

def display_products(items_list):
    result_text_products.config(state=tk.NORMAL)
    result_text_products.delete(1.0, tk.END)
    for item in items_list:
        result_text_products.insert(tk.END, f"{item} - Price: {items[item]['price']}\n")
    result_text_products.config(state=tk.DISABLED)

def search():
    query = entry_search.get().capitalize()
    result_text.delete(1.0, tk.END)
    matching_varieties = [variety for variety, data in items.items() if query == data.get("product", "").capitalize()]
    
    if matching_varieties:
        result_text.insert(tk.END, f"Search results for product '{query}':\n\n")
        display_products_as_buttons(matching_varieties)
        notebook.select(frame_products)
    else:
        result_text.insert(tk.END, f"No varieties found for product '{query}'")

def login():
    username = entry_login_username.get()
    password = entry_login_password.get()

    if username in user_credentials and user_credentials[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        notebook.select(frame_search)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def apply_style_filter():
    query = product_var.get()
    style = style_var.get()

    matching_varieties = [variety for variety, data in items.items() if
                          (query == data.get("product", "").capitalize() and style == data.get("style", "").capitalize())]

    print("Before clearing:", result_text_products.get("1.0", tk.END))  # Check current content before deletion

    # Clear previous search results
    result_text_products.config(state=tk.NORMAL)
    result_text_products.delete("1.0", tk.END)
    
    print("After clearing:", result_text_products.get("1.0", tk.END))  # Check content after deletion

    if matching_varieties:
        result_text_products.insert(tk.END, f"Filtered by '{query}' and '{style}':\n\n")
        display_products_as_buttons(matching_varieties)
        notebook.select(frame_products)
    else:
        result_text_products.insert(tk.END, f"No items found for '{query}' and '{style}'")
    result_text_products.config(state=tk.DISABLED)


def apply_coupon():
    coupon_code = entry_coupon.get()
    if coupon_code == "DISCOUNT20":
        messagebox.showinfo("Coupon Applied", "Coupon code applied successfully! You get a 20% discount.")
    else:
        messagebox.showerror("Invalid Coupon", "Invalid coupon code. Please enter a valid coupon.")

def submit_signup():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()

    if not username or not password or not email:
        messagebox.showerror("Error", "All fields must be filled")
        return

    user_credentials[username] = password

    message = f"Sign-up successful!\nUsername: {username}\nPassword: {password}\nEmail: {email}"
    messagebox.showinfo("Success", message)

    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def open_review_dialog():
    # Prompt user to enter a review using a dialog box
    review_text = askstring("Write a Review", "Enter your review:")
    if review_text:
        # Process the review_text as needed
        messagebox.showinfo("Review Submitted", "Your review has been submitted!")

selected_products = []

def display_shopping_cart():
    global result_text_cart
    result_text_cart.delete(1.0, tk.END)
    total_price = 0
    
    for item in selected_products:
        result_text_cart.insert(tk.END, f"{item} - Price: {items[item]['price']}\n")
        # Extracting numerical values from price strings and summing them
        price = int(items[item]['price'].replace('$', ''))
        total_price += price
        
    result_text_cart.insert(tk.END, f"Total Price: ${total_price}\n")

def add_to_cart(item):
    global selected_products
    selected_products.append(item)
    display_shopping_cart()

def switch_to_target_tab(item, target_tab):
    add_to_cart(item)
    print(f"Clicked on {item} in {target_tab}")

def add_product_to_cart(product):
    selected_products.append(product)
    display_shopping_cart()

def display_products_as_buttons(items_list):
    global result_text_products
    result_text_products.delete(1.0, tk.END)
    
    if items_list:
        for item in items_list:
            btn = tk.Button(
                result_text_products,
                text=f"{item} - Price: {items[item]['price']}",
                command=lambda item=item: add_product_to_cart(item)
            )
            btn.pack()
        
        go_to_cart_btn = tk.Button(result_text_products, text="Go to Cart", command=lambda: notebook.select(frame_cart))
        go_to_cart_btn.pack()
    else:
        result_text_products.insert(tk.END, "No matching items found.")

def display_checkout():
    result_text_checkout.delete(1.0, tk.END)
    total_price = 0
    for item in selected_products:
        result_text_checkout.insert(tk.END, f"{item} - Price: {items[item]['price']}\n")
        # Extracting numerical values from price strings and summing them
        price = int(items[item]['price'].replace('$', ''))
        total_price += price
        
    result_text_checkout.insert(tk.END, f"\nTotal Price: ${total_price}\n")

def show_checkout():
    notebook.select(frame_checkout)
    display_checkout()

def proceed_to_payments():
    notebook.select(frame_payments)

def display_payments():
    payment_method = payment_var.get()
    result_text_payments.config(state=tk.NORMAL)
    result_text_payments.delete(1.0, tk.END)
    result_text_payments.insert(tk.END, f"Selected Payment Method: {payment_method}")
    result_text_payments.config(state=tk.DISABLEED)

def redirect():
    messagebox.showinfo("Redirecting", "Redirecting to payment gateway...")
        
root = tk.Tk()
root.title("MarketPlace Express")

notebook = ttk.Notebook(root)

frame_signup = tk.Frame(notebook)
frame_login = tk.Frame(notebook)
frame_search = tk.Frame(notebook)
frame_products = tk.Frame(notebook)
frame_filter = tk.Frame(notebook)
frame_coupons = tk.Frame(notebook)
frame_reviews = tk.Frame(notebook)
frame_cart = tk.Frame(notebook)
frame_payments = tk.Frame(notebook)

label_username = tk.Label(frame_signup, text="Username:")
label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entry_username = tk.Entry(frame_signup)
entry_username.grid(row=0, column=1, padx=10, pady=10)

label_password = tk.Label(frame_signup, text="Password:")
label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_password = tk.Entry(frame_signup, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

label_email = tk.Label(frame_signup, text="Email:")
label_email.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
entry_email = tk.Entry(frame_signup)
entry_email.grid(row=2, column=1, padx=10, pady=10)

submit_button = tk.Button(frame_signup, text="Submit", command=submit_signup)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

label_login_username = tk.Label(frame_login, text="Username:")
label_login_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entry_login_username = tk.Entry(frame_login)
entry_login_username.grid(row=0, column=1, padx=10, pady=10)

label_login_password = tk.Label(frame_login, text="Password:")
label_login_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_login_password = tk.Entry(frame_login, show="*")
entry_login_password.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(frame_login, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

label_search = tk.Label(frame_search, text="Enter product:")
label_search.pack(pady=10)
entry_search = tk.Entry(frame_search)
entry_search.pack(pady=10)

btn_search = tk.Button(frame_search, text="Search", command=search)
btn_search.pack(pady=10)

result_text = tk.Text(frame_search, height=10, width=40)
result_text.pack()

result_text_products = tk.Text(frame_products, height=10, width=40)
result_text_products.pack()

product_label = tk.Label(frame_filter, text="Select Product:")
product_label.pack(pady=5)

product_var = tk.StringVar()
product_dropdown = ttk.Combobox(frame_filter, textvariable=product_var, values=list(set(item['product'] for item in items.values())))
product_dropdown.pack()

style_label = tk.Label(frame_filter, text="Select Style:")
style_label.pack(pady=5)

style_var = tk.StringVar()
style_dropdown = ttk.Combobox(frame_filter, textvariable=style_var, values=list(set(item['style'] for item in items.values())))
style_dropdown.pack()

apply_filter_btn = tk.Button(frame_filter, text="Apply Filter", command=apply_style_filter)
apply_filter_btn.pack(pady=10)

label_coupon = tk.Label(frame_coupons, text="Enter Coupon Code:")
label_coupon.pack(pady=10)
entry_coupon = tk.Entry(frame_coupons)
entry_coupon.pack(pady=5)

btn_apply_coupon = tk.Button(frame_coupons, text="Apply Coupon", command=apply_coupon)
btn_apply_coupon.pack(pady=10)

# Reviews Frame
frame_reviews = tk.Frame(notebook)
label_reviews = tk.Label(frame_reviews, text="Reviews")
label_reviews.pack()

# Reviews Frame
frame_reviews = tk.Frame(notebook)
label_reviews = tk.Label(frame_reviews, text="Reviews")
label_reviews.pack()

# Button to open the Review dialog
btn_open_review_dialog = tk.Button(frame_reviews, text="Write a Review", command=open_review_dialog)
btn_open_review_dialog.pack()

label_cart = tk.Label(frame_cart, text="Shopping Cart:")
label_cart.pack(pady=10)

result_text_cart = tk.Text(frame_cart, height=10, width=40)
result_text_cart.pack()
btn_checkout = tk.Button(frame_cart, text="Proceed to Checkout", command=show_checkout)
btn_checkout.pack()

frame_checkout = tk.Frame(notebook)
label_checkout = tk.Label(frame_checkout, text="Checkout")
label_checkout.pack()

result_text_checkout = tk.Text(frame_checkout, height=10, width=40)
result_text_checkout.pack()

proceed_to_payments_btn = tk.Button(frame_checkout, text="Proceed to Payments", command=proceed_to_payments)
proceed_to_payments_btn.pack()

payment_label = tk.Label(frame_payments, text="Select Payment Method:")
payment_label.pack(pady=5)

payment_var = tk.StringVar()
payment_dropdown = ttk.Combobox(frame_payments, textvariable=payment_var, values=["Cash", "Card", "UPI"])
payment_dropdown.pack()

result_text_payments = tk.Text(frame_payments, height=5, width=40)
result_text_payments.pack()

enter_payment_btn = tk.Button(frame_payments, text="Proceed to Pay", command=redirect)
enter_payment_btn.pack(pady=10)

frame_colors = {
    "frame_signup": "#FFD700",    # Gold
    "frame_login": "#00BFFF",     # Deep Sky Blue
    "frame_search": "#90EE90",    # Light Green
    "frame_products": "#FF6347",  # Tomato
    "frame_filter": "#BA55D3",    # Medium Orchid
    "frame_coupons": "#FFA07A",   # Light Salmon
    "frame_reviews": "#87CEEB",   # Sky Blue
    "frame_cart": "#FFE4C4",      # Bisque
    "frame_checkout": "#00CED1",  # Dark Turquoise
    "frame_payments": "#FFD700"   # Gold (same as frame_signup for example)
}

style = ttk.Style()
style.configure("TNotebook", padding=100 , background="#F0F0F0",  # Background color of the tabs
                tabposition="n",      # Position of the tabs (north)
                ) 

style.configure("TNotebook.Tab",
                background="#D3D3D3",
                foreground="#000000",  # Text color of individual tabs
                font=("Helvetica", 10, "bold"),  # Font of the tab text
                )

for frame_name, color in frame_colors.items():
    frame_name = globals()[frame_name]  # Access the frame widget by its name
    frame_name.configure(bg=color)

notebook.add(frame_signup, text='Sign Up')
notebook.add(frame_login, text='Login')
notebook.add(frame_search, text='Search')
notebook.add(frame_products, text='Products')
notebook.add(frame_filter, text='Filter')
notebook.add(frame_coupons, text='Coupons')
notebook.add(frame_reviews, text='Reviews')
notebook.add(frame_cart, text='Shopping Cart')
notebook.add(frame_checkout, text='Checkout')
notebook.add(frame_payments, text='Payments')

notebook.pack()

root.mainloop()


import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter.simpledialog import askstring

user_credentials = {"admin": "password"}
items = {
    "Levis": {"price": "$39", "product": "Pants", "style": "Daily"},
    "Van Heusen": {"price": "$89", "product": "Shirts", "style": "Party"},
    "Arrow": {"price": "$59", "product": "Shirts", "style": "Daily"},
    "Pepe Jeans": {"price": "$79", "product": "Pants", "style": "Party"}
}

def display_products(items_list):
    result_text_products.config(state=tk.NORMAL)
    result_text_products.delete(1.0, tk.END)
    for item in items_list:
        result_text_products.insert(tk.END, f"{item} - Price: {items[item]['price']}\n")
    result_text_products.config(state=tk.DISABLED)

def search():
    query = entry_search.get().capitalize()
    result_text.delete(1.0, tk.END)
    matching_varieties = [variety for variety, data in items.items() if query == data.get("product", "").capitalize()]
    
    if matching_varieties:
        result_text.insert(tk.END, f"Search results for product '{query}':\n\n")
        display_products_as_buttons(matching_varieties)
        notebook.select(frame_products)
    else:
        result_text.insert(tk.END, f"No varieties found for product '{query}'")

def login():
    username = entry_login_username.get()
    password = entry_login_password.get()

    if username in user_credentials and user_credentials[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome, {username}!")
        notebook.select(frame_search)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def apply_style_filter():
    query = product_var.get()
    style = style_var.get()

    matching_varieties = [variety for variety, data in items.items() if
                          (query == data.get("product", "").capitalize() and style == data.get("style", "").capitalize())]

    print("Before clearing:", result_text_products.get("1.0", tk.END))  # Check current content before deletion

    # Clear previous search results
    result_text_products.config(state=tk.NORMAL)
    result_text_products.delete("1.0", tk.END)
    
    print("After clearing:", result_text_products.get("1.0", tk.END))  # Check content after deletion

    if matching_varieties:
        result_text_products.insert(tk.END, f"Filtered by '{query}' and '{style}':\n\n")
        display_products_as_buttons(matching_varieties)
        notebook.select(frame_products)
    else:
        result_text_products.insert(tk.END, f"No items found for '{query}' and '{style}'")
    result_text_products.config(state=tk.DISABLED)


def apply_coupon():
    coupon_code = entry_coupon.get()
    if coupon_code == "DISCOUNT20":
        messagebox.showinfo("Coupon Applied", "Coupon code applied successfully! You get a 20% discount.")
    else:
        messagebox.showerror("Invalid Coupon", "Invalid coupon code. Please enter a valid coupon.")

def submit_signup():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()

    if not username or not password or not email:
        messagebox.showerror("Error", "All fields must be filled")
        return

    user_credentials[username] = password

    message = f"Sign-up successful!\nUsername: {username}\nPassword: {password}\nEmail: {email}"
    messagebox.showinfo("Success", message)

    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_email.delete(0, tk.END)

def open_review_dialog():
    # Prompt user to enter a review using a dialog box
    review_text = askstring("Write a Review", "Enter your review:")
    if review_text:
        # Process the review_text as needed
        messagebox.showinfo("Review Submitted", "Your review has been submitted!")

selected_products = []

def display_shopping_cart():
    global result_text_cart
    result_text_cart.delete(1.0, tk.END)
    total_price = 0
    
    for item in selected_products:
        result_text_cart.insert(tk.END, f"{item} - Price: {items[item]['price']}\n")
        # Extracting numerical values from price strings and summing them
        price = int(items[item]['price'].replace('$', ''))
        total_price += price
        
    result_text_cart.insert(tk.END, f"Total Price: ${total_price}\n")

def add_to_cart(item):
    global selected_products
    selected_products.append(item)
    display_shopping_cart()

def switch_to_target_tab(item, target_tab):
    add_to_cart(item)
    print(f"Clicked on {item} in {target_tab}")

def add_product_to_cart(product):
    selected_products.append(product)
    display_shopping_cart()

def display_products_as_buttons(items_list):
    global result_text_products
    result_text_products.delete(1.0, tk.END)
    
    if items_list:
        for item in items_list:
            btn = tk.Button(
                result_text_products,
                text=f"{item} - Price: {items[item]['price']}",
                command=lambda item=item: add_product_to_cart(item)
            )
            btn.pack()
        
        go_to_cart_btn = tk.Button(result_text_products, text="Go to Cart", command=lambda: notebook.select(frame_cart))
        go_to_cart_btn.pack()
    else:
        result_text_products.insert(tk.END, "No matching items found.")

def display_checkout():
    result_text_checkout.delete(1.0, tk.END)
    total_price = 0
    for item in selected_products:
        result_text_checkout.insert(tk.END, f"{item} - Price: {items[item]['price']}\n")
        # Extracting numerical values from price strings and summing them
        price = int(items[item]['price'].replace('$', ''))
        total_price += price
        
    result_text_checkout.insert(tk.END, f"\nTotal Price: ${total_price}\n")

def show_checkout():
    notebook.select(frame_checkout)
    display_checkout()

def proceed_to_payments():
    notebook.select(frame_payments)

def display_payments():
    payment_method = payment_var.get()
    result_text_payments.config(state=tk.NORMAL)
    result_text_payments.delete(1.0, tk.END)
    result_text_payments.insert(tk.END, f"Selected Payment Method: {payment_method}")
    result_text_payments.config(state=tk.DISABLEED)

def redirect():
    messagebox.showinfo("Redirecting", "Redirecting to payment gateway...")
        
root = tk.Tk()
root.title("MarketPlace Express")

notebook = ttk.Notebook(root)

frame_signup = tk.Frame(notebook)
frame_login = tk.Frame(notebook)
frame_search = tk.Frame(notebook)
frame_products = tk.Frame(notebook)
frame_filter = tk.Frame(notebook)
frame_coupons = tk.Frame(notebook)
frame_reviews = tk.Frame(notebook)
frame_cart = tk.Frame(notebook)
frame_payments = tk.Frame(notebook)

label_username = tk.Label(frame_signup, text="Username:")
label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entry_username = tk.Entry(frame_signup)
entry_username.grid(row=0, column=1, padx=10, pady=10)

label_password = tk.Label(frame_signup, text="Password:")
label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_password = tk.Entry(frame_signup, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

label_email = tk.Label(frame_signup, text="Email:")
label_email.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
entry_email = tk.Entry(frame_signup)
entry_email.grid(row=2, column=1, padx=10, pady=10)

submit_button = tk.Button(frame_signup, text="Submit", command=submit_signup)
submit_button.grid(row=3, column=0, columnspan=2, pady=10)

label_login_username = tk.Label(frame_login, text="Username:")
label_login_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
entry_login_username = tk.Entry(frame_login)
entry_login_username.grid(row=0, column=1, padx=10, pady=10)

label_login_password = tk.Label(frame_login, text="Password:")
label_login_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_login_password = tk.Entry(frame_login, show="*")
entry_login_password.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(frame_login, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

label_search = tk.Label(frame_search, text="Enter product:")
label_search.pack(pady=10)
entry_search = tk.Entry(frame_search)
entry_search.pack(pady=10)

btn_search = tk.Button(frame_search, text="Search", command=search)
btn_search.pack(pady=10)

result_text = tk.Text(frame_search, height=10, width=40)
result_text.pack()

result_text_products = tk.Text(frame_products, height=10, width=40)
result_text_products.pack()

product_label = tk.Label(frame_filter, text="Select Product:")
product_label.pack(pady=5)

product_var = tk.StringVar()
product_dropdown = ttk.Combobox(frame_filter, textvariable=product_var, values=list(set(item['product'] for item in items.values())))
product_dropdown.pack()

style_label = tk.Label(frame_filter, text="Select Style:")
style_label.pack(pady=5)

style_var = tk.StringVar()
style_dropdown = ttk.Combobox(frame_filter, textvariable=style_var, values=list(set(item['style'] for item in items.values())))
style_dropdown.pack()

apply_filter_btn = tk.Button(frame_filter, text="Apply Filter", command=apply_style_filter)
apply_filter_btn.pack(pady=10)

label_coupon = tk.Label(frame_coupons, text="Enter Coupon Code:")
label_coupon.pack(pady=10)
entry_coupon = tk.Entry(frame_coupons)
entry_coupon.pack(pady=5)

btn_apply_coupon = tk.Button(frame_coupons, text="Apply Coupon", command=apply_coupon)
btn_apply_coupon.pack(pady=10)

# Reviews Frame
frame_reviews = tk.Frame(notebook)
label_reviews = tk.Label(frame_reviews, text="Reviews")
label_reviews.pack()

# Reviews Frame
frame_reviews = tk.Frame(notebook)
label_reviews = tk.Label(frame_reviews, text="Reviews")
label_reviews.pack()

# Button to open the Review dialog
btn_open_review_dialog = tk.Button(frame_reviews, text="Write a Review", command=open_review_dialog)
btn_open_review_dialog.pack()

label_cart = tk.Label(frame_cart, text="Shopping Cart:")
label_cart.pack(pady=10)

result_text_cart = tk.Text(frame_cart, height=10, width=40)
result_text_cart.pack()
btn_checkout = tk.Button(frame_cart, text="Proceed to Checkout", command=show_checkout)
btn_checkout.pack()

frame_checkout = tk.Frame(notebook)
label_checkout = tk.Label(frame_checkout, text="Checkout")
label_checkout.pack()

result_text_checkout = tk.Text(frame_checkout, height=10, width=40)
result_text_checkout.pack()

proceed_to_payments_btn = tk.Button(frame_checkout, text="Proceed to Payments", command=proceed_to_payments)
proceed_to_payments_btn.pack()

payment_label = tk.Label(frame_payments, text="Select Payment Method:")
payment_label.pack(pady=5)

payment_var = tk.StringVar()
payment_dropdown = ttk.Combobox(frame_payments, textvariable=payment_var, values=["Cash", "Card", "UPI"])
payment_dropdown.pack()

result_text_payments = tk.Text(frame_payments, height=5, width=40)
result_text_payments.pack()

enter_payment_btn = tk.Button(frame_payments, text="Proceed to Pay", command=redirect)
enter_payment_btn.pack(pady=10)

frame_colors = {
    "frame_signup": "#FFD700",    # Gold
    "frame_login": "#00BFFF",     # Deep Sky Blue
    "frame_search": "#90EE90",    # Light Green
    "frame_products": "#FF6347",  # Tomato
    "frame_filter": "#BA55D3",    # Medium Orchid
    "frame_coupons": "#FFA07A",   # Light Salmon
    "frame_reviews": "#87CEEB",   # Sky Blue
    "frame_cart": "#FFE4C4",      # Bisque
    "frame_checkout": "#00CED1",  # Dark Turquoise
    "frame_payments": "#FFD700"   # Gold (same as frame_signup for example)
}

style = ttk.Style()
style.configure("TNotebook", padding=100 , background="#F0F0F0",  # Background color of the tabs
                tabposition="n",      # Position of the tabs (north)
                ) 

style.configure("TNotebook.Tab",
                background="#D3D3D3",
                foreground="#000000",  # Text color of individual tabs
                font=("Helvetica", 10, "bold"),  # Font of the tab text
                )

for frame_name, color in frame_colors.items():
    frame_name = globals()[frame_name]  # Access the frame widget by its name
    frame_name.configure(bg=color)

notebook.add(frame_signup, text='Sign Up')
notebook.add(frame_login, text='Login')
notebook.add(frame_search, text='Search')
notebook.add(frame_products, text='Products')
notebook.add(frame_filter, text='Filter')
notebook.add(frame_coupons, text='Coupons')
notebook.add(frame_reviews, text='Reviews')
notebook.add(frame_cart, text='Shopping Cart')
notebook.add(frame_checkout, text='Checkout')
notebook.add(frame_payments, text='Payments')

notebook.pack()

root.mainloop()
