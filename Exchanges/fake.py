from brownie import accounts,Fake
import os



#brownie run fake --network bsc-test


def deploy():
    owner = accounts.add(os.getenv("PRIVATE_KEY2"))
    user = accounts.add(os.getenv("PRIVATE_KEY3"))
    fake_contract = Fake.deploy(1000000000000000000000000000,"WBNB","WBNB",{"from": owner})

    fake_contract.transfer(user, 1, {"from": owner})

    breakpoint()


def main():
    deploy()
