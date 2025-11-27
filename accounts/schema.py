from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CustomCookieAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "accounts.authenticate.CustomCookieAuthentication"
    name = "cookieAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "cookie",
            "name": "access_token",
        }
