# 🔐 ShareVault - Secure File Sharing API

Welcome to **ShareVault**, a secure and efficient file-sharing service built using **FastAPI**, **MongoDB**, and **JWT Authentication**. Upload, share, and track downloads of your files with temporary, one-time-use access codes.

---

## 🚀 Features

- ✅ User Registration & JWT-based Login
- 🔐 Authenticated File Upload
- 🧾 Auto-generated Download Codes
- ⏳ Expiry Timer for Files
- ♻️ Auto-cleanup for Expired Files (via Scheduler)
- 📦 MongoDB Integration with Async I/O
- 📊 View Uploaded File Stats
- 🔓 Public Download Route (no login required)
- ⚙️ Organized Modular Architecture

---

## 🛠️ Tech Stack

| Tool         | Usage                          |
|--------------|--------------------------------|
| FastAPI      | Backend API framework          |
| MongoDB      | NoSQL database (Motor async)   |
| JWT (PyJWT)  | Token-based authentication     |
| APScheduler  | Background job scheduling      |
| Pydantic     | Data validation & schemas      |

---

## 📦 Setup Instructions

### 🔧 Requirements

- Python 3.10+
- MongoDB instance (local or Atlas)

### 📥 Installation

---
```bash
# Clone the repo
git clone https://github.com/kashifkhanai/sharevault.git
cd sharevault-api

# Setup virtual environment
python -m venv env
source env/bin/activate  

# Install dependencies
pip install -r requirements.txt

---
