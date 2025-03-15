
# Terminal Chatbot

This project implements a terminal-based chatbot with command routing and asynchronous email functionality.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [Architecture](#architecture)


## Project Description

This project provides a chatbot system that allows users to interact with various services through a command-line interface. It includes features for command routing, asynchronous email sending, and extensibility through a database-driven command registration system.

## Features

- **Command Routing:** Routes commands to different services based on a database mapping.
- **Asynchronous Email Sending:** Sends emails using SendGrid and Celery for background processing.
- **Extensible Command Registration:** Allows adding new commands and services through a database.
- **Terminal Client:** Provides a command-line interface for interacting with the chatbot.
- **Dockerized Deployment:** Uses Docker and Docker Compose for easy setup and deployment.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.
- Python 3.x

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [your-repository-url]
    cd [your-repository-directory]
    ```

2.  **Create a `.env` file:**

    Create a `.env` file in the project root directory and add your environment variables:

    ```
    SENDGRID_API_KEY=YOUR_SENDGRID_API_KEY
    POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD
    ```

3.  **Build and run the Docker containers:**

    ```bash
    docker compose --env-file .env up --build
    ```

### Running the Application

1.  **Open a new terminal window.**

2.  **Run the `terminal_chatbot.py` script:**

    ```bash
    python terminal_chatbot.py http://localhost:5050
    ```

3.  **Enter your messages at the prompt:**

    ```
    Welcome to the Terminal Chatbot!
    Please send a message to your server at url http://localhost:5050
    At any time Ctrl-C will exit the application

    /shrug hello
    -->hello ¯\_(ツ)_/¯

    /email [email address removed] subject body
    -->Email was queued
    ```

## Usage

-   Use commands starting with `/` to trigger specific actions (e.g., `/shrug`, `/email`).
-   Register new commands and their corresponding server URLs using the `/register` endpoint of the `chatbot_parser` service.

## Architecture

The project consists of the following services:

-   **`chatbot_parser`:** Routes commands based on a database mapping.
-   **`email_server`:** Handles email sending requests.
-   **`shrug_command`:** Adds a shrug emoji to messages.
-   **`worker`:** Processes asynchronous email tasks using Celery.
-   **`postgres_container`:** Stores command mappings.
-   **`redis_container`:** Acts as a message broker for Celery.
-   **`job_viewer`:** Provides a web interface for monitoring Celery tasks.
-   **`terminal_chatbot.py`:** A command-line client for interacting with the chatbot.


This project was done under the guidance of Rishabh Thakur and Prof. Kay Ashaolu.
