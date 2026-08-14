"""Trusted SQLite datasets for AI-authored SQL practice drills.

The AI is told only the schema description below.  It may propose a read-only
reference query, but it never supplies table setup or fixture data: that comes
exclusively from this small, version-controlled catalogue.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Final


@dataclass(frozen=True)
class SqlFixture:
    """One independent, server-only dataset for a schema family."""

    id: str
    label: str
    setup_sql: str


@dataclass(frozen=True)
class SqlSchemaFamily:
    """A fixed schema contract safe to show to a model or learner."""

    id: str
    topics: tuple[str, ...]
    visible_schema: str
    fixtures: tuple[SqlFixture, ...]

    @property
    def server_only_setups(self) -> tuple[str, ...]:
        """Static setup SQL used for judging; do not add this to AI prompts."""
        return tuple(fixture.setup_sql for fixture in self.fixtures)


EMPLOYEES: Final = SqlSchemaFamily(
    id="employees",
    topics=("employees", "staff", "salary", "departments", "teams"),
    visible_schema=(
        "employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT, "
        "salary INTEGER, hired_on TEXT, manager_id INTEGER)"
    ),
    fixtures=(
        SqlFixture("employees-a", "balanced departments", """
CREATE TABLE employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER, hired_on TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (1,'Ava','Engineering',98000,'2021-03-10',NULL), (2,'Ben','Engineering',76000,'2023-07-01',1),
 (3,'Cora','Sales',72000,'2022-01-18',NULL), (4,'Dylan','Sales',72000,'2024-02-12',3),
 (5,'Eli','Support',54000,'2020-11-25',NULL);
"""),
        SqlFixture("employees-b", "ties and a singleton", """
CREATE TABLE employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER, hired_on TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (11,'Farah','Design',88000,'2022-05-09',NULL), (12,'Gus','Design',88000,'2023-10-14',11),
 (13,'Hana','Engineering',105000,'2019-08-30',NULL), (14,'Ivo','Legal',83000,'2021-12-01',NULL);
"""),
        SqlFixture("employees-c", "small reporting chain", """
CREATE TABLE employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER, hired_on TEXT, manager_id INTEGER);
INSERT INTO employees VALUES
 (21,'June','Operations',69000,'2020-04-20',NULL), (22,'Kai','Operations',61000,'2024-01-05',21),
 (23,'Lena','Operations',61000,'2024-06-15',21), (24,'Moe','Finance',91000,'2021-09-11',NULL);
"""),
    ),
)

ORDERS: Final = SqlSchemaFamily(
    id="orders",
    topics=("orders", "customers", "sales", "revenue", "purchases"),
    visible_schema=(
        "customers(id INTEGER PRIMARY KEY, name TEXT, city TEXT); "
        "orders(id INTEGER PRIMARY KEY, customer_id INTEGER, ordered_on TEXT, status TEXT, total_cents INTEGER)"
    ),
    fixtures=(
        SqlFixture("orders-a", "mixed statuses", """
CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, ordered_on TEXT, status TEXT, total_cents INTEGER);
INSERT INTO customers VALUES (1,'Asha','Leeds'),(2,'Bo','York'),(3,'Cai','Leeds'),(4,'Dee','Bath');
INSERT INTO orders VALUES (101,1,'2025-01-03','paid',2599),(102,1,'2025-01-04','refunded',2599),(103,2,'2025-01-05','paid',4500),(104,3,'2025-01-06','pending',1200);
"""),
        SqlFixture("orders-b", "repeat buyer", """
CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, ordered_on TEXT, status TEXT, total_cents INTEGER);
INSERT INTO customers VALUES (10,'Emi','Bristol'),(11,'Finn','York'),(12,'Gia','Bristol');
INSERT INTO orders VALUES (201,10,'2024-12-29','paid',999),(202,10,'2025-02-01','paid',3000),(203,11,'2025-02-02','cancelled',1800);
"""),
        SqlFixture("orders-c", "empty order customer", """
CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(id INTEGER PRIMARY KEY, customer_id INTEGER, ordered_on TEXT, status TEXT, total_cents INTEGER);
INSERT INTO customers VALUES (20,'Hal','Oxford'),(21,'Inez','Oxford'),(22,'Jo','Derby');
INSERT INTO orders VALUES (301,21,'2025-03-10','paid',5000),(302,21,'2025-03-11','paid',5000),(303,22,'2025-03-12','pending',750);
"""),
    ),
)

EVENTS: Final = SqlSchemaFamily(
    id="events",
    topics=("events", "activity", "logs", "analytics", "sessions"),
    visible_schema=(
        "events(id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, occurred_at TEXT, duration_seconds INTEGER)"
    ),
    fixtures=(
        SqlFixture("events-a", "multiple event types", """
