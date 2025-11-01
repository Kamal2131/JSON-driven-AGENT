from fastapi import APIRouter, Query, Path, HTTPException
from typing import Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/dummy", tags=["Dummy Endpoints"])

# Dummy data stores
COUNTRIES = [
    {"id": "IN", "name": "India", "code": "+91"},
    {"id": "US", "name": "United States", "code": "+1"},
    {"id": "UK", "name": "United Kingdom", "code": "+44"},
    {"id": "CA", "name": "Canada", "code": "+1"}
]

CITIES = {
    "IN": [
        {"id": "MUM", "name": "Mumbai", "country_id": "IN"},
        {"id": "DEL", "name": "Delhi", "country_id": "IN"},
        {"id": "BLR", "name": "Bangalore", "country_id": "IN"},
        {"id": "HYD", "name": "Hyderabad", "country_id": "IN"}
    ],
    "US": [
        {"id": "NYC", "name": "New York", "country_id": "US"},
        {"id": "LAX", "name": "Los Angeles", "country_id": "US"},
        {"id": "CHI", "name": "Chicago", "country_id": "US"}
    ],
    "UK": [
        {"id": "LON", "name": "London", "country_id": "UK"},
        {"id": "MAN", "name": "Manchester", "country_id": "UK"}
    ],
    "CA": [
        {"id": "TOR", "name": "Toronto", "country_id": "CA"},
        {"id": "VAN", "name": "Vancouver", "country_id": "CA"}
    ]
}

PRODUCTS = {
    "electronics": [
        {"id": "P001", "name": "Laptop", "category": "electronics", "price": 50000},
        {"id": "P002", "name": "Mobile Phone", "category": "electronics", "price": 30000},
        {"id": "P003", "name": "Tablet", "category": "electronics", "price": 25000}
    ],
    "clothing": [
        {"id": "P004", "name": "T-Shirt", "category": "clothing", "price": 500},
        {"id": "P005", "name": "Jeans", "category": "clothing", "price": 1500},
        {"id": "P006", "name": "Jacket", "category": "clothing", "price": 3000}
    ],
    "books": [
        {"id": "P007", "name": "Python Programming", "category": "books", "price": 800},
        {"id": "P008", "name": "AI Handbook", "category": "books", "price": 1200}
    ]
}

BRANDS = {
    "P001": [{"id": "B001", "name": "Dell", "product_id": "P001"}, {"id": "B002", "name": "HP", "product_id": "P001"}],
    "P002": [{"id": "B003", "name": "Samsung", "product_id": "P002"}, {"id": "B004", "name": "Apple", "product_id": "P002"}],
    "P003": [{"id": "B005", "name": "iPad", "product_id": "P003"}, {"id": "B006", "name": "Samsung Tab", "product_id": "P003"}]
}

# Endpoints
@router.get("/countries")
def get_countries():
    """Get all countries"""
    return {
        "success": True,
        "data": COUNTRIES,
        "message": "Countries fetched successfully"
    }

@router.get("/cities")
def get_cities(country: str = Query(..., description="Country ID or name")):
    """Get cities by country"""
    country_obj = next((c for c in COUNTRIES if c["id"] == country or c["name"].lower() == country.lower()), None)
    if not country_obj:
        raise HTTPException(status_code=404, detail="Country not found")
    
    cities = CITIES.get(country_obj["id"], [])
    return {
        "success": True,
        "data": cities,
        "country": country_obj["name"],
        "message": "Cities fetched successfully"
    }

@router.get("/categories")
def get_categories():
    """Get product categories"""
    categories = [
        {"id": "electronics", "name": "Electronics", "description": "Electronic devices"},
        {"id": "clothing", "name": "Clothing", "description": "Apparel and fashion"},
        {"id": "books", "name": "Books", "description": "Books and publications"}
    ]
    return {
        "success": True,
        "data": categories,
        "message": "Categories fetched successfully"
    }

@router.get("/products")
def get_products(category: str = Query(..., description="Category ID")):
    """Get products by category"""
    products = PRODUCTS.get(category, [])
    if not products:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return {
        "success": True,
        "data": products,
        "category": category,
        "message": "Products fetched successfully"
    }

@router.get("/brands")
def get_brands(product: str = Query(..., description="Product ID")):
    """Get brands by product"""
    brands = BRANDS.get(product, [])
    if not brands:
        return {
            "success": True,
            "data": [],
            "message": "No brands found for this product"
        }
    
    return {
        "success": True,
        "data": brands,
        "product": product,
        "message": "Brands fetched successfully"
    }

# Form submission endpoints
class OrderRequest(BaseModel):
    country: str
    city: str
    category: str
    product: str
    brand: Optional[str] = None
    quantity: int = 1
    customer_name: str
    customer_email: str

@router.post("/orders/create")
def create_order(request: OrderRequest):
    """Create a new order"""
    import uuid
    from datetime import datetime
    
    order_id = f"ORD{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4().int)[:6]}"
    
    # Get product details
    product_obj = None
    for cat_products in PRODUCTS.values():
        product_obj = next((p for p in cat_products if p["id"] == request.product), None)
        if product_obj:
            break
    
    total_amount = product_obj["price"] * request.quantity if product_obj else 0
    
    return {
        "success": True,
        "data": {
            "order_id": order_id,
            "status": "confirmed",
            "created_at": datetime.now().isoformat(),
            "customer": {
                "name": request.customer_name,
                "email": request.customer_email
            },
            "delivery": {
                "country": request.country,
                "city": request.city
            },
            "items": {
                "category": request.category,
                "product": request.product,
                "brand": request.brand,
                "quantity": request.quantity
            },
            "payment": {
                "amount": total_amount,
                "currency": "INR"
            }
        },
        "message": "Order created successfully"
    }

class RegistrationRequest(BaseModel):
    country: str
    city: str
    full_name: str
    email: str
    phone: str
    category: str

@router.post("/registrations/create")
def create_registration(request: RegistrationRequest):
    """Create a new registration"""
    import uuid
    from datetime import datetime
    
    reg_id = f"REG{datetime.now().strftime('%Y%m%d')}{str(uuid.uuid4().int)[:6]}"
    
    return {
        "success": True,
        "data": {
            "registration_id": reg_id,
            "status": "pending_verification",
            "created_at": datetime.now().isoformat(),
            "applicant": {
                "name": request.full_name,
                "email": request.email,
                "phone": request.phone
            },
            "location": {
                "country": request.country,
                "city": request.city
            },
            "category": request.category
        },
        "message": "Registration created successfully"
    }
