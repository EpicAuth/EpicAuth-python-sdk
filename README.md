# EpicAuth Python SDK

Official Python SDK for **EpicAuth** — a modern authentication and licensing solution for applications.

[![PyPI version](https://img.shields.io/pypi/v/epicauth.svg)](https://pypi.org/project/epicauth/)
[![Python versions](https://img.shields.io/pypi/pyversions/epicauth.svg)](https://pypi.org/project/epicauth/)
[![License](https://img.shields.io/badge/license-Elastic%20License%202.0-blue.svg)](LICENSE)

## Installation

Install the latest version from PyPI:

```bash
pip install epicauth
```

Upgrade to the latest version:

```bash
pip install --upgrade epicauth
```

## Quick Start

```python
from epicauth import EpicAuth

EpicAuthApp = EpicAuth(
    name="MyApplication",
    ownerid="YOUR_OWNER_ID",
    version="1.0",
    hash_to_check=get_checksum(),
)
```

That's it. Your application can now communicate with EpicAuth.

## Initialization

The `EpicAuth` client is initialized with your application information:

```python
from epicauth import EpicAuth

EpicAuthApp = EpicAuth(
    name="MyApplication",
    ownerid="YOUR_OWNER_ID",
    version="1.0",
    hash_to_check="YOUR_FILE_HASH",
)

EpicAuthApp.init()
```

### Parameters

| Parameter       | Type  | Description                    |
| --------------- | ----- | ------------------------------ |
| `name`          | `str` | Your EpicAuth application name |
| `ownerid`       | `str` | Your EpicAuth owner ID         |
| `version`       | `str` | Current application version    |
| `hash_to_check` | `str` | Application integrity hash     |

## Example

A complete example can be found in the official example repository:

**EpicAuth Python Example**

https://github.com/epicauth-org/EpicAuth-Python-Example

The example repository demonstrates how to integrate the SDK into a Python application.

## Features

* Simple Python API
* EpicAuth authentication
* Application initialization
* License management
* Application version checking
* Update detection
* Application integrity verification
* Lightweight integration
* PyPI distribution

## Requirements

* Python 3.10+
* `requests`

Install the SDK and its dependencies automatically with:

```bash
pip install epicauth
```

## Project Structure

```text
EpicAuth-python-sdk/
├── src/
│   └── epicauth/
│       ├── __init__.py
│       └── client.py
├── examples/
│   └── main.py
├── LICENSE
├── README.md
└── pyproject.toml
```

## Development

Clone the repository:

```bash
git clone https://github.com/epicauth-org/EpicAuth-python-sdk.git
cd EpicAuth-python-sdk
```

Install the package locally:

```bash
pip install -e .
```

## Versioning

EpicAuth Python SDK follows semantic versioning:

```text
MAJOR.MINOR.PATCH
```

For example:

```text
1.0.0
1.1.0
1.1.1
```

See the [Releases](https://github.com/epicauth-org/EpicAuth-python-sdk/releases) page for available versions.

## PyPI

The package is available on PyPI:

https://pypi.org/project/epicauth/

Install it with:

```bash
pip install epicauth
```

## License

EpicAuth Python SDK is licensed under the **Elastic License 2.0**.

See [`LICENSE`](LICENSE) for the complete license terms.

## Links

* **PyPI:** https://pypi.org/project/epicauth/
* **GitHub:** https://github.com/epicauth/EpicAuth-python-sdk
* **Examples:** https://github.com/epicauth/EpicAuth-Python-Example
* **EpicAuth:** https://epicauth.cc

---

Made for developers using **EpicAuth**.
