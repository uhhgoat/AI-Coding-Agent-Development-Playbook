# Example Module Map

This synthetic example demonstrates the expected map shape. It is not an
architecture recommendation.

## Metadata

- Scope: `src/orders/`
- Status: `mapped`
- Verified baseline: `<commit-or-date>`
- Related maps: `payments` only when changing the authorization contract;
  `notifications` only when changing event consumers

## Purpose And Boundaries

The orders module validates order requests, coordinates payment authorization,
persists accepted orders, and publishes the resulting domain event. It does not
implement payment providers or notification delivery.

## Sources Of Truth

| Path or symbol | Why authoritative |
| --- | --- |
| `src/orders/OrderController.*` | Request boundary and response mapping. |
| `src/orders/OrderService.*` | Order workflow and sequencing. |
| `src/orders/OrderRepository.*` | Persistence contract. |
| `src/orders/OrderPlaced.*` | Published event data contract. |

## Nodes

| Node | Responsibility |
| --- | --- |
| `OrderController` | Converts transport requests into order commands. |
| `OrderService` | Validates and coordinates the order workflow. |
| `PaymentPort` | External authorization boundary owned by the payments module. |
| `OrderRepository` | Stores accepted orders. |
| `EventPublisher` | Publishes committed domain events. |
| `OrderPlaced` | Carries the stable order identifier and accepted totals. |

## Connections

| Relationship | Kind | Concise logic |
| --- | --- | --- |
| `OrderController -> OrderService` | `calls` | Delegates one validated transport command and maps the returned result. |
| `OrderService -> PaymentPort` | `calls` | Requests authorization before any order is persisted. |
| `OrderService -> OrderRepository` | `writes` | Persists only an order whose authorization succeeded. |
| `OrderService -> EventPublisher` | `publishes` | Publishes `OrderPlaced` after persistence succeeds, never before. |
| `EventPublisher -> OrderPlaced` | `serializes` | Emits the event contract consumed outside this module. |

## Runtime Flow

1. `OrderController` maps a request to a command.
2. `OrderService` validates it and calls `PaymentPort`.
3. On successful authorization, `OrderRepository` persists the order.
4. After persistence, `EventPublisher` publishes `OrderPlaced`.
5. Authorization or persistence failure stops the remaining steps.

## Change Impact And Validation

- Payment sequencing changes require the payments map and an integration test.
- `OrderPlaced` shape changes require the notification-consumer map and contract
  tests.
- Repository-only changes remain inside this map unless storage configuration
  lives elsewhere.
- Run the focused order workflow tests, then the affected boundary tests.

## Known Gaps

- Replace this sample section with explicit unverified relationships, or write
  `None known at <baseline>`.
