from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os


# Below we're deploying the associated image and metadata for each token on our last deployed 
# NFT contract to IPFS. We're also storing the metadata for each token locally. So everything 
# is set up except the actual linking from token to tokenURI (which we do in set_tokenuri.py)

# Below we're saying, on our latest deployed NFT contract, for each token, grab the image that
# the token is supposed to refer to, and deploy it to IPFS. Then grab the imageURI of the image 
# on IPFS and add it to the metadata for the token. Fill in the rest of the metadata of the 
# token, store the file in the ./metadata/rinkeby folder (or whatever chain the contract is 
# deployed on, and then upload the metadata to IPFS as well so the token can then map to 
# its tokenURI and in turn the ImageURI. (We don't map the tokens to the tokenURI here though. 
# We do that in set_tokenuri.py). 

def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()           # number of tokens minted on the contract
    print(f"You have created {number_of_advanced_collectibles} collectibles!") 
    for token_id in range(number_of_advanced_collectibles):                         # for each token
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id)) 
        metadata_file_name = (f"./metadata/{network.show_active()}/{token_id}-{breed}.json") # file name will look like this
        collectible_metadata = metadata_template                                    #  The metadata should follow the template in ./metadata/sample_metadata.py)
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")   # if metadata file already exists, then skip (means we've already stored the metadata for that token)
        else:                                                                       # else create metadata and store it in a separate file for each token
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)      # upload the image to IPFS and grab the ImageURI
            collectible_metadata["image"] = image_uri   # store the imageURI in our metadata
            with open(metadata_file_name, "w") as file: # write the metadata to a file
                json.dump(collectible_metadata, file)   # dump the file here
            upload_to_ipfs(metadata_file_name)          # upload the metadata to IPFS



# Below what we're doing is we're inputting a local file path of an image or metadata file, and 
# we're uploading it to an IPFS node on our local machine, and then returning the 
# URI that the image or file is stored at. (This will be the tokenURI if it's a metadata file 
# or the imageURI if it's an image.)

# This is uploading to the IPFS node of our own machine. So we have to have the IPFS daemon 
# running. We could alternatively just upload it to IPFS through Pinata (a third party) 
# that will pin our NFTs for us. (We wrote the code to do this in upload_to_pinata.py if 
# you decide to do that in the future)
def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp: # rb means open in binary (bc it's an image)
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"  # This is our IPFS URL (we spun up our machine as an IPFS node!)
        endpoint = "/api/v0/add" # This is the IPFS API endpoint that we use to upload our files to IPFS
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary}) # This makes a post request with the file to the endpoint
        ipfs_hash = response.json()["Hash"] # The API returns a few items, we're grabbing the has of the image (IPFS hashes everything stored on it so it's pretty easy to just work with the hashes. As always, if you change even one pixel, the hash changes completely.)
        filename = filepath.split("/")[-1:][0] # This basically turns "./img/0-PUG.png" into "0-PUG.png"
        uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}" # finally, print out the IPFS tokenURI/imageURI. This link will take us to where our data/image is stored on IPFS.
        print(uri)
        return uri