# Bulgarian vocabulary extender

*Miroslav Dzhokanov, 2025*

## Abstract

**Introduction:** For training bulgarian language tokenizers a high-quality set of validated *words* is needed.

**Purpose:** This project aims at building *the largest vocabulary* of valid Bulgarian words available online.

**Data:** Data will be fetched from *Chitanka, GitHub, Kaggle, HuggingFace*, other public and private sources.

**Results:** The initial `Chitanka` set of words has been increased by `+10.6%`.

**Keywords:** *bulgarian language, words, vocabulary, dictionary*

## Data

Following datasets will be used in current project. 

### 1. [Chitanka Rechnik](https://rechnik.chitanka.info/)
* **Size**: 4 013 667 words (not unique) , 119 677 lemmas (not unique)
* **Quality**: Medium-quality (invalid words, spaced words, dashed words, latin symbols). Probably **semi-automatically verified**.
* **License**: MIT
* **Description**: Chitanka has a *publicly* available vocabulary since 2010. It provides both *words* and *lemmas*.

### 2. [BG-PoS-dataset](https://www.kaggle.com/datasets/auhide/bulgarian-part-of-speech-dataset4)
* **Size**: 1 348 103 words (not unique)
* **Quality**: High-quality (invalid words, names).
* **License**: CC0: Public Domain
* **Description**: POS-tagged dataset, specifically designed for token classification.

### 3. [BG-dictionary-2024](https://huggingface.co/datasets/thebogko/bulgarian-dictionary-2024)
* **Size**: 1 147 604 words (not unique)
* **Quality**: Medium-quality (invalid words, dashed words, names, latin symbols).
* **License**: Apache 2.0
* **Description**: POS-tagged dataset, specifically designed for token classification.

### 4. [BG WordLists](https://github.com/miglen/bulgarian-wordlists)
* **Size**: 234 115 words (unique) 
* **License**: GPL-3.0
* **Quality**: Medium-quality (invalid words, dashed words, duplicates). Automatically scrapped and parsed words.
* **Description**: *Public* git repo providing lists of bulgarian words (incl. names, abbreviations, profanity lists, etc.). 

### 5. [WordHelper](https://github.com/pepk0/WordHelper)
* **Size**: 233 972 words (unique)
* **License**: MIT
* **Quality**: High-quality (duplicates). Probably **not manually verified**.
* **Description**: *Public* git repo providing a list of words, used for crossword suggestions.

### 6. [Stork Project](https://github.com/project-stork) 
* **Size**: 1 294 882 words (unique)
* **License**: Private
* **Quality**: Low-quality (invalid words, stitched words). Automatically scrapped and parsed words.
* **Description**: A private dataset. Probably the largest BG dataset created ever (700M sentences, 3B words). We have TF-IDF-scored all the words across all sentences. In result we came up with a ranking of 10M unique Bulgarian words. The **first 10%** of the list (**highest TF-IDF scores**) will be used as a source in the current project.

### 7.  [IBL BAS Vocabulary]( https://ibl.bas.bg/rbe/lang/bg/)
* **Size**: 124 000 lemmas (unique)
* **License**: Private
* **Quality**: Highest-quality. **Manually verified**.
* **Description**: The Institute for Bulgarian Language in BAS posess official Bulgarian dictionary. Unfortunately, they don't want to share the data in a machine-readable format. However, we can use their online vocabulary for checking the validity of some words, if in doubt (the site has anti-bot system, so it can't be automatically scrapped).
