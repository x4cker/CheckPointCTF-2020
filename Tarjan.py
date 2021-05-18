import json
def lca(pair):
    high = max(pair)
    low = min(pair)
    print(low)
    print(high)
    equal = high == low # when combining parameters = something == something , the parameters return a value of True of False.
    #which then gets to an if, - if not equal means the parameter needs to return False in order to proceed to the loop
    if not equal:
        if high % 2 == 0: #if the leftover equals = 0 when divided by two means the number is zugi
            high = (high - 2) // 2 #Integer Division - results only full integer for int result and not float.
            pair[0] = high
            pair[1] = low

        else: #Dividing Zugi and E Zugi ints
            high = (high - 1) // 2
            pair[0] = high
            pair[1] = low

    else:               # IF EQUAL Return the LCA - While its not Equal it returns to make the function again - taking the same pair and recursing it.
                        #Which makes this a Special loop function which loops until it reachs the ELSE - and when it does it prints the Current LCA.
        return pair[0] #When their are both equal - return one of the pairs as they are both the same.
    return lca(pair) #If the function reachs this point , it will return again to the beggining with the new pair generated to find a better lca until both numbers
                    # LCA is Equal


with open('tree.txt', 'r') as tree_file: #Opening the Tree file in read mode.
    tree = tree_file.read()
with open('pairs.txt', 'r') as pairs_file:
    pairs_list = json.load(pairs_file) #Loading arrary with json is just easier and looks better and does all faster!
    flag = ''

    for pair in pairs_list:
        print("THE LCA")
        print(pair)
        print(lca(pair))
        flag += tree[lca(pair)] # Prints the results from the tree, exactly as printing tree[20123], the will print the letter from the text file that is opened with "with"
        print(flag)
    print(f"FLAG: {flag}")








