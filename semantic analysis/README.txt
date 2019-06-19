*FILES NEEDED TO EXECUTE*
--> main.py : This file will execute generate_documents.py and semantic_analysis.py in sequence and generate output. 'document' and 'output' folder can be deleted to test main.py execution.


*FILES DESCRIPTION*
1. generate_documents.py : It generate document folder and documents.json inside it. documents.json contains all documents (19043 documents) data after cleaning them from 22 .sgm files of input folder.

2. main.py : Actual file which is neeeded to execute. It will just execute generate_documents.py and semantic_analysis.py in sequence.

3. semantic_analysis.py : It contains actual algorithm of semantic analysis using vector IR model. It generates output folder and .txt files inside it. Output folder which was generated after execution is submitted.