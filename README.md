# TechToniX Event Management System

## Table of Contents

* [Introduction](#introduction)
* [Features](#features)
* [Installation](#installation)
* [Usage](#usage)
* [Folder Structure](#folder-structure)
* [Key Views and Functionalities](#key-views-and-functionalities)
* [Models](#models)
* [Forms](#forms)
* [Templates](#templates)
* [Authentication](#authentication)
* [Authorization](#authorization)
* [Admin Interface](#admin-interface)
* [Future Enhancements](#future-enhancements)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

## Introduction

The TechToniX Event Management System is a web application designed to streamline the process of organizing, managing, and attending events. Built using the Django framework, this system provides a user-friendly interface for organizers to create and manage events, and for attendees to view and register for them.

## Features

* **Event Management:**
    * Create, edit, and delete events.
    * Categorize events.
    * Set event dates, times, venues, and descriptions.
    * Manage event status (pending, approved, rejected).
* **Ticket Management:**
    * Define multiple ticket types for each event (e.g., VIP, Regular).
    * Set ticket prices and availability.
* **Registration Management:**
    * Allow users to register for events.
    * Manage event registrations.
* **Organizer Dashboard:**
    * A centralized dashboard for organizers to manage their events.
    * View a list of events created by the organizer.
    * Quick access to create, edit, and delete events.
* **User Authentication and Authorization:**
    * User registration and login.
    * Role-based access control (organizer, admin).
    * Organizers can only manage events they create.
    * Admins have full control over all events.
* **Frontend:**
    * User-friendly HTML templates.
* **Database:**
    * PostgreSQL database.

## Installation

1.  **Clone the repository:**

    ```
    git clone <repository_url>
    cd TechToniX
    ```

2.  **Set up a virtual environment (recommended):**

    ```
    python3 -m venv venv
    source venv/bin/activate # On Linux/macOS
    venv\Scripts\activate.bat # On Windows
    ```

3.  **Install dependencies:**

    ```
    pip install -r requirements.txt
    ```

4.  **Configure the database:**

    * Ensure you have PostgreSQL installed and running.
    * Create a database for the project.
    * Copy the `config/.env.example` file to `config/.env`

        ```
        cp config/.env.example config/.env
        ```

    * Update the `config/.env` file with your database settings:

        ```
        DB_ENGINE=django.db.backends.postgresql
        DB_NAME=<your_database_name>
        DB_USER=<your_database_user>
        DB_PASSWORD=<your_database_password>
        DB_HOST=localhost
        DB_PORT=5432
        ```

    * Optionally, update the Secret Key and other settings in `config/.env`.

5.  **Apply database migrations:**

    ```
    python manage.py migrate
    ```

6.  **Create a superuser:**

    ```
    python manage.py createsuperuser
    ```

7.  **Run the development server:**

    ```
    python manage.py runserver
    ```

8.  **Access the application:**

    Open your web browser and navigate to `http://localhost:8000/`.

## Usage

1.  **Registration and Login:**

    * Users can register for an account.
    * Registered users can log in to the system.

2.  **Event Listing and Details:**

    * View a list of approved events on the homepage.
    * Click on an event to see its details.

3.  **Organizer Functionality (for organizers and admins):**

    * **Organizer Dashboard:**
        * Access the dashboard to view and manage your events (`/events/dashboard/`).
        * Create a new event by clicking "Create New Event".
        * Edit event details by clicking "Edit".
        * Delete an event by clicking "Delete".
    * **Creating an Event:**
        * Fill in the event form with event details, including name, category, date, time, venue, description, and image.
        * Add ticket types with their names, prices, and quantities.
        * Submit the form to create the event. The event will be created with a "pending" status.
    * **Editing an Event:**
        * Modify event details and ticket information.
        * Submit the form to update the event.
    * **Deleting an Event:**
        * Confirm the deletion of the event.
        * The event will be removed from the system.

4.  **Admin Functionality:**

    * Admins can access the Django admin interface (`/admin/`) to manage users, events, and other data.
    * Admins can approve or reject events.


## Key Views and Functionalities

* **`app/views.py`**:
    * `home`: Displays a list of upcoming approved events.
* **`event/views.py`**:
    * `EventListView`: Displays a list of approved events.
    * `EventCategoryListView`: Displays events filtered by category.
    * `EventDetailView`: Displays detailed information about a specific event.
    * `OrganizerDashboardView`: Displays the organizer's dashboard, listing their events.
    * `EventCreateView`: Handles the creation of new events and associated tickets.
    * `EventEditView`: Handles editing existing events and their tickets.
    * `EventDeleteView`: Handles deleting events.
* **`authentication/views.py`**:
    * `SignInView`: Handles user login.
    * `SignUpView`: Handles user registration.
    * `ProfileView`: Handles user profile display.
    * `LogoutView`: Handles user logout

## Models

* **`event/models.py`**:
    * `Event`: Represents an event with details like name, category, date, time, venue, description, image, status, and organizer.
    * `Category`: Represents event categories (e.g., Music, Sports, Conference).
    * `Ticket`: Represents ticket types for an event, with details like name, price, and quantity.
    * `Registration`: Represents a user's registration for an event and the associated ticket.
* **`authentication/models.py`**:
    * `CustomUser`: (If you have a custom user model) Represents a user with fields like email, password, role, etc.

## Forms

* **`event/forms.py`**:
    * `EventForm`: For creating and editing events.
    * `TicketFormSet`: A formset for managing multiple tickets associated with an event.
* \*\*`authentication/forms.py`:
    * `SignInForm`: For user login.
    * `SignUpForm`: For user registration.

## Templates

* **`templates/app/base.html`**: Base template for the application, providing the basic structure.
* **`templates/app/home.html`**: Template for the homepage, displaying upcoming events.
* **`templates/event/event_list.html`**: Displays a list of events.
* **`templates/event/event_detail.html`**: Displays detailed information about an event.
* **`templates/event/event_form.html`**: Form for creating and editing events.
* **`templates/event/organizer_dashboard.html`**: Displays the organizer dashboard.
* **`templates/event/event_confirm_delete.html`**: Confirmation page for deleting an event.
* **`templates/authentication/signin.html`**: Sign in page.
* **`templates/authentication/signup.html`**: Sign up page.
* **`templates/authentication/profile.html`**: User profile page.

## Authentication

* The `authentication` application handles user authentication.
* Users can register and log in to the system.
* Login functionality is implemented in `authentication/views.py` using `SignInForm`.
* Registration functionality is implemented in `authentication/views.py` using `SignUpForm`.
* The system uses Django's built-in authentication mechanisms.

## Authorization

* The system implements role-based access control.
* Users are assigned roles, such as "organizer" or "admin".
* The `OrganizerOrAdminRequiredMixin` in `event/views.py` restricts access to certain views (e.g., event creation, editing, deletion, and the organizer dashboard) to organizers and administrators.
* Admins have full access to manage all events and users.
* Organizers can only manage the events they have created.

## Admin Interface

* Django's admin interface (`/admin/`) provides a way to manage users, events, categories, and other data.
* Admins can use the admin interface to approve or reject events, manage user roles, and perform other administrative tasks.

## Future Enhancements

* Implement user registration for events.
* Add the ability for users to buy tickets.
* Implement event search and filtering.
* Enhance the UI with a modern frontend framework (e.g., React, Vue.js).
* Add support for event reminders and notifications.
* Implement social sharing features for events.
* Add support for different event types (e.g., online, in-person).
* Implement a rating and review system for events.

## Contributing

We welcome contributions to the TechToniX project. To contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Implement your changes.
4.  Write tests for your changes.
5.  Ensure that all tests pass.
6.  Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any questions, feedback, or support, please contact me at alokkumarpanda72@gmail.com.
