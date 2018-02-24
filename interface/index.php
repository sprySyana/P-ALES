<!DOCTYPE html>
<html>
<head>
    <title>P-ALES</title>
    <meta charset="utf-8">
    <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body>
    <div class="nav">
        <header>
            <h1>P-ALES</h1>
        </header>
        <nav>
            <ul>
                <li><a href="index.php">Tableaux chromatiques</a></li>
                <li><a href="a_propos.php">À propos</a></li>
            </ul>
        </nav>    
    </div>
    <div class="main">
        <p>Affichage des tableaux chromatiques (SVG)</p>
        <h3>Choisir une langue</h3>
		<?
			// Create the list of files in a directory
			$dir = 'svg';
			$filesClean = array_diff(scandir($dir), array('.', '..'));
			// Verification of content in list $files
			//~ print_r($filesClean);
			// Construct drop-down list
			print("<form name=\"Choix de la langue\" method=\"POST\" action=\"index.php\">\n");
			print("\t\t\t<select name=\"langue\">\n");
			// Read each element of list $files
			foreach ($filesClean as $tab) {
				$lang = substr($tab,0,-4);
				if($lang != "style") {
					print("\t\t\t\t<option value=\"".$lang."\">".$lang."</option>\n");
				}
			}
			print("\t\t\t</select>\n");
			print("\t\t\t<input type=\"submit\" name=\"bouton\" value=\"OK\"/>\n");
			print("\t\t</form>\n");
			if(isset($_POST['bouton'])) {
				$select_lang = $_POST['langue'];
				print("\t\t".$select_lang." : \n");
				print("\t\t<object type=\"image/svg+xml\" data=\"svg/".$select_lang.".svg\" class=\"tab\">svg</object>\n");
			}
		?>
	</div>
</body>
</html>
