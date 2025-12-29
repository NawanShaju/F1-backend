from flask import jsonify, make_response

"""
Create standardized API response

Args:
    result: Query result (list or dict) or None
    msg: Error message if result is None
    
Returns:
    Flask response with appropriate status code
"""
def create_response(result, msg=None):
    if result is None:
        return make_response(jsonify({'error': msg or 'Internal server error'}), 500)
    elif len(result) == 0:
        return make_response(jsonify({'error': 'Data not available'}), 404)
    
    return make_response(jsonify(result), 200)