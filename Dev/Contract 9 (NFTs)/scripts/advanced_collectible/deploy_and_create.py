from scripts.helpful_scripts import get_account, OPENSEA_URL, get_contract, fund_with_link
from brownie import AdvancedCollectible, config, network

def deploy_and_create():
    account = get_account()
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account}, 
        publish_source=config["networks"][network.show_active()].get("verify")
    )

    # Need to fund contract with LINK so that it can pay the VRFCoordinator for its random number
    fund_with_link(advanced_collectible.address)
    creating_tx = advanced_collectible.createCollectible({"from":account})
    creating_tx.wait(1)
    print("New token has been created!")
    return advanced_collectible, creating_tx



def main():
    deploy_and_create()