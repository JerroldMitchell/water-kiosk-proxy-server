#!/usr/bin/env python3
"""
Appwrite Proxy Server
Intercepts student requests and automatically adds Appwrite authentication
Students don't need to know the API key
"""

import os
import json
import logging
from flask import Flask, request, jsonify
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
APPWRITE_ENDPOINT = os.environ.get('APPWRITE_ENDPOINT', 'http://localhost/v1')
APPWRITE_PROJECT_ID = os.environ.get('APPWRITE_PROJECT_ID', '689107c288885e90c039')
APPWRITE_API_KEY = os.environ.get('APPWRITE_API_KEY', '0f3a08c2c4fc98480980cbe59cd2db6b8522734081f42db3480ab2e7a8ffd7c46e8476a62257e429ff11c1d6616e814ae8753fb07e7058d1b669c641012941092ddcd585df802eb2313bfba49bf3ec3f776f529c09a7f5efef2988e4b4821244bbd25b3cd16669885c173ac023b5b8a90e4801f3584eef607506362c6ae01c94')
APPWRITE_DATABASE_ID = os.environ.get('APPWRITE_DATABASE_ID', '6864aed388d20c69a461')
CUSTOMERS_COLLECTION_ID = os.environ.get('CUSTOMERS_COLLECTION_ID', 'customers')

# Allowed collections (only customers for now)
ALLOWED_COLLECTIONS = ['customers']

app = Flask(__name__)

