#!/usr/bin/env php
<?php
// The whole structure of this program is scuffed
// ...

// Problems:
// I don't check if user is valid
// I don't fix encoding problems (from cmd to php-csv)
// $cmd i though i'll use different ones for all formats, but no











function out_to_csv($out) {
    // out to csv file
    if (($handle = fopen("tasklist.csv", "w")) !== FALSE) {
        for ($i = 0; $i < count($out); $i++) {
            $larr = str_getcsv($out[$i], ',', "\"", "\\");
            
            fputcsv($handle, $larr, ",", "\"", "\\");
        }
        fclose($handle);
    }
}

function out_to_txt($out) {
    // out to txt file
    if (($handle = fopen("tasklist.txt", "w")) !== FALSE) {
        for ($i = 0; $i < count($out); $i++) {
            $larr = str_getcsv($out[$i], ',', "\"", "\\"); 
            foreach ($larr as $key => $val) {
                //$val = trim($val, "\"");
                $larr[$key] = str_pad($val, 30-strlen($val), " ", STR_PAD_RIGHT);
            }


            fwrite($handle, implode(" | ", $larr) . "\n");
        }
        fclose($handle);
    }
}

function out_to_html($out) {
    // out to html file
    if (($handle = fopen("tasklist.html", "w")) !== FALSE) {
        fwrite($handle, "<html><body><table>");
        foreach ($out as $line) {
            
            $larr = str_getcsv($line, ',', '"', "\\");
            //print_r($line);

            fwrite($handle, "<tr>");
            foreach ($larr as $key => $val) {
                $larr[$key] = str_pad($val, 30-strlen($val), " ", STR_PAD_RIGHT);
                fwrite($handle, "<td>{$val}</td>");
            }
            fwrite($handle, "</tr>");
        }
        fwrite($handle, "</table></body></html>");
        fclose($handle);
    }
}





//echo $argc;
//echo print_r($argv);

$file_format = "txt";



// handle argument parsing and cheking if they are correct
if ($argc > 3 || $argc < 2) {
    // wrong numeber of args passed
    // Users wrong, don't care enough to handle it
    exit(1);
}

if (in_array($argv[1], ["txt", "html", "csv"])) {
    $file_format = $argv[1];
} else {
    echo "Bad format";
    exit(1);
} // I didn't do user name validation
    // if username is invalid the program vill likly only output header or empty



// is user valid?, do i care?
$out = [];
if ($argc == 2) {
    // only format passed, dafault to all users
    switch ($file_format) {
        case "txt":
            $cmd = $argc == 2 ? '/mnt/c/Windows/System32/tasklist.exe /V /FO CSV ' : '/mnt/c/Windows/System32/tasklist.exe /V /FO CSV /FI "USERNAME eq ' . $argv[2] . '"';
            exec($cmd, $out);
            // encoding issues enshew
            file_put_contents("tasklist.txt", "");
            
            out_to_txt($out);
            // file created, now pause, after pause delete the file
            echo "Press enter to continue...";
            fgets(STDIN);
            unlink("tasklist.txt");
            break;



        case "html":
            $cmd = $argc == 2 ? '/mnt/c/Windows/System32/tasklist.exe /V /FO CSV' : '/mnt/c/Windows/System32/tasklist.exe /V /FO CSV /FI "USERNAME eq ' . $argv[2] . '"';
            exec($cmd, $out);
            // encoding issues enshew
            file_put_contents("tasklist.html", "");
            
            out_to_html($out);
            // file created, now pause, after pause delete the file
            echo "Press enter to continue...";
            fgets(STDIN);
            unlink("tasklist.html");
            break;



        case "csv":
            $cmd = $argc == 2 ? '/mnt/c/Windows/System32/tasklist.exe /V /FO CSV' : '/mnt/c/Windows/System32/tasklist.exe /V /FO CSV /FI "USERNAME eq ' . $argv[2] . '"';
            exec($cmd, $out);
            array_splice($out, 1, 1);
            // encoding forblems apear
            file_put_contents("tasklist.csv", " ");
            
            out_to_csv($out);
            // file created, now pause, after pause delete the file
            echo "Press enter to continue...";
            fgets(STDIN);
            unlink("tasklist.csv");
            break;
    }
    
    
}



