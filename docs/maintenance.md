# Maintenir et publier le point d’entrée

## Une source pour les applications

Modifier les instructions uniquement dans `plugins/mati-brain/skills/mati-brain/SKILL.md`. Les deux marketplaces publient le même dossier de plugin :

- `.agents/plugins/marketplace.json` pour Codex et les imports compatibles;
- `.claude-plugin/marketplace.json` pour Claude.

Les manifestes du plugin se trouvent dans `plugins/mati-brain/.codex-plugin/plugin.json` et `plugins/mati-brain/.claude-plugin/plugin.json`. La connexion partagée est décrite dans `plugins/mati-brain/.mcp.json`.

Ce dépôt public contient le point d’entrée et la documentation d’installation. Garder les méthodes privées, les données de travail et les secrets dans leurs systèmes respectifs.

## Publier une nouvelle version

1. Modifier la source utile et le journal des changements de la version.
2. Augmenter la version dans **les deux manifestes du plugin**. Ne pas ajouter de version dans les marketplaces : les manifestes du plugin sont la source de vérité. La première version est `0.1.0`.
   La CI compare les cinq fichiers livrés dans `plugins/mati-brain` à la révision Git de base. Elle refuse un changement de leur contenu sans augmentation de version. Une modification de documentation seule ne demande pas d'augmentation.
3. Exécuter depuis la racine du dépôt :

   ```sh
   python3 scripts/validate.py
   python3 -m unittest discover -s tests
   python3 scripts/release.py --output dist
   ```

4. Relire les archives produites et faire passer la CI de la modification avant fusion.
5. Publier un tag correspondant à la version, par exemple `v0.1.0`, sur la révision validée. La publication de release doit utiliser les archives générées par la CI de ce tag.
6. Vérifier les fichiers publiés et contrôler une nouvelle installation ou mise à jour dans chaque application annoncée compatible.

Ne pas modifier manuellement une archive : elle doit toujours pouvoir être reconstruite depuis la révision publiée. Une modification du skill doit accompagner un changement de version, afin que les applications détectent une nouvelle livraison.

## Deux types de mise à jour

| Changement | Livraison |
|---|---|
| Instructions d’entrée, compatibilité ou connexion du plugin | Nouvelle version de ce dépôt, puis actualisation par l’application ou remplacement du ZIP |
| Méthode ou référence privée dans Brain | Publication dans Brain; pas de réinstallation du plugin si son interface reste compatible |

Une tâche commencée peut conserver sa publication Brain. Pour vérifier une nouvelle méthode, commencer une nouvelle consultation. Le plugin n’a pas de mécanisme qui force toutes les applications à se mettre à jour; consulter le [guide d’installation](installation.md) pour les parcours pris en charge.

## Distribution gérée par une organisation Claude

Le parcours organisationnel Claude est distinct de l’ajout personnel de ce dépôt public. Il exige actuellement un dépôt GitHub **privé ou interne**. L’actualisation automatique est une option à activer; elle se déclenche lors de la fusion d’une PR comportant une hausse de version sur la branche par défaut. Une poussée directe ne suffit pas. Le dépôt public Mati n’est donc pas une source à importer telle quelle dans ce parcours. [Gestion des plugins Claude en organisation](https://support.claude.com/en/articles/13837433-manage-plugins-for-your-organization).

## Contrôle avant annonce aux employés

Vérifier la version chargée, la connexion personnelle et une vraie lecture Brain. Conserver la distinction entre validation du paquet, import réussi et utilisation complète dans un compte employé. Les archives et guides de la version initiale ne prouvent pas à eux seuls cette dernière étape.

Les procédures et limites des plateformes ont été relues le **16 septembre 2026**. Les revalider si l’interface ou le comportement de distribution change.
