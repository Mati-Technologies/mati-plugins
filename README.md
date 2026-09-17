# Plugins Mati

**Mati Brain** aide ton assistant à retrouver les méthodes Mati auxquelles tu as accès et à les utiliser pour ton travail.

Le plugin est le point d’entrée dans ton assistant. **Mati héberge déjà le service Brain** auquel il se connecte : tu n’as aucun serveur à installer. Ce dépôt public fournit les instructions de connexion; les méthodes privées sont chargées depuis Brain après vérification de tes accès.

- Marketplace : **`mati`**
- Plugin : **`mati-brain`**, version **0.2.0**
- Source : [Mati-Technologies/mati-plugins](https://github.com/Mati-Technologies/mati-plugins)

## Commencer

1. Installe le plugin avec le [guide de ton application](docs/installation.md).
2. Termine la connexion Google avec ton compte **`@mati.tech`**; ce compte doit avoir les droits Brain attribués par Mati.
3. Dans une nouvelle conversation, demande : **« Connecter Mati Brain : vérifie mon accès au catalogue et lis une fiche commune autorisée, sans ouvrir de dossier client. »**
4. Après confirmation de la lecture, demande : **« Commencer avec Mati. Montre-moi ce que je peux faire avec mes accès. »**

Le catalogue et une vraie lecture doivent réussir avant que l’assistant annonce la connexion comme prête. L’installation ne donne pas de nouveaux droits sur les méthodes ou les autres applications. Chaque personne conserve ses propres connexions.

## Hermes

Le dépôt fournit aussi un paquet **Agent Plugins v1** à sa racine (`plugin.json`, `mcp.json`, `skills/`), généré depuis la même source que Claude et Codex :

```sh
hermes plugins install Mati-Technologies/mati-plugins
```

Active ensuite `mati-brain` si l’installateur ne l’a pas activé. **Installation du paquet et connexion Google sont distinctes.** Le [parcours Hermes](docs/installation.md#hermes--paquet-portable) décrit la limite OAuth des versions vérifiées; le paquet seul ne garantit pas encore un accès Brain utilisable dans Hermes.

## Pour l’équipe qui maintient le plugin

Le [guide de maintenance](docs/maintenance.md) explique la source unique, les versions et la publication. Le [skill](plugins/mati-brain/skills/mati-brain/SKILL.md) contient les instructions de l’assistant.

Les parcours ci-dessous sont documentés à partir des interfaces et sources officielles. L’installation complète de cette version dans un compte employé reste à valider pour chaque application.
