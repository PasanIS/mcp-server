
"""MCP Restaurant Backend Tools Package"""

from .menu_tool import *
from .orders_tool import *
from .customer_tool import *
from .promos_tool import *
from .reviews_tool import *
from .analytics_tool import *
from .staff_tool import *
from .health_tool import *

__all__ = [
    # -----Menu tools
    "get_menu_items",
    "get_menu_item_details",
    "create_menu_item",
    "update_menu_item",

    # -----Order tools
    "create_order",
    "get_order_details",
    "get_customer_orders",
    "get_orders_by_status",
    "update_order_status",
    "get_order_journey",
    "get_filtered_orders",

    # -----Customer tools
    "register_customer",
    "get_customer_profile",
    "update_customer_profile",
    "customer_login",

    # -----Promo tools
    "apply_promo_code",
    "get_promo_details",

    # -----Review tools
    "get_order_reviews",
    "create_review",

    # -----Analytics tools
    "get_dashboard_stats",
    "get_popular_items",
    "get_revenue_stats",

    # -----Staff tools
    "staff_login",

    # -----Health tools
    "check_backend_health",
]