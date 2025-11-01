# Workflow Configuration Guide

## JSON Configuration Structure

All workflow configurations are defined in JSON files. No hardcoding in Python code!

### Basic Structure

```json
{
  "api_name": "Workflow Name",
  "endpoint": "/api/endpoint",
  "method": "GET|POST|PUT|PATCH|DELETE",
  "description": "What this workflow does",
  "parameters": {
    "param_name": {
      "type": "string|integer|boolean",
      "required": true|false,
      "location": "body|query|path",
      "default": "default_value",
      "depends_on": "other_param" | ["param1", "param2"],
      "api_call": "/api/to/fetch/options?param={param}",
      "response_field": "path.to.data[].field"
    }
  }
}
```

### Parameter Configuration Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Data type: string, integer, boolean, etc. |
| `required` | boolean | Yes | Whether parameter is mandatory |
| `location` | string | Yes | Where to send: body, query, or path |
| `default` | any | No | Default value if not found in user input |
| `depends_on` | string/array | No | Parameter(s) this depends on |
| `api_call` | string | No | API endpoint to fetch options from |
| `response_field` | string | No | JSON path to extract values |

### Response Field Path Notation

- `data` - Direct field access
- `data[]` - Array in data field
- `data[].field_name` - Extract field_name from each array item
- `classPlanList[].PolicyId` - Extract PolicyId from classPlanList array
- `nested.object.field` - Nested object access

### Examples

#### 1. Simple GET Request

```json
{
  "api_name": "Get States",
  "endpoint": "/states",
  "method": "GET",
  "description": "Fetch all available states",
  "parameters": {
    "active": {
      "type": "boolean",
      "required": false,
      "location": "query",
      "default": true
    }
  }
}
```

#### 2. POST with Dependencies

```json
{
  "api_name": "Create Order",
  "endpoint": "/orders/create",
  "method": "POST",
  "description": "Create a new order",
  "parameters": {
    "customer_name": {
      "type": "string",
      "required": true,
      "location": "body"
    },
    "product": {
      "type": "string",
      "required": true,
      "location": "body",
      "depends_on": "customer_name",
      "api_call": "/products?customer={customer_name}",
      "response_field": "data[].product_name"
    },
    "quantity": {
      "type": "integer",
      "required": true,
      "location": "body",
      "default": 1
    }
  }
}
```

#### 3. Multi-level Dependencies

```json
{
  "api_name": "Book Appointment",
  "endpoint": "/appointments/book",
  "method": "POST",
  "description": "Book a medical appointment",
  "parameters": {
    "city": {
      "type": "string",
      "required": true,
      "location": "body"
    },
    "hospital": {
      "type": "string",
      "required": true,
      "location": "body",
      "depends_on": "city",
      "api_call": "/hospitals?city={city}",
      "response_field": "data[].name"
    },
    "doctor": {
      "type": "string",
      "required": true,
      "location": "body",
      "depends_on": ["city", "hospital"],
      "api_call": "/doctors?city={city}&hospital={hospital}",
      "response_field": "data[].doctor_name"
    },
    "date": {
      "type": "string",
      "required": true,
      "location": "body"
    }
  }
}
```

#### 4. Path Parameters

```json
{
  "api_name": "Update User",
  "endpoint": "/users/{user_id}",
  "method": "PUT",
  "description": "Update user information",
  "parameters": {
    "user_id": {
      "type": "string",
      "required": true,
      "location": "path"
    },
    "name": {
      "type": "string",
      "required": false,
      "location": "body"
    },
    "email": {
      "type": "string",
      "required": false,
      "location": "body"
    }
  }
}
```

## How It Works

1. **User Input** → Agent receives natural language request
2. **Workflow Selection** → Supervisor matches request to workflow
3. **Parameter Collection** → Agent collects parameters:
   - Extracts from user input using LLM
   - Fetches dependent options from APIs
   - Uses LLM to select from options
4. **API Execution** → Calls the configured endpoint
5. **Response** → Returns formatted result

## Adding New Workflows

1. Create a new JSON file in this directory
2. Follow the structure above
3. Restart the agent
4. The workflow is automatically available!

**No code changes needed!** 🎉

## Tips

- Use descriptive `api_name` for better routing
- Set `default` values for optional parameters
- Use `depends_on` for cascading dropdowns
- Test `response_field` paths with actual API responses
- Keep `description` clear for LLM understanding
