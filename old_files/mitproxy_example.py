from mitmproxy import http, ctx

def request(flow: http.HTTPFlow) -> None:
    # Check if the request method is POST or GET
    if flow.request.method in ["POST", "GET"]:
        # Log the request method, URL, and headers
        ctx.log.info(f"{flow.request.method} Request - URL: {flow.request.pretty_url}")
        for name, value in flow.request.headers.items():
            ctx.log.info(f"  {name}: {value}")

        # If it's a POST request, log the request content
        if flow.request.method == "POST":
            ctx.log.info(f"  Request Content: {flow.request.text}")

def response(flow: http.HTTPFlow) -> None:
    # Check if the response status code is 200 (OK)
    if flow.response.status_code == 200:
        # Log the response status code and headers
        ctx.log.info(f"Response - Status Code: {flow.response.status_code}")
        for name, value in flow.response.headers.items():
            ctx.log.info(f"  {name}: {value}")

        # Log the response content
        ctx.log.info(f"  Response Content: {flow.response.text}")

# Run the mitmproxy instance
if __name__ == "__main__":
    mitmdump_args = ["-s", "mitproxy_example.py"]
    
    from mitmproxy.tools.main import mitmdump
    mitmdump(mitmdump_args)
