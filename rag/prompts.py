FIXING_CONTEXT_PROMPT = """
Ton rôle est d'analyser et de comprendre le contexte d'une entrée textuelle qui peut être mal formatée, incomplète ou ambiguë. Tu dois extraire les informations importantes, les reformuler de manière claire et organiser le contenu pertinent pour en tirer un contexte compréhensible. Voici les étapes à suivre :

1. Identifier les éléments clés : Repère les informations importantes telles que les noms, dates, lieux, événements ou autres données contextuelles utiles.
2. Corriger le format : Si des informations sont mal structurées ou confuses, reformule-les clairement tout en préservant leur sens original.
3. Synthétiser le contexte : Crée un résumé concis et clair de ce que tu as compris, même si certains détails sont incomplets ou incorrects.

Ton objectif est de fournir un résumé clair et exploitable du contexte malgré les erreurs ou le mauvais formatage.

Texte à analyser : {retrived_context}

Contexte extrait :
"""


FIXING_QUESTION_PROMPT = """
Vous allez recevoir une question contenant des répétitions ou des erreurs de formulation. Corrigez-les en veillant à conserver le sens global de la question. Remplacez les nombres en lettres par des chiffres tout en respectant l'ordre original des mots autant que possible.

{question}
"""

ANSWER_PROMPT = """
Formulez une réponse sous forme de réplique basée uniquement sur les informations fournies dans le contexte suivant, sans ajouter de données externes. Répondez directement, sans introduction ni phrases superflues. Mentionnez toutes les informations et chiffres mentionnées dans l'analyse et n'ignorez aucune information pertinente.

Contexte : {context}
"""

TESTING_PROMPT = """
Vérifiez si les deux questions suivantes sont à la fois sémantiquement similaires. Si elles le sont, retournez simplement 'True'.
Sinon, retournez 'False'.

Question 1 : {q1}

Question 2 : {q2}
"""
