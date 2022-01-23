from web3 import Web3
import time  
from halo import Halo
from ABI import locate , panABI 
# from ABI import new  as sellABI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import clipboard as clip 
from config import pKey, tokenWallet





# assigning values 
clip.copy("")
bsc =  "https://bsc-dataseed.binance.org/"
web3 =  Web3(Web3.HTTPProvider(bsc))
PCRA,wbnb  = locate['PCRA'], locate['wbnb']

# pKey = ""
proceed = False 




# define functions to use
def generateSellABI(CA):

    global sellABI 

    try:

        with open(f"{CA}.abi",'r') as file:
            sellABI =  file.readline()

    except FileNotFoundError as e:
        print("File not found , getting abi for you now do not close the browser \n browser would close by its self")
        driver = webdriver.Chrome(executable_path='/home/grey/.webdrivers4Me/chromedriver_8')
        driver.get(f"https://bscscan.com/address/{CA}#code")

        aa =  driver.find_element_by_xpath('//*[@id="divVmTrace"]/a')
        aa.click()
        clip.copy(clip.paste() )
        sellABI =  clip.paste() 

        with open(f"{CA}.abi",'w') as file:
            file.write(sellABI) 

        driver.quit() 

    finally:

        

        return sellABI   


def sellTokenInput(cont_id,symbol):
    
    bal = getTokenBalance(cont_id)
    while True:
        command = input(f"\n Press 1 to sell all tokens\n Press 2  to enter figure manually")
        if command =='1':


            return int(bal['CBal'])
        elif command=='2':

            while True:
                print(f"\t\t\t\t\t\tCurrent Balance {bal['CBal']}")
                try:
                    manValue = int(input("Enter Value here: "))
                    if manValue > bal['CBal']:
                        print(f"Error Value Specified is greater than your Available balance available balance is :{bal['CBal']} and you specified {manValue}")
                    else:
                        print("Value Accepted")
                        return manValue

                except ValueError as e:
                    print("Enter valid integer without decimals")
        else:
            print("\t\t\t\twhat did you  just type? Read the instruction and try again")

def getBnbBalance(tokenWallet):

        balance = web3.eth.get_balance(tokenWallet)
        humanReadable =  web3.fromWei(balance,'ether')
        
        return {'readable': humanReadable, 'wei':balance}

def getTokenBalance(token):
    global tokenWallet, sellABI
    token_contract = web3.eth.contract(token,abi=sellABI)
    balance =  token_contract.functions.balanceOf(tokenWallet).call()
    symbol =  token_contract.functions.symbol().call()
    readable =  web3.fromWei(balance,'ether')

    print(f"Balance for {symbol} is {readable}")
    return {"RBal":balance, "CBal":readable}

def swapTokenToBnb(ctrInstance,tokenValue,cont_id,):
    global wbnb
    print(ctrInstance)
    print(tokenValue)
    print(cont_id)
    with Halo(text="swapping Tokens for BNB", spinner="dots"):
        print("i am here 0")
        pancakeswap2_txn =  ctrInstance.functions.swapExactTokensForETHSupportingFeeOnTransferTokens(
            tokenValue, 0,
            [cont_id,wbnb],
            tokenWallet,
            (int(time.time())+10000)
        ).buildTransaction({
            'from': tokenWallet,
            'gasPrice':web3.toWei('5','gwei'),
            'nonce': web3.eth.get_transaction_count(tokenWallet)
        })
    print("i am here 1")
    with Halo(text="Signing Transaction", spinner='dots' ):
        signed_txn =  web3.eth.account.sign_transaction(pancakeswap2_txn, private_key=pKey)
        tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        with open("sellTXN.txt" ,'a') as file:
            file.write(f"{time.ctime()} \n Transaction Receipt: {web3.toHex(tx_token)}")
            file.write("\n")
        print()
        print("Transaction Completed")

def main():
    
    while True:
        if web3.isConnected():
            print("\nConnection successful")
            proceed =  True 
            break
        else:
            print("\nUnable to connect to BSC check internet... trying again")
            time.sleep(1)
            print()
            print(wbnb)
            print(PCRA)    

    if proceed:

        #token to sell contract id 
        token = web3.toChecksumAddress(input("Enter  the contract address of token you want to sell : ")) 
        
        # set up  the pancakeswap contract
        PCSC = web3.eth.contract(address=PCRA, abi=panABI)
        generateSellABI(token)
        # contractd instance for sell token
        sellToken = web3.eth.contract(token,abi=sellABI)
        symbol =  sellToken.functions.symbol().call()
        # getTokenBalance(sellToken)
        

        tokenValue1 = sellTokenInput(token, symbol)

        tokenValue2=  web3.toWei(tokenValue1, "ether")  #pass this into the swap funcniton
        
        # approve
        # approveToken(token)
        while True:
            finalSell = input("type yes or number 7 and i would sell this instant:>>>\t   ").strip()
            if finalSell.lower() == 'yes' or finalSell=='7':
                # swaptoken
                swapTokenToBnb(PCSC,tokenValue2,token)
                print("Swap Done")
                break
            
        

if __name__ == "__main__":
    main()