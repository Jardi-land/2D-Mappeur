# Notes de rappels pour mon TM:

### Type de « Tools »:
- hand_tool
- zoom_tool

### Fonctions et classes dans les fichiers:
_Légende:_

📂 Dossier
🌉 Image
📋 Fichier python
🟨 Class
🕰 Init
🟣 Function

_Ordre de lecture:_ (exécution)

Main -> Interface (puis chemins séparés)

_Workflow:_

📂Mappeur_files:
- 🌉Image uniquement pour l’instant

📋interface_outline:
- 🟨outline_interface:
	- 🕰: Instance de la class out_worker
	- 🟣line:
		- Ligne de côté dans la work_zone
	- 🟣nothing_color: 
		- Couleur sous l’interface
	- 🟣tool_info_sharing:
		- Récupère le current_tool de l’instance out_worker et le return
	- 🟣update:
		- Exécute nothing_color, line, et update de l’instance de la class out_worker

📋interface:
- 🟨Interface:
	- 🕰: Instance de la class work_zone, Instance de la class outline_interface
	- 🟣send_tool:
		- Exécute tool_info_sharing de l’instance de la work_zone et lui envoie en paramètre tool_info_sharing de l’instance de outline_interface
	- 🟣layout_2 (temporaire):
		- Couleur sous la work_zone
	- 🟣layout_1 (temporaire):
		- Update l’instance de la class outline_interface
	- 🟣draw:
		- Exécute send_tool, layout_2 et layout_1

📋main:
- 🟣main:
	- 🕰: Instance de la class Interface
	- Boucle de Frame contenant le fonction draw de l’instance de la class Interface

📋out_worker:
- 🟨button:
	- 🟣is_over:
		- Permet de savoir si la souris se trouve sur le bouton
	- 🟣get_tool:
		- Permet de changer le tool si le bouton est cliqué et que ce n’est pas déjà le même tool
	- 🟣update:
		- Permet de changer l’image et de l’afficher
- 🟨out_worker:
	- 🕰: Instance des boutons depuis la class button
	- 🟣send_tool:
		- Return le current_tool
	- 🟣update:
		- Permet de set current_tool et d’envoyer les update vers les tools qui en ont besoin

📋settings:
- 🕰: Set les variables par défauts pour la fenêtre

📋wk:
- 🟨work_zone:
	- 🟣mouse_click:
		- Permet de détecter les cliques dans la work zone
	- 🟣tool_info_sharing:
		- Permet de récupérer le tool et le définir dans la class
	- 🟣draw:
		- Permet d’afficher la work zone TS
	- 🟣update:
		- Permet d’exécuter le tool « hand tool » et la fonction draw

