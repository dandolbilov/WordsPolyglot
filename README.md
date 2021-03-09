# WordsPolyglot

This is a website for Language Learning.  
It's built with Python (Django) and jQuery.  

*The website is hosted for free on Heroku now.*  
*Heroku free plan has PostgreSQL* ***Row Limit = 10000*** *(it's not enough).*  
*That's the problem, because I have more interesting pet-projects to continue.*  

## Use Case 1 : learning one foreign language.

Steps:
1. Select (or Import) target Ranked Words list.
    1.1. Select target language (e.g., "German").
    1.2. Select target level ([CEFR Level](https://en.wikipedia.org/wiki/Common_European_Framework_of_Reference_for_Languages) or number of words, e.g., "German: A1").
    1.3. Rank (auto-rank) target words with [frequency lists](https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists).
2. Customize (add) target words by user personal context.
    2.1. Select priority topics and life situations.
    2.2. User can be a tourist, business visitor or immigrant.
    2.3. User (worker) can be a doctor, engineer, etc.
    2.4. Upgrade words ranking for selected priority topics.
3. Build User Words list.
    3.1. Old (existing in User Words) target words are marked as "known" (or hidden).
    3.2. Each "unknown" target word has Sentences/Phrases (with audio).
    3.3. Select the most useful sentence as Phrase1 (for any new word).
    3.4. Select several other sentences as Examples (for the same word).
    3.5. Add the word to User Words (fields: Word, PoS, URank, Phrase1, Examples).
    3.6. User can edit URank (user word rank) and Examples fields.
4. Learn the words (list of Phrase1).
    4.1. Export the word cards to Anki file.
    4.2. Export the list of Phrase1 to all-in-one audio file.
5. Go to the next level or import custom words (step 1).

## Use Case 2 : learning multiple languages.

* Build User Words list more carefully.
    * Collect the most useful phrases only.
    * Prefer phrases with many (languages) audio files.
* **Memorize the chain of phrases** in "major" language (English).
    * Phrase1 can contains **two** phrases (Examples field is not used).
    * **Link:** each next entry word is selected from previous Phrase1.
    * **Learn the same chain of phrases in other languages.**

*Example of phrases link:*

Word (entry) | PoS | URank | Phrase1
---- | --- | ----- | -------
| | | *English*
name | noun | 1 | Your name, please. / What's the name of this **street**?
**street** | noun | 2 |
| | | *German*
Name | | 1 | Ihren Namen, bitte. / Wie heißt diese Straße?
Straße | | 2 |
| | | *Spanish*
nombre | | 1 | Su nombre, por favor. / ¿Cómo se llama esta calle?
calle | | 2 |
| | | *French*
Nom | | 1 | Votre nom, s'il vous plaît. / Comment se nomme cette rue?
rue | | 2 |
| | | *Russian*
имя | | 1 | Ваше имя, пожалуйста. / Как называется эта улица?
улица | | 2 |

## Running Locally (http://localhost:5000/).

```
$ pip install -r requirements.txt

$ python manage.py collectstatic

$ python manage.py makemigrations

$ python manage.py migrate

$ python manage.py createsuperuser

$ heroku local
or
$ heroku local web -f Procfile.windows
```
