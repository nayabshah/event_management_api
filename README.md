# Event Management API

This is a FastAPI application for managing events and attendees. It provides features for creating, managing, and tracking events and attendees.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)

## Prerequisites

Make sure you have the following installed:

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/nayabshah/event_management_api.git
   cd event_management_api

## Create a virtual environment (optional but recommended):

- python -m venv venv
- source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Install the required packages:

- pip install fastapi sqlalchemy databases[sqlite] pandas

## Running the Application
- To run the FastAPI application, use the following command:

`uvicorn main:app --reload`

## Running Tests
- Before running the tests, make sure to clear the test.db file to ensure a clean state for testing. You can do this by deleting the file or running the following command:

`rm test.db  # On Windows use 'del test.db'`

- To run the tests, use the following command:

`pytest`

- Make sure you have pytest installed. If you don't have it installed, you can add it to your requirements:

`pip install pytest`