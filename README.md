# MarketPlace Express(Name of the appln)
# 🛒 MarketPlace Express

**A feature-rich desktop e-commerce application built with Python & Tkinter.**

This project simulates a complete shopping experience, from user sign-up to viewing order history. It's designed to be a comprehensive example for anyone learning GUI development, data persistence, and application structure in Python.

![Language](https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ✨ Features

### 👤 **Complete User Authentication System**
- **User Sign-Up:** Securely create new accounts with username, password, and email validation.
- **Login & Logout:** A full session management system for users.
- **Persistent Profiles:** User data (credentials, wishlist, orders) is saved to a local `users.json` file.

### 🛍️ **Dynamic Product Catalog**
- **Product Browsing:** View items in a clean, scrollable list of cards.
- **Live Search:** Instantly find products by typing in the search bar.
- **Advanced Filtering:** Narrow down the product list by category (e.g., "Pants", "Shirts") and style (e.g., "Daily", "Party").

### 💳 **Full Shopping & Checkout Workflow**
- **Shopping Cart:** Add/remove items, view quantities, and see a running subtotal.
- **Wishlist:** Save items you're interested in to your personal profile.
- **Functional Coupon System:** Apply the `DISCOUNT20` coupon to get a real 20% discount on your order.
- **Order History:** All completed purchases are stored and viewable in the user's profile, including order ID, date, items, and final price.

### 🎨 **Modern & Responsive UI**
- **Tabbed Navigation:** Cleanly organized into logical sections like Home, Products, Cart, and Profile.
- **Themed Widgets:** Uses modern `ttk` widgets for a professional look and feel across platforms.
- **Dynamic Updates:** The UI intelligently refreshes when you log in, add items to your cart, or make a purchase.

## ⚙️ Setup and Installation

Get the application running on your local machine in just a few steps.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Kathitjoshi/MarketPlace-Express
.git
    cd MarketPlace-Express

    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    # On Windows
    python -m venv venv
    .\venv\Scripts\activate

    # On macOS & Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    The only external library required besides tkinter(have it installed as well in VM env or locally) is `Pillow` for image handling.
    ```bash
    pip install Pillow
    ```


4.  **Run the Application**
    You're ready to go!
    ```bash
    python Python_proj_1stsem.py
    ```

## 📖 How to Use

Follow a typical user journey through the application:

1.  **Launch the app** and you'll land on the Home screen.
2.  Navigate to the **Sign Up** tab and create a new account.
3.  Go to the **Login** tab and sign in with your new credentials.
4.  Head to the **Products** tab. Browse, search, and filter items.
5.  **Add items** to your **Shopping Cart** and **Wishlist**.
6.  Go to the **Coupons** tab and apply `DISCOUNT20`.
7.  View the updated total in your **Shopping Cart** and proceed to the **Checkout** tab.
8.  **Confirm and Pay** to complete the purchase.
9.  Finally, visit your **Profile** tab to see your new purchase in the **Order History** and view your **Wishlist**.

## 🌟 Why This Project is Useful

### 🎓 **For Learners & Students**
- **Complete Project Example:** Goes beyond simple scripts to show how a full application is structured.
- **Covers Core Concepts:** Demonstrates GUI programming, state management, event handling, and file I/O (JSON).
- **Perfect Portfolio Piece:** An ideal project to showcase for first-semester or beginner-level developer roles.

### 🛠️ **For Hobbyists & Builders**
- **Solid Foundation:** A great starting point or template for your own desktop application ideas.
- **Easy to Extend:** The procedural structure makes it easy to add new features or modify existing ones.
- **No External Dependencies:** Besides Pillow, it runs on a standard Python installation, making it highly portable.

## 🛠️ Technical Details

- **Language**: Python 3
- **GUI Framework**: Tkinter, with a focus on the modern `ttk` themed widgets.
- **Libraries**: `Pillow` for image manipulation, `json` for data serialization, `os` for path management, and `re` for email validation.
- **Data Storage**: User data, wishlists, and order history are stored in a human-readable `users.json` file. This choice keeps the project simple and free of database dependencies.


## 🔮 Roadmap

Future enhancements could include:
- [ ] **Database Integration:** Migrating from `json` to a more robust database like `SQLite`.
- [ ] **Admin Panel:** A separate view for an admin to add, edit, or remove products from the catalog.
- [ ] **OOP Refactoring:** Restructuring the code into classes (e.g., `App`, `User`, `Product`) for better scalability and maintenance.
- [ ] **Enhanced Product Details:** Adding more product attributes like size, color, and stock quantity.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Kathitjoshi/MarketPlace-Express
/issues).

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information. (You can create a `LICENSE` file with the MIT license text if you wish).

## 👨‍💻 Author

-   **Kathitjoshi** - [https://github.com/Kathitjoshi]

---

**Built with ❤️ and Python. Happy coding!**


