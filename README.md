# 🛍️ ShopSavvy AI

**ShopSavvy AI** is a full-stack eCommerce web application powered by **Django (backend)** and **React (frontend)**. It includes cutting-edge AI features like product recommendations and a conversational chatbot using Hugging Face.

---

## 🔗 Live Demo

_(Add deployed URLs here later, e.g. Netlify for frontend + Render/Vercel/EC2 for backend)_

---

## 🚀 Features

### 👤 Users
- User registration and login with JWT
- Token-based authentication for secure API access

### 🛒 Catalog
- Browse products by category
- View product details

### 📦 Orders
- Add to cart and checkout flow
- Razorpay-integrated payment on checkout
- Order summary and history

### 🤖 AI Modules
- **Smart Recommendations**: Uses Hugging Face model to suggest similar products
- **Chatbot**: Natural conversation flow using Hugging Face conversational models

---

## 🧠 Tech Stack

| Layer        | Stack                                |
|--------------|---------------------------------------|
| Backend      | Django, MySQL, Django REST Framework |
| Frontend     | React, Vite, Axios, React Router     |
| AI           | Hugging Face Transformers API        |
| Payment      | Razorpay JS SDK                      |
| Deployment   | Docker (optional), GitHub Actions (optional) |

---

## 🛠️ Project Structure

shopsavvy-backend/
├── users/
├── catalog/
├── orders/ # Includes payment integration (Razorpay)
├── recommendations/
├── chatbot/
└── manage.py

shopsavvy-frontend/
├── components/
├── pages/
├── routers.jsx # All route declarations
├── App.jsx
└── main.jsx

yaml
Copy code

---

## ⚙️ Backend Setup (Django + MySQL)

1. **Clone & setup virtual environment**
   ```bash
   git clone https://github.com/yourusername/shopsavvy-backend.git
   cd shopsavvy-backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
Configure MySQL & environment

Update settings.py with DB credentials

Add .env (optional)

Run migrations & server

bash
Copy code
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Test API Endpoints

Use Postman or Swagger

Ensure JWT is working via login/register

💻 Frontend Setup (React + Vite)
Setup React App

bash
Copy code
cd shopsavvy-frontend
npm install
Configure .env

ini
Copy code
VITE_API_BASE_URL=http://localhost:8000/api
VITE_RAZORPAY_KEY=your_razorpay_key
Run Dev Server

bash
Copy code
npm run dev
Routing

Defined in routers.jsx

Routes: /login, /register, /products, /product/:id, /orders, /checkout, /recommendations, /chat

🧪 Testing the App
🔹 Backend
Unit test APIs with Postman or Swagger

JWT Token checks

Razorpay webhook simulation

🔹 Frontend
Manual test all routes and API connections

Test Razorpay payment popup

Ensure chatbot + recommendation API responds

✅ Automated frontend testing can be added using Jest + React Testing Library

📦 Deployment Tips
Frontend: Deploy on Netlify, Vercel, or Firebase

Backend: Deploy on Render, EC2, or Railway

CORS: Ensure CORS is properly configured on Django

Domain Mapping: Point frontend domain to Netlify, backend to your server

📚 Future Enhancements
Admin dashboard

Product search & filtering

Wishlist & reviews

Multi-language chatbot support

Unit & e2e test suite

🤝 Contributors
You – Backend & Frontend Developer

Hugging Face – For model APIs

Razorpay – For payments

📜 License
MIT License