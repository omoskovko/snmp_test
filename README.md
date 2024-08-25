[![Docker Image CI](https://github.com/omoskovko/snmp_test/actions/workflows/docker-image.yml/badge.svg)](https://github.com/omoskovko/snmp_test/actions/workflows/docker-image.yml)

# SNMP Test Project

This project contains tests for SNMP (Simple Network Management Protocol) using Python and pytest.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/omoskovko/snmp_test.git
    cd snmp_test
    ```

2. Create a docker image:
    ```sh
    docker build -t my-snmp-image .
    ```

3. Create docker container:
    ```sh
    docker run --name my-snmp-container -it -d my-snmp-image
    ```

## Usage

To run the SNMP tests, use the following command:
```sh
docker exec my-snmp-container /home/usnmp/snmp_test/run_test.sh
```

## Tests
The tests are written using pytest and are located in the test_snmp.py file. The tests check the SNMP values against expected values.

## Example Test
```
@pytest.mark.asyncio(loop_scope="module")
@pytest.mark.parametrize("community_string, ip_address, snmp_port, oid, expected_value_func", [
    pytest.param(
        "private",
        "127.0.0.1",
        1161,
        "1.3.6.1.2.1.1.1.0", 
        get_uname_output, 
        id="sysDescr"
    ),
])
async def test_snmp_oid_value(snmpd_server, community_string, 
                              ip_address, snmp_port, oid, expected_value_func):
    """
    Tests the value of a specific SNMP OID without using MIB names.
    """
    # Get the expected value from uname output
    expected_value = await expected_value_func()
    oid_value = await get_snmp_value(community_string, ip_address, snmp_port, oid)
    print(f"OID {oid} value: {oid_value}")  # Print the value for visibility

    # Assert the expected value (replace with your actual expectation)
    # expected_value = "Linux 3d6c71da4ed1 5.15.153.1-microsoft-standard-WSL2 #1 SMP Fri Mar 29 23:14:13 UTC 2024 x86_64"  # Example: expecting "Linux" for sysDescr
    print(f"Expected value: {expected_value}")
    assert oid_value == expected_value, f"OID {oid} value does not match the expected value: {expected_value}"
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes.

1. Fork the repository.
2. Create a new branch (git checkout -b feature-branch).
3. Make your changes.
4. Commit your changes (git commit -m 'Add some feature').
5. Push to the branch (git push origin feature-branch).
6. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
