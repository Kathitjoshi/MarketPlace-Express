# 🛒 MarketPlace Express

**A feature-rich desktop e-commerce application built with Python & Tkinter.**

This project simulates a complete shopping experience, from user sign-up to viewing order history. It's designed to be a comprehensive example for anyone learning GUI development, data persistence, and application structure in Python.

![Language](https://img.shields.io/badge/Language-Python-blue?style=for-the-badge&logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ✨ Features

### 👤 Complete User Authentication System
- **User Sign-Up:** Securely create new accounts with username, password, and email validation
- **Login & Logout:** Full session management system for users
- **Persistent Profiles:** User data (credentials, wishlist, orders) saved to local `users.json` file

### 🛍️ Dynamic Product Catalog
- **Product Browsing:** View items in a clean, scrollable list of cards
- **Live Search:** Instantly find products by typing in the search bar
- **Advanced Filtering:** Narrow down products by category (e.g., "Pants", "Shirts") and style (e.g., "Daily", "Party")

### 💳 Full Shopping & Checkout Workflow
- **Shopping Cart:** Add/remove items, view quantities, and see running subtotal
- **Wishlist:** Save items you're interested in to your personal profile
- **Functional Coupon System:** Apply `DISCOUNT20` coupon for real 20% discount
- **Order History:** All completed purchases stored and viewable in user profile

### 🎨 Modern & Responsive UI
- **Tabbed Navigation:** Cleanly organized sections (Home, Products, Cart, Profile)
- **Themed Widgets:** Modern `ttk` widgets for professional cross-platform appearance
- **Dynamic Updates:** UI intelligently refreshes on login, cart updates, or purchases

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Git (for cloning the repository)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Kathitjoshi/MarketPlace-Express.git
   cd MarketPlace-Express
   ```

2. **Create a Virtual Environment** (Recommended)
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS & Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   > **Note:** `tkinter` is usually included with Python installations and doesn't need separate installation.

4. **Verify Image Files**
   
   Ensure the `images/` directory exists in the project root and contains:
   - `arrow_shirt.png`
   - `levis_pants.png`
   - `pepe_jeans_pants.png`
   - `vanheusen_shirt.png`

5. **Run the Application**
   ```bash
   python Python_proj_1stsem.py
   ```

## 📖 Usage Guide

Follow this typical user journey:

1. **Launch** the application - you'll land on the Home screen
2. Navigate to **Sign Up** tab and create a new account
3. Go to **Login** tab and sign in with your credentials
4. Head to **Products** tab to browse, search, and filter items
5. **Add items** to your Shopping Cart and Wishlist
6. Visit **Coupons** tab and apply `DISCOUNT20` for 20% off
7. View updated total in Shopping Cart and proceed to **Checkout**
8. **Confirm and Pay** to complete your purchase
9. Check your **Profile** tab to see order history and wishlist

## 🎯 Why This Project?

### 🎓 For Learners & Students
- **Complete Project Example:** Full application structure beyond simple scripts
- **Core Concepts Coverage:** GUI programming, state management, event handling, file I/O
- **Portfolio Ready:** Perfect showcase project for beginner-level developer positions

### 🛠️ For Hobbyists & Builders
- **Solid Foundation:** Great starting point for desktop application ideas
- **Easy to Extend:** Procedural structure makes adding features straightforward
- **Minimal Dependencies:** Runs on standard Python installation (highly portable)

## 🔧 Technical Stack

- **Language:** Python 3.7+
- **GUI Framework:** Tkinter with modern `ttk` themed widgets
- **Image Processing:** Pillow (PIL)
- **Data Storage:** JSON files for user data persistence
- **Additional Libraries:** `json`, `os`, `re` (all built-in)

### Project Structure
```
MarketPlace-Express/
├── Python_proj_1stsem.py    # Main application file
├── requirements.txt          # Python dependencies
├── users.json               # User data storage (created on first run)
├── images/                  # Product images directory
│   ├── arrow_shirt.png
│   ├── levis_pants.png
│   ├── pepe_jeans_pants.png
│   └── vanheusen_shirt.png
```

## 🗺️ Roadmap

Future enhancements planned:

- [ ] **Database Integration:** Migrate from JSON to SQLite for better data management
- [ ] **Admin Panel:** Separate interface for product catalog management
- [ ] **OOP Refactoring:** Convert to class-based architecture (`App`, `User`, `Product`)
- [ ] **Enhanced Product Details:** Add size, color, stock quantity attributes
- [ ] **Payment Integration:** Mock payment gateway simulation
- [ ] **Email Notifications:** Order confirmation emails
- [ ] **Multi-language Support:** Internationalization features

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/Kathitjoshi/MarketPlace-Express/issues).

### How to Contribute

1. **Fork** the Project
2. **Create** your Feature Branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** your Changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push** to the Branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open** a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comments for complex logic
- Test new features thoroughly
- Update documentation as needed

## 📝 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

## 👨‍💻 Author

**Kathit Joshi**
- GitHub: [@Kathitjoshi](https://github.com/Kathitjoshi)
- Project Link: [MarketPlace Express](https://github.com/Kathitjoshi/MarketPlace-Express)

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Inspired by modern e-commerce platforms
- Thanks to the open-source community

---

<div align="center">

**Built with ❤️ and Python**

⭐ **Star this repo if you found it helpful!** ⭐

</div>
