from mcp.server.fastmcp import FastMCP
import socket
import time
from concurrent.futures import ThreadPoolExecutor

# Initialize FastMCP server
mcp = FastMCP("local_server")

site_list = [
    "www.baidu.com",
    "www.google.com",
    "www.github.com", 
    "www.bilibili.com"]

@mcp.tool()
def pp() -> str:
    def format_result(site):
        return site + "\t" + tcp_ping(site) + "\n"

    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(format_result, site_list))
    return "".join(results)

def tcp_ping(host: str, port: int = 80, timeout: float = 3.0) -> str:
    try:
        start = time.time()
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        delay = (time.time() - start) * 1000  # 转为毫秒
        return f"{delay:.2f}ms"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')