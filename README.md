# Lead-Mgmt-FastAPI-Demo
## An application to manage leads for attorneys, built with Python + FastAPI

Lead Management System is a Demo FastAPI Application designed to manage leads and attorneys for a law firm or legal services company. 
It provides a public form for prospects to submit their information, notifies attorneys of new leads, and offers an internal UI for attorneys to view and update lead statuses.

## Features

- **Public Lead Submission**: Prospects can fill out a form with their name, email, and resume/CV to submit a new lead.
- **Email Notifications**: When a new lead is created, the system sends email notifications to the prospect (acknowledgment) and an available attorney (new lead notification).
- **Attorney Authentication**: Attorneys can securely authenticate using JWT-based authentication to access the internal UI.
- **Lead Management**: Authenticated attorneys can view a list of all leads, including the prospect's information and the current status of each lead.
- **Lead Status Updates**: Attorneys can update the status of a lead (e.g., from "PENDING" to "REACHED_OUT") after reaching out to the prospect.
- **Role-Based Access Control (RBAC)**: Certain operations, such as updating lead statuses, are restricted to authenticated attorneys only.

## Technologies Used
- **Python 3.9+**
- **FastAPI** - Modern, fast, and high-performance web framework for building APIs with Python.
- **SQLite** - Lightweight and file-based database for development and testing purposes.
- **SQLAlchemy** - Python SQL toolkit and Object-Relational Mapping (ORM) library for interacting with the database.
- **Pydantic** - Data validation and settings management library for Python.
- **Uvicorn** - Lightning-fast ASGI server for running FastAPI applications.
- **Bcrypt** - Library for secure password hashing and verification.
- **Python-Jose** - Library for JSON Web Token (JWT) handling.

## Getting Started
### Prerequisites
- Python 3.9 or later
- pip (Python package installer)
- Installation

### Clone the repository:

```
git clone https://github.com/your-username/lead-management-system.git
cd lead-management-system
```

### Create a virtual environment and activate it:

```
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

### Install the required dependencies:

```
pip install -r requirements.txt
```

### Set up the database:

```
touch leads.db
python init_db.py
```

#### (Optional) Populate the database with dummy data:
Use `Lead-Mgmt-System-FastAPI-Demo-V1/dummy_data-sqlite3.txt` file for dummy data.


### Start the FastAPI application:
```
cd app/
uvicorn main:app --reload --port 8000

```
The application will be accessible at **[http://localhost:8000](http://localhost:8000)**, and the interactive API documentation will be available at **[http://localhost:8000/docs](http://localhost:8000/docs)**.

## Configuration

You can set the required variables in a .env file or export them in your shell.

## Contributing

Contributions are welcome! Please follow the guidelines in the CONTRIBUTING.md file.

## License

This project is licensed under the MIT License.

## Acknowledgments

- **FastAPI** - The official FastAPI documentation and resources.
- **SQLAlchemy** - SQLAlchemy documentation and tutorials.
- **Pydantic** - Pydantic documentation and examples.
