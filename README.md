# Project Name README

Welcome to the project! This readme will guide you through setting up and running the Docker services included in this repository.

## Prerequisites

Before you start, make sure you have Docker and Docker Compose installed on your system.

## Setup

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/hunzlahmalik/tax-assist-chat
   ```

2. Navigate to the project directory:

   ```bash
   cd tax-assist-chat
   ```

3. Create a `.env` file and configure the environment variables according to your needs. You can use the provided `.env.example` as a template.

## Running the Services

### Building and Starting the Services

If you've made changes to the Docker configuration or if this is your first time running the services, it's recommended to rebuild the Docker images. You can do this by running:

```bash
docker-compose up --build
```

## Docker Services

This project utilizes Docker Compose to manage multiple services. Here's a brief overview of the services defined in the `docker-compose.yml` file:

- **PostgreSQL**: A PostgreSQL database service.
- **Redis**: A Redis service for caching and message broker.
- **Nginx**: An Nginx web server acting as a reverse proxy.
- **Traefik**: A reverse proxy and load balancer for routing incoming requests to the appropriate service.
- **Django**: A Django backend service.
- **Next.js**: A Next.js frontend service.
- **FastAPI OCR**: A FastAPI service for Optical Character Recognition using Tesseract.

Each service is configured with its own dependencies, environment variables, volumes, and network settings.

## Additional Resources

- [Django Docker Template](https://github.com/amerkurev/django-docker-template)
- [OCR Tesseract Docker](https://github.com/ricktorzynski/ocr-tesseract-docker)
- [ChatGPT](https://github.com/nisabmohd/ChatGPT)
- [Groq Playground](https://console.groq.com/playground)
- [Django Rest Framework Simple JWT](https://github.com/jazzband/djangorestframework-simplejwt)

Feel free to explore these resources for additional insights and functionalities.

## Feedback

If you encounter any issues or have suggestions for improvements, please open an issue on GitHub or reach out to the project maintainers.
