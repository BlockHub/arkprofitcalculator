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


def gen_balance_report():
    addresses = []
    with open('wallets.txt', 'r') as wallets:
        for wallet in wallets:
            addresses.append(wallet.strip('\n'))

    blacklist = []
    with open('blacklist.txt', 'r') as txids:
        for txid in txids:
            blacklist.append(txid)

    df_list = []
    for address in addresses:
        balances = []
        timestamps = []
        balance_over_time = arkdb.Address.balance_over_time(address)
        for i in balance_over_time:
            balances.append(i.amount/info.ARK)
            timestamps.append(utils.arkt_to_datetime(i.timestamp))

        df = DataFrame({'Amount': balances, 'Date': timestamps})
        df_list.append(df)

    sheetlist = []
    for i in addresses:
        sheetlist.append(i[:12])

    dfs_tabs(df_list, sheetlist, 'balancereport.xlsx')


def main():
    arkdb.set_connection(
        host=config.CONNECTION['HOST'],
        database=config.CONNECTION['DATABASE'],
        user=config.CONNECTION['USER'],
        password=config.CONNECTION['PASSWORD'],
    )
    gen_balance_report()


if __name__ == '__main__':
    main()