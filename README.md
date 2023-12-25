API Documentation
---------------------------------------------------------------------------------------------------------------------------------

Project Setup -
--------------------------------------------------------------------------------------------------------------------------------
1) - # First navigate to the directory containing filename "manage.py" in the project folder then open terminal(command prompt) on this path.

2) - # Install modules using pip(type below command in command prompt).
    pip install -r requirements.txt

3) - # Now run project using following command in the same command prompt.
    python manage.py runserver

4) - # Now open postman and test api endpoints.

--------------------------------------------------------------------------------------------------------------------------------
Overview

This documentation provides details about the API endpoints exposed by the application.
The API allows users to perform operations related to vendors and purchase orders.

---------------------------------------------------------------------------------------------------------------------------------
Authentication

All endpoints require authentication. Users must include a valid access token in the request headers(Bearer token in authorization section of postman).

Base URL
The base URL for all API endpoints is http://127.0.0.1:8000.

API Endpoints - 

1. Authentication

    1.1 Obtain Access Token
    Endpoint:  /api/token/
    Description: Obtain an access token.
    Request:POST
    Body:
    {
     "username":"vishal",
     "password":"vishal123"
    }

    Response:
    {
    "refresh": "your_access_token",
    "access": "Bearer"
    }

    Note 1:  above username and password is defaut. one can create separate user using command "python manage.py createsuperuser" in the   same terminal(command prompt).

    Note 2: Include access token in authorization section(Bearer token section) in postman to access all endpoints.
    

    1.2 Refresh Access Token
    Endpoint:  /api/token/refresh/
    Description: Refresh an access token.
    Request(POST):
    {
    "refresh": "your_refresh_token"
    }

    Response:
    {
    "access_token": "your_new_access_token",
    "token_type": "Bearer",
    "expires_in": 3600
    }



2. Vendors

    ---------------------------------------------------------------------------------------------
    2.1  Create Vendors
    Endpoint:  /api/vendors/
    Description:  create a new vendor.
    Permissions: User must be authenticated.

    Request Body(POST):
    {
    "name": "Vendor Name",
    "contact_details": "Contact Details",
    "address": "Vendor Address",
    "vendor_code": "Unique Vendor Code"
    }

    ---------------------------------------------------------------------------------------------
    2.2 List all Vendors
    Endpoint:  /api/vendors/
    Description: List all vendors .
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    Request: GET
    Body: None
    Response:
    [
    {
    "id": ,
    "name": "",
    "contact_details": "",
    "address": "Mumbai",
    "vendor_code": "",
    "on_time_delivery_rate": 0.0,
    "quality_rating_avg": 0.0,
    "average_response_time": 0.0,
    "fulfillment_rate": 0.0
}
    ...
    ]

    2.3 Retrieve Vendor
    Endpoint:  /api/vendors/<int:pk>/
    Description: Retrieve a specific vendor by ID.
    Permissions: User must be authenticated.
    Request(GET):  /api/vendors/1/
    Body: None

    Response :
    {
    "id": 1,
    "name": "Farhan Akhtar",
    "contact_details": "9548545752",
    "address": "New Mumbai",
    "vendor_code": "vendor1",
    "on_time_delivery_rate": 0.3333333333333333,
    "quality_rating_avg": 4.75,
    "average_response_time": 96.0,
    "fulfillment_rate": 1.0
    }

    -------------------------------------------------------------------------------------------
    2.3 Update Vendor
    Endpoint:  /api/vendors/<int:pk>/
    Description:  update a specific vendor by ID.
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    Request: PUT

    Body:
    {        
        "name": "Salim Sheikh",
        "contact_details": "9548452154",
        "address": "Pune",
        "vendor_code": "vendor4",
        "on_time_delivery_rate": 0.0,
        "quality_rating_avg": 0.0,
        "average_response_time": 0.0,
        "fulfillment_rate": 0.0
    }

    Response:
    {
    "id": 4,
    "name": "Salim Sheikh",
    "contact_details": "9548452154",
    "address": "Pune",
    "vendor_code": "vendor4",
    "on_time_delivery_rate": 0.0,
    "quality_rating_avg": 0.0,
    "average_response_time": 0.0,
    "fulfillment_rate": 0.0
    }
    ------------------------------------------------------------------------------------------
    2.4 Delete Vendor
    Endpoint:  /api/vendors/<int:pk>/
    Description:  Delete a specific vendor by ID.
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    
    Request(DELETE): /api/vendors/4/
    Response: 204 No Content

    ------------------------------------------------------------------------------------------
