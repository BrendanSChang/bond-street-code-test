# bond-street-code-test

This repository contains the Bond Street Credit Mini-Score code test.

To run the script from the command line, simply run `CreditMiniScore.py --input path/to/input`.

The input file should be in the following format:

```
Business name
Business owner
Business assets (dollar amount)
Requested loan amount
Previous loan amount 1
Previous loan duration 1 (in months)
Previous loan payment history (in days overdue for each payment, separated by commas)
.
.
.
Previous loan amount n
Previous loan duration n
Previous loan payment history n
```

where the total number of payment history items for each loan should be the same as the loan duration. This
application assumes that payments are due monthly.

Below is an example input file for a business with a single previous 3-month loan. The first payment was made in
advance of the payment due date, the second was made on the payment due date, and the third was made late.

```
My Business
John Smith
25000
10000
5000
3
-5,0,16
```