# Add CORS headers to all responses
@app.after_request
def add_cors_headers(response):
    """Add CORS headers to allow browser requests from any origin"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, ngrok-skip-browser-warning'
    return response

@app.route('/', methods=['GET', 'OPTIONS'])
def status():
    """Status page"""
    return jsonify({
        'status': 'Appwrite Proxy Server Active',
        'message': 'Students can access Appwrite without needing API key',
        'version': '1.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'status': 'GET / - This status page',
            'list_customers': 'GET /v1/databases/{db_id}/collections/customers/documents',
            'get_customer': 'GET /v1/databases/{db_id}/collections/customers/documents/{doc_id}',
            'create_customer': 'POST /v1/databases/{db_id}/collections/customers/documents',
            'update_customer': 'PATCH /v1/databases/{db_id}/collections/customers/documents/{doc_id}',
            'delete_customer': 'DELETE /v1/databases/{db_id}/collections/customers/documents/{doc_id}'
        }
    })

@app.route('/v1/databases/<database_id>/collections/<collection_id>/documents', methods=['GET', 'POST', 'OPTIONS'])
def handle_documents(database_id, collection_id):
    """Handle GET (list) and POST (create) requests to documents"""

    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        return '', 200

    # Validate collection
    if collection_id not in ALLOWED_COLLECTIONS:
        return jsonify({'error': f'Collection "{collection_id}" is not allowed'}), 403

    # Validate database
    if database_id != APPWRITE_DATABASE_ID:
        return jsonify({'error': 'Invalid database ID'}), 403

    try:
        method = request.method

        # Build Appwrite URL
        appwrite_url = f'{APPWRITE_ENDPOINT}/databases/{database_id}/collections/{collection_id}/documents'

        # Add query parameters if present
        if request.args:
            appwrite_url += '?' + urllib.parse.urlencode(request.args)

        # Prepare headers with API key
        headers = {
            'X-Appwrite-Project': APPWRITE_PROJECT_ID,
            'X-Appwrite-Key': APPWRITE_API_KEY,
            'Content-Type': 'application/json'
        }

        logger.info(f'{method} {appwrite_url}')
        logger.debug(f'Query parameters received: {dict(request.args)}')

        if method == 'GET':
            # Handle GET request (list documents)
            request_obj = urllib.request.Request(appwrite_url, headers=headers)
            response = urllib.request.urlopen(request_obj, timeout=30)
            data = json.loads(response.read().decode('utf-8'))
            return jsonify(data), response.status

        elif method == 'POST':
            # Handle POST request (create document)
            body = request.get_json() or {}

            # Validate required fields for customer creation
            if collection_id == 'customers':
                if 'data' not in body:
                    return jsonify({'error': 'Missing required "data" field'}), 400
                if 'phone_number' not in body['data']:
                    return jsonify({'error': 'Missing required field: phone_number'}), 400

            data = json.dumps(body).encode('utf-8')
            request_obj = urllib.request.Request(appwrite_url, data=data, headers=headers, method='POST')
            response = urllib.request.urlopen(request_obj, timeout=30)
            result = json.loads(response.read().decode('utf-8'))

            logger.info(f'Created document in {collection_id}')
            return jsonify(result), 201

    except urllib.error.HTTPError as e:
        error_data = json.loads(e.read().decode('utf-8'))
        return jsonify(error_data), e.code
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/v1/databases/<database_id>/collections/<collection_id>/documents/<document_id>', methods=['GET', 'PATCH', 'DELETE', 'OPTIONS'])
def handle_document(database_id, collection_id, document_id):
    """Handle GET (retrieve), PATCH (update), and DELETE (remove) requests for specific documents"""

    # Handle CORS preflight requests
    if request.method == 'OPTIONS':
        return '', 200

    # Validate collection
    if collection_id not in ALLOWED_COLLECTIONS:
        return jsonify({'error': f'Collection "{collection_id}" is not allowed'}), 403

    # Validate database
    if database_id != APPWRITE_DATABASE_ID:
        return jsonify({'error': 'Invalid database ID'}), 403

    try:
        method = request.method

        # Build Appwrite URL
        appwrite_url = f'{APPWRITE_ENDPOINT}/databases/{database_id}/collections/{collection_id}/documents/{document_id}'

        # Prepare headers with API key
        headers = {
            'X-Appwrite-Project': APPWRITE_PROJECT_ID,
            'X-Appwrite-Key': APPWRITE_API_KEY,
            'Content-Type': 'application/json'
        }

        logger.info(f'{method} {appwrite_url}')

        if method == 'GET':
            # Handle GET request (retrieve document)
            request_obj = urllib.request.Request(appwrite_url, headers=headers)
            response = urllib.request.urlopen(request_obj, timeout=30)
            data = json.loads(response.read().decode('utf-8'))
            return jsonify(data), response.status

        elif method == 'PATCH':
            # Handle PATCH request (update document)
            body = request.get_json() or {}

            if 'data' not in body:
                return jsonify({'error': 'Missing required "data" field'}), 400

            data = json.dumps(body).encode('utf-8')
            request_obj = urllib.request.Request(appwrite_url, data=data, headers=headers, method='PATCH')
            response = urllib.request.urlopen(request_obj, timeout=30)
            result = json.loads(response.read().decode('utf-8'))

            logger.info(f'Updated document {document_id} in {collection_id}')
            return jsonify(result), 200

        elif method == 'DELETE':
            # Handle DELETE request (remove document)
            request_obj = urllib.request.Request(appwrite_url, headers=headers, method='DELETE')
            response = urllib.request.urlopen(request_obj, timeout=30)

            logger.info(f'Deleted document {document_id} from {collection_id}')
            return jsonify({'success': True, 'message': 'Document deleted'}), 204

    except urllib.error.HTTPError as e:
        try:
            error_data = json.loads(e.read().decode('utf-8'))
            return jsonify(error_data), e.code
        except:
            return jsonify({'error': f'HTTP {e.code}'}), e.code
    except Exception as e:
        logger.error(f'Error: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    logger.info(f'🚀 Appwrite Proxy Server starting on port {port}')
    logger.info(f'📡 Appwrite Endpoint: {APPWRITE_ENDPOINT}')
    logger.info(f'🔐 Project ID: {APPWRITE_PROJECT_ID}')
    app.run(host='0.0.0.0', port=port, debug=False)
