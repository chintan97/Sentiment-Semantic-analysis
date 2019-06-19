*FILES NEEDED TO EXECUTE*
--> sentiment_analysis.py : It will generate output folder when executed. Sample output folder after program execution is submitted. 'output' folder can be deleted to test execution of sentiment_analysis.py file.


*FILES DESCRIPTION*
1. change_sentiwords.py : script used to filter sentiwords.txt file. After extracting words and polarity, they are stored in sentiwords_new.json in json format.

2. fetch_tweets.py : script used to extract more than 2000 tweets based upon Twitter search API.

3. sentiment_analysis.py: actual file which contains sentiment analysis algorith.

4. sentiwords.txt : lexical dictionary provided by SentiWords [https://hlt-nlp.fbk.eu/technologies/sentiwords]

5. sentiwords_new.json : json file which is generated after executing change_sentiwords.py.

6. tweets_data.json : tweets data which is fetched after executing fetch_tweets.py