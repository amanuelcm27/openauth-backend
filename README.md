# OpenAuth Backend (MFA Core)

OpenAuth Backend is the **open-source Multi-Factor Authentication (MFA) engine** that powers the OpenAuth SDK and UI kits.

It provides secure, extensible MFA flows such as **TOTP (Authenticator Apps)** and **Email OTP**, and is designed to support additional MFA methods like **SMS**, **push-based verification**, **passkeys (WebAuthn)**, and **biometric authentication** in the future.

This repository contains the **authentication logic and API layer**, not the hosted SaaS infrastructure.

---

## ✨ Features

* 🔐 Secure MFA engine built with Django & Django REST Framework
* 🔑 App-level authentication using `X-App-Secret`
* ⏱️ Time-based One-Time Passwords (TOTP)
* 📧 Email OTP verification
* 🧩 Designed for extensibility (add new MFA methods)
* 📦 Powers the OpenAuth SDK & UI kits
* 🧪 Deterministic, testable business logic

---

## 🧠 Architecture Overview

This backend acts as a **headless MFA service**.

```text
Developer App
   │
   │  (X-App-Secret)
   ▼
OpenAuth Backend API
   │
   ├── TOTP (Authenticator Apps)
   ├── Email OTP
   └── Future MFA Providers
```

Client applications **never** interact with this API directly.

Instead, they use:

* **OpenAuth SDK** – typed API wrapper
* **OpenAuth UI** – ready-made MFA screens (React Native / Expo)

---

## 🔗 Related Repositories

* **frontend sdk and cli client** : https://github.com/amanuelcm27/openauth-frontend/
* **Frontend SDK**

  * ``` npm install @openauthdev/sdk ```
  * Provides typed JavaScript/TypeScript access to this API

* **UI Kits**

  * ``` npm install @openauthdev/ui ```
  * Optional plug-and-play MFA screens for mobile apps

---

## 🔐 Security Model

### App Authentication

All requests are authenticated using an **App Secret**:

```
X-App-Secret: <your_app_secret>
```

This ensures:

* Only registered developer apps can access the API
* MFA data is isolated per developer app

### User Identity

Users are identified by:

```
external_user_id
```

This is **your own user ID**, not managed by OpenAuth.

---

## 🧩 Supported MFA Methods


### ✅ TOTP (Authenticator Apps)

* Google Authenticator
* Authy
* Microsoft Authenticator
* Any RFC 6238–compatible app

**Flow:**

    1. Generate secret
    2. Show QR code
    3. Verify 6-digit code

---

### ✅ Email OTP

* 6-digit OTP
* SHA-256 hashed storage
* Expiry enforced
* One-time use

**Flow:**

    1. Register email
    2. Send OTP
    3. Verify OTP

---

## 📡 API Endpoints (Summary)
### Developer Registration and App creation

* `POST /developer/register/`
* `POST /developer/create_app/`


### TOTP

* `POST /mfa/totp/setup/`
* `POST /mfa/totp/verify/`

### Email OTP

* `POST /mfa/email/setup/`
* `POST /mfa/email/send/`
* `POST /mfa/email/verify/`

### Status

* `GET /mfa/status/`

> Full request/response shapes are documented in the SDK.

---

## ⚙️ Local Development

### Requirements

* Python 3.10+
* Django
* Django REST Framework
* PostgreSQL or SQLite (for development)

---

### Installation

```bash
git clone https://github.com/amanuelcm27/openauth-backend.git
cd openauth-backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your-django-secret
DEBUG=true
DEFAULT_FROM_EMAIL=no-reply@openauth.dev
EMAIL_HOST=...
EMAIL_PORT=...
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
```

> No secrets are committed to this repository.

---

### Run the Server

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🧩 Extending OpenAuth (Adding New MFA Methods)

OpenAuth is designed to be **extended**.

You can contribute new MFA methods such as:

* SMS OTP
* Push notifications
* Backup codes
* Passkeys / WebAuthn
* Biometric verification

Each MFA method typically includes:

* Model(s)
* Setup endpoint
* Verification endpoint
* Expiry & replay protection
* Tests

See `CONTRIBUTING.md` for full guidelines.

---

## 🤝 Contributing

We welcome contributions!

Please read **CONTRIBUTING.md** before submitting a pull request.

### You can contribute:

* New MFA methods
* Security improvements
* Bug fixes
* Documentation


---

## 📄 License

MIT License

This project is licensed under the [MIT License](LICENSE.md) - see the LICENSE.md file for details.

---

