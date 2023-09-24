with open("app/utils/configs/ipfs.txt", "r") as f:
        imageURI_list_hashes = [line.strip() for line in f.readlines()]
