# Twelvefold Financial Management System (TFMS)

A robust, web-based financial and administrative management system designed specifically for the Twelvefold Self-Help Group. Built with Django, TFMS digitizes and automates the group's core operations, including monthly contributions, loan processing, penalty tracking, and meeting attendance.

## 🚀 Features

### 1. Role-Based Access Control (RBAC)
* **Administrator (Treasurer/Secretary):** Full access to record contributions, approve/reject loans, issue fines, manage members, and view global financial reports.
* **Regular Member:** A restricted, personalized dashboard to view their personal contribution history, track their specific fines, and apply for loans.

### 2. Smart Loan Management Engine
* **Automated Limits:** Enforces a strict borrowing limit (maximum of 60% of the member's total monthly contributions).
* **Single Active Loan Policy:** Prevents members from applying for a new loan if they have an active or pending balance.
* **Proxy Applications:** Allows members to officially apply for loans on behalf of another beneficiary.
* **Interest Tracking:** Automatically logs the agreed-upon interest rate and calculates remaining balances based on recorded repayments.

### 3. Automated Meeting Register & Fines
* **Smart Roll Call:** Administrators can record meeting attendance using a simple checkbox interface.
* **Auto-Penalties:** The system automatically cross-references the attendance list with the active member database and instantly generates a KES 100 fine for every absentee.

### 4. Financial Reporting & Data Security
* **Printable Monthly Reports:** Generates professional, invoice-style monthly summaries of all cash inflows (contributions, paid fines) and outflows (loans).
* **One-Click Backups:** Allows administrators to securely download the SQLite database directly from the dashboard for offline storage.

## 🛠️ Tech Stack

* **Backend:** Python, Django 5.x
* **Database:** SQLite (File-based, zero-configuration)
* **Frontend:** HTML5, CSS3, Bootstrap 5, Bootstrap Icons
* **Architecture:** Multi-tenant MVT (Model-View-Template)

## ⚙️ Installation & Setup

Follow these steps to run the project locally on your machine.

**1. Clone the repository**
```bash
git clone [https://github.com/yourusername/twelvefold-fms.git](https://github.com/yourusername/twelvefold-fms.git)
cd twelvefold-fms
