import asyncio
from pysnmp.hlapi.asyncio import getCmd, walkCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity

async def get_snmp_value(community, host, port, oid, timeout=5):
    """
    Get the value of a specific SNMP OID without using MIB names.
    """

    # Initialize SNMP engine
    snmp_engine = SnmpEngine()
    community_data = CommunityData(community, mpModel=0)
    transport_target = UdpTransportTarget((host, port))
    context_data = ContextData()

    # Create ObjectIdentity using the OID directly
    object_identity = ObjectIdentity(oid)

    oid_result_value = ""
    try:
        # Perform SNMP GET request with a timeout
        error_indication, error_status, error_index, var_binds = await asyncio.wait_for(
            getCmd(snmp_engine, community_data, transport_target, context_data, ObjectType(object_identity)),
            timeout=timeout  # Adjust timeout as needed
        )

        # Check for errors
        if error_indication:
            print(f"SNMP error: {error_indication}")
        elif error_status:
            print(f"SNMP error: {error_status.prettyPrint()}")
        else:
            # Get the value of the OID
            oid_value = var_binds[0][1].prettyPrint()
            print(f"OID {oid} value: {oid_value}")  # Print the value for visibility
            oid_result_value = oid_value

    except TimeoutError:
        pass
    finally:
        # Ensure cleanup even if there's an error or timeout
        snmp_engine.transportDispatcher.closeDispatcher()
    
    return oid_result_value

async def get_snmpwalk_result(community, host, port, oid, timeout=10):
    # Initialize SNMP engine
    snmp_engine = SnmpEngine()

    iterator = walkCmd(
        snmp_engine,
        CommunityData(community),
        UdpTransportTarget((host, port)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        lexicographicMode=False,
    )

    walk_result = []
    try:
        async for errorIndication, errorStatus, errorIndex, varBinds in iterator:
            if errorIndication:
                print(errorIndication)
                break
            elif errorStatus:
                print('%s at %s' % (errorStatus.prettyPrint(),
                                    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
                break
            else:
                for varBind in varBinds:
                    walk_result.append((str(varBind[0]), type(varBind[1]).__name__, str(varBind[1])))
    except asyncio.TimeoutError:
        print(f"SNMP walk operation timed out after {timeout} seconds")
    finally:
        # Ensure cleanup even if there's an error or timeout
        snmp_engine.transportDispatcher.closeDispatcher()
    return walk_result

async def map_oids_to_last_index(community, host, port, void):
    result = await get_snmpwalk_result(community, host, port, void)

    oid_map = {}
    for oid, type, value in result:
        index = oid.split('.')[-1]
        oid_map[index] = (oid, type, value)

    return oid_map

# Example usage:
# asyncio.run(map_oids_to_interfaces("sysview", "127.0.0.1", 1161))