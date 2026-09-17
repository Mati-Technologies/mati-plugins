# Maintenir et publier le point d’entrée

## Une source pour les applications

Modifier les instructions uniquement dans `plugins/mati-brain/skills/mati-brain/SKILL.md`. Les deux marketplaces publient le même dossier de plugin :

- `.agents/plugins/marketplace.json` pour Codex et les imports compatibles;
- `.claude-plugin/marketplace.json` pour Claude.

Les manifestes du plugin se trouvent dans `plugins/mati-brain/.codex-plugin/plugin.json` et `plugins/mati-brain/.claude-plugin/plugin.json`. La connexion partagée est décrite dans `plugins/mati-brain/.mcp.json`.

Le paquet portable Hermes est exposé à la racine : `plugin.json`, `mcp.json`, `skills/mati-brain/SKILL.md`. Ces fichiers sont générés et suivis dans Git pour permettre `hermes plugins install Mati-Technologies/mati-plugins` sans compilation. **Ne pas les modifier à la main** : après un changement de la source, exécuter `python3 scripts/portable.py`. La validation refuse toute divergence, tout lien symbolique et tout fichier supplémentaire dans les skills portables. Les champs de présentation Codex restent dans son manifeste; ils ne sont pas copiés dans le format portable.

Le nom installé est `mati-brain`, même si le dépôt se nomme `mati-plugins`. Le transport portable est `streamable-http`; le fichier `.mcp.json` Claude/Codex conserve son transport `http`. Aucun secret n’est embarqué.

Ce dépôt public contient le point d’entrée et la documentation d’installation. Garder les méthodes privées, les données de travail et les secrets dans leurs systèmes respectifs.

## Publier une nouvelle version

1. Modifier la source utile et le journal des changements de la version.
2. Augmenter la version dans **les deux manifestes du plugin**. Ne pas ajouter de version dans les marketplaces : les manifestes du plugin sont la source de vérité. La première version est `0.1.0`.
   La CI compare les cinq fichiers livrés dans `plugins/mati-brain` et les trois fichiers portables à la révision Git de base. Le manifeste portable reprend la version Codex lors de la génération. Elle refuse un changement de leur contenu sans augmentation de version. Une modification de documentation seule ne demande pas d'augmentation.
3. Exécuter depuis la racine du dépôt :

   ```sh
   python3 scripts/portable.py
   python3 scripts/validate.py
   python3 -m unittest discover -s tests
   python3 scripts/release.py --output dist
   ```

Les trois archives sont `mati-brain-vX.Y.Z.zip` (Claude/Codex), `mati-brain-skill-vX.Y.Z.zip` (skill seul) et `mati-brain-hermes-vX.Y.Z.zip` (paquet portable), accompagnées de `SHA256SUMS`.

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

## Vérifier la compatibilité Hermes

Avec un checkout Hermes et son environnement Python installé, le contrôle suivant charge le dépôt puis l’archive avec le véritable adaptateur Hermes, sans connexion réseau ni authentification :

```sh
/path/to/hermes/venv/bin/python scripts/check_hermes.py --hermes-root /path/to/hermes --archive dist/mati-brain-hermes-v0.2.0.zip
```

Pour une installation complète de test, utiliser un `HERMES_HOME` temporaire vide et `hermes plugins install file:///chemin/absolu/du/depot --enable`. Le dépôt doit être commité car l’installateur le clone. Vérifier ensuite `hermes plugins list` et la découverte du skill/MCP. Ne pas utiliser un profil employé pour ce contrôle de paquet.

Cette validation de chargement et d’installation ne prouve ni le consentement Google, ni la compatibilité du callback, ni une lecture Brain dans Hermes. Voir la limite amont et le parcours de connexion dans le guide d’installation.

Contrôle du 17 septembre 2026 avec Hermes `13e72fb205` : installation et activation du dépôt commité dans un `HERMES_HOME` temporaire réussies; version 0.2.0 affichée, source et archive chargées avec un skill et un MCP distant sans diagnostic. Aucun OAuth ni appel au Brain effectué depuis ce profil de test.
