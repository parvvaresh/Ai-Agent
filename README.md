# AI Database Agent

An intelligent AI-powered agent that interacts with MySQL databases using natural language queries. Built with FastAPI, LangChain, and LangGraph, this service allows users to query databases using conversational language (including Persian) and receive human-readable responses.

## Features

-  **Natural Language Processing**: Query your database using plain language (English and Persian supported)
-  **Intelligent SQL Generation**: Automatically converts natural language questions into SQL queries
-  **Safety First**: Read-only operations to prevent accidental data modifications
-  **FastAPI Backend**: High-performance async API with automatic documentation
-  **Docker Ready**: Fully containerized with Docker Compose
-  **LangGraph Integration**: Stateful agent workflow with message history
-  **MySQL Database**: Complete database setup with initialization scripts

## Technology Stack

- **Framework**: FastAPI
- **AI/ML**: LangChain, LangGraph, Google GenAI
- **Database**: MySQL 8.0 with SQLAlchemy ORM
- **Testing**: Pytest with async support
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker and Docker Compose installed
- Python 3.10+ (for local development)
- Google GenAI API key

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Ai-Agent
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```env
# Database Configuration
DB_HOST=db
DB_PORT=3306
DB_NAME=your_database_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password

# Google GenAI Configuration
GOOGLE_API_KEY=your_google_api_key

# Application Configuration
APP_ENV=development
```

### 3. Run with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d
```

The application will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MySQL**: localhost:3307

### 4. Stop Services

```bash
docker-compose down

# Remove volumes (WARNING: This deletes database data)
docker-compose down -v
```

## Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run Tests

```bash
pytest
```

## Project Structure

```
Ai-Agent/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── agent/
│   │   ├── agent_service.py    # Agent business logic
│   │   ├── graph.py            # LangGraph workflow definition
│   │   └── tools.py            # Database tools for the agent
│   ├── api/
│   │   ├── router.py           # API router configuration
│   │   └── endpoints/
│   │       └── agent.py        # Agent API endpoints
│   ├── core/
│   │   └── config.py           # Application configuration
│   ├── database/
│   │   └── session.py          # Database session management
│   ├── models/
│   │   └── shop.py             # Database models
│   └── schemas/
│       └── agent.py            # Pydantic schemas
├── data/
│   └── init.sql                # Database initialization script
├── test/
│   ├── conftest.py             # Pytest configuration
│   └── test_agent.py           # Agent tests
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## API Usage

### Health Check

```bash
curl http://localhost:8000/
```

Response:
```json
{
  "status": "ok",
  "message": "AI Database Agent is running!"
}
```

### Query the Agent

```bash
curl -X POST http://localhost:8000/api/v1/agent/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How many products are in the database?",
    "session_id": "user123"
  }'
```

### Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## Configuration

### Database Configuration

The database configuration is managed through environment variables:
- `DB_HOST`: Database host (default: `db` for Docker)
- `DB_PORT`: Database port (default: `3306`)
- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password

### AI Configuration

- `GOOGLE_API_KEY`: Your Google GenAI API key for LLM access

## Database Initialization

The MySQL database is automatically initialized with the script in `data/init.sql` when the container first starts. Modify this file to customize your initial database schema and data.

## Safety Features

The agent is designed with safety in mind:
- **Read-Only Mode**: Only SELECT queries are allowed
- **Schema Validation**: Agent has access to database schema information
- **Error Handling**: Graceful handling of invalid queries or errors

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest test/test_agent.py
```

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:
1. Ensure the database container is healthy: `docker-compose ps`
2. Check database logs: `docker-compose logs db`
3. Verify environment variables in `.env` file

### Port Conflicts

If port 8000 or 3307 is already in use:
1. Stop the conflicting service
2. Or modify the port mappings in `docker-compose.yml`

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For issues, questions, or contributions, please open an issue in the repository.

---

