from web3 import Web3 
import time 
from ABI import panABI
# from ABI import new as sellABI
from config import pKey, tokenWallet
from halo import Halo 
import  clipboard  as clip 

# just access data in config to fill in private key and address 


'''if transaction if failing you can try to increaes your gas limit instead of gas its self
so i tried using 250_000 for the a token and transaction failed twicee
upgraded it to 500_000 and it worked''' 
# fix this by creating a  dictionary that holds private key as well as bnb wallet address

input("press enter to start")
# addresses needed for the trading 
wbnb = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"
PCRA = "0x10ED43C718714eb63d5aA57B78B54704E256024E"



CA = ""
sellABI = ''

#specify a value to skip the main header in decimal i.e 0.01 or 0.001 value should be in bnb
amount = ''

if (pKey and tokenWallet) == "":

    print("as a note of warning: private key or wallet address is empty check config.py file to input data")
    print()
    print("if config.py doesnt exist create one in same directory and pass variable \n'pKey'='your private key', 'tokenWallet'='wallet address' ")
    print()
    input("press ctrl+c to cancle or press enter to continue")

if not amount:
    amount = float(input("you didnt specify an amount please specify an amount in bnb now"))
    if not amount or amount <= 0:
        raise ValueError(f"your specified amount cannot be 0 or lesser than 0 you specified {amount}")


# connecting to web3
with Halo(text="connecting to web3", spinner='dots'):
    bsc =  "https://bsc-dataseed.binance.org/"
    web3 =  Web3(Web3.HTTPProvider(bsc))
    print("\nconnected" if web3.isConnected() else "not connected")

# this would break if you dont have selenium installed 

def generateSellABI(CA):

    global sellABI 

    try:

        with open(f"{CA}.abi",'r') as file:
            sellABI =  file.readline()

    except FileNotFoundError as e:
        print("File not found , getting abi for you now")
        driver = webdriver.Chrome(executable_path='/home/grey/.webdrivers4Me/chromedriver_8')
        driver.get(f"https://bscscan.com/address/{CA}#code")

        aa =  driver.find_element_by_xpath('//*[@id="divVmTrace"]/a')
        aa.click()
        clip.copy(clip.paste() )
        sellABI =  clip.paste() 

        with open(f"{CA}.abi",'w') as file:
            file.write(sellABI )
            
        driver.quit()

    finally:

        
        return sellABI 


def approveToken(CA):
    global tokenWallet, sellABI
     
       
    token2sell =  web3.eth.contract(CA, abi=sellABI)
    token2sellBal = token2sell.functions.balanceOf(tokenWallet).call()
    symbol =  token2sell.functions.symbol().call()
    token2sellReadable =  web3.fromWei(token2sellBal,'ether')

    # approving token 


    approve =  token2sell.functions.approve(PCRA,token2sellBal).buildTransaction({
        'from': tokenWallet,
        'gasPrice': web3.toWei('5','gwei'),
        'nonce': web3.eth.get_transaction_count(tokenWallet)
    })

    signTran =  web3.eth.account.sign_transaction(approve, private_key=pKey)
    tx_ = web3.eth.send_raw_transaction(signTran.rawTransaction)

    with Halo(text="Writing transaction to file", spinner='dots'):
        with open("approve.txn",'a') as file:
            file.write(f"{time.ctime()}:{symbol} : {web3.toHex(tx_)}")
            file.write("\n")




with Halo(text= "now listening for token  just copy correct token to clip board and we would take it from there", spinner="dots"):
    clip.copy("")
    while True:
        tokenToBuy =  clip.paste()
        if len(tokenToBuy) == 42 and tokenToBuy[:2] =='0x':
            # initializes the contract 
            tokenToBuy =  web3.toChecksumAddress(clip.paste())
            contract =  web3.eth.contract(address=PCRA, abi=panABI)
            CA = tokenToBuy
            print("token Received")

            break
        else:
            continue   

# what token to swap for what token 
# tokenToBuy =  web3.toChecksumAddress(input("enter TokenAddress"))
# tokenToSpend =  web3.toChecksumAddress(wbnb)

BNB =  web3.toChecksumAddress(wbnb)
# steam = "0xc0924edefb2c0c303de2d0c21bff07ab763163b5"
nonce =  web3.eth.get_transaction_count(tokenWallet)
start = time.time()
secToWait = 60

# nonce1 =  web3.eth.get_transaction(main_wal)
# print("to Wei:")
# print(web3.towei(0.01732234, "ether"))

#initialiizng the contract to make the transactions

pancake_txn =  contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
    0,#set 0 to specify minimum amount of token you want to receive consider decimans 
    [BNB,tokenToBuy],
    tokenWallet,
    (int(time.time())+secToWait) 
).buildTransaction({
    "from":tokenWallet,
    'value': web3.toWei(amount,'ether'), #this is the token (BNB)amount you want to swap from 
    'gas': 250_000,
    'gasPrice':web3.toWei('5','gwei'),
    'nonce': nonce,
})
# passs your private key into it  at 

'''
with Halo(text=" approving... ", spinner='dots'):
    print("\nSigning the transaction with Keys")
    signed_txn = web3.eth.account.sign_transaction(pancake_txn, private_key=pKey)
    tx_token =  web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print("Done")


with Halo(text="Please Wait", spinner='dots'):
    print("\nwriting  transaction hash to file ")
    with open("transactions.txt" ,'a') as file:
        file.write(f"Transaction made on {time.ctime()} : \n Token Purchased:  {tokenToBuy}\n Transaction hash: {web3.toHex(tx_token)}")
        file.write("\n")
'''

# uncomment it to also approve token
'''
while True:
    print()
    val = input("\n Press 1 To approve Token Press 2 to skip : ")

    if val=='1':
        # getting theh sell abi for this token
        print("Getting sell contract info token")
        
        generateSellABI(CA)

        # Approving token assuming generateSellABI has overwritten sellABI to its value
        print("Approving token")
        approveToken(CA)
        print("token Approved")
        break 
    elif val =='2':
        print("Exiting Program now ")
        break 
    else:
        print("invalid input try again ")
        '''