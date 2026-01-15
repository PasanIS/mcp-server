
"""Tests for the server module"""

import pytest
import asyncio
from typing import Dict, Any, List

# -----Import tools
from backend_mcp.tools import (
    # -----Menu tools
    get_menu_items,
    get_menu_item_details,
    create_menu_item,
    update_menu_item,

    # -----Order tools
    create_order,
    get_order_details,
    get_customer_orders,
    get_orders_by_status,
    update_order_status,
    get_order_journey,
    get_filtered_orders,

    # -----Customer tools
    register_customer,
    get_customer_profile,
    update_customer_profile,
    customer_login,

    # -----Promo tools
    apply_promo_code,
    get_promo_details,

    # -----Review tools
    get_order_reviews,
    create_review,

    # -----Analytics tools
    get_dashboard_stats,
    get_popular_items,
    get_revenue_stats,

    # -----Staff tools
    staff_login,

    # -----Health tools
    check_backend_health,
)

from backend_mcp.config import settings

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for the tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def sample_customer_id():
    """Get a sample customer ID for testing"""
    try:
        order = await get_order_details(1)
        return order.get('customer_id')
    except:
        return 1

@pytest.fixture
async def sample_menu_item_id():
    """Get a sample menu item ID for testing"""
    try:
        items = await get_menu_items()
        if items:
            return items[0]['id']
    except:
        pass
    return 1


# -----Health Check Test
class TestHealth:
    """Test health check functionality."""

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_backend_health(self):
        # -----Test if backend is healthy/responding
        result = await check_backend_health()

        assert result is not None
        assert 'status' in result
        assert result['status'] == 'healthy'
        print(f"  Backend is healthy: {result}")

    @pytest.mark.asyncio
    async def test_backend_health_format(self):
        # -----Test health check response format
        result = await check_backend_health()

        assert isinstance(result, dict)
        assert 'response' in result
        print(f"  Health check response format valid")


# -----Tool Tests
# ------(menu_tool)
class TestMenuTools:

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_menu_items(self):
        # -----Test fetching all menu items
        items = await get_menu_items()

        assert isinstance(items, list)
        print(f"Found {len(items)} menu items")

        if items:
            item = items[0]
            assert 'id' in item
            assert 'name' in item
            assert 'price' in item
            assert 'category' in item
            print(f"  Sample: {item['name']} - ${item['price']}")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_menu_items_by_category(self):
        # -----Test filtering menu items by category
        categories = ['appetizer', 'main_course', 'dessert', 'beverage', 'side']

        for category in categories:
            items = await get_menu_items(category=category)
            assert isinstance(items, list)

            for item in items:
                assert item['category'] == category

            print(f"  Category '{category}': {len(items)} items")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_menu_items_by_availability(self):
        # -----Test filtering menu items by availability
        # -----Get available items
        available = await get_menu_items(is_available=True)
        assert isinstance(available, list)

        for item in available:
            assert item['is_available'] is True

        print(f"  Available items: {len(available)}")

        # -----Get unavailable items
        unavailable = await get_menu_items(is_available=False)
        assert isinstance(unavailable, list)

        for item in unavailable:
            assert item['is_available'] is False

        print(f"  Unavailable items: {len(unavailable)}")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_menu_item_details(self, sample_menu_item_id):
        # -----Test fetching specific menu item details
        item = await get_menu_item_details(sample_menu_item_id)

        assert isinstance(item, dict)
        assert item['id'] == sample_menu_item_id
        assert 'name' in item
        assert 'price' in item
        assert 'category' in item
        assert 'is_available' in item

        print(f"  Item details: {item['name']}")
        print(f"  Price: ${item['price']}")
        print(f"  Category: {item['category']}")
        print(f"  Available: {item['is_available']}")


