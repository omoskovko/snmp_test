import asyncio

async def get_command_output(command):
    # Helper function to run shell commands asynchronously
    process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    return stdout.decode("utf-8").strip(), stderr.decode("utf-8").strip()

async def get_command_lines(command):
    # Helper function to run shell commands asynchronously and return lines
    process = await asyncio.create_subprocess_shell(command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()
    command_list = []
    if stderr:
        return command_list
    
    for line in stdout.decode("utf-8").splitlines():
        command_list.append(line)
    return command_list

async def get_uname_output():
    # Helper function to run uname commands asynchronously
    # uname_s = await asyncio.create_subprocess_exec("uname", "-s", stdout=asyncio.subprocess.PIPE)
    uname_s_output, _ = await get_command_output("uname -s")    
    uname_n_output, _ = await get_command_output("uname -n")
    uname_r_output, _ = await get_command_output("uname -r")
    uname_v_output, _ = await get_command_output("uname -v")
    uname_m_output, _ = await get_command_output("uname -m")

    return f"{uname_s_output} {uname_n_output} {uname_r_output} {uname_v_output} {uname_m_output}"

async def get_ip_addr_info(command="ip addr show"):
    ip_link_output = await get_command_lines(command)
    interfaces = {}
    link_index = ""
    for line in ip_link_output:
        if ": " in line:
            link_res_list = [v.split("@")[0] for v in line.split(": ")]
            link_index = link_res_list[0]
            interfaces[link_index]= link_res_list
        else:
            interfaces[link_index].append(line.strip())
    return interfaces

