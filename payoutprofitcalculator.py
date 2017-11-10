import arkdbtools.dbtools as arkdb
import arkdbtools.config as info
import arkdbtools.utils as utils
from pandas import DataFrame
from pandas import ExcelWriter
import config


def dfs_tabs(df_list, sheet_list, file_name):
    writer = ExcelWriter(file_name, engine='xlsxwriter')
    for dataframe, sheet in zip(df_list, sheet_list):
        dataframe.to_excel(writer, sheet_name=sheet, startrow=0, startcol=0)
    writer.save()


def gen_payout_report():
    addresses = {}
    with open('wallets.txt', 'r') as wallets:
        for wallet in wallets:
            addresses.update({wallet.strip('\n'): {'payouthistory': None,
                                                   'balance_history': None,
                                                   'startbalance': None}})

    blacklist = []
    with open('blacklist.txt', 'r') as txids:
        for txid in txids:
            blacklist.append(txid)

    for address in addresses:
        balance_history = arkdb.Address.balance_over_time(address)
        # payout gets all transactions received by the address, where the senderId is a registered delegate
        payouts = arkdb.Address.payout(address)

        # in case some transactions were not payouts, they need to be manually removed.
        payouthistory = [tx for tx in payouts if tx.id not in blacklist or tx.senderId not in blacklist]
        addresses[address]['payouthistory'] = payouthistory
        addresses[address]['balance_history'] = balance_history

    df_list = []

    for address in addresses:
        timestamps = []
        payoutamounts = []
        balance_at_payouts = []
        ROI = []
        txids = []

        for payouts in addresses[address]['payouthistory']:
            for x in addresses[address]['balance_history']:
                balance_at_payout = x.amount
                balance_timestamp = x.timestamp
                if x.timestamp > payouts.timestamp:
                    break

            balance_at_payouts.append(balance_at_payout/info.ARK)
            timestamps.append(utils.arkt_to_datetime(payouts.timestamp))
            payoutamounts.append(payouts.amount/info.ARK)
            txids.append(payouts.id)
            ROI.append((payouts.amount / abs((balance_at_payout - payouts.amount))) * 100)
        df = DataFrame({'Tx_id': txids, 'Timestamp': timestamps, 'Amount': payoutamounts, 'Balance at payout': balance_at_payouts,
                        'ROI': ROI})
        df_list.append(df)

    sheetlist = []
    for i in addresses:
        sheetlist.append(i[:12])

    dfs_tabs(df_list, sheetlist, 'payoutreport.xlsx')


def main():
    arkdb.set_connection(
        host=config.CONNECTION['HOST'],
        database=config.CONNECTION['DATABASE'],
        user=config.CONNECTION['USER'],
        password=config.CONNECTION['PASSWORD'],
    )
    gen_payout_report()


if __name__ == '__main__':
    main()



