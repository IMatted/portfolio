<html>
    <head>
        <title>Brevet Time Dashboard Consumer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 30px; }
            table { border-collapse: collapse; width: 50%; margin-top: 20px; }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
            th { background-color: #f2f2f2; }
            li { margin: 9px}
            hr {height: 1px; background-color: #333;}
        </style>
    </head>
    <body>
        <h1>Brevets Control Times Consumer Dashboard</h1>

        <h3>All Tracked Times (Fetched via REST API)</h3>
        <table>
            <thead>
                <tr>
                    <th>Open Time</th>
                    <th>Close Time</th>
                </tr>
            </thead>
        <tbody>
            <?php
            $json = @file_get_contents('http://laptop-service/listAll');
            
            if ($json === FALSE) {
                echo "<tr><td colspan='2'>No database data found. Submit times using the calculator first!</td></tr>";
            } else {
                $obj = json_decode($json);
                $brevets = $obj->brevets;
                
                foreach ($brevets as $submission) {
                    if (isset($submission->controls) && is_array($submission->controls)) {
                        
                        foreach ($submission->controls as $time_entry) {
                            if (empty($time_entry->open) && empty($time_entry->close)) {
                                continue;
                            }
                            
                            echo "<tr>";
                            echo "<td>" . htmlspecialchars($time_entry->open) . "</td>";
                            echo "<td>" . htmlspecialchars($time_entry->close) . "</td>";
                            echo "</tr>";
                        }
                    }
                }
            }
            ?>
        </tbody>
        </table>

        <h3>Quick Links to Raw API Outputs</h3>
        <ul>
            <p>JSON</p>
            <li><a href="http://localhost:5001/listAll" target="_blank">View All (JSON)</a></li>
            <li><a href="http://localhost:5001/listOpenOnly" target="_blank">View All Open (JSON)</a></li>
            <li><a href="http://localhost:5001/listCloseOnly" target="_blank">View All Close (JSON)</a></li>
            <li><a href="http://localhost:5001/listOpenOnly/json?top=3" target="_blank">Top 3 Open Only (JSON)</a></li>
            <hr style="margin-left: 0px; width:15%;">
            <p>CSV</p>
            <li><a href="http://localhost:5001/listAll/csv" target="_blank">Download All (CSV)</a></li>
            <li><a href="http://localhost:5001/listOpenOnly/csv" target="_blank">Download All Open (CSV)</a></li>
            <li><a href="http://localhost:5001/listCloseOnly/csv" target="_blank">Download All Close (CSV)</a></li>
            <li><a href="http://localhost:5001/listOpenOnly/csv?top=3" target="_blank">Download Top 3 Open Only (CSV)</a></li>
        </ul>
    </body>
</html>