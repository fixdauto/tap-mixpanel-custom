# mixpanel_custom

`mixpanel_custom` is a Singer tap for Mixpanel.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

It uses the Mixpanel Engage API to fetch cohort and cohort member data.

## Installation

```bash
pipx install mixpanel_custom
```

## Configuration

### Accepted Config Options

```bash
{
  "api_secret": "YOUR_API_SECRET"
  "start_date": "rfc3339_date_string"
  "project_timezone": "US/Eastern"
  "date_window_size": "30"
  "attribution_window": "5"
  "user_agent": "tap-mixpanel <api_user_email@your_company.com>"
  "cohortIDs": ["List of cohort IDs"]
}
```

A full list of supported settings and capabilities for this
tap is available by running:

```bash
mixpanel_custom --about
```

## Usage

You can easily run `mixpanel_custom` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
mixpanel_custom --version
mixpanel_custom --help
mixpanel_custom --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `mixpanel_custom/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `mixpanel_custom` CLI interface directly using `poetry run`:

```bash
poetry run mixpanel_custom --help
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to develop your own taps and targets.
