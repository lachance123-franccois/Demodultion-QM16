# Demodultion-QM16
Démodulation complète d’un signal QAM-16 : chargement et analyse du signal, démodulation cohérente I/Q, extraction des symboles, décodage en texte ASCII et évaluation des performances via le BER. Comparaison des résultats simulés avec la théorie en fonction du rapport Eb/N0.


Pipeline de traitement

Le traitement du signal est structuré en plusieurs étapes :

Chargement du signal binaire échantillonné
Démodulation cohérente I/Q (mélange + filtrage passe-bas)
Extraction des symboles par moyennage
Décodage via projection sur la constellation QAM-16
Analyse des performances avec le taux d’erreur binaire (BER)
Résultats
Paramètres du signal
Nombre d’échantillons : 294 600
Fréquence d’échantillonnage : 100 MHz
Distance minimale de la constellation : 2.0000
Composantes I/Q

Les signaux I et Q obtenus après démodulation présentent des niveaux discrets cohérents avec une modulation QAM-16, confirmant le bon fonctionnement de la démodulation.

Message décodé (référence)

Le système permet de reconstruire le message transmis :

Fable de Jean de La Fontaine,
Le Torrent et la Rivière, Livre VIII, fable 23

Le texte est correctement restitué en conditions de faible bruit.

Effet du bruit

Pour un faible rapport signal sur bruit (exemple : 1 dB), le message décodé devient :

Vdfle õe KeAn la LÁ Fojt`mne,
Le@Torvent ìd0lÁ WiöiS¨rm, pHmvre ÆIII

Ces erreurs illustrent la dégradation des performances en présence de bruit.

Analyse
La constellation QAM-16 permet une transmission efficace mais sensible au bruit
Le BER augmente lorsque le rapport Eb/N0 diminue
Le système reste fiable pour des valeurs élevées de Eb/N0

Pour approfondir les concepts utilisés :
https://en.wikipedia.org/wiki/Quadrature_amplitude_modulation
https://en.wikipedia.org/wiki/Bit_error_rate

Ce projet met en évidence les différentes étapes d’une chaîne de réception numérique QAM-16 et permet d’analyser concrètement l’impact du bruit sur la qualité de transmission