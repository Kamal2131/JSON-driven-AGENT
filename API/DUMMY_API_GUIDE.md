# Dummy API Endpoints Guide

## Overview
Comprehensive dummy endpoints for testing the dynamic agent system with realistic form-filling scenarios.

## Available Endpoints

### 1. Countries
```
GET /api/v1/dummy/countries
```
Returns list of countries with ID, name, and phone code.

**Response:**
```json
{
  "success": true,
  "data": [
    {"id": "IN", "name": "India", "code": "+91"},
    {"id": "US", "name": "United States", "code": "+1"}
  ]
}
```

### 2. Cities
```
GET /api/v1/dummy/cities?country={country}
```
Returns cities for a specific country.

**Parameters:**
- `country` (query): Country ID or name

**Response:**
```json
{
  "success": true,
  "data": [
    {"id": "MUM", "name": "Mumbai", "country_id": "IN"},
    {"id": "DEL", "name": "Delhi", "country_id": "IN"}
  ],
  "country": "India"
}
```

### 3. Categories
```
GET /api/v1/dummy/categories
```
Returns product categories.

**Response:**
```json
{
  "success": true,
  "data": [
    {"id": "electronics", "name": "Electronics", "description": "Electronic devices"},
    {"id": "clothing", "name": "Clothing", "description": "Apparel"}
  ]
}
```

### 4. Products
```
GET /api/v1/dummy/products?category={category}
```
Returns products for a category.

**Parameters:**
- `category` (query): Category ID

**Response:**
```json
{
  "success": true,
  "data": [
    {"id": "P001", "name": "Laptop", "category": "electronics", "price": 50000},
    {"id": "P002", "name": "Mobile Phone", "category": "electronics", "price": 30000}
  ]
}
```

### 5. Brands
```
GET /api/v1/dummy/brands?product={product}
```
Returns brands for a product.

**Parameters:**
- `product` (query): Product ID

**Response:**
```json
{
  "success": true,
  "data": [
    {"id": "B001", "name": "Dell", "product_id": "P001"},
    {"id": "B002", "name": "HP", "product_id": "P001"}
  ]
}
```

### 6. Create Order
```
POST /api/v1/dummy/orders/create
```
Creates a new order.

**Request Body:**
```json
{
  "country": "India",
  "city": "Mumbai",
  "category": "electronics",
  "product": "P001",
  "brand": "Dell",
  "quantity": 2,
  "customer_name": "John Doe",
  "customer_email": "john@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "order_id": "ORD20240115123456",
    "status": "confirmed",
    "created_at": "2024-01-15T10:30:00",
    "customer": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "delivery": {
      "country": "India",
      "city": "Mumbai"
    },
    "items": {
      "category": "electronics",
      "product": "P001",
      "brand": "Dell",
      "quantity": 2
    },
    "payment": {
      "amount": 100000,
      "currency": "INR"
    }
  }
}
```

### 7. Create Registration
```
POST /api/v1/dummy/registrations/create
```
Creates a new registration.

**Request Body:**
```json
{
  "country": "India",
  "city": "Delhi",
  "full_name": "Jane Smith",
  "email": "jane@example.com",
  "phone": "+919876543210",
  "category": "electronics"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "registration_id": "REG20240115123456",
    "status": "pending_verification",
    "created_at": "2024-01-15T10:30:00",
    "applicant": {
      "name": "Jane Smith",
      "email": "jane@example.com",
      "phone": "+919876543210"
    },
    "location": {
      "country": "India",
      "city": "Delhi"
    },
    "category": "electronics"
  }
}
```

## Dependency Chain Examples

### Order Creation Flow
```
1. GET /dummy/countries → Select country
2. GET /dummy/cities?country={country} → Select city
3. GET /dummy/categories → Select category
4. GET /dummy/products?category={category} → Select product
5. GET /dummy/brands?product={product} → Select brand (optional)
6. POST /dummy/orders/create → Create order
```

### Registration Flow
```
1. GET /dummy/countries → Select country
2. GET /dummy/cities?country={country} → Select city
3. GET /dummy/categories → Select category
4. POST /dummy/registrations/create → Create registration
```

## Data Available

### Countries (4)
- India (IN)
- United States (US)
- United Kingdom (UK)
- Canada (CA)

### Cities per Country
- India: Mumbai, Delhi, Bangalore, Hyderabad
- US: New York, Los Angeles, Chicago
- UK: London, Manchester
- Canada: Toronto, Vancouver

### Categories (3)
- Electronics
- Clothing
- Books

### Products
- Electronics: Laptop, Mobile Phone, Tablet
- Clothing: T-Shirt, Jeans, Jacket
- Books: Python Programming, AI Handbook

### Brands
- Laptop: Dell, HP
- Mobile: Samsung, Apple
- Tablet: iPad, Samsung Tab

## Testing with Agent

### Example 1: Create Order
```
You: I want to order a laptop from India
Agent: [Automatically collects all parameters and creates order]
```

### Example 2: Create Registration
```
You: Register me for electronics in Mumbai
Agent: [Collects details and creates registration]
```

### Example 3: View Data
```
You: Show me all countries
Agent: [Displays country list]
```

## Notes

- All endpoints return consistent JSON structure
- Dependency chains are properly maintained
- Realistic data for testing
- Error handling for invalid inputs
- Supports the dynamic agent's parameter collection
