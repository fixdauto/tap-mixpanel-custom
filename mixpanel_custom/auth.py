"""mixpanel_custom Authentication."""


from singer_sdk.authenticators import SimpleAuthenticator


class mixpanel_customAuthenticator(SimpleAuthenticator):
    """Authenticator class for mixpanel_custom."""

    @classmethod
    def create_for_stream(cls, stream) -> "mixpanel_customAuthenticator":
        return cls(
            stream=stream,
            auth_headers={
                "Private-Token": stream.config.get("auth_token")
            }
        )
