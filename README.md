# sponsor-a-pup


Sponsor-a-Pup
Project Description
Sponsor-a-Pup is a web application that connects animal lovers with puppies in need of sponsorship. Users can sign up, log in, and subscribe to sponsor a pup via a secure payment flow powered by Stripe. The application features multi-step sign-up and login processes, dynamic content display for individual puppy profiles, and staff views for managing pup details and updates.


Technologies Used
Backend Framework: Django
Authentication: Django's built-in auth system with custom views for multi-step sign-up and login flows
Payment Processing: Stripe API for subscription-based sponsorships
Frontend: HTML, CSS (custom styles with Figma design integration)
Version Control: Git & GitHub
Environment Management: Python virtual environments (pipenv) and a .env file for sensitive configuration
Database: PostgreSQL (or another supported DB configured via Django settings)


Build/Code Process
Project Setup:

Created a Django project and app structure.
Set up virtual environments using pipenv and managed dependencies.
Configured environment variables in a .env file (e.g., SECRET_KEY, Stripe API key).
Multi-Step User Authentication:

Designed custom multi-step sign-up processes including name, email & phone, address, and password collection.
Integrated CSRF protection in forms and used Django’s session framework to store intermediate data.
Customized login views to redirect authenticated users away from sign-in pages.
Stripe Integration:

Built a view to create Stripe checkout sessions for subscription payments.
Configured success and cancel URLs using Django’s URL reversing and environment settings.
User and Sponsor Models:

Extended Django’s User model to create a custom SponsorUser for handling sponsor-specific data.
Implemented views for user profile management and sponsorship dashboards.
Additional Features:

Developed CRUD operations for puppy profiles and updates.
Implemented staff views to manage content, including pup details and media.
Deployment & Version Control:

Managed branches via Git for feature development and merged code from local branches into main.
Prepared the project for deployment by keeping sensitive credentials out of source code using a .env file.


Key Learnings/Takeaways
Multi-Step Forms:
Building a multi-step sign-up process helped reinforce concepts around session management and form validation in Django.

Separation of Concerns:
Separating logic into multiple views (and optionally using Django Form Wizard) improved code readability and maintainability.

Security Best Practices:
Implementing CSRF tokens, using environment variables for sensitive data, and redirecting authenticated users from public pages reinforced secure coding practices.

Third-Party Integration:
Integrating Stripe for handling subscriptions provided real-world experience with external APIs and payment processing.

Version Control Discipline:
Managing branches and using Git effectively streamlined the development process and helped in maintaining a clean codebase.
