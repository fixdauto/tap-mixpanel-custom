"""REST client handling, including mixpanel_customStream base class."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from mixpanel_custom.auth import mixpanel_customAuthenticator
import mixpanel_custom.tap

import singer

LOGGER = singer.get_logger()

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class mixpanel_customStream(RESTStream):
    """mixpanel_custom stream class."""

    # if tapfile.STREAM_TYPES == 'CohortsStream':
    url_base = "https://mixpanel.com/api/2.0/"
    # else:
    #     url_base = 'https://mixpanel.com/api/2.0/engage?filter_by_cohort={"id":554004}&output_properties=["$email"]'
    LOGGER.info(f'url base is: {url_base}')
    # OR use a dynamic url_base:
    # @property
    # def url_base(self) -> str:
    #     """Return the API URL root, configurable via tap settings."""
    #     return self.config["api_url"]

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.next_page"  # Or override `get_next_page_token`.

    @property
    def authenticator(self) -> mixpanel_customAuthenticator:
        """Return a new authenticator object."""
        return mixpanel_customAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {'Authorization': 'Basic NTNiMjcyODNjNjhmZDk2Yjc1N2M5YjU1N2Q5NTljMjM6'}
        return headers

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        # TODO: If pagination is required, return a token which can be used to get the
        #       next page. If this is the final page, return "None" to end the
        #       pagination loop.
        if self.next_page_token_jsonpath:
            all_matches = extract_jsonpath(
                self.next_page_token_jsonpath, response.json()
            )
            first_match = next(iter(all_matches), None)
            next_page_token = first_match
        else:
            next_page_token = response.headers.get("X-Next-Page", None)

        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        # if mixpanel_custom.tap.STREAM_TYPES == 'CohortMembersStream':
        #     params: dict = {"filter_by_cohort": "{'id': 554004}", "output_properties": "['$email']"}
        # else:
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def prepare_request_payload(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Optional[dict]:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        LOGGER.info(f'response is: {response}')
        LOGGER.info(f'response.json is: {response.json()}')
        LOGGER.info(f'self.records_jsonpath is: {self.records_jsonpath}')
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        """As needed, append or transform raw data to match expected structure."""
        # TODO: Delete this method if not needed.
        return row
