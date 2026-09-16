# Installer et connecter Mati Brain

**Brain est déjà hébergé par Mati.** Le plugin public installe le point d’entrée et indique à ton assistant comment joindre ce service. Il ne contient pas les méthodes privées et ne lance pas de serveur sur ton ordinateur.

Pour lire Brain, connecte ton compte Google professionnel **`@mati.tech`**. Mati doit aussi lui avoir attribué les droits nécessaires : une connexion Google réussie ne donne pas automatiquement accès au contenu. Cette connexion est distincte de ton abonnement à Claude ou ChatGPT.

Adresse du service à utiliser dans les procédures ci-dessous :

```text
https://mati-brain-pilot.tail760c23.ts.net/mcp
```

Garde une seule connexion Brain active dans l’application. Si tu utilisais déjà un skill ou un connecteur Mati Brain, repère-le avant l’installation; vérifie le nouveau parcours avant de désactiver un ancien doublon. Le plugin ne remplace pas tes connexions aux autres outils de travail. Ne colle jamais de mot de passe, code de connexion, jeton ou URL de retour OAuth dans une conversation.

## Claude Chat ou Cowork — compte individuel

Ce parcours est disponible avec Claude Pro ou Max; un abonnement Team n’est pas nécessaire. Il concerne Chat sur le web, Chat dans Claude Desktop et Cowork.

