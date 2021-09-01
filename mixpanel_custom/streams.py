"""Stream type classes for mixpanel_custom."""

import requests
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable, cast
import copy
import urllib
import json

from singer_sdk import typing as th  # JSON Schema typing helpers

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
import mixpanel_custom.tap

import singer

LOGGER = singer.get_logger()

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")

class CohortMembersStream(RESTStream):
    """Define custom stream."""
    name = "members"
    path = ""
    primary_keys = ["distinct_id", "cohort_id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "members.json"

    url_base = 'https://mixpanel.com/api/2.0/engage'

    records_jsonpath = "$[*]"  # Or override `parse_response`.

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {'Authorization': self.config['api_secret']}
        return headers
    
    @property
    def cohort_IDs(self) -> str:
        """Return the cohort IDs, configurable via tap settings."""
        return self.config["cohortIDs"]

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any],
        session_id: Optional[Any], cohortID: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params = {'filter_by_cohort': '{"id": %s}' % cohortID}
        if next_page_token != None:
            params['page'] = next_page_token
            params['session_id'] = session_id
        #the rest of this method encodes the parameters so that they match the format that the Mixpanel Engage API expects
        if isinstance(params, dict):
            params = params.items()
        for i, param in enumerate(params):
                if isinstance(param[1], list):
                    params[i] = (param[0], json.dumps(param[1]),)
        result = urllib.parse.urlencode([(k, isinstance(v, bytes) and v.encode('utf-8') or v) for k, v in params])
        return result


    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())


    def prepare_request(
        self, context: Optional[dict], next_page_token: Optional[Any], session_id: Optional[Any], cohortID: Optional[Any]
    ) -> requests.PreparedRequest:
        """Prepare a request object.
        If partitioning is supported, the `context` object will contain the partition
        definitions. Pagination information can be parsed from `next_page_token` if
        `next_page_token` is not None.
        """
        http_method = self.rest_method
        url: str = self.get_url(context)
        params: dict = self.get_url_params(context, next_page_token, session_id, cohortID)
        request_data = self.prepare_request_payload(context, next_page_token)
        headers = self.http_headers

        authenticator = self.authenticator
        if authenticator:
            headers.update(authenticator.auth_headers or {})

        request = cast(
            requests.PreparedRequest,
            self.requests_session.prepare_request(
                requests.Request(
                    method=http_method,
                    url=url,
                    params=params,
                    headers=headers,
                    json=request_data,
                )
            ),
        )
        return request

 
    def request_records(self, cohortID: Optional[str], context: Optional[dict]) -> Iterable[dict]:
        """Request records from REST endpoint(s), returning response records.
        If pagination is detected, pages will be recursed automatically.
        """
        next_page_token: Any = None
        session_id: Any = None
        prepared_request = self.prepare_request(
                context, next_page_token=next_page_token, session_id=session_id, cohortID=cohortID
            )
        resp = self._request_with_backoff(prepared_request, context)
        response_json = resp.json()
        next_page_number = 0
        page_size = response_json['page_size']
        #loop for pagination
        while True:
            for row in self.parse_response(resp):
                yield row
            count = len(response_json['results'])
            LOGGER.info(f'current page length is: {count}')
            if page_size > len(response_json['results']):
                break
            next_page_number += 1
            session_id = response_json['session_id']
            prepared_request = self.prepare_request(
                context, next_page_number, session_id, cohortID
            )
            resp = self._request_with_backoff(prepared_request, context)
            response_json = resp.json()
            

    def get_records(self, context: Optional[dict]) -> Iterable[Dict[str, Any]]:
        """Return a generator of row-type dictionary objects.
        Each row emitted should be a dictionary of property names to their values.
        """
        cohortIDs = self.cohort_IDs
        for cohortID in cohortIDs:
            for row in self.request_records(cohortID, context):
                for result in row['results']:
                    records = {}
                    records["distinct_id"] = result["$distinct_id"]
                    record_properties = result["$properties"]
                    if "$email" in record_properties:
                        records["email"] = record_properties["$email"]
                    records["cohort_id"] = cohortID
                    yield records




class CohortsStream(RESTStream):
    """Define custom stream."""
    name = "cohorts"
    path = "cohorts/list"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "cohorts.json"

    url_base = "https://mixpanel.com/api/2.0/"

    records_jsonpath = "$[*]"  # Or override `parse_response`.
    next_page_token_jsonpath = "$.next_page"  # Or override `get_next_page_token`.

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {'Authorization': self.config['api_secret']}
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
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result rows."""
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())