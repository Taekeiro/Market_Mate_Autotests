# Market Mate Test Automation

Automated end-to-end test suite for the Grocery Mate demo site (https://grocerymate.masterschool.com) using Python, Selenium WebDriver and pytest, organized with the Page Object Model.

---

## 📁 Project Structure

```
Market_Mate_Autotests/
├── pages/                    # Page Object classes
│   ├── base_page.py
│   ├── login_page.py
│   ├── store_page.py
│   ├── cart_page.py
│   └── rating_page.py
│
├── tests/                    # pytest test modules
│   ├── test_age_verification.py
│   ├── test_age_modal_state_transition.py
│   ├── test_cart_feature.py
│   ├── test_free_shipping.py
│   └── test_rating.py
│
├── utils/                    # helper modules
│   ├── constants.py          # base URLs, credentials, thresholds
│   └── checkout.py           # reusable checkout function
│
├── conftest.py               # pytest fixtures (webdriver setup/teardown)
├── requirements.txt          # Python dependencies
└── README.md                 # project overview and instructions
```

---

## 🛠 Prerequisites

- Python 3.8+  
- Google Chrome browser  
- [ChromeDriver](https://chromedriver.chromium.org/) matching your Chrome version, available in your `PATH`  
- (Optional) `virtualenv` or `venv` for isolated environment

---

## 🚀 Installation

1. **Clone the repo**  
   ```
   git clone https://github.com/Taekeiro/Market_Mate_Autotests.git
   cd Market_Mate_Autotests
   ```

2. **Create & activate virtual environment**  
   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**  
   ```
   pip install -r requirements.txt
   ```

---

## ⚙ Configuration

1. In `utils/constants.py`, fill in the valid and invalid user credentials, e.g.:

   ```python
   BASE_URL            = "https://grocerymate.masterschool.com"
   PRODUCT_PAGE_URL    = f"{BASE_URL}/store"
   VALID_USER   = {"email": "testuser@example.com", "password": "Test@123"}
   INVALID_USER = {"email": "invalid@example.com", "password": "wrongpass"}
   FREE_SHIPPING_THRESHOLD = 20.00
   ```

2. Ensure `chromedriver` is on your `PATH`, or specify its location in your `conftest.py` if needed.

---

## ▶️ Running the Tests

From the project root:

```bash
pytest -v --maxfail=1
```

- `-v` for verbose output  
- `--maxfail=1` stops after the first failure  

You can also run a single test module:

```bash
pytest tests/test_cart_feature.py -v
```

Or a single test by name:

```bash
pytest -k "test_submit_invalid_rating" -v
```

---

## ✅ What’s Covered

1. **Age Verification** (valid, underage, state-transition across new tab)  
2. **Cart Features** (clear cart, add single item, add multiple quantities)  
3. **Dynamic Shipping Costs** (free vs. below-threshold)  
4. **Add to Cart Popup** (positive & known-bug negative)  
5. **Product Rating System** (submit, invalid-rating error, edit, delete)

---

## 🤝 Contributing

1. Fork the repository  
2. Create a feature branch: `git checkout -b feature/YourFeature`  
3. Commit your changes: `git commit -m "Add awesome feature"`  
4. Push to your fork: `git push origin feature/YourFeature`  
5. Open a Pull Request

Please follow the existing Page Object Model structure and add new locators & methods in the `pages/` package, and tests under `tests/`.

---

## 📄 License

This project is provided for educational purposes under the MIT License. See `LICENSE` for details.