1. Ouvre **Customize → Plugins**. Pour Cowork, ouvre d’abord l’onglet Cowork.
2. Sous **Personal plugins**, choisis **+ → Add marketplace → Add from a repository**.
3. Indique `https://github.com/Mati-Technologies/mati-plugins`.
4. Dans le marketplace **mati**, installe **mati-brain**.
5. Ouvre **Customize → Connectors**, puis la connexion Brain. Choisis **Connect** lorsqu’elle le demande.
6. Dans la fenêtre Google, choisis ton compte **`@mati.tech`**, termine le consentement, puis reviens dans Claude.
7. Dans une nouvelle conversation, ouvre **+ → Connectors** et active Brain s’il ne l’est pas. Passe à la [vérification de lecture](#vérifier-la-connexion-avec-une-lecture).

Le [Centre d’aide Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) décrit l’ajout personnel du marketplace. Il ne garantit pas un délai d’actualisation automatique; contrôle la version lors d’une annonce Mati.

### Si le connecteur Brain n’apparaît pas

1. Ouvre **Customize → Connectors → + → Add custom connector**.
2. Donne-lui le nom **Mati Brain** et colle l’adresse du service ci-dessus.
3. Laisse les champs facultatifs **OAuth Client ID** et **OAuth Client Secret** vides. Aucun secret partagé n’est à fournir.
4. Choisis **Add**, puis **Connect** dans la fiche du connecteur.
5. Authentifie ton compte **`@mati.tech`**, reviens dans Claude et active Brain dans **+ → Connectors** de la conversation.

Sur un espace Team ou Enterprise, un propriétaire doit d’abord rendre le connecteur disponible; chaque employé le connecte ensuite avec son propre compte. Les étapes sont tirées du [guide officiel des connecteurs distants](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).

## Claude Code

**Connexion native en préparation :** le service Brain n’accepte pas encore le retour de connexion local utilisé par cette application. Le plugin peut être installé, mais le login reste bloqué tant que cette compatibilité n’est pas activée côté Mati. Le parcours Claude Chat/Cowork utilise une connexion différente.

Dans une session Claude Code :

```text
/plugin marketplace add Mati-Technologies/mati-plugins
/plugin install mati-brain@mati
```

Choisis l’installation pour ton utilisateur. Dans **`/plugin` → Marketplaces → mati**, active **Enable auto-update** : les marketplaces tiers ne l’activent pas par défaut. Redémarre Claude Code après l’installation ou une mise à jour. [Installation et mises à jour Claude Code](https://code.claude.com/docs/en/discover-plugins).

Une fois la compatibilité de connexion confirmée par Mati :

1. Lance **`/mcp`** dans la session.
2. Sélectionne le serveur Brain fourni par le plugin, en vérifiant son adresse. Son nom affiché peut inclure un préfixe du plugin.
3. Lance l’authentification, puis connecte ton compte Google **`@mati.tech`** dans le navigateur.
4. Reviens dans Claude Code et vérifie l’état du serveur dans **`/mcp`**. Si une connexion antérieure a expiré, utilise **Re-authenticate**.
5. Demande la [vérification de lecture](#vérifier-la-connexion-avec-une-lecture).

Si aucune entrée Brain n’est visible après redémarrage, vérifie l’activation de **mati-brain** dans **`/plugin`** avant d’ajouter un deuxième serveur. Un refus d’adresse de retour OAuth est un problème de compatibilité à transmettre au mainteneur; ne change pas les adresses ni les droits au hasard. [Authentification MCP dans Claude Code](https://code.claude.com/docs/en/mcp#authenticate-with-remote-mcp-servers).

## Codex — installer le plugin

**Connexion native en préparation :** le service Brain n’accepte pas encore le retour de connexion local de Codex. Les étapes ci-dessous installent et préparent le plugin; elles ne constituent pas actuellement une connexion réussie. La compatibilité côté service doit être confirmée avant le test de lecture.

Pour ajouter le marketplace depuis le terminal :

```sh
codex plugin marketplace add Mati-Technologies/mati-plugins
codex plugin add mati-brain@mati
```

Relance l’application de bureau ou commence une nouvelle session CLI. Dans **Plugins**, vérifie que **mati-brain** est activé. Dans la CLI, **`/plugins`** ouvre le gestionnaire. L’installation et la connexion sont deux étapes distinctes.

### Connexion dans l’application de bureau

1. Ouvre **Settings → MCP servers**.
2. Repère Brain et vérifie que son adresse correspond à celle indiquée en début de guide.
3. Sélectionne **Authenticate** si une connexion est requise.
4. Choisis ton compte Google **`@mati.tech`** dans le navigateur et termine le consentement.
5. Reviens dans l’application; utilise **Restart** si l’interface le demande, puis ouvre une nouvelle tâche.
6. Dans le champ de message, **`/mcp`** affiche les serveurs. Demande ensuite la [vérification de lecture](#vérifier-la-connexion-avec-une-lecture).

Si Brain n’apparaît pas, vérifie le plugin et relance l’application. L’ajout manuel d’un autre serveur n’est pas nécessaire tant que l’entrée du plugin peut être utilisée. Ces libellés sont ceux de la [documentation MCP OpenAI](https://learn.chatgpt.com/docs/extend/mcp?surface=cli); le parcours complet avec cette version de Brain reste à attester.

### Connexion dans la CLI

Le serveur fourni par ce plugin se nomme **`mati-brain`**. Vérifie sa présence et son adresse :

```sh
codex mcp list
codex mcp get mati-brain
```

Une fois la compatibilité de connexion confirmée côté Mati, lance l’authentification du serveur du plugin :

```sh
codex mcp login mati-brain --oauth-client-registration dcr
```

Le nom **`mati-brain`** a été observé dans la liste locale après installation du plugin. Si ton installation affiche un autre nom, vérifie son adresse avant de l’utiliser; ne confonds pas une ancienne connexion manuelle avec celle du plugin. Termine l’authentification Google **`@mati.tech`** dans le navigateur, puis démarre une nouvelle session Codex et demande la lecture de vérification. Si l’entrée manque, passe par le gestionnaire du plugin dans l’application. Si le login refuse l’adresse de retour OAuth, transmets cette erreur au mainteneur.

Les commandes `list`, `get` et `login` sont présentes dans l’aide locale de Codex CLI 0.153.4. La connexion native et sa compatibilité avec le service Brain restent à vérifier avant de déclarer ce parcours prêt.

### Mettre le plugin à jour

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

**Cette version est destinée à l’application ChatGPT de bureau dans ce parcours.** La présence de `.mcp.json` entraîne le classement **Desktop only**, même avec une connexion HTTPS distante. Dans **Plugins**, ouvre **mati-brain**, installe-le s’il est disponible dans ton espace et utilise la connexion proposée avec ton compte **`@mati.tech`**. Termine par la lecture de vérification. [Import et synchronisation des plugins ChatGPT](https://learn.chatgpt.com/docs/enterprise/plugin-management).

**ChatGPT web et mobile : intégration non disponible avec ce paquet.** Leurs conversations ne lisent pas la configuration MCP locale de Codex. Il faudrait un parcours d’application ou de connecteur compatible distinct, qui n’est pas livré ici. Pour un compte individuel, l’ajout direct de ce dépôt GitHub dans ChatGPT web n’est pas établi. Publier le dépôt sur GitHub ne l’inscrit pas automatiquement au répertoire public OpenAI.

## Installation par ZIP — solution de secours

Les [versions publiées](https://github.com/Mati-Technologies/mati-plugins/releases) fournissent les archives préparées depuis la même source. Utilise l’archive de plugin dans une application qui accepte l’import de plugins. Si ton interface ne permet que l’import de skills, utilise l’archive de skill puis le parcours de connexion correspondant ci-dessus. Dans Claude Chat ou Cowork, suis les étapes **Si le connecteur Brain n’apparaît pas**.

Choisis la connexion interactive proposée; aucun jeton à copier ni en-tête secret n’est fourni dans le ZIP. Une archive importée est une copie : **elle ne se met pas à jour depuis GitHub**. Remplace-la lors d’une nouvelle version du point d’entrée.

## Vérifier la connexion avec une lecture

Dans une nouvelle conversation, demande :

**« Connecter Mati Brain : vérifie mon accès au catalogue et lis une fiche commune autorisée, sans ouvrir de dossier client. »**

L’assistant doit accomplir ces trois lectures réelles, dans l’ordre :

1. Commencer une consultation avec **`brain_begin`**.
2. Charger le catalogue avec **`brain_catalog`**, en conservant l’identifiant reçu.
3. Choisir dans ce catalogue une fiche commune disponible et la lire avec **`brain_read`**, dans la même consultation.

Il confirme ensuite le titre de la fiche, sa version et la publication utilisée, sans recopier de données privées. Aucune recherche de client ni écriture n’est nécessaire. S’il ne peut pas terminer, il indique l’étape bloquée au lieu d’annoncer « connecté ».

Après réussite : **« Commencer avec Mati. Montre-moi ce que je peux faire avec mes accès. »**

## Si la connexion ne fonctionne pas

| Ce que tu observes | Suite utile |
|---|---|
| Les outils Brain sont absents | Vérifier l’installation, l’activation du plugin et de sa connexion, puis ouvrir une nouvelle conversation. Reprendre le parcours propre à l’application. |
| L’application demande une nouvelle connexion ou signale une session expirée | Relancer **Connect**, **Authenticate**, **Re-authenticate** ou la commande de login appropriée; choisir le bon compte `@mati.tech`. |
| Le compte est reconnu, mais Brain refuse l’accès ou une fiche reste indisponible | Faire vérifier les droits par le responsable Mati. Un refus ne se contourne pas en déclarant un rôle dans le chat ou en utilisant le compte d’un collègue. |
| Délai dépassé, service indisponible ou erreur serveur | Réessayer une fois; si cela persiste, signaler l’application, l’heure et le message. Ne pas réinstaller en boucle ni conclure à un retrait de droits. |
| Le navigateur signale une adresse de retour OAuth refusée | Signaler un problème de compatibilité de connexion au mainteneur. Ne pas remplacer l’adresse par une valeur inventée. |

Un code HTTP seul ne suffit pas toujours à distinguer une session expirée d’un refus de droits; conserver le message exact et l’étape concernée. Ne partage pas de secret ni d’URL contenant un code d’authentification.

**État de validation :** sources officielles et aides locales relues le 16 septembre 2026. La réussite complète avec un vrai compte employé, le contrôle de retrait d’accès et un cas métier complet restent à réaliser séparément. Cette documentation ne modifie aucun compte ni aucun droit.
