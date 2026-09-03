# Cognixia Bank Management System

A full-stack banking management dashboard designed for managing customers, their accounts, and financial transactions.

## 🚀 Overview

This application provides an administrative interface for a banking institution. It allows for:
- **Customer Management**: View and manage customer profiles.
- **Account Management**: Track different account types (Savings, Checking) and their balances.
- **Transaction Ledger**: Monitor real-time transfers, deposits, and withdrawals with atomic consistency.

### Tech Stack
- **Frontend**: React, TypeScript, Vite, CSS3
- **Backend**: FastAPI (Python), Pydantic
- **Database**: MongoDB
- **Communication**: REST API with Vite Proxy configuration

---

## 🛠️ Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+**
- **Node.js (v18+)** and **npm**
- **MongoDB** (Running locally or via a cloud provider like MongoDB Atlas)

---

## 📦 Installation & Setup

### 1. Backend Setup (FastAPI)

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  (Optional but recommended) Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install fastapi uvicorn pymongo python-dotenv
    ```

4.  Configure environment variables:
    Create a `.env` file in the `backend/` folder and add your MongoDB connection string:
    ```env
    MONGO_URI=mongodb://localhost:27017
    ```

5.  Start the backend server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`. You can access the interactive Swagger documentation at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup (React)

1.  Open a new terminal window and navigate to the `frontend` directory:
    ```bash
    cd frontend
    ```

2.  Install the project dependencies:
    ```bash
    npm install
    ```

3.  Start the development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at the URL shown in your terminal (usually `http://localhost:5173`).

---

## 🚦 Running the Project

To run the full application:
1.  Ensure **MongoDB** is running.
2.  Start the **Backend** server.
3.  Start the **Frontend** development server.
4.  Open your browser to the **Frontend** URL.

## 🛣️ API Endpoints

The backend exposes several RESTful endpoints:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/v1/customers` | `GET` | List all active customers |
| `/api/v1/accounts` | `GET` | List all accounts |
| `/api/v1/accounts` | `POST` | Create a new account |
| `/api/v1/transactions` | `GET` | List all transactions |
| `/api/v1/transactions/transfer` | `POST` | Perform an atomic transfer between accounts |

---

## 📂 Project Structure

```text
Cognixia-JUMP-Project/
├── backend/               # FastAPI Application
│   ├── controllers/       # API Route handlers
│   ├── models/            # Pydantic schemas
│   ├── services/          # Core business logic
│   ├── db.py              # MongoDB connection setup
│   └── main.py            # Entry point
├── frontend/              # React Application
│   ├── src/
│   │   ├── App.tsx        # Main Dashboard component
│   │   └── App.css        # Styling
│   └── vite.config.ts     # Vite configuration with API proxy
└── README.md              # Project documentation
```
