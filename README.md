# Rotom Backend - API Server

Python-based REST API server for the Rotom Kitchen Management System.

Provides endpoints for ESP32 devices to query ingredients and recipes from MongoDB database.

## Overview

The backend serves as the central hub between the ESP32 embedded devices and MongoDB database:
- Validates incoming requests against Label Base system
- Executes database queries with filtering and sorting
- Returns formatted JSON responses
- Handles error cases gracefully

## API Endpoints

### GET /api/ingredients

Retrieve complete list of available ingredients.

**Response:** Array of ingredients with complete details

### GET /api/recipes?ingredients=1,2,3

Query recipes containing ANY of the specified ingredients (partial match).

**Parameters:**
- `ingredients` (required): Comma-separated ingredient IDs

**Response:** Array of recipes sorted alphabetically by name

### GET /api/recipes/exact?ingredients=1,2,3

Query recipes containing EXACTLY the specified ingredient set.

**Parameters:**
- `ingredients` (required): Comma-separated ingredient IDs

**Response:** Array of recipes matching exact ingredient set (up to 10 random results)

For complete API documentation and request/response examples, see ../README.md

## Installation

### Prerequisites
- Python 3.8+
- MongoDB 4.4+
- pip package manager

### Setup

1. Create virtual environment:
```bash
cd rotom-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure database connection in config.py:
```python
MONGODB_URI = "mongodb://localhost:27017"
DATABASE_NAME = "rotom_db"
API_PORT = 5000
```

4. Start the server:
```bash
python main.py
```

Server will be accessible at http://localhost:5000

## Project Structure

```
rotom-backend/
├── main.py                Main application entry point
├── config.py              Configuration settings
├── requirements.txt       Python dependencies
├── models/
│   ├── ingredient.py      Pydantic model for ingredients
│   └── recipe.py          Pydantic model for recipes
├── routes/
│   ├── ingredients.py     Ingredient endpoint handlers
│   ├── recipes.py         Recipe endpoint handlers
│   └── __init__.py        Route initialization
└── README.md              This file
```

## Validation

### Label Base Integration

Validates ingredient tags against label_base.json from rotom-db:
- Prevents invalid or misspelled tags
- Ensures consistency across all recipes and ingredients

### Data Validation Rules

- Ingredient IDs must be numeric and exist in database
- Recipe ingredient references must point to valid ingredients
- Quantities must be positive numbers
- Tags must be defined in Label Base system
- Recipes with missing ingredients are flagged but returned

## Testing

### Using curl

```bash
# Get all ingredients
curl http://localhost:5000/api/ingredients

# Query recipes with ingredient 1 or 2
curl http://localhost:5000/api/recipes?ingredients=1,2

# Query recipes with exactly ingredients 1 and 2
curl http://localhost:5000/api/recipes/exact?ingredients=1,2
```

## Performance Considerations

- Endpoints optimized for ESP32 memory constraints
- Responses limited to essential fields
- Query results capped at 10-25 items per request
- Connection pooling configured for efficiency

## Database Integration

Connects to MongoDB collections:
- `ingrediente`: Ingredient data with stock tracking
- `retete`: Recipe definitions with ingredient requirements
- `label_base`: Tag definitions for validation

Refer to ../rotom-db/README.md for database schema details.

## Troubleshooting

**MongoDB Connection Error:**
- Verify MongoDB is running and accessible
- Check MONGODB_URI configuration
- Ensure firewall allows connections

**Invalid Ingredient IDs:**
- Verify ingredient exists in database
- Check ID format (must be numeric)
- Seed database if empty

**Missing Dependencies:**
- Run pip install -r requirements.txt
- Ensure virtual environment is activated

## Related Documentation

- Main project overview: ../README.md
- Database schemas: ../rotom-db/README.md
- Label Base system: ../rotom-db/LABELS.md
