import pytest
import asyncio
from common.commands import get_uname_output, get_ip_addr_info
from common.snmp_lib import map_oids_to_last_index, get_snmp_value

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

@pytest.mark.asyncio(loop_scope="module")
@pytest.mark.parametrize("comunity, host, port, ifIndex, ifDescr, expected_value_func", [
    pytest.param("sysview", "127.0.0.1", 1161,
        "1.3.6.1.2.1.2.2.1.1", 
        "1.3.6.1.2.1.2.2.1.2",
        get_ip_addr_info, id="ip_addr_info"
        ),
    ]
)
async def test_ip_link_value(snmpd_server, comunity, host, port, ifIndex, 
                              ifDescr, expected_value_func,
    ):
    """
    Tests the value of a specific SNMP OID without using MIB names.
    """
    link_interfaces = await expected_value_func()
    ifIndex_map = await map_oids_to_last_index(comunity, host, port, ifIndex)
    ifDescr_map = await map_oids_to_last_index(comunity, host, port, ifDescr)

    for _, (index, descr, *info) in link_interfaces.items():
        assert ifIndex_map[index][2] == index
        assert ifDescr_map[index][2] == descr

@pytest.mark.asyncio(loop_scope="module")
@pytest.mark.parametrize("comunity, host, port, ifDescr, ipAddrTable, expected_value_func", [
    pytest.param("sysview", "127.0.0.1", 1161,
        "1.3.6.1.2.1.2.2.1.2",
        "1.3.6.1.2.1.4.20.1",
        get_ip_addr_info, id="ifconfig_info"
        ),
    ]
)
async def test_ifconfig_value(snmpd_server, comunity, host, port, 
                              ifDescr, ipAddrTable, expected_value_func,
    ):
    """
    Tests the value of a specific SNMP OID without using MIB names.
    """
    link_interfaces = await expected_value_func("ifconfig")
    ifDescr_map = await map_oids_to_last_index(comunity, host, port, ifDescr)

    for _, (_, _, value) in ifDescr_map.items():
        assert link_interfaces[value][0] == value

        print(link_interfaces[value])
        inet_info = [s for s in [v for v in link_interfaces[value] if "inet " in v][0].split(" ") if s]
        ip = inet_info[1]
        ipAdEntAddr_value = await get_snmp_value(comunity, host, port, f"{ipAddrTable}.1.{ip}")
        assert ipAdEntAddr_value == ip

        ipAdEntNetMask_value = await get_snmp_value(comunity, host, port, f"{ipAddrTable}.3.{ip}")
        assert ipAdEntNetMask_value == inet_info[3]