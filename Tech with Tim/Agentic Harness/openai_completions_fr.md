| Champ | Signification |
| --- | --- |
| `id` | Identifiant de la réponse générée. |
| `choices` | Liste des réponses possibles du modèle. |
| `finish_reason` | Raison de la fin de génération (`stop`, `length`, etc.). |
| `index` | Index de la réponse dans le tableau `choices`. |
| `logprobs` | Informations sur les probabilités des tokens générés, si disponibles. |
| `message` | Objet contenant le message généré par le modèle. |
| `message.role` | Rôle du message, ici `assistant`. |
| `message.content` | Texte final destiné à l’utilisateur. |
| `message.refusal` | Indication éventuelle d'un refus de répondre. |
| `message.annotations` | Annotations éventuelles associées au contenu. |
| `message.audio` | Données audio éventuelles. |
| `message.function_call` | Informations sur un appel de fonction, selon le format utilisé. |
| `message.tool_calls` | Liste des appels d’outils éventuels. |
| `message.reasoning` | Raisonnement éventuel renvoyé par le modèle ou l'implémentation ; champ non standard. |
| `created` | Date de création au format timestamp Unix. |
| `model` | Nom du modèle utilisé. |
| `object` | Type d’objet retourné, ici `chat.completion`. |
| `metadata` | Métadonnées supplémentaires éventuelles. |
| `moderation` | Informations éventuelles liées à la modération. |
| `service_tier` | Niveau de service utilisé, si applicable. |
| `system_fingerprint` | Identifiant lié à la configuration du système d'inférence. |
| `usage` | Statistiques d'utilisation des tokens. |
| `usage.completion_tokens` | Nombre de tokens générés par le modèle. |
| `usage.prompt_tokens` | Nombre de tokens fournis en entrée. |
| `usage.total_tokens` | Nombre total de tokens utilisés. |
| `usage.completion_tokens_details` | Détails supplémentaires sur les tokens générés, si disponibles. |
| `usage.prompt_tokens_details` | Détails supplémentaires sur les tokens d'entrée, par exemple les tokens mis en cache ou associés à des images ou de l'audio. |