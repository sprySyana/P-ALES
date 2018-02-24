<? session_start(); ?>
<html>
	<head>
		<title>Descente de gradient couleur</title>
	</head>
	<body>

	<H1>Descente de gradient couleur</H1>
	<p><u>Objectif</u> : partir d'une matrice de distance entre paires de phonèmes et effectuer une descente de gradient pour obtenir des couleurs pour chaque phonème de manière à ce que les couleurs soient le plus distantes quand les phonèmes sont les plus fréquents</p>

<?php
set_time_limit(10000);
// les données de session
// bool : phoneme['x'] : existence du phoneme 'x'
// int :  paire['x']['y'] : fréquence des phonemes 'x' et 'y' consécutivement
// array()()() : couleur['x'] : triples valeurs RGB pour le phoneme 'x'

// chargement du fichier
function load_frequences(){
	// nettoyage des données de session
	unset($_SESSION['phoneme']);
	unset($_SESSION['paire']);
	unset($_SESSION['couleur']);
	// chargement du fichier de paires
	$content = file_get_contents("pairesAdj.txt");
	$fs = strlen($content);
	print "<br/>le fichier de paires pèse : $fs octets";
	$lignes = explode("\n",$content);
	print "<br/>le fichier de paires contient : ".sizeof($lignes)." paires";
	$nblignes = 0;
	// génération du tableau en session de phonèmes et de paires
	foreach ($lignes as $ligne){
		$laligne = explode("\t",$ligne);
		$nblignes++;
		if (strlen($laligne[2])>0) /* && $nblignes<10)*/{
			if (!isset($_SESSION["phoneme"][$laligne[0]])) $_SESSION["phoneme"][$laligne[0]]=true;
			if (!isset($_SESSION["phoneme"][$laligne[1]])) $_SESSION["phoneme"][$laligne[1]]=true;
			$_SESSION["paire"][$laligne[0]][$laligne[1]]=(int)$laligne[2];
			}
		}
	// génération des paires inexistantes et suppression des paires doubles (x-y et y-x) en gardant la plus élevée
	$cpt_doublons=0;
	foreach ($_SESSION["phoneme"] as $lephoneme1 => $levrai){
		foreach ($_SESSION["phoneme"] as $lephoneme2 => $lautrevrai){
			if (isset($_SESSION["paire"][$lephoneme1][$lephoneme2]) 
				&& isset($_SESSION["paire"][$lephoneme2][$lephoneme1])
				&& ($lephoneme2 != $lephoneme1)){
				$cpt_doublons++;
				if ($_SESSION["paire"][$lephoneme1][$lephoneme2]>$_SESSION["paires"][$lephoneme2][$lephoneme2])
					unset($_SESSION["paire"][$lephoneme2][$lephoneme1]);
				else unset($_SESSION["paire"][$lephoneme1][$lephoneme2]);
				}
			}
		}
	print "<br/>toutes les combinaisons ont été (re)générées, dont $cpt_doublons doublons supprimés";

	// lissage des valeurs sur l'empan 30-300
	lisse_paires_frequences(30,300);
	print "<br/>Le fichier contient ".sizeof($_SESSION["phoneme"])." phonèmes distincts";

	// on rajoute à 10 les paires qui ne sont pas décalrées comme paires d'exception (à distancier mais pas trop)
	foreach ($_SESSION["phoneme"] as $lephoneme1 => $levrai){
		foreach ($_SESSION["phoneme"] as $lephoneme2 => $lautrevrai){
			if (!isset($_SESSION["paire"][$lephoneme1][$lephoneme2]) && 
				!isset($_SESSION["paire"][$lephoneme1][$lephoneme1]))
				$_SESSION["paire"][$lephoneme1][$lephoneme2]=10;
		}
	}

	genere_liste_couleurs();
	print "<br/>Espace couleur généré...";
	print "<br/>Lancement du calcul...";
	print "<META http-equiv=\"refresh\" content=\"3; URL=".$_SERVER['SCRIPT_NAME']."?compute\">";
	
	}

