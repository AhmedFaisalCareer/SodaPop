# SodaPop 🥤

A colorful Streamlit soda-ordering app with a customer shop, drink customization, cart and checkout, order tracking, and an admin dashboard.

## Features
- Bright pink, orange, and cream design
- Shop landing page and searchable menu with product pictures
- Classic sodas, fruit fizz, sparkling lemonade, and signature flavours
- Custom sizes, ice levels, extra flavour shots, and quantities
- Shopping cart, delivery details, and checkout
- Cash on delivery or manual online-payment reference
- SQLite persistence for menu and orders
- Customer order tracking
- Admin dashboard with sales metrics, order status management, and menu editor

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install packages: `pip install -r requirements.txt`
4. Run: `streamlit run app.py`
5. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Admin password
For local development, the fallback password is `sodapop123`. The app no longer displays it on the login screen. For deployment, set a strong password in `.streamlit/secrets.toml`:

```toml
OWNER_PASSWORD = "replace-with-a-long-unique-password"
```

Alternatively, set an environment variable named `OWNER_PASSWORD`. Environment variables take priority. Do not commit secrets to a public repository.

## Payments
The online-payment option is a manual workflow only. It does not charge a card, verify a transfer, or process payments automatically. For real payments, integrate a supported payment provider and verify payment server-side. Never collect card numbers, PINs, passwords, or OTPs in this app.

## Database and hosting
Orders and menu items are stored in `sodapop.db` beside `app.py`. Back up this file regularly. Some hosts use temporary filesystems; production deployments should use persistent storage or a managed database.

## Notes
- Product pictures load from remote image URLs and require an internet connection.
- The fallback admin password is suitable only for local testing. Configure your own password before public deployment.
