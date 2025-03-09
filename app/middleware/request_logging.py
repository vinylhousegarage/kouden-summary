from flask import request, g, Response

def setup_request_logging(app):

    @app.before_request
    def log_request_info():
        g.request_body = request.get_data(as_text=True)
        app.logger.info(f"Request: {request.method} {request.url}")
        app.logger.info(f"Request Headers: {dict(request.headers)}")
        app.logger.info(f"Request Body: {g.request_body}")

    @app.after_request
    def log_response_info(response: Response):
        response_body = response.get_data(as_text=True)

        if not app.debug and len(response_body) > 500:
            response_body = response_body[:500] + "..."

        app.logger.info(f"Response: {response.status}")
        app.logger.info(f"Response Headers: {dict(response.headers)}")
        app.logger.info(f"Response Body: {response_body}")
        return response
