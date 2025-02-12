# Conception

Document de conception de l'outil pdf2chunks.

## Besoins

Création de chunks vectorisé à destination d'une BDD vectoriel (Milvus) pour être exploité par des requêtes au sein du pipeline RAG.

## Contraintes

- N'importe quel PDF doit pouvoir être parser.
- Il faut impérativement préserver la véracité de la donnée entre le PDF et la BDD.
- L'outil doit être le plus simple et concis possible.
- Utilisation du format Milvus pour la BDD (Vecteur + Données).

## Exceptions

- N'inclue pas la gestion des images et formules mathématiques dans les PDF.
- Ne prend pas les PDF protégés et/ou cryptés.
- Demande un minimum de structuration du document (niveau de titres au minimum).

## Technologies

- Python3 (uv, camelot-py, pdfplumber)
- Milvus 
- Modèle SFR-embedding-mistral
- Modèle mistral-7B
- Ollama

## Fonctionnalités principales

- Parser un document PDF pour déterminer la structure du document (titres, tableaux, paragraphes...).
- Création d'une Dictionnaire de tous les éléments avec leur metadatas.
- Découpage en chunks, utilisationn de la méthode overlap en cas de contenu trop long.
- Vectorisation des chunks avec le modèle d'embedding.
- Ajout à la BDD (Milvus).

## Formats des contenus

### Structure post parser 
```python
pdf_structure = {
  'title': 'Rapport Annuel 2024',
  'sections': [
      {
          'title': 'Résumé Exécutif',
          'path': 'resume_executif',
          'type': 'text',
          'content': '[[PAGE_MARKER_550e8400-e29b-41d4-a716-446655440000:1]]Contenu du résumé...[[PAGE_MARKER_550e8400-e29b-41d4-a716-446655440001:2]]Suite du résumé',
          'subsections': []
      },
      {
          'title': 'Résultats Financiers',
          'path': 'resultats_financiers',
          'subsections': [
              {
                  'title': 'Budget Global',
                  'path': 'resultats_financiers/budget_global',
                  'type': 'table',
                  'content': '[[PAGE_MARKER_550e8400-e29b-41d4-a716-446655440002:2]]Département | Budget\nR&D | 500K€',
                  'subsections': []
              }
          ]
      }
  ]
}
```

### Formats des Chunks 

**Chunks naturels (avant découpage) :**
```python 
# Type text
chunks = {
   'chunk_123': {
       'title': 'Introduction',
       'path': 'chapitre1/section1', 
       'type': 'text',
       'content': '[[PAGE_MARKER_550e8400-e29b-41d4-a716-446655440000:1]]Paragraphe entier...[[PAGE_MARKER_550e8400-e29b-41d4-a716-446655440001:2]]Suite du paragraphe' # Pas de limite de taille
   }
}

# Type table
chunks = {
   'chunk_789': {
       'title': 'Budget 2024',
       'path': 'finance/budgets/2024',
       'type': 'table',
       'content': '[[PAGE_MARKER_550e8400-e29b-41d4-a716-446655440002:5]]Département | Budget | Dépenses\nR&D | 500K€ | 450K€\nMarketing | 300K€ | 280K€\nIT | 200K€ | 190K€'
   }
}
```


**Chunks découpés :**
```python
# Type text
chunks = {
    'chunk_123_1': {  # Nouveau suffixe pour identifier les sous-parties
        'page': 1,
        'title': 'Introduction',
        'path': 'chapitre1/section1',
        'type': 'text', 
        'content': 'Première partie du paragraphe...'  # Taille contrôlée
    },
    'chunk_123_2': {
        'page': 1,
        'title': 'Introduction',
        'path': 'chapitre1/section1',
        'type': 'text',
        'content': 'Partie du paragraphe avec overlap...'  # Contient une partie du chunk précédent
    }
}

# Type table
chunks = {
    'chunk_789_sub_1': {
        'page': 5,
        'title': 'Budget 2024',
        'path': 'finance/budgets/2024',
        'type': 'table',
        'content': 'Département | Budget | Dépenses\nR&D | 500K€ | 450K€'
    },
    'chunk_789_sub_2': {
        'page': 5,
        'title': 'Budget 2024',
        'path': 'finance/budgets/2024',
        'type': 'table',
        'content': 'Département | Budget | Dépenses\nMarketing | 300K€ | 280K€\nIT | 200K€ | 190K€'
    }
}
```

### Format à destination du modèle embed 

**Type text :**
```text 
[METADATA]
Page: 1
Title: Introduction
Path: chapitre1/section1
Type: text

[CONTENT]
Ce document présente les résultats de notre étude sur...
```

**Type table :**
```text 
[METADATA]
Page: 2
Title: Résultats Financiers
Path: chapitre2/resultats/finance
Type: table

[CONTENT]
Année | Revenue | Profit
2023 | 100K€ | 20K€
2024 | 150K€ | 30K€
```

### Format attendu par Milvus 

```python 
# Type text
text_data = {
    'id': 'chunk_123',
    'vector': [0.1, 0.2, ...],
    'metadata': {
        'page': 1,
        'title': 'Introduction',
        'path': 'chapitre1/section1',
        'type': 'text',
        'content': 'Ce document présente les résultats de notre étude sur...'
    }
}

# Type table 
table_data = {
    'id': 'chunk_124',
    'vector': [0.3, 0.4, ...],
    'metadata': {
        'page': 2,
        'title': 'Résultats Financiers',
        'path': 'chapitre2/resultats/finance',
        'type': 'table',
        'content': 'Année | Revenue | Profit\n2023 | 100K€ | 20K€\n2024 | 150K€ | 30K€'
    }
}
```

## Liens utiles

### Python
- [Python](https://www.python.org/) - Programming language.
- [UV](https://docs.astral.sh/uv/) - An extremely fast Python package and project manager.
- [Camelot-py](https://pypi.org/project/camelot-py/) - PDF Table Extraction for Humans.
- [PDF-Plumber](https://pypi.org/project/pdfplumber/) - Plumb a PDF for detailed information about each text character, rectangle, and line.

### BDD
- [Milvus](https://milvus.io/fr) - Open-source vector database built for GenAI applications.

### Modèles IA

#### sfr-embedding-mistral
An embedding model created by Salesforce Research that you can use for semantic search.
- [🤗 Salesforce/SFR-Embedding-Mistral](https://huggingface.co/Salesforce/SFR-Embedding-Mistral)
- [Ollama: avr/sfr-embedding-mistral](https://ollama.com/avr/sfr-embedding-mistral)

#### mistral-7B
The 7B model released by Mistral AI, updated to version 0.3. 
- [🤗 mistralai/Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3)
- [Ollama: mistral](https://ollama.com/library/mistral)

## Misc 
- [Ollama](https://ollama.com/) - Ollama is an open-source tool that allows running and managing large language models locally.
