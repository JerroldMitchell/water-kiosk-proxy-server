# Appwrite Proxy Server

A secure proxy server that allows students to access Appwrite without needing to know the API key.

## Purpose

This proxy server sits between students and Appwrite, automatically adding authentication credentials to requests. Students don't need to know the API key - they simply make HTTP requests to the proxy.

## Features

- ✅ Automatically adds API key to all Appwrite requests
- ✅ Restricts access to allowed collections only (currently: `customers`)
- ✅ Validates database and collection IDs
- ✅ Validates required fields for customer creation
- ✅ Supports full CRUD operations
- ✅ Comprehensive logging and error handling
- ✅ Simple JSON responses

## Prerequisites

- Python 3.7+
- Appwrite running at `http://localhost/v1`
- Flask 3.0.0

## Installation

1. **Create virtual environment**:
```bash
python3 -m venv proxy_env
source proxy_env/bin/activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Running the Server

### Quick Start

```bash
./start_proxy.sh
```

This starts the proxy server on port 3000 (default).

### Manual Start

```bash
python3 appwrite_proxy.py
```

### Custom Port

```bash
PORT=9000 python3 appwrite_proxy.py
```

## Accessing from Students

### Configure ngrok (on your home server)

The proxy server needs to be exposed via ngrok. Add this to your `~/.config/ngrok/ngrok.yml`:

```yaml
proxy:
  proto: http
  addr: 3000
  domain: your-domain.ngrok-free.app
```

Then run:
```bash
ngrok start proxy
```

### Students can then access:

**Get all customers:**
```bash
curl https://your-domain.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents
```

**Create a customer:**
```bash
curl -X POST https://your-domain.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents \
  -H "Content-Type: application/json" \
  -d '{
    "documentId": "unique()",
    "data": {
      "phone_number": "+254700000123",
      "pin": "1234",
      "full_name": "John Doe",
      "is_registered": true,
      "active": true
    }
  }'
```

**Get a specific customer:**
```bash
curl https://your-domain.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents/DOCUMENT_ID
```

**Update a customer:**
```bash
curl -X PATCH https://your-domain.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents/DOCUMENT_ID \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "credits": 50,
      "active": false
    }
  }'
```

**Delete a customer:**
```bash
curl -X DELETE https://your-domain.ngrok-free.app/v1/databases/6864aed388d20c69a461/collections/customers/documents/DOCUMENT_ID
```

## Supported Endpoints

- `GET /` - Status page with available endpoints
- `GET /v1/databases/{db_id}/collections/customers/documents` - List all customers
- `POST /v1/databases/{db_id}/collections/customers/documents` - Create a customer
- `GET /v1/databases/{db_id}/collections/customers/documents/{doc_id}` - Get specific customer
- `PATCH /v1/databases/{db_id}/collections/customers/documents/{doc_id}` - Update a customer
- `DELETE /v1/databases/{db_id}/collections/customers/documents/{doc_id}` - Delete a customer

## Customer Data Fields

When creating or updating a customer, use these fields in the `data` object:

```json
{
  "phone_number": "string (required)",
  "pin": "string",
  "full_name": "string",
  "is_registered": "boolean",
  "active": "boolean",
  "credits": "integer",
  "account_id": "string",
  "created_at": "string",
  "registration_state": "string"
}
```

## Configuration

Environment variables (optional):

```bash
APPWRITE_ENDPOINT=http://localhost/v1
APPWRITE_PROJECT_ID=689107c288885e90c039
APPWRITE_DATABASE_ID=6864aed388d20c69a461
APPWRITE_API_KEY=<your-api-key>
PORT=3000
```

## Security Features

- ✅ API key is never exposed to students
- ✅ Only allows access to `customers` collection
- ✅ Validates database and collection IDs
- ✅ Validates required fields for creation
- ✅ All requests logged with timestamps
- ✅ Proper HTTP error codes and messages

## Logging

The server logs all requests with timestamp, method, and path:

```
2024-11-09 12:34:56,789 - INFO - GET /v1/databases/6864aed388d20c69a461/collections/customers/documents
2024-11-09 12:35:01,234 - INFO - Created document in customers
2024-11-09 12:35:15,567 - ERROR - Collection "invalid" is not allowed
```

## Troubleshooting

### "Connection refused" to Appwrite
- Verify Appwrite is running: `docker ps | grep appwrite`
- Check Appwrite is on port 80: `lsof -i :80`
- Restart Appwrite if needed

### "Invalid API key"
- Verify `APPWRITE_API_KEY` environment variable
- Check the key in your Appwrite dashboard

### Port already in use
- Change PORT: `PORT=3001 python3 appwrite_proxy.py`
- Or kill the process: `kill -9 $(lsof -t -i :3000)`

### ngrok tunnel not connecting
- Verify proxy is running on correct port
- Check ngrok configuration in `~/.config/ngrok/ngrok.yml`
- Verify ngrok is running: `ngrok start proxy`

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Future Enhancements

- [ ] Rate limiting per student
- [ ] Student API keys for tracking usage
- [ ] Support for additional collections
- [ ] Query validation and sanitization
- [ ] Request/response caching
- [ ] Metrics and analytics dashboard

## License

This tool is provided as-is for the Water Kiosk Dashboard project.
