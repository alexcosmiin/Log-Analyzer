import os
import html


class HTMLReporter:
    TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <title>Test Report</title>
    <style>
        .passed {{ color: green; }}
        .failed {{ color: red; }}
        .error {{ color: orange; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        pre {{ white-space: pre-wrap; word-wrap: break-word; }}
        .log-block {{ display: none; margin-top: 5px; background-color: #f9f9f9; padding: 10px; border: 1px dashed #ccc; }}
        .toggle-button {{ cursor: pointer; color: blue; text-decoration: underline; }}
    </style>
    <script>
        function toggleLog(id) {{
            var x = document.getElementById(id);
            if (x.style.display === "none") {{
                x.style.display = "block";
            }} else {{
                x.style.display = "none";
            }}
        }}
    </script>
</head>
<body>
    <h1>Test Execution Report</h1>
    <p>Execution time: {execution_time} seconds</p>

    <h2>Summary</h2>
    <table>
        <tr><th>Total</th><th>Passed</th><th>Failed</th><th>Success Rate</th></tr>
        <tr>
            <td>{total}</td>
            <td class="passed">{passed}</td>
            <td class="failed">{failed}</td>
            <td>{success_rate:.2f}%</td>
        </tr>
    </table>

    <h2>Detailed Results</h2>
    <table>
        <tr>
            <th>Test</th>
            <th>Status</th>
            <th>Duration</th>
            <th>Details</th>
        </tr>
        {test_rows}
    </table>
</body>
</html>
"""

    def _get_status_class(self, status):
        """Map status to CSS class"""
        return status.lower()

    def generate(self, results, output_file):
        """Generate HTML report"""
        test_rows = []
        for i, test in enumerate(results.get('tests', [])):
            status_class = self._get_status_class(test.get('status', 'UNKNOWN'))
            name = html.escape(test.get('name', 'Unnamed test'))
            message = html.escape(test.get('message', ''))
            duration = test.get('duration', 'N/A')
            log_lines = test.get('log', [])
            log_id = f"log-{i}"

            log_html = "<br>".join(html.escape(line) for line in log_lines)

            test_rows.append(f"""
                <tr>
                    <td>{name}</td>
                    <td class="{status_class}">{test.get('status', 'UNKNOWN')}</td>
                    <td>{duration}</td>
                    <td>
                        <pre>{message}</pre>
                        <div class="toggle-button" onclick="toggleLog('{log_id}')">Show/Hide Log</div>
                        <div id="{log_id}" class="log-block">
                            <pre>{log_html}</pre>
                        </div>
                    </td>
                </tr>
            """)

        # Ensure the reports directory exists
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)

        with open(output_file, 'w') as f:
            f.write(self.TEMPLATE.format(
                execution_time=results.get('execution_time', 'N/A'),
                total=results.get('total', 0),
                passed=results.get('passed', 0),
                failed=results.get('failed', 0),
                success_rate=results.get('success_rate', 0),
                test_rows='\n'.join(test_rows)
            ))
