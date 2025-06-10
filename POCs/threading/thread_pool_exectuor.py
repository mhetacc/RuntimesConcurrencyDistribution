import concurrent.futures
import xmlrpc.client

# works

URLS = ['http://localhost:8001',
        'http://localhost:8002',]


def encapsulate_proxy(bob_url, term, commit_index) -> tuple[int, bool]:
    with xmlrpc.client.ServerProxy(bob_url, allow_none=True) as bob_proxy:
            return bob_proxy.append_entries_rpc(term, commit_index)

 
results = []
# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_result = {executor.submit(encapsulate_proxy, url, None, None): url for url in URLS}
    for future in concurrent.futures.as_completed(future_result):
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (future_result, exc))
        else:
            print('Append result ', data)
            results.append(data)

print("Results: ", results)