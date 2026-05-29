# Odoo Sales Order Automation

## Overview

This module automates the complete sales workflow in Odoo using a single button from the Sales Order form.

The automation process integrates multiple Odoo modules:

* Sales
* Inventory
* Accounting
* Payments

The goal of this module is to simplify the entire sales cycle and reduce manual operations.

---

# Features

## Sales Order Automation

A new button called:

```text
Automate Sale Order
```

is added to the Sales Order form.

The button appears only when the Sales Order is in quotation state.

---

# Automated Workflow

When the user clicks the automation button, the system automatically performs the following actions:

## 1. Confirm Sales Order

The quotation is confirmed programmatically using the standard Odoo workflow.

```python
self.action_confirm()
```

---

## 2. Validate Delivery Orders

The system automatically:

* Retrieves related delivery orders
* Reserves stock quantities
* Sets delivered quantities
* Validates transfers

```python
picking.action_assign()
picking.button_validate()
```

---

## 3. Create Customer Invoice

Customer invoices are created automatically from the Sales Order.

```python
self._create_invoices()
```

---

## 4. Post Invoice

The generated invoice is posted automatically.

```python
invoices.action_post()
```

---

## 5. Register Payment

The system automatically creates and registers customer payments using the Odoo payment registration wizard.

```python
account.payment.register
```

The invoice payment state becomes:

```text
Paid
```

---

# Validation Rules

The module validates the following cases before processing:

* No customer selected
* No products added
* Insufficient stock availability
* No payment journal available

Validation errors are raised using:

```python
ValidationError
```

---

# Technical Details

## Implemented Using Standard Odoo Methods

The module follows Odoo standard workflows and avoids direct SQL queries.

### Main Methods Used

| Method                     | Purpose             |
| -------------------------- | ------------------- |
| `action_confirm()`         | Confirm Sales Order |
| `action_assign()`          | Reserve stock       |
| `button_validate()`        | Validate delivery   |
| `_create_invoices()`       | Create invoices     |
| `action_post()`            | Post invoice        |
| `action_create_payments()` | Register payment    |

---

# Inventory Flow

The module works with:

* `stock.picking`
* `stock.move`

Each delivery order may contain multiple stock moves depending on the ordered products.

---

# Modules Required

* sale_management
* stock
* account

---

# Odoo Version

Developed and tested on:

```text
Odoo 17
```

---

# Installation

1. Copy the module into the custom addons folder
2. Restart Odoo server
3. Update Apps List
4. Install the module

---

# Example Workflow

```text
Quotation
    ↓
Confirm Sales Order
    ↓
Create Delivery Order
    ↓
Reserve Products
    ↓
Validate Delivery
    ↓
Create Invoice
    ↓
Post Invoice
    ↓
Register Payment
    ↓
Invoice Paid
```

---

# Author

Salah Haitham
