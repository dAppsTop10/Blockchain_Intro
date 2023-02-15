import pytest, brownie
from brownie import config, network, Arbitrage,accounts,Contract
from scripts.helper_scripts import  toWei, approve_erc20, FORKED_BLOCHCHAINS, ZERO_ADDRESS
from scripts.get_weth import get_weth


def test_deploy():
    weth_token = config["networks"][network.show_active()]["weth-token"]
    dai_token = config["networks"][network.show_active()]["dai-token"]
    uni_router_address = config["networks"][network.show_active()]["uniswap-router"]
    sushi_router_address = config["networks"][network.show_active()]["sushiswap-router"]

    arbitrage, owner = deploy_arbitrage()

    assert arbitrage.address != ZERO_ADDRESS
    assert owner == accounts[0]
    assert arbitrage.wethAddress() == weth_token
    assert arbitrage.daiAddress() == dai_token
    assert arbitrage.uniswapRouterAddress() == uni_router_address
    assert arbitrage.sushiswapRouterAddress() == sushi_router_address



def test_deposit():
    weth_token = config["networks"][network.show_active()]["weth-token"]
    arbitrage, owner = deploy_arbitrage()
    amount = toWei(5)
    approve_erc20(weth_token, arbitrage.address, amount, owner)
    deposit_tx = arbitrage.deposit(amount, {"from": owner})
    deposit_tx.wait(1)
    weth = Contract.from_explorer("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
    print("balance of arbitrage contract: ", weth.balanceOf(arbitrage))
  
    assert arbitrage.arbitrageAmount() == amount


def test_withdraw():

    weth_token = config["networks"][network.show_active()]["weth-token"]

    arbitrage, owner = deploy_arbitrage()
    amount = toWei(5)

    approve_erc20(weth_token, arbitrage.address, amount, owner)

    deposit_tx = arbitrage.deposit(amount, {"from": owner})
    deposit_tx.wait(1)
    weth = Contract.from_explorer("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
    print("balance of arbitrage before withdraw: ", weth.balanceOf(arbitrage))
    withdraw_amount = toWei(2)

    withdraw_tx = arbitrage.withdraw(withdraw_amount, {"from": owner})
    withdraw_tx.wait(1)
    weth = Contract.from_explorer("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
    print("balance of arbitrage after withdraw 2 wei: ", weth.balanceOf(arbitrage))
  
    assert arbitrage.arbitrageAmount() == amount - withdraw_amount

def test_get_price():


    arbitrage, owner = deploy_arbitrage()
    amount = toWei(5)
    result_uni = arbitrage.getPrice_uniswap(amount)
    uni_price = result_uni /1e18
    print("with 5 eth  in uniswap you will get :", uni_price)
    result_sushi = arbitrage.getPrice_sushiswap(amount)
    susi_price = result_sushi.return_value / 1e18
    print("with 5 eth  in sushiswap you will get :", susi_price )

    if uni_price > susi_price:
        test_diff = check_diff(uni_price,susi_price,amount)

    else:
        test_diff = check_diff( susi_price, uni_price,amount)


def check_diff(higherPrice,lowerPrice,amountIn):
 
    difference= ((higherPrice - lowerPrice) * 10 ** 18) /higherPrice
    payed_fee = (2 * (amountIn * 3)) / 1000

    if difference > payed_fee:
        print("good to go")
    else:
        print("not worth it")

def test_make_arbitrage():
    weth = Contract.from_explorer("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")
    weth_token = config["networks"][network.show_active()]["weth-token"]

    arbitrage, owner = deploy_arbitrage()

    amount = toWei(5)

    approve_erc20(weth_token, arbitrage.address, amount, owner)

    deposit_tx = arbitrage.deposit(amount, {"from": owner})
    deposit_tx.wait(1)
    # Try to make arbitrage and revert if it's not profitable

    print("make arbitrage")
    print("balance of weth before arb ", arbitrage.arbitrageAmount()/1e18)
    arbitrage_tx = arbitrage.makeArbitrage({"from": owner})
    arbitrage_tx.wait(1)

    print("balance of weth arbitrage after arb ",arbitrage.arbitrageAmount()/1e18)

  



def deploy_arbitrage():
    weth_token = config["networks"][network.show_active()]["weth-token"]
    dai_token = config["networks"][network.show_active()]["dai-token"]
    uni_router_address = config["networks"][network.show_active()]["uniswap-router"]
    sushi_router_address = config["networks"][network.show_active()]["sushiswap-router"]

    owner = accounts[0]
    get_weth(owner, 10)

    arbitrage = Arbitrage.deploy(uni_router_address,sushi_router_address,weth_token,dai_token,{"from": owner}
    )

    return arbitrage, owner

def main():
    test_make_arbitrage()
