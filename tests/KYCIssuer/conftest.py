#!/usr/bin/python3

import pytest


@pytest.fixture(scope="module")
def ikyc(KYCIssuer, org, accounts):
    kyc = accounts[0].deploy(KYCIssuer, org)
    org.setVerifier(kyc, False, {'from': accounts[0]})
    kyc.addInvestor(
        "investor1".encode(),
        1,
        '0x000001',
        1,
        9999999999,
        (accounts[1],),
        {'from': accounts[0]}
    )
    yield kyc