// lissage des fréquences des paires de phonèmes
function lisse_paires_frequences($minval, $maxval){
	// on cherche le min et le max
	$min = 100000;
	$max = 0;
	foreach($_SESSION["phoneme"] AS $phon1 => $truth1){
		foreach($_SESSION["phoneme"] AS $phon2 => $truth2){
			if (isset($_SESSION["paire"][$phon1][$phon2])){
				//print "\t<br/>[".$phon1.",".$phon2."] = (".$_SESSION["paire"][$phon1][$phon2].")";
				if ($_SESSION["paire"][$phon1][$phon2]>$max) $max = $_SESSION["paire"][$phon1][$phon2];
				if ($_SESSION["paire"][$phon1][$phon2]<$min) $min = $_SESSION["paire"][$phon1][$phon2];
				}
			}
		}

	print "<br/>Balayage fréquences absolues AVANT LISSAGE (min is $min, max is $max)";

	// et maintenant on rééquilibre les valeurs
	foreach($_SESSION["phoneme"] AS $phon1 => $truth1){
		foreach($_SESSION["phoneme"] AS $phon2 => $truth2){
			if (isset($_SESSION["paire"][$phon1][$phon2])){
				$valeur = $_SESSION["paire"][$phon1][$phon2];
				$nouvellevaleur = (($valeur-$min)* ($maxval - $minval) / ($max-$min))+$minval;
				$_SESSION["paire"][$phon1][$phon2]=$nouvellevaleur;
				}
			}
		}


	$min = 100000;
	$max = 0;
	foreach($_SESSION["phoneme"] AS $phon1 => $truth1){
		foreach($_SESSION["phoneme"] AS $phon2 => $truth2){
			if (isset($_SESSION["paire"][$phon1][$phon2])){
				//print "\t<br/>[".$phon1.",".$phon2."] = (".$_SESSION["paire"][$phon1][$phon2].")";
				if ($_SESSION["paire"][$phon1][$phon2]>$max) $max = $_SESSION["paire"][$phon1][$phon2];
				if ($_SESSION["paire"][$phon1][$phon2]<$min) $min = $_SESSION["paire"][$phon1][$phon2];
				}
			}
		}
	print "<br/>Balayage fréquences absolues APRES LISSAGE (min is $min, max is $max)";




	}

// génération aléatoire des couleurs de chaque phoneme
function genere_liste_couleurs(){
	foreach($_SESSION['phoneme'] as $phon => $truth) $_SESSION['couleur'][$phon]=array(rand(0,255),rand(0,255),rand(0,255));
	}
	
