An Apache-style access log is at `/app/access.log`. Each line has the common log
format: `<client-ip> - - [<timestamp>] "<METHOD> <path> HTTP/1.1" <status> <bytes>`.

Analyze the log and write a JSON summary report to `/app/report.json`. The report
must be a single JSON object with exactly these three keys:

- `total_requests` (integer): the number of non-empty lines in the log.
- `unique_ips` (integer): the number of distinct client IP addresses (the first
  field of each line).
- `top_path` (string): the request path that appears most often across all
  requests (the log has a unique most-common path, so no tie-breaking is needed).

Success criteria:

1. `/app/report.json` exists and contains a valid JSON object.
2. `total_requests` equals the number of non-empty lines in `/app/access.log`.
3. `unique_ips` equals the number of distinct client IPs in `/app/access.log`.
4. `top_path` equals the most frequently requested path in `/app/access.log`.