# -----(orders_tool)
class TestOrderTools:

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_order_details(self):
        # -----Test fetching order details
        order = await get_order_details(1)

        assert isinstance(order, dict)
        assert order['id'] == 1
        assert 'customer_id' in order
        assert 'status' in order
        assert 'order_type' in order
        assert 'final_amount' in order
        assert 'items' in order

        print(f"  Order #{order['id']}")
        print(f"  Customer ID: {order['customer_id']}")
        print(f"  Status: {order['status']}")
        print(f"  Type: {order['order_type']}")
        print(f"  Amount: ${order['final_amount']}")
        print(f"  Items: {len(order['items'])}")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_orders_by_status(self):
        # -----Test filtering orders by status
        statuses = ['pending', 'confirmed', 'preparing', 'ready',
                    'out_for_delivery', 'delivered', 'cancelled']

        for status in statuses:
            try:
                orders = await get_orders_by_status(status)
                assert isinstance(orders, list)

                for order in orders:
                    assert order['status'] == status

                print(f"  Status '{status}': {len(orders)} orders")
            except Exception as e:
                print(f"  Status '{status}': No orders or error - {e}")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_order_journey(self):
        # -----Test fetching order journey/history
        journey = await get_order_journey(1)

        assert isinstance(journey, list)

        if journey:
            step = journey[0]
            assert 'id' in step
            assert 'status' in step
            assert 'timestamp' in step

            print(f"  Order journey has {len(journey)} steps:")
            for step in journey:
                timestamp = step.get('timestamp', 'N/A')
                status = step.get('status', 'N/A')
                notes = step.get('notes', '')
                print(f"  - {status} at {timestamp}")
                if notes:
                    print(f"    Notes: {notes}")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_customer_orders(self, sample_customer_id):
        # -----Test fetching all orders for a customer
        orders = await get_customer_orders(sample_customer_id)

        assert isinstance(orders, list)

        for order in orders:
            assert order['customer_id'] == sample_customer_id

        print(f"  Customer {sample_customer_id} has {len(orders)} orders")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_filtered_orders(self):
        # -----Test advanced order filtering
        # -----Filter by status
        pending_orders = await get_filtered_orders(status='pending')
        assert isinstance(pending_orders, list)
        print(f"  Filtered by status: {len(pending_orders)} pending orders")

        # -----Filter by order type
        delivery_orders = await get_filtered_orders(order_type='delivery')
        assert isinstance(delivery_orders, list)
        print(f"  Filtered by type: {len(delivery_orders)} delivery orders")

        # -----Filter by amount range
        affordable_orders = await get_filtered_orders(
            min_amount=0,
            max_amount=50
        )
        assert isinstance(affordable_orders, list)
        print(f"  Filtered by amount: {len(affordable_orders)} orders under $50")

        # -----Pagination
        first_page = await get_filtered_orders(skip=0, limit=5)
        assert isinstance(first_page, list)
        assert len(first_page) <= 5
        print(f"  Pagination: {len(first_page)} orders in first page")


# -----(customer_tool)
class TestCustomerTools:

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_customer_profile(self, sample_customer_id):
        # -----Test fetching customer profile
        customer = await get_customer_profile(sample_customer_id)

        assert isinstance(customer, dict)
        assert customer['id'] == sample_customer_id
        assert 'email' in customer
        assert 'first_name' in customer
        assert 'last_name' in customer

        print(f"  Customer profile:")
        print(f"  Name: {customer['first_name']} {customer['last_name']}")
        print(f"  Email: {customer['email']}")
        print(f"  Phone: {customer.get('phone', 'N/A')}")
        print(f"  Address: {customer.get('address', 'N/A')}")


# -----(analytics_tool)
class TestAnalyticsTools:

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_dashboard_stats(self):
        # -----Test fetching dashboard statistics
        stats = await get_dashboard_stats()

        assert isinstance(stats, dict)
        assert 'todays_orders_count' in stats
        assert 'todays_revenue' in stats
        assert 'pending_orders_count' in stats
        assert 'completed_today_count' in stats
        assert 'average_order_value' in stats

        print(f"  Dashboard Statistics:")
        print(f"  Today's orders: {stats['todays_orders_count']}")
        print(f"  Today's revenue: ${stats['todays_revenue']}")
        print(f"  Pending orders: {stats['pending_orders_count']}")
        print(f"  Completed today: {stats['completed_today_count']}")
        print(f"  Avg order value: ${stats['average_order_value']}")
        print(f"  Total pending: {stats.get('pending_orders_total', 'N/A')}")
        print(f"  Total completed: {stats.get('completed_orders_total', 'N/A')}")

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_popular_items(self):
        # -----Test fetching popular items
        # -----Test with different time ranges
        today = await get_popular_items(limit=5, days=1)
        week = await get_popular_items(limit=10, days=7)
        month = await get_popular_items(limit=15, days=30)

        for period, items, days in [
            ('Today', today, 1),
            ('This Week', week, 7),
            ('This Month', month, 30)
        ]:
            assert isinstance(items, list)
            print(f"\n Popular Items - {period} (last {days} days):")

            for i, item in enumerate(items, 1):
                name = item.get('menu_item_name', 'N/A')
                count = item.get('order_count', 0)
                quantity = item.get('total_quantity', 0)
                rank = item.get('rank', i)

                print(f"  {rank}. {name}")
                print(f"     Orders: {count}, Total Qty: {quantity}")