function descente(){
	// la valeur de différence entre deux boucles - mis à 100 pour démarrer
	$deltaboucle = 100;
	$time1 = time();
	print "<br/>starting time is :".$time1;
	// le compteur de boucles pour savoir à la fin
	$compteurboucles = 0;
	while ($compteurboucles<10){ 
		$lastdistrec= "\n<table border='thin solid black'>\n\t<tr><td>Paire</td><td>Dist2D</td><td>Dist3D</td><td>Dist3D2</td></tr>";
		$compteurboucles ++;
		// on définit la somme des erreurs de distance sur un tour de phonèmes
		$erreur_boucle = 0;
		$erreur_next = 0;
		//print "<textarea>";print_r($paires_phonemes_distance);print "</textarea>";
		// double boucle sur les phonemes en vérifiant que la paire existe
		foreach($_SESSION['phoneme'] AS $phon1 => $truth1){
			foreach($_SESSION['phoneme'] as $phon2 => $truth2){
				if (isset($_SESSION['paire'][$phon1][$phon2])){
					// on récupère les deux couleurs
					$couleur_phon1 = $_SESSION['couleur'][$phon1];
					$couleur_phon2 = $_SESSION['couleur'][$phon2];
					// on récupère la distance 2D
					$distance2D = $_SESSION['paire'][$phon1][$phon2]; 
					// on calcule la distance 3D (pythagore en 3D)
					$distance3D = sqrt(pow($couleur_phon1[0]-$couleur_phon2[0],2)
									  +pow($couleur_phon1[1]-$couleur_phon2[1],2)
									  +pow($couleur_phon1[2]-$couleur_phon2[2],2));
					// on calcule la différence absolue de distance
					$deltadist = abs($distance3D - $distance2D);
					// on l'ajoute pour mémoire dans l'erreur préalable aux modifications
					$erreur_boucle += abs($deltadist);

					// on procède à une rédcution simple : passer à 0,90 fois la distance sur chaque axe (donc réduction de 0.05 de chaque coté)			

					// on évacue le cas des distances minimum
					if ($distance2D==10 && $distance3D>$distance2D){}// on fait rien en fait
					// s'il faut rapprocher les points (Dist3D>Dist2D)
					else if ($distance3D>$distance2D){
						// si le R de phon1 inférieur au R de phon2
						if ($couleur_phon1[0]<$couleur_phon2[0]) {
							$couleur_phon1[0] += $deltadist * 0.001;
							$couleur_phon2[0] -= $deltadist * 0.001;
							}
						else {
							$couleur_phon1[0] -= $deltadist * 0.001;
							$couleur_phon2[0] += $deltadist * 0.001;
							}
						// idem V
						if ($couleur_phon1[1]<$couleur_phon2[1]) {
							$couleur_phon1[1] += $deltadist * 0.001;
							$couleur_phon2[1] -= $deltadist * 0.001;
							}
						else {
							$couleur_phon1[1] -= $deltadist * 0.001;
							$couleur_phon2[1] += $deltadist * 0.001;
							}
						// idem B
						if ($couleur_phon1[2]<$couleur_phon2[2]) {
							$couleur_phon1[2] += $deltadist * 0.001;
							$couleur_phon2[2] -= $deltadist * 0.001;
							}
						else {
							$couleur_phon1[2] -= $deltadist * 0.001;
							$couleur_phon2[2] += $deltadist * 0.001;
							}
					}// fin de s'il faut rapprocher
					// s'il faut les écarter
					else {
						// si le R de phon1 inférieur au R de phon2
						if ($couleur_phon1[0]<$couleur_phon2[0]) {
							$couleur_phon1[0] -= $deltadist * 0.005;
							$couleur_phon2[0] += $deltadist * 0.005;
							}		
						else {
							$couleur_phon1[0] += $deltadist * 0.005;
							$couleur_phon2[0] -= $deltadist * 0.005;
							}
						// idem V
						if ($couleur_phon1[1]<$couleur_phon2[1]) {
							$couleur_phon1[1] -= $deltadist * 0.005;
							$couleur_phon2[1] += $deltadist * 0.005;
							}
						else {
							$couleur_phon1[1] += $deltadist * 0.005;
							$couleur_phon2[1] -= $deltadist * 0.005;
							}
						// idem B
						if ($couleur_phon1[2]<$couleur_phon2[2]) {
							$couleur_phon1[2] -= $deltadist * 0.005;
							$couleur_phon2[2] += $deltadist * 0.005;
							}
						else {
							$couleur_phon1[2] += $deltadist * 0.005;
							$couleur_phon2[2] -= $deltadist * 0.005;
							}
					} // fin de s'il faut les écarter
			
			// on recale entre 0 et 255 
			foreach($couleur_phon1 as $rvb => $val){
				if ($val<0) $couleur_phon1[$rvb]=0;
				else if ($val>255) $couleur_phon1[$rvb]=255;
			}
			foreach($couleur_phon2 as $rvb => $val){
				if ($val<0) $couleur_phon1[$rvb]=0;
				else if ($val>255) $couleur_phon1[$rvb]=255;
			}

					//	on calcule la distance avec les nouveaux points
					$distance3D2 = sqrt(pow($couleur_phon1[0]-$couleur_phon2[0],2)
									  +pow($couleur_phon1[1]-$couleur_phon2[1],2)
									  +pow($couleur_phon1[2]-$couleur_phon2[2],2));
					// on calcule la différence de distance 2D 3D (pour vérifier si ça a bien baissé)
					if ($distance2D>10){
						$deltadist2 = $distance3D2 - $distance3D;
						$erreur = $distance2D - $distance3D2;}
					else $deltadist2 = 0;
					// affichage de # de couleur pour distinguer les pas qui ont réduit l'erreur
					//if ($destadist2>=0) echo "<font color=green>#</font>"; else echo "<font color=red>#</font>";
					// calcul de l'erreur totale de fin de boucle
					$erreur_next += abs($erreur);
					// on remet les couleurs dans le tableau de session
					$_SESSION['couleur'][$phon1] = array($couleur_phon1[0],$couleur_phon1[1],$couleur_phon1[2]);
					$_SESSION['couleur'][$phon2] = array($couleur_phon2[0],$couleur_phon2[1],$couleur_phon2[2]);
					$lastdistrec.= "\n<tr><td>$paire</td><td>$distance2D</td><td>$distance3D</td><td>$distance3D2</td></tr>";
		
				}
				$deltaboucle = $erreur_next - $erreur_boucle;
				$lastdistrec. "</table><br/><br/><br/>";
				//print "<br/>Delta boucle : $deltaboucle";//Total erreur = $erreur_boucle // Total erreur next = $erreur_next";
			}// fin de si la paire existe
		}// fin du foreach phon 2
	}// fin du foreach phon 1
	print "<br/>Nb boucles = $compteurboucles<br/>Err_prev : $erreur_boucle<br/>Err_next : $erreur_next<br/>Delta boucle : $deltaboucle";
	// print $lastdistrec;
	// montre les couleurs
/*	print "<H2>Table des paires de couleurs</H2> <ul><li>Chaque ligne correspond à une paire de phonèmes</ul><table border=1>";
	foreach($paires_phonemes_distance as $paire => $dist){
		if ($dist>10){
			$phone = explode("-",$paire);
			$colphon1 = "rgb(".(int)$liste_phonemes_couleurs[$phone[0]][0].",".
								(int)$liste_phonemes_couleurs[$phone[0]][1].",".
								(int)$liste_phonemes_couleurs[$phone[0]][1].")";
			$colphon2 = "rgb(".(int)$liste_phonemes_couleurs[$phone[1]][0].",".
								(int)$liste_phonemes_couleurs[$phone[1]][1].",".
								(int)$liste_phonemes_couleurs[$phone[1]][1].")";
			print "<tr><td>$paire</td><td>$dist</td><td style=\"background-color:$colphon1;color:$colphon2;\" width=30px>$colphon1</td>
									  <td style=\"background-color:$colphon2;color:$colphon1;\" width=30px>$colphon2</td></tr>";
		}	
	}
	print "</table>";*/
	
	$time2 = time();
	print "<br/>next time is $time2<br/>Time Shift for $compteurboucle is : ".($time2-$time1);
	print "<H2>Table des couleurs</H2><table border=1>";
	foreach($_SESSION['couleur'] as $phon => $cols)
		print "<tr><td>$phon</td><td>".(int)$cols[0]."</td><td>".(int)$cols[1]."</td><td>".(int)$cols[2]."</td><td style=\"background-color:rgb(".(int)$cols[0].",".(int)$cols[1].",".(int)$cols[2].");\" width=50px>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</td></tr>";
	print "</table>";
	//$_SESSION['colors'] = $liste_phonemes_couleurs;
	print "<META http-equiv=\"refresh\" content=\"3; URL=".$_SERVER['SCRIPT_NAME']."?compute\">";

}
	
	
	
	
if (!isset($_GET['compute']))
	load_frequences();
else 
	{
	print "<br/>On lance la descente...";
	descente();
	}

// le script de debug pour afficher les variables de sessions etc.
//include_once("debug.php");

?>

	</body>
</html>