CREATE TABLE events(id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, occurred_at TEXT, duration_seconds INTEGER);
INSERT INTO events VALUES (1,1,'login','2025-01-01T09:00:00',0),(2,1,'view','2025-01-01T09:02:00',45),(3,2,'login','2025-01-01T10:00:00',0),(4,2,'purchase','2025-01-01T10:04:00',90),(5,3,'view','2025-01-02T08:00:00',30);
"""),
        SqlFixture("events-b", "repeat activity", """
CREATE TABLE events(id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, occurred_at TEXT, duration_seconds INTEGER);
INSERT INTO events VALUES (11,4,'view','2025-02-04T12:00:00',20),(12,4,'view','2025-02-04T12:05:00',25),(13,4,'logout','2025-02-04T12:06:00',0),(14,5,'login','2025-02-05T07:00:00',0);
"""),
        SqlFixture("events-c", "duration edge cases", """
CREATE TABLE events(id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, occurred_at TEXT, duration_seconds INTEGER);
INSERT INTO events VALUES (21,6,'upload','2025-03-01T11:00:00',300),(22,7,'upload','2025-03-01T11:05:00',300),(23,6,'download','2025-03-01T11:10:00',5),(24,8,'login','2025-03-02T11:00:00',0);
"""),
    ),
)

INVENTORY: Final = SqlSchemaFamily(
    id="inventory",
    topics=("inventory", "products", "stock", "warehouse", "suppliers"),
    visible_schema=(
        "inventory(id INTEGER PRIMARY KEY, sku TEXT, category TEXT, warehouse TEXT, "
        "units_in_stock INTEGER, reorder_level INTEGER, unit_price_cents INTEGER)"
    ),
    fixtures=(
        SqlFixture("inventory-a", "two warehouses", """
CREATE TABLE inventory(id INTEGER PRIMARY KEY, sku TEXT, category TEXT, warehouse TEXT, units_in_stock INTEGER, reorder_level INTEGER, unit_price_cents INTEGER);
INSERT INTO inventory VALUES (1,'PEN-01','office','north',40,15,199),(2,'NOTE-02','office','north',10,20,499),(3,'MUG-01','kitchen','south',8,8,1299),(4,'TEA-03','kitchen','south',30,10,699);
"""),
        SqlFixture("inventory-b", "reorder ties", """
CREATE TABLE inventory(id INTEGER PRIMARY KEY, sku TEXT, category TEXT, warehouse TEXT, units_in_stock INTEGER, reorder_level INTEGER, unit_price_cents INTEGER);
INSERT INTO inventory VALUES (11,'CABLE-1','electronics','east',5,10,899),(12,'MOUSE-2','electronics','east',5,10,2499),(13,'SOAP-1','cleaning','west',22,12,350),(14,'TOWEL-4','cleaning','west',12,12,799);
"""),
        SqlFixture("inventory-c", "category spread", """
CREATE TABLE inventory(id INTEGER PRIMARY KEY, sku TEXT, category TEXT, warehouse TEXT, units_in_stock INTEGER, reorder_level INTEGER, unit_price_cents INTEGER);
INSERT INTO inventory VALUES (21,'LAMP-7','home','north',0,5,3299),(22,'BOOK-9','media','north',18,6,1599),(23,'GAME-4','media','south',6,6,4599),(24,'RUG-2','home','south',14,4,5999);
"""),
    ),
)

SCHEMA_FAMILIES: Final[tuple[SqlSchemaFamily, ...]] = (EMPLOYEES, ORDERS, EVENTS, INVENTORY)


def choose_schema(topic: str | None = None, seed: str | int | None = None) -> SqlSchemaFamily:
    """Choose a deterministic family, preferring an explicitly relevant topic.

    ``seed`` permits varied AI-generated drills while keeping their judge data
    reproducible.  Unknown topics intentionally fall back to all families.
    """
    words = {word for word in (topic or "").lower().replace("_", " ").split() if word}
    candidates = tuple(family for family in SCHEMA_FAMILIES if words.intersection(family.topics)) or SCHEMA_FAMILIES
    digest = sha256(f"{topic or ''}|{seed or ''}".encode("utf-8")).digest()
    return candidates[int.from_bytes(digest[:8], "big") % len(candidates)]


def visible_schema_description(family: SqlSchemaFamily) -> str:
    """Return the only schema text appropriate for an AI-generation prompt."""
    return family.visible_schema

