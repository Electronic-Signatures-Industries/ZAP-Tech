#!/usr/bin/python3

import pytest

from brownie import accounts


@pytest.fixture(scope="module", autouse=True)
def setup(approve_many, org, nft, cust):
    nft.mint(org, 100000, 0, "0x00", {'from': accounts[0]})
    nft.transfer(accounts[2], 1000, {'from': accounts[0]})
    nft.transfer(cust, 500, {'from': accounts[0]})
    nft.transfer(cust, 500, {'from': accounts[2]})
    org.setEntityRestriction(cust.ownerID(), True, {'from': accounts[0]})


def test_from_org(nft, cust):
    '''restricted custodian - org to custodian'''
    with pytest.reverts("Receiver restricted: Issuer"):
        nft.transfer(cust, 1000, {'from': accounts[0]})


def test_from_investor(nft, cust):
    '''restricted custodian - investor to custodian'''
    with pytest.reverts("Receiver restricted: Issuer"):
        nft.transfer(cust, 1000, {'from': accounts[2]})


def test_transferInternal(nft, cust):
    '''restricted custodian - internal transfer'''
    with pytest.reverts("Authority restricted"):
        cust.transferInternal(nft, accounts[2], accounts[3], 500, {'from': accounts[0]})


def test_to_org(nft, cust):
    '''restricted custodian - to org'''
    with pytest.reverts("Sender restricted: Issuer"):
        cust.transfer(nft, accounts[0], 500, {'from': accounts[0]})


def test_to_investor(nft, cust):
    '''restricted custodian - to investor'''
    with pytest.reverts("Sender restricted: Issuer"):
        cust.transfer(nft, accounts[2], 500, {'from': accounts[0]})


def test_org_transferFrom(nft, cust):
    '''restricted custodian - org transfer out with transferFrom'''
    nft.transferFrom(cust, accounts[2], 500, {'from': accounts[0]})
