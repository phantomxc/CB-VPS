<?php	
    $conn = pg_connect('host=localhost dbname=cameron user=cameron password=cameron');
	if (!$conn) {
		die("Error in connection: " . pg_last_error());
	}
?>
