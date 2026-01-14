
"""
Restaurant Backend MCP Server - Main Server
Provides MCP tools, resources, and prompts
Interact with the restaurant backend API
"""

from fastmcp import FastMCP
from .config import settings
from . import tools
from . import resources
from . import prompts

# -----Initialize MCP server
mcp = FastMCP(
    name="Restaurant Backend API",
    version="1.0.0"
)


# -----Tools Registration

# -----(menu_tool)
@mcp.tool()
async def get_menu_items(
        category: str = None,
        is_available: bool = None):

    return await tools.get_menu_items(category, is_available)

@mcp.tool()
async def get_menu_item_details(item_id: int):

    return await tools.get_menu_item_details(item_id)

@mcp.tool()
async def create_menu_item(
        name: str,
        price: float,
        category: str,
        description: str = None,
        is_available: bool = True,
        image_url: str = None,
        preparation_time: int = None):

    return await tools.create_menu_item(
        name, price, category, description, is_available, image_url, preparation_time
    )

@mcp.tool()
async def update_menu_item(
        item_id: int,
        name: str = None,
        price: float = None,
        category: str = None,
        description: str = None,
        is_available: bool = None,
        image_url: str = None,
        preparation_time: int = None):

    return await tools.update_menu_item(
        item_id, name, price, category, description, is_available, image_url, preparation_time
    )


# -----(orders_tool)
@mcp.tool()
async def create_order(
        customer_id: int,
        order_type: str,
        items: list,
        delivery_address: str = None,
        special_instructions: str = None,
        promo_code: str = None):

    return await tools.create_order(
        customer_id, order_type, items, delivery_address, special_instructions, promo_code
    )

@mcp.tool()
async def get_order_details(order_id: int):

    return await tools.get_order_details(order_id)

@mcp.tool()
async def get_customer_orders(customer_id: int):

    return await tools.get_customer_orders(customer_id)

@mcp.tool()
async def get_orders_by_status(status: str):

    return await tools.get_orders_by_status(status)

@mcp.tool()
async def update_order_status(
        order_id: int,
        status: str,
        staff_id: int = None,
        notes: str = None):

    return await tools.update_order_status(order_id, status, staff_id, notes)

@mcp.tool()
async def get_order_journey(order_id: int):

    return await tools.get_order_journey(order_id)

@mcp.tool()
async def get_filtered_orders(
        status: str = None,
        order_type: str = None,
        customer_id: int = None,
        start_date: str = None,
        end_date: str = None,
        min_amount: float = None,
        max_amount: float = None,
        skip: int = 0,
        limit: int = 100):

    return await tools.get_filtered_orders(
        status, order_type, customer_id, start_date, end_date, min_amount, max_amount, skip, limit
    )


# -----(customer_tool)
@mcp.tool()
async def register_customer(
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        phone: str = None,
        address: str = None):

    return await tools.register_customer(
        email, first_name, last_name, password, phone, address
    )

@mcp.tool()
async def get_customer_profile(customer_id: int):

    return await tools.get_customer_profile(customer_id)

@mcp.tool()
async def update_customer_profile(
        customer_id: int,
        first_name: str = None,
        last_name: str = None,
        phone: str = None,
        address: str = None,
        password: str = None):

    return await tools.update_customer_profile(
        customer_id, first_name, last_name, phone, address, password
    )

@mcp.tool()
async def customer_login(email: str, password: str):

    return await tools.customer_login(email, password)


# -----(promos_tool)
@mcp.tool()
async def apply_promo_code(promo_code: str, order_amount: float):

    return await tools.apply_promo_code(promo_code, order_amount)

@mcp.tool()
async def get_promo_details(promo_id: int):

    return await tools.get_promo_details(promo_id)


# -----(reviews_tool)
@mcp.tool()
async def get_order_reviews(order_id: int):

    return await tools.get_order_reviews(order_id)

@mcp.tool()
async def create_review(
        customer_id: int,
        rating: int,
        comment: str = None,
        order_id: int = None,
        menu_item_id: int = None):

    return await tools.create_review(
        customer_id, rating, comment, order_id, menu_item_id
    )


# -----(analytics_tool)
@mcp.tool()
async def get_dashboard_stats():

    return await tools.get_dashboard_stats()

@mcp.tool()
async def get_popular_items(limit: int = 10, days: int = 1):

    return await tools.get_popular_items(limit, days)

@mcp.tool()
async def get_revenue_stats(
        start_date: str,
        end_date: str,
        group_by: str = "day"):

    return await tools.get_revenue_stats(start_date, end_date, group_by)


# -----(staff_tool)
@mcp.tool()
async def staff_login(email: str, password: str, user_type: str = "staff"):

    return await tools.staff_login(email, password, user_type)


# -----(health_tool)
@mcp.tool()
async def check_backend_health():

    return await tools.check_backend_health()


# -----Resources Registration

@mcp.resource("menu://all")
async def menu_resource():

    return await resources.get_menu_resource("all")

@mcp.resource("menu://category/{category}")
async def menu_category_resource(category: str):

    return await resources.get_menu_resource(category)


# -----Prompts Registration

@mcp.prompt()
async def create_order_prompt(customer_name: str = None):

    return prompts.create_order_prompt(customer_name)


@mcp.prompt()
async def track_order_prompt(order_id: int):

    return prompts.track_order_prompt(order_id)


@mcp.prompt()
async def order_assistance_prompt():

    return prompts.order_assistance_prompt()


# -----Main Entry Point

def main():
    import logging

    # -----Logging configuration
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Starting Restaurant Backend MCP Server")
    logger.info(f"Backend URL: {settings.backend_url}")
    logger.info(f"Environment: {settings.environment}")

    # -----Run MCP server
    mcp.run()

if __name__ == "__main__":
    main()