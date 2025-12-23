
# Contributing to OpenAuth Backend

First off — thank you for considering contributing to **OpenAuth**
OpenAuth is a community-driven, extensible Multi-Factor Authentication (MFA) platform, and contributions of all kinds are welcome.

This document outlines how to contribute **code, ideas, and improvements** to the OpenAuth backend.

---

## 📌 Scope of This Repository

This repository contains the **core MFA backend**, built with:

* Django
* Django REST Framework
* Cryptographically secure OTP flows
* App-level authentication via `X-App-Secret`

This backend powers:

* `npm install @openauthdev/sdk`
* `npm install @openauthdev/ui`
* `npm install @openauthdev/cli`

Frontend SDKs and UI kits live in **separate repository** and have its own contribution guidelines.

---

## 🤝 Ways to Contribute

You can contribute by:

* Adding **new MFA methods**
* Improving **security or correctness**
* Fixing bugs
* Improving documentation
* Adding tests
* Reviewing pull requests
* Proposing architectural improvements

You **do not** need to contribute frontend code to contribute here.

---

## 🔐 MFA Methods We Actively Encourage

We especially welcome contributions for:

* SMS OTP
* Backup / recovery codes
* Push-based MFA
* WebAuthn / Passkeys
* Biometric-backed flows
* Rate limiting / abuse prevention
* Device trust & re-authentication strategies

If you are unsure whether your idea fits, open an issue first.

---

## 🧠 Design Principles

When contributing, please align with these principles:

  1. **Security first**
  2. **Stateless API design**
  3. **Backend-agnostic clients**
  4. **Explicit MFA setup and verification**
  5. **No user identity ownership**
    (OpenAuth uses `external_user_id`, never manages user accounts)

---

## 🏗️ Project Structure (High-Level)

```text
mfa/
 ├── models.py        # MFA-related models
 ├── views.py         # API endpoints
 ├── serializers.py  
developers/
 ├── models.py        # Developer Registration and app creation
 ├── views.py         # API endpoints
 ├── serializers.py  
```

Each MFA method should be:

* Isolated
* Explicit
* Testable
* Replay-safe

---

## 🧩 Adding a New MFA Method

A typical MFA contribution includes:

### 1. Models

* Store secrets securely
* Support expiry
* Prevent reuse

### 2. Setup Endpoint

* Registers MFA method for a user
* Attaches to a `Client`
* Validates developer app

### 3. Verification Endpoint

* Verifies proof (OTP, biometric assertion, etc.)
* Enforces expiry and one-time use
* Returns a clear success/failure response

### 4. Tests

* Expired credentials
* Invalid credentials
* Replay attempts

---

## 🔑 Authentication Rules

All endpoints **must**:

* Require `X-App-Secret`
* Scope data to `DeveloperApp`
* Never leak data across apps

Do **not**:

* Accept user credentials
* Store plaintext OTPs
* Trust client-side timestamps

---

## ⚙️ Local Development Setup

### Requirements

* Python 3.10+
* Django
* Django REST Framework
* SQLite (dev) or PostgreSQL

---

### Setup

```bash
git clone https://github.com/amanuelcm27/openauth-backend.git
cd openauth-backend

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🧪 Testing

All contributions **must include tests**.

Run tests with:

```bash
python manage.py test
```

If your PR adds a new MFA method, tests are mandatory.

---

## 📐 API Conventions

* JSON only
* Explicit error messages
* Proper HTTP status codes
* No silent failures

Example error response:

```json
{
  "success": false,
  "error": "Invalid or expired OTP"
}
```

---

## 🔒 Security Guidelines

* Never log secrets
* Hash OTPs before storage
* Enforce expiration
* Prevent replay attacks
* Avoid timing leaks where possible

If you find a **security vulnerability**, **do not open a public issue**.
Instead, contact the maintainer privately.

---

## 🧾 Commit & PR Guidelines

### Commits

* Use clear, descriptive messages
* Prefer small, focused commits

### Pull Requests

* One feature or fix per PR
* Include tests
* Reference related issues
* Explain **why**, not just **what**


---

## 📄 License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE.md).

---

