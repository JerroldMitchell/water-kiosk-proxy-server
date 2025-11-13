# Appwrite Database Access Guide for Purdue Students

Welcome! This guide explains how to access the Tusafishe Water Kiosk database for the dashboard development project.

## Quick Start

### 1. Get the Endpoint URL

Ask your supervisor for the ngrok endpoint URL. It will look like:
```
https://xxxxx-xxxxx-xxxxx.ngrok-free.app
```

### 2. Test Your Connection

Open a terminal and run:
```bash
curl https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents
```

You should get back a JSON response with customer data.

## CRUD Operations

All examples use `YOUR_ENDPOINT_URL` - replace with the actual ngrok URL provided.

### 1. CREATE - Add a New Customer

```bash
curl -X POST https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents \
  -H "Content-Type: application/json" \
  -d '{
    "documentId": "unique()",
    "data": {
      "phone_number": "+254700000123",
      "pin": "1234",
      "full_name": "Jane Smith",
      "is_registered": true,
      "active": true,
      "credits": 100,
      "account_id": "TSF123456"
    }
  }'
```

**Response:** Returns the created customer document with unique ID.

### 2. READ - Get All Customers

```bash
curl https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents
```

**Response:** Returns a JSON array of all customers.

### 3. READ - Get a Specific Customer

First, you need the customer's document ID. You can get this from the LIST response above.

```bash
curl https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents/DOCUMENT_ID
```

Replace `DOCUMENT_ID` with the actual ID from the response.

**Example:**
```bash
curl https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents/66a1234567890abcdef123
```

### 4. UPDATE - Modify a Customer

```bash
curl -X PATCH https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents/DOCUMENT_ID \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "credits": 50,
      "active": false,
      "full_name": "Jane Doe Updated"
    }
  }'
```

You only need to include the fields you want to change.

### 5. DELETE - Remove a Customer

```bash
curl -X DELETE https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents/DOCUMENT_ID
```

## Customer Fields Reference

When creating or updating customers, you can use these fields:

| Field | Type | Example | Notes |
|-------|------|---------|-------|
| `phone_number` | String | `"+254700000123"` | **Required for creation** |
| `pin` | String | `"1234"` | 4-digit PIN for kiosk access |
| `full_name` | String | `"John Doe"` | Customer's name |
| `is_registered` | Boolean | `true` | Registration completion status |
| `active` | Boolean | `true` | Current subscription status |
| `credits` | Integer | `100` | Water credits balance |
| `account_id` | String | `"TSF123456"` | Generated account identifier |
| `created_at` | String | ISO timestamp | Auto-generated |
| `registration_state` | String | `"completed"` | Current registration step |

## Using in Your Code

### JavaScript/Node.js Example

```javascript
const endpoint = 'https://YOUR_ENDPOINT_URL';
const dbId = '6864aed388d20c69a461';
const collectionId = 'customers';

// Get all customers
fetch(`${endpoint}/v1/databases/${dbId}/collections/${collectionId}/documents`)
  .then(response => response.json())
  .then(data => console.log(data));

// Create a customer
fetch(`${endpoint}/v1/databases/${dbId}/collections/${collectionId}/documents`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    documentId: 'unique()',
    data: {
      phone_number: '+254700000123',
      pin: '1234',
      full_name: 'Student Test',
      is_registered: true,
      active: true
    }
  })
})
.then(response => response.json())
.then(data => console.log('Created:', data));
```

### Python Example

```python
import requests
import json

endpoint = 'https://YOUR_ENDPOINT_URL'
db_id = '6864aed388d20c69a461'
collection_id = 'customers'

# Get all customers
url = f'{endpoint}/v1/databases/{db_id}/collections/{collection_id}/documents'
response = requests.get(url)
print(response.json())

# Create a customer
headers = {'Content-Type': 'application/json'}
data = {
    'documentId': 'unique()',
    'data': {
        'phone_number': '+254700000456',
        'pin': '5678',
        'full_name': 'Another Student',
        'is_registered': True,
        'active': True
    }
}
response = requests.post(url, headers=headers, json=data)
print('Created:', response.json())
```

### React Example

```javascript
import { useState, useEffect } from 'react';

function CustomerDashboard() {
  const [customers, setCustomers] = useState([]);
  const endpoint = 'https://YOUR_ENDPOINT_URL';
  const dbId = '6864aed388d20c69a461';
  const collectionId = 'customers';

  useEffect(() => {
    fetch(`${endpoint}/v1/databases/${dbId}/collections/${collectionId}/documents`)
      .then(res => res.json())
      .then(data => setCustomers(data.documents));
  }, []);

  return (
    <div>
      <h1>Customers: {customers.length}</h1>
      <ul>
        {customers.map(customer => (
          <li key={customer.$id}>
            {customer.full_name} ({customer.phone_number})
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Important Notes

### ✅ What You Have

- ✅ Full read/write access to the `customers` collection
- ✅ No API key needed - the proxy handles authentication
- ✅ Complete CRUD capability for database testing
- ✅ Real data that reflects actual dashboard usage

### ⚠️ What You Cannot Do

- ❌ Access other collections (only `customers` is allowed)
- ❌ Delete the database
- ❌ Access other Appwrite services
- ❌ See the actual API key (it's hidden by the proxy)

### 🔒 Security

- Your requests are proxied through a secure server
- The API key is never exposed
- All changes are logged
- The connection is encrypted (HTTPS)

## Troubleshooting

### "Connection refused"
- Make sure the endpoint URL is correct
- Ask your supervisor to verify ngrok is running
- Try the endpoint in your browser first

### "Invalid request"
- Check you're using the correct HTTP method (GET, POST, PATCH, DELETE)
- Verify your JSON syntax is correct
- Make sure required fields are included

### "Collection not found"
- Double-check the database ID and collection ID
- They should be:
  - Database: `6864aed388d20c69a461`
  - Collection: `customers`

### "Document not found" (when getting/updating/deleting)
- The document ID might not exist
- List all documents first to find valid IDs
- Document IDs are in the `$id` field of responses

## Need Help?

- Check the main README.md in the proxy_server directory
- Ask your supervisor (me!)
- Review the examples above and adapt them for your use case

## Common Workflows

### Workflow 1: Create Test Data

```bash
# Create 3 test customers
for i in {1..3}; do
  curl -X POST https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents \
    -H "Content-Type: application/json" \
    -d "{
      \"documentId\": \"unique()\",
      \"data\": {
        \"phone_number\": \"+2547000001$i\",
        \"pin\": \"1234\",
        \"full_name\": \"Test Customer $i\",
        \"is_registered\": true,
        \"active\": true,
        \"credits\": 100
      }
    }"
done
```

### Workflow 2: Update Customer Status

```bash
# Get a customer ID first
curl https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents

# Copy the $id from response, then update
CUSTOMER_ID="66a1234567890abcdef123"
curl -X PATCH https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents/$CUSTOMER_ID \
  -H "Content-Type: application/json" \
  -d '{"data": {"active": false, "credits": 25}}'
```

### Workflow 3: Export Customer List to CSV

```bash
curl https://YOUR_ENDPOINT_URL/v1/databases/6864aed388d20c69a461/collections/customers/documents \
  | jq -r '.documents[] | [.phone_number, .full_name, .credits, .active] | @csv' \
  > customers.csv
```

## Questions?

Reach out to your supervisor for:
- Endpoint URL changes
- Access issues
- Data format questions
- Integration help

Happy coding! 🚀
