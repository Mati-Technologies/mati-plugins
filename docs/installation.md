# Installer Mati Brain

Choisis ton application. Garde une seule installation et une seule connexion Brain actives dans cette application. Si tu utilisais déjà un skill ou un connecteur Mati Brain, repère-le avant d’ajouter le plugin; vérifie le nouveau parcours avant de désactiver un ancien doublon.

L’authentification et le consentement se font dans ton propre compte. Le plugin ne remplace pas tes connexions aux autres outils de travail.

## Claude Chat ou Cowork — compte individuel

Ce parcours est disponible avec Claude Pro ou Max; un abonnement Team n’est pas nécessaire. Il concerne Chat sur le web, Chat dans Claude Desktop et Cowork.

1. Ouvre **Customize → Plugins**. Pour Cowork, ouvre d’abord l’onglet Cowork.
2. Sous **Personal plugins**, choisis **+ → Add marketplace → Add from a repository**.
3. Indique `https://github.com/Mati-Technologies/mati-plugins`.
4. Dans le marketplace **mati**, installe **mati-brain**.
5. Suis la connexion proposée, puis commence une nouvelle conversation.

Les libellés peuvent varier avec la version de Claude. Le [Centre d’aide Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) est la référence de ce parcours, vérifiée le 16 septembre 2026. Il ne garantit pas un délai de mise à jour automatique des marketplaces personnels; contrôle la version lorsqu’une mise à jour Mati est annoncée.

## Claude Code

Dans une session Claude Code :

```text
/plugin marketplace add Mati-Technologies/mati-plugins
/plugin install mati-brain@mati
```

Choisis l’installation pour ton utilisateur. Dans **`/plugin` → Marketplaces → mati**, active **Enable auto-update** : les marketplaces tiers ne l’activent pas par défaut. Redémarre Claude Code après l’installation ou une mise à jour. Termine l’authentification Brain depuis **`/mcp`** si elle est demandée.

L’actualisation dépend de l’application et de ses réglages; elle ne remplace pas le consentement à une connexion. [Installation et mises à jour Claude Code](https://code.claude.com/docs/en/discover-plugins).

## Codex — application de bureau ou CLI

Pour ajouter le marketplace depuis le terminal :

```sh
codex plugin marketplace add Mati-Technologies/mati-plugins
codex plugin add mati-brain@mati
```

Relance l’application de bureau ou commence une nouvelle session CLI. Dans l’application, retrouve **mati-brain** dans **Plugins**, vérifie son activation et termine la connexion demandée. Dans la CLI, **`/plugins`** ouvre le gestionnaire.

Pour actualiser la source :

```sh
codex plugin marketplace upgrade mati
```

Vérifie ensuite la version proposée dans le gestionnaire et applique la mise à jour disponible. Ce guide ne suppose pas une actualisation automatique permanente des installations locales.

Ces commandes sont présentes dans l’aide locale de **Codex CLI 0.153.4**, vérifiée le 16 septembre 2026. Sources : [marketplaces Codex](https://developers.openai.com/plugins/build/plugins) et [applications compatibles avec les plugins](https://learn.chatgpt.com/docs/plugins). L’extension IDE ne prend pas les plugins en charge.

## ChatGPT — distribution par un espace de travail

Un administrateur peut importer ce dépôt dans **Admin → Plugins → Add → Import marketplace** :

- **Source** : `https://github.com/Mati-Technologies/mati-plugins`
- **Path** : vide
- **Branch, tag, or commit** : vide pour suivre la branche par défaut

Il configure ensuite la disponibilité du plugin. Les nouveaux marketplaces importés ont une synchronisation quotidienne; **Sync now** permet de l’actualiser plus tôt. Chaque employé doit encore disposer de ses accès et connecter son compte.

**Cette version est destinée à l’application ChatGPT de bureau dans ce parcours.** La présence de `.mcp.json` entraîne le classement **Desktop only**, même avec une connexion HTTPS distante. [Import et synchronisation des plugins ChatGPT](https://learn.chatgpt.com/docs/enterprise/plugin-management).

Pour un compte ChatGPT individuel, ce guide ne promet pas l’ajout de ce dépôt GitHub directement dans ChatGPT web ou mobile. Utilise le parcours local Codex compatible ou un plugin rendu disponible dans ton espace de travail. Publier le dépôt sur GitHub ne l’inscrit pas automatiquement au répertoire public OpenAI.

## Installation par ZIP — solution de secours

Les [versions publiées](https://github.com/Mati-Technologies/mati-plugins/releases) fournissent les archives préparées depuis la même source. Utilise l’archive de plugin dans une application qui accepte l’import de plugins. Si ton interface ne permet que l’import de skills, utilise l’archive de skill et ajoute séparément le connecteur Brain :

```text
https://mati-brain-pilot.tail760c23.ts.net/mcp
```

Choisis la connexion interactive proposée; aucun jeton à copier ni en-tête secret n’est fourni dans le ZIP. Une archive importée est une copie : **elle ne se met pas à jour depuis GitHub**. Remplace-la lors d’une nouvelle version du point d’entrée.

## Vérifier que tu peux travailler

Dans une nouvelle conversation, demande : **« Utilise Mati Brain pour me montrer ce que je peux faire et m’aider à commencer. »**

Le résultat doit provenir du catalogue actuellement accessible à ton compte. Si l’assistant ne voit pas Brain ou si la connexion est refusée, transmets le message d’erreur à la personne qui t’accompagne, sans secret de connexion. Un plugin installé ne prouve pas encore une lecture réussie.

**État de validation :** les procédures sont documentées; leur exécution complète avec cette version et un compte employé reste à confirmer dans chaque application.
