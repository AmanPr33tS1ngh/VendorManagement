# Vendor Management System

This project implements a Vendor Management System with RESTful APIs for vendor and purchase order management, as well as vendor performance evaluation metrics.

## API Endpoints

### Vendors

- **Create Vendor**: `POST /api/vendors/`
- **List All Vendors**: `GET /api/vendors/`
- **Retrieve Vendor**: `GET /api/vendors/{vendor_id}/`
- **Update Vendor**: `PUT /api/vendors/{vendor_id}/`
- **Delete Vendor**: `DELETE /api/vendors/{vendor_id}/`

### Purchase Orders

- **Create Purchase Order**: `POST /api/purchase_orders/`
- **List All Purchase Orders**: `GET /api/purchase_orders/`
- **Retrieve Purchase Order**: `GET /api/purchase_orders/{po_id}/`
- **Update Purchase Order**: `PUT /api/purchase_orders/{po_id}/`
- **Delete Purchase Order**: `DELETE /api/purchase_orders/{po_id}/`

### Vendor Performance Evaluation

- **Retrieve Vendor Performance Metrics**: `GET /api/vendors/{vendor_id}/performance`

## Model Design

### Vendor Model

- **Fields**:
  - `name`: Vendor's name (CharField)
  - `contact_details`: Contact information of the vendor (TextField)
  - `address`: Physical address of the vendor (TextField)
  - `vendor_code`: Unique identifier for the vendor (CharField)
  - `on_time_delivery_rate`: Percentage of on-time deliveries (FloatField)
  - `quality_rating_avg`: Average rating of quality based on purchase orders (FloatField)
  - `average_response_time`: Average time taken to acknowledge purchase orders (FloatField)
  - `fulfillment_rate`: Percentage of purchase orders fulfilled successfully (FloatField)

### Purchase Order (PO) Model

- **Fields**:
  - `po_number`: Unique number identifying the PO (CharField)
  - `vendor`: ForeignKey linking to Vendor model
  - `order_date`: Date when the order was placed (DateTimeField)
  - `delivery_date`: Expected or actual delivery date of the order (DateTimeField)
  - `items`: Details of items ordered (JSONField)
  - `quantity`: Total quantity of items in the PO (IntegerField)
  - `status`: Current status of the PO (CharField)
  - `quality_rating`: Rating given to the vendor for this PO (FloatField)
  - `issue_date`: Timestamp when the PO was issued to the vendor (DateTimeField)
  - `acknowledgment_date`: Timestamp when the vendor acknowledged the PO (DateTimeField, nullable)

### Historical Performance Model

- **Fields**:
  - `vendor`: ForeignKey linking to Vendor model
  - `date`: Date of the performance record (DateTimeField)
  - `on_time_delivery_rate`: Historical record of on-time delivery rate (FloatField)
  - `quality_rating_avg`: Historical record of quality rating average (FloatField)
  - `average_response_time`: Historical record of average response time (FloatField)
  - `fulfillment_rate`: Historical record of fulfillment rate (FloatField)

## Usage

1. Ensure you have Django installed and set up the project environment.
2. Start the Django development server.
3. Use tools like `curl`, `Postman`, or write scripts in Python using `requests` library to interact with the API endpoints.