# -----(promos_tool)
class TestPromoTools:

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_apply_promo_code(self):
        # -----Test applying promo codes
        result = await apply_promo_code("TESTCODE123", 100.0)

        assert isinstance(result, dict)
        assert 'valid' in result
        assert 'discount_amount' in result
        assert 'final_amount' in result

        print(f"✓ Promo code test:")
        print(f"  Valid: {result['valid']}")
        print(f"  Discount: ${result.get('discount_amount', 0)}")
        print(f"  Final: ${result.get('final_amount', 0)}")
        print(f"  Message: {result.get('message', 'N/A')}")


# -----(error_handling)
class TestErrorHandling:

    @pytest.mark.asyncio
    async def test_get_nonexistent_order(self):
        # -----Test fetching a non-existent order
        with pytest.raises(Exception):
            await get_order_details(999999)
        print(" Correctly raises exception for non-existent order")

    @pytest.mark.asyncio
    async def test_get_nonexistent_menu_item(self):
        # -----Test fetching a non-existent menu item
        with pytest.raises(Exception):
            await get_menu_item_details(999999)
        print(" Correctly raises exception for non-existent menu item")

    @pytest.mark.asyncio
    async def test_get_nonexistent_customer(self):
        # -----Test fetching a non-existent customer
        with pytest.raises(Exception):
            await get_customer_profile(999999)
        print(" Correctly raises exception for non-existent customer")

# ------(manual_test_runner)
async def run_manual_tests():
    """
    Manual test runner for quick verification.

    Usage:
        uv run python tests/test_server.py
    """
    print("\n" + "=" * 60)
    print("RESTAURANT BACKEND MCP - MANUAL TEST SUITE")
    print("=" * 60)
    print(f"\nBackend URL: {settings.backend_url}")
    print("Make sure your FastAPI backend is running!\n")

    # -----Test Health
    print("\n" + "=" * 60)
    print("TEST 1: HEALTH CHECK")
    print("=" * 60)
    try:
        health = await check_backend_health()
        print(f" Backend is healthy: {health}")
    except Exception as e:
        print(f" Health check failed: {e}")
        return

    # -----Test Menu Items
    print("\n" + "=" * 60)
    print("TEST 2: MENU ITEMS")
    print("=" * 60)
    try:
        items = await get_menu_items()
        print(f" Found {len(items)} menu items")
        if items:
            item = items[0]
            print(f"  Sample: {item['name']} - ${item['price']}")

            # -----Test get details
            details = await get_menu_item_details(item['id'])
            print(f" Got details for: {details['name']}")
    except Exception as e:
        print(f" Menu test failed: {e}")

    # -----Test Orders
    print("\n" + "=" * 60)
    print("TEST 3: ORDERS")
    print("=" * 60)
    try:
        order = await get_order_details(1)
        print(f"  Order #{order['id']} retrieved")
        print(f"  Status: {order['status']}")
        print(f"  Amount: ${order['final_amount']}")

        # -----Test journey
        journey = await get_order_journey(1)
        print(f" Order journey has {len(journey)} steps")
    except Exception as e:
        print(f" Order test failed: {e}")

    # -----Test Dashboard Stats
    print("\n" + "=" * 60)
    print("TEST 4: ANALYTICS")
    print("=" * 60)
    try:
        stats = await get_dashboard_stats()
        print(f"  Dashboard stats:")
        print(f"  Today's orders: {stats['todays_orders_count']}")
        print(f"  Today's revenue: ${stats['todays_revenue']}")

        # -----Test popular items
        popular = await get_popular_items(limit=5)
        print(f"  Top {len(popular)} popular items")
    except Exception as e:
        print(f"  Analytics test failed: {e}")

    print("\n" + "=" * 60)
    print("MANUAL TESTS COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    # -----Run manual tests
    asyncio.run(run_manual_tests())