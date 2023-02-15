from brownie import network, interface, config,accounts
from scripts.helper_scripts import fromWei, toWei



def get_weth(account, amount):
    weth_address = config["networks"][network.show_active()]["weth-token"]

    weth = interface.IWeth(weth_address)

    deposit_tx = weth.deposit({"from": account, "value": toWei(amount)})
    deposit_tx.wait(1)

    print(f"You recieved {amount} weth")

def main():
    account = accounts[0]
    amount = toWei(10)
    get_weth(account, amount)
