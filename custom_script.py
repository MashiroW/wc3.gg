from mitmproxy import http, ctx

def request(flow: http.HTTPFlow) -> None:
    if url_to_find in flow.request.pretty_url:
        referer = flow.request.headers.get("referer")
        if referer:
            ctx.log.info(f"Found Referer: {referer}")
        else:
            ctx.log.info("No Referer found.")