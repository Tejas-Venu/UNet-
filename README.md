# UNet NGO Donation & Volunteering Platform  

A full-stack platform that connects **users with NGOs**, enabling **donations, volunteering, and project discovery**. The system is designed to bring transparency and personalization to social impact initiatives.  

## 🚀 Features  
- **User & NGO Management** – Sign up, manage profiles, and connect seamlessly.  
- **Donations & Payments** – Secure payment gateway with **custom transaction verification**.  
- **Volunteering** – Users can discover NGO projects and register as volunteers.  
- **Recommendation System** – Suggests NGOs and causes tailored to user preferences.  
- **Notifications** – Automated donor & NGO notifications powered by **Twilio**.  
- **Analytics Dashboard** – Insights into donations and volunteering activities for transparency.  
- **Scalable Backend** – Modular **Django apps** (`donations`, `ngos`, `users`, `projects`, `payments`).  
- **Cross-Platform Mobile App** – Built with **Flutter**, ensuring accessibility and ease of use.  


> ⚠️ **Note**: The **Flutter app code is not included in this repository** to keep the design and implementation of the mobile application design confidential/private. This repository contains the **Django backend** and related services only.  


## 🛠 Tech Stack  
- **Frontend**: Flutter  
- **Backend**: Django 
- **Database**: PostgreSQL  
- **AI/ML**: User-based collaborative recommendation system  
- **Notifications**: Twilio API  
- **Authentication**: Secure JWT-based system  


## 🔑 Key Modules  
- `donations`: Handles donation logic, history, and verification.  
- `payments`: Secure payment gateway with custom verification.  
- `projects`: NGO project listings + volunteer registration.  
- `users`: Authentication and profile management.  
- `ngos`: NGO onboarding and management.  

## 📊 Analytics & Transparency  
- Personalized donation insights.  
- NGO dashboards for project performance.  
- End-to-end transparency with transaction logs.  

## ⚡ Setup Instructions  
1. Clone the repo:  
   ```bash
   git clone https://github.com/your-username/UNet-NGO-Donation-Platform.git
   cd UNet-NGO-Donation-Platform
   ```

2. Create & activate virtual environment:
   ```bash
    python -m venv venv
    source venv/bin/activate   # Linux/Mac
    venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
   
5. Start development server:
   ```bash
   python manage.py runserver
   ```

## 📱 Mobile App
- Flutter-based app to access the platform.
- Supports donations, volunteering, and NGO recommendations.
- Connected to backend APIs for real-time data.
