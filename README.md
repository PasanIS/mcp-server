# Restaurant Backend MCP Server
### MCP (Model Context Protocol) server for interacting with the Restaurant FastAPI backend.
## Installation
    cd mcp-servers/backend-mcp
    uv sync 

## Configuration
Update the BASE_URL in src/backend_mcp/server.py to match your FastAPI backend URL:
    
    (python)
    BASE_URL = "http://localhost:8000"  # Change this to your backend URL

## Available Tools
### Menu Management

-   get_menu_items - Browse menu items with filters
-   get_menu_item_details - Get detailed item information
-   create_menu_item - Add new menu items (staff only)
-   update_menu_item - Update existing items (staff only)

### Order Management

-   create_order - Place new orders
-   get_order_details - Get order information
-   get_customer_orders - Get all orders for a customer
-   get_orders_by_status - Filter orders by status
-   update_order_status - Update order status
-   get_order_journey - View order status history
-   get_filtered_orders - Advanced order filtering

### Customer Management

-   register_customer - Create new customer account
-   get_customer_profile - Get customer information
-   update_customer_profile - Update customer details
-   customer_login - Authenticate customer

### Promo Codes

-   apply_promo_code - Validate and calculate discounts
-   get_promo_details - Get promo code information

### Reviews

-   get_order_reviews - Get order reviews
-   create_review - Submit a review

### Analytics

-   get_dashboard_stats - Overall statistics
-   get_popular_items - Most ordered items
-   get_revenue_stats - Revenue analysis

### Staff Operations

-   staff_login - Staff authentication

### System

-   check_backend_health - Backend health check

## Running the Server
### For Development/Testing
    uv run python -m backend_mcp.server
### As MCP Server (for Claude Desktop)
#### Add to your Claude Desktop config:
    (.json)
    {
      "mcpServers": {
        "restaurant-backend": {
          "command": "uv",
          "args": [
            "--directory",
            "/path/to/mcp-servers/backend-mcp",
            "run",
            "backend-mcp"
          ]
        }
      }
    }
### Testing
    uv run python test_server.py
    **Make sure your FastAPI backend is running before testing.
### Environment Variables
You can override the backend URL using environment variables:
    
    export BACKEND_URL="http://<your-backend-url>:8000"

## Architecture
    Chatbot (Claude) 
        ↓ (MCP Protocol)
    Backend MCP Server
        ↓ (HTTP/REST)
    FastAPI Backend
        ↓
    Database

##  Next

- Create Database MCP Server for direct SQL operations
Implement authentication/authorization
- Add error handling and retry logic
- Add caching for frequently accessed data