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
docker exec -it my-snmp-container /home/usnmp/snmp_test/run_test.sh
```

## Tests
The tests are written using pytest and are located in the test_snmp.py file. The tests check the SNMP values against expected values.

## Example Test
```
# Get the expected value from uname output
expected_value = await expected_value_func()
oid_value = await get_snmp_value(community_string, ip_address, snmp_port, oid)
print(f"OID {oid} value: {oid_value}")  # Print the value for visibility

# Assert the expected value
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
