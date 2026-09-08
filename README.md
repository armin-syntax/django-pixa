# **Pixa**

A clean, minimal, responsive photo-sharing platform inspired by modern visual discovery platforms such as Pinterest and Unsplash.

Pixa allows users to discover photos, upload and manage their own content, interact with other users, follow profiles, like and save photos, and manage their accounts.

The project was built with Django and focuses on keeping the application simple, clean, and easy to extend.

## **✨ Features**

### **📸 Photos**

* Explore photo feed
* Upload photos
* Photo detail pages
* Photo titles and captions
* Photo tags
* Like / unlike photos
* Save / unsave photos
* Saved photos page
* Photo ownership and management

### **👤 Users & Profiles**

* User profiles
* Profile information
* User photo galleries
* Follow / unfollow users
* Followers and following relationships
* Profile-based photo discovery

### **🔐 Authentication**

* User registration
* Login
* Logout
* Password reset
* Password reset email flow
* Custom password reset templates
* Django authentication views
* Authentication-aware navigation and pages

### **🎨 UI & UX**

* Responsive design
* Pinterest-style masonry photo layout
* Clean and minimal interface
* Responsive navigation
* Reusable UI components
* Custom forms and authentication templates
* Custom error pages
* Photo action menus
* User-friendly alerts and messages

### **📄 Pages**

Pixa currently includes:

* Explore
* About
* Register
* Login
* Logout
* Profile
* Upload Photo
* Photo Detail
* Saved Photos
* Password Reset
* Password Reset Done
* Password Reset Confirm
* Password Reset Complete
* 404 Error Page

## **🛠 Tech Stack**

### **Backend**

* Python
* Django
* Django Authentication
* Django Templates
* Django ORM
* SQLite / PostgreSQL

### **Frontend**

* HTML5
* CSS3
* Vanilla JavaScript

### **Development**

* Git
* GitHub

The project does not require a frontend framework such as React or Vue.

Django handles the server-side rendering, authentication, database interaction, and application logic.

## **🏗 Architecture**

Pixa follows a traditional Django server-rendered architecture.

```text
Browser
   │
   ▼
Django
   │
   ├── URLs
   │
   ├── Views
   │
   ├── Templates
   │
   ├── Forms
   │
   ├── Models
   │
   └── Authentication
          │
          ▼
       Database
```

## **🔐 Authentication**

Pixa uses Django's built-in authentication system.

The authentication flow includes:

```text
Register
   │
   ▼
Login
   │
   ├── Logout
   │
   └── Authenticated User
          │
          ├── Profile
          ├── Upload Photo
          ├── Like / Unlike
          ├── Save / Unsave
          └── Follow / Unfollow

Forgot Password
   │
   ▼
Password Reset Email
   │
   ▼
Reset Password
   │
   ▼
Password Reset Complete
```

The password reset functionality is based on Django's built-in authentication views, with custom templates to match the Pixa interface.

## **🗃️ Core Functionality**

### **Follow System**

Users can follow and unfollow other users.

The relationship allows Pixa to represent:

```text
User
 ├── Followers
 └── Following
```

### **Like System**

Users can like or unlike photos.

Each photo can have multiple likes while preventing duplicate likes from the same user.

### **Save System**

Users can save photos for later.

Saved photos are available from the user's saved photos page.

### **Photo Upload**

Authenticated users can upload photos with information such as:

```text
Photo
├── Image
├── Title
├── Caption
├── Author
├── Tags
├── Created At
└── Updated At
```

The upload functionality is restricted to authenticated users.

## **🎨 Design**

Pixa follows a minimal visual direction:

* Clean typography
* Simple spacing
* Subtle borders
* Minimal controls
* Responsive layouts
* Content-focused photo cards
* Neutral visual design
* Red accent color
* Minimal animations and visual effects

The goal is to make the interface easy to understand without unnecessary visual complexity.

## **📸 Screenshots**

A quick look at the main Pixa interfaces.

| Explore                             | Photo Details                                   |
| ----------------------------------- | ----------------------------------------------- |
| ![Explore](screenshots/explore.png) | ![Photo Details](screenshots/photo-details.png) |

| Profile                             | Authentication                  |
| ----------------------------------- | ------------------------------- |
| ![Profile](screenshots/profile.png) | ![Login](screenshots/login.png) |

## **🚀 Getting Started**

### **1. Clone the repository**

```bash
git clone https://github.com/armin-syntax/pixa.git
cd pixa
```

### **2. Create a virtual environment**

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### **3. Install dependencies**

```bash
pip install -r requirements.txt
```

### **4. Apply migrations**

```bash
python manage.py migrate
```

### **5. Create a superuser**

```bash
python manage.py createsuperuser
```

### **6. Run the development server**

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

## **⚙️ Configuration**

For development, Django's default configuration can be used.

For production, make sure to properly configure:

* `SECRET_KEY`
* `DEBUG`
* `ALLOWED_HOSTS`
* Database
* Static files
* Media files
* Email configuration
* Security settings

Sensitive configuration values should be stored in environment variables rather than committed to the repository.

## **🧪 Development**

The project is currently designed as a Django monolithic application:

```text
Django
├── Backend
├── Templates
├── Static Files
├── Authentication
└── Database
```

This approach keeps the application straightforward and makes it suitable for learning, experimentation, and further development.

## **🔮 Future Improvements**

Possible future improvements include:

* Django REST Framework API
* React frontend
* AJAX / Fetch-based interactions
* Infinite scrolling
* Advanced photo search
* Tag-based filtering
* Pagination improvements
* Notifications
* User activity feed
* Comments
* Image optimization
* Cloud media storage
* PostgreSQL in production
* Docker support
* Nginx + Gunicorn deployment
* Automated tests
* CI/CD with GitHub Actions

These features are not required for the current version of Pixa but could be added as the project evolves.

## **🤖 Why Was This Made?**

I'm primarily interested in backend development, and I don't want to spend most of my time building frontend interfaces.

For this project, the frontend was built with the assistance of AI so I could focus more on the Django backend, application logic, authentication, database design, and overall functionality.

The frontend source code is available in a separate repository:

**Frontend:** https://github.com/armin-syntax/pixa-template

Pixa started as a frontend interface and evolved into a complete Django application with authentication, user interactions, photo management, and responsive UI.

The goal was to build a simple and realistic project while keeping the focus on backend development.

## **📌 Inspiration**

The concept and visual direction are inspired by modern platforms focused on discovering and sharing visual content, including Pinterest and Unsplash.

Pixa is an independent project and is not affiliated with, sponsored by, or associated with either platform.

## **🤝 Contributing**

Contributions are welcome.

If you find a bug, have an idea for improving the application, or want to add a feature, feel free to open an issue or submit a pull request.

When contributing, please try to keep the code simple, readable, and consistent with the existing project structure.

## **📄 License**

This project is open source.

See the [`LICENSE`](LICENSE) file for the exact terms and conditions.

---

Built with Django and a lot of curiosity.
