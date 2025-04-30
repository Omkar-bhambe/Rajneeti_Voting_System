# 🗳️ Rajneeti: Voter Management & Voting System

A web-based voting platform built with **Flask**, designed to securely manage admin and voter registrations, conduct elections, and visualize results. This system includes role-based authentication, password recovery, and vote tracking features with a clean frontend interface using HTML, CSS, Bootstrap and Tailwind.

---

## 📁 Project Structure
---

## 🚀 Features

- ✅ Admin and Voter registration & login
- 🔐 Secure session handling using Flask sessions
- 🔄 Password recovery system for both roles
- 🗳️ Voting functionality with candidate vote tracking
- 📊 Real-time result visualization with charts
- 🧭 Navigation-friendly user interface
- 🎨 Bootstrap and Tailwind CSS-based styling

---

## 🛠️ Technologies Used

- **Frontend**: HTML, CSS, Tailwind
- **Backend**: Python (Flask)
- **Database**: MySQL (via `pymysql`)
---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/omkar-bhambe/voter_system.git
   cd voter_system

2. Setup a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

3. Install dependencies
   ```bash
      pip install -r requirements.txt

4. Configure MySQL
  - Create a database named voter_db
  - Update credentials in VoterDb.py

5. Run the app
   ```bash 
      python app.py

## 🔐 Admin Panel

- URL: /admin
- Features:
   - View registered voters
   - View election results 
   - Register new and unique candidates
   - Starting of new session

## 🧪 Voter Panel
- URL: /voter/login
- Features:
   - Cast vote once per session
   - Forgot password option
   - Secure voting with validation