3. Purchase Orders
    3.1 Create Purchase Orders
    Endpoint:  /api/purchase_orders/
    Description:  create a new purchase order.
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    Request Body(POST):
    {
    "vendor": 1,  
    "po_number": "PO7",
    "order_date": "2023-12-25",
    "delivery_date": "2023-12-30",
    "items": [items in json format],
    "quantity": 10,
    "status": "pending",
    "quality_rating": null,
    "issue_date": "2023-11-30",
    "acknowledgment_date": null
    }


    Response:
    {
    "id": 7,
    "po_number": "PO7",
    "order_date": "2023-12-25T00:00:00Z",
    "delivery_date": "2023-12-30T00:00:00Z",
    "items": [items],
    "quantity": 10,
    "status": "pending",
    "quality_rating": null,
    "issue_date": "2023-11-30T00:00:00Z",
    "acknowledgment_date": null,
    "vendor": 1
    }
    --------------------------------------------------------------------------------------------
    3.2 List all Purchase Orders
    Endpoint:  /api/purchase_orders/
    Description:  List all purchase order.
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    Request:POST /api/purchase_orders/
    Body: None
    Response: List of Purchase orders
    ---------------------------------------------------------------------------------------------

    3.3 Retrieve Purchase Order By po_number
    Endpoint:  /api/purchase_orders/<str:po_number>/
    Description: Retrieve a specific purchase order by PO number.
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    Request(GET):  /api/purchase_orders/PO7/
    Body: None
    Response : PO7 Purchase Order Details
    ---------------------------------------------------------------------------------------------
    3.4  Update Purchase Order By po_number
    Endpoint:  /api/purchase_orders/<str:po_number>/
    Description: Update a specific purchase order by PO number.
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    Request(PUT):  /api/purchase_orders/PO7/
    Body:
    { 
    "po_number": "PO7",
    "order_date": "2023-12-25T00:00:00Z",
    "delivery_date": "2023-12-30T00:00:00Z",
    "items": [items],
    "quantity": 15,
    "status": "pending",
    "quality_rating": null,
    "issue_date": "2023-11-30T00:00:00Z",
    "acknowledgment_date": null,
    "vendor": 1
    }
    Response : Updated Purchase Order Details


    -----------------------------------------------------------------------------------------------
    3.5  Delete Purchase Order By po_number
    Endpoint:  /api/purchase_orders/<str:po_number>/
    Description: Delete a specific purchase order by PO number.
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    Request(PUT):  /api/purchase_orders/PO7/
    Body: None
    Response: 204 No Content
    
    -----------------------------------------------------------------------------------------------

    3.6 Acknowledge Purchase Order
    Endpoint:  /api/purchase_orders/<str:po_number>/acknowledge/
    Description: Acknowledge a specific purchase order.
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    Request: PUT  /api/purchase_orders/PO2/acknowledge/
    Body:
    {
    "id": 2,
    "po_number": "PO2",
    "order_date": "2023-11-30",
    "delivery_date": "2023-12-05",
    "items": [items in json format],
    "quantity": 10,
    "status": "completed",
    "quality_rating": null,
    "issue_date": "2023-11-30",
    "acknowledgment_date": "2023-12-03",
    "vendor": 1
    }

    ------------------------------------------------------------------------------------------
4. Vendor Performance
    4.1 Retrieve Vendor Performance Metrics
    Endpoint:  /api/vendors/<int:id>/performance/
    Description: Retrieve performance metrics of a specific vendor.
    Permissions: User must be authenticated(add access token in "Bearer token" in Authorization section).
    Request: GET
    Body: None
    Response Example:
    {
    "on_time_delivery_rate": 95.2,
    "quality_rating_avg": 4.5,s
    "average_response_time": 15.3,
    "fulfillment_rate": 98.7
    }

    Note : To get performance metrics at realtime use websocket in postman then hit below url to connect.

    websocket url -  ws://localhost:8000/api/vendors/<int:vendor_id>/performance/


