# Barbershop Booking

A Django web application for booking appointments at a barbershop. Clients can browse barbers and services, choose an available date and time, create and manage their bookings, while barbers can manage their appointments and update booking statuses.

## Features

- User registration and authentication
- Client and barber roles
- Browse active barbers
- Browse active services and prices
- Book an appointment
- View available dates and time slots
- View personal bookings
- Cancel bookings
- Barber appointment management
- Update booking status
- Django admin panel

## Database Schema
![Знімок екрана 2026-10-06 о 00.05.44.png](../../Desktop/%D0%97%D0%BD%D1%96%D0%BC%D0%BE%D0%BA%20%D0%B5%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202026-10-06%20%D0%BE%2000.05.44.png)

## Getting Started

These instructions will help you set up the project locally for development and testing.

### Prerequisites

You need:

- Python 3.12+
- Git

### Installation

Clone the repository:

```bash
git clone <repository-url>
cd barbershop-booking
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate
```

Create a superuser:

```bash
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

The Django admin panel is available at:

```text
http://127.0.0.1:8000/admin/
```

## Running the Tests

Run the complete test suite with:

```bash
python manage.py test
```

The tests cover the main booking functionality, including:

- Booking service logic
- Available booking slots
- Booking validation
- Booking list views
- Barber booking management
- Booking cancellation
- Booking status updates
- Access restrictions for clients and barbers

## Code Quality

The project uses Ruff for Python code formatting and linting.

Format the project:

```bash
ruff format .
```

Check formatting without changing files:

```bash
ruff format --check .
```

Run the linter:

```bash
ruff check .
```

## Built With

- Django — Web framework
- SQLite — Development database
- Bootstrap — Frontend styling
- Django Crispy Forms — Form rendering
- Pillow — Image handling
- Ruff — Code formatting and linting

## Project Structure

```text
barbershop_booking/
├── booking/
│   ├── migrations/
│   ├── tests/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── services.py
│   ├── urls.py
│   └── views.py
├── static/
├── templates/
├── media/
├── manage.py
└── README.md
```

## Booking Flow

A client creates a booking by:

1. Selecting a barber
2. Selecting a service
3. Selecting an available date
4. Selecting an available time
5. Confirming the booking

The application validates the selected slot before creating the booking.

## Roles

### Client

Clients can:

- Browse barbers and services
- Create bookings
- View their own bookings
- Cancel their bookings

### Barber

Barbers can:

- View their appointments
- See their own schedule
- Mark appointments as completed
- Mark appointments as no-show

### Admin

Administrators can manage application data through the Django admin panel.

## Deployment

This project is currently intended for local development and educational purposes.

Before deploying to production, configure:

- A production database
- Production `SECRET_KEY`
- `DEBUG = False`
- Allowed hosts
- Static and media file serving
- Production email backend
- HTTPS
- Appropriate security settings

## Author

Yan Marynets