import pytest
import asyncio
import os
import time


def determine_scope(fixture_name, config):
    # https://docs.pytest.org/en/stable/fixture.html#dynamic-scope
    if config.option.function_scope:
        return "function"
    return "session"


def pytest_addoption(parser):
    parser.addoption(
        "--function_scope",
        action="store_true",
        default=False,
        help="Run fixture in function scope",
    )

@pytest.fixture(scope=determine_scope)
async def snmpd_server():
    """
    Asynchronous fixture to start and manage an SNMPd server using asyncio.
    """

    log_file = "/dev/stdout"
    conf_file = "/home/usnmp/snmp_test/snmpd.conf"

    # Ensure log directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    cmd = ["snmpd", "-f", "-Lsd", "-Lf", log_file, "-c", conf_file]

    try:
        process = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

        # Check if the process is still running
        if process.returncode is not None:
            stdout, stderr = await process.communicate()
            raise RuntimeError(f"Failed to start snmpd: {stderr.decode()}")

        # Read stdout and stderr continuously
        end_time = time.time() + 10  # Timeout after 10 seconds
        while True:
            snmpd_log = await process.stdout.readline()
            snmpd_log = snmpd_log.decode('utf-8')  # Decode the bytes to a string

            if snmpd_log:
                print(f"snmpd stdout: {snmpd_log}")
                if "NET-SNMP version" in snmpd_log:
                    break

            if time.time() > end_time:
                raise TimeoutError("Timeout while starting snmpd server")

        # Return the process to the test
        yield process

    except Exception as e:
        pytest.fail(f"Failed to start snmpd server: {e}")

    finally:
        # Teardown: Terminate the SNMPd server
        if process.returncode is None:
            process.terminate()
            await process.wait()

