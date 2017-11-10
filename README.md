# arkprofitcalculator
A simple script using arkdbtools to calculate staking rewards and balance over time.


This script connects to an ark-node and creates a report of historical staking rewards and balance over time.

If you have no experience setting up an ark-node, follow this guide: https://github.com/Nijmegen-Consultancy-Group/arkdbtools/blob/master/arkdbtools/readme.md

To set up, first edit the config.py with your connection parameters. If you are querying a node on localhost, there is no need to edit this file.

arkprofitcalculator/config.py
```python
CONNECTION = {
    # location of the ark-node
    'HOST': 'localhost',
    # blockchain you wish to query
    'DATABASE': 'ark_mainnet',
    # standard user used by the node is 'ark'. This one always exists.
    'USER': 'ark',
    'PASSWORD': None,
}
```

Then install the dependencies:

```sh
pip install -r requirements.txt
```

now enter the addresses you wish to receive reports on. Just enter them in wallets.txt using notepad or

```sh
nano wallets.txt
```

seperate the addresses with an enter:

arkprofitcalculator/wallets.txt
```
addressone
addresstwo
```

If you notice that there are transactions in the payoutreport.xlsx that weren't payouts, and you wish to omit these transactions in future
calculations; add them to blacklist.txt. You can also use this to remove sender addresses.

arkprofitcalculator/wallets.txt
```
txid
senderaddress
```

The report generates 2 .xlsx files: 
```
'payoutreport.xlsx'
'balancereport.xlsx'
```

Each tab in the xlsx files concerns a single wallet. The payoutreport shows the amount in Ark, balance at time of payout, ROI (payout/balance * 100)
and txids of the payouts. The balance report shows the balance over time over each wallet, including payouts.

If you have any requests for additions to this calculationscript, feel free to add an issue. If you used the payoutscript and wish to support development,
donations are welcome at AJwHyHAArNmzGfmDnsJenF857ATQevg8HY. If you are setting up an ark-node, make sure to use my referall link at digitalocean: https://m.do.co/c/b5eee933a448





