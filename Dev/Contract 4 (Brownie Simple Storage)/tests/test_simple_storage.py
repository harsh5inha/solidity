from brownie import SimpleStorage, accounts

# These are two tests we wrote which check to see if our functions were working as expected
# Note though that we actually do deploy new contracts each time we run these tests
# However they don't actually go on to any real chains because we're just deploying and updating on a local Ganache chain etc.
# We're just using the first of the generated accounts from Ganache here

def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected


def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    expected = 15
    txn = simple_storage.store(expected, {"from": account})
    txn.wait(1)
    # Assert
    assert expected == simple_storage.retrieve()