# Revolut Analysis

Python 3 script to analyse Revolut transactions.

This script can:

 - plot meaningful charts

 - check for errors in your statement

 - generate italian ISEE related values ("mean balance average" and "balance at 31/12/20XX"). 

## How to run it

To run the script execute the following command

```bash
./src/main.py STATEMENT_PATH [STATEMENT_PATH ...]
```

where `STATEMENT_PATH` is the path of your Revolut statement (csv or txt format).

You can generate your statement in the Revolut app for each currency that you have.

Some examples of csv statements can be found in the folder examples.
