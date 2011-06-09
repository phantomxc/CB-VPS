<?php
    include("../db/db.php");
?>
<div>
    <input type="checkbox" name="leased"> Leased </input> <input type="checkbox" name="owned"> Owned</input> <br />
    <br />
    Region:
    <br />
    <select id="region">
        <option selected="">All</option>
        <?php 
            $sql = "SELECT DISTINCT(region) FROM properties;";
            $result = pg_query($conn, $sql);
            
            while ($row = pg_fetch_array($result)) {
                echo "<option>" .  $row[0] . "</option>";
            
            }
        ?>
    </select>
    <br />
    Division:
    <br />
    <select id="division">
        <option selected="">All</option>
        <?php 
            $sql = "SELECT DISTINCT(division) FROM properties;";
            $result = pg_query($conn, $sql);
            
            while ($row = pg_fetch_array($result)) {
                echo "<option>" .  $row[0] . "</option>";
            
            }
        ?>
    </select>
    <br />
    <br />

    <input type="button" value="Run"></input>

</div>
