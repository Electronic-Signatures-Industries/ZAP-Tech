#!/usr/bin/python3

import pytest

from brownie import accounts


@pytest.fixture(scope="module", autouse=True)
def setup(approve_many, org, nft):
    nft.mint(org, 100000, 0, "0x00", {"from": accounts[0]})


def test_org_txfrom(nft, cust):
    """Org transferFrom custodian"""
    nft.transfer(accounts[1], 10000, {"from": accounts[0]})
    nft.transfer(cust, 10000, {"from": accounts[1]})
    nft.transferFrom(cust, accounts[1], 5000, {"from": accounts[0]})
    assert nft.balanceOf(accounts[1]) == 5000
    assert nft.balanceOf(cust) == 5000
    assert nft.custodianBalanceOf(accounts[1], cust) == 5000


def test_member_txfrom(nft, cust):
    """Member transferFrom custodian"""
    nft.transfer(accounts[1], 10000, {"from": accounts[0]})
    nft.transfer(cust, 10000, {"from": accounts[1]})
    with pytest.reverts("Insufficient allowance"):
        nft.transferFrom(cust, accounts[1], 5000, {"from": accounts[1]})
    with pytest.reverts("Insufficient allowance"):
        nft.transferFrom(cust, accounts[1], 5000, {"from": accounts[2]})
