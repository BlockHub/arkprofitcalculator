import balanceovertimegenerator
import payoutprofitcalculator
import config
import arkdbtools.dbtools


def main():
    arkdbtools.dbtools.set_connection(
        host=config.CONNECTION['HOST'],
        database=config.CONNECTION['DATABASE'],
        user=config.CONNECTION['USER'],
        password=config.CONNECTION['PASSWORD'],
    )
    payoutprofitcalculator.gen_payout_report()
    balanceovertimegenerator.gen_balance_report()


if __name__ == '__main__':
    main()