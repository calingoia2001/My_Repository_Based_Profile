import pjsua2 as pj
import time
import random

    
endpoint_config = pj.EpConfig()
endpoint_config.logConfig.level = 9
endpoint_config.medConfig.sndClockRate = 8000

endpoint = pj.Endpoint()

endpoint.libCreate()
endpoint.libInit(endpoint_config)
endpoint.audDevManager().setNullDev()

print("Endpoint initialized..")

# Create SIP transport
sip_transport_config = pj.TransportConfig()
transport_type = pj.PJSIP_TRANSPORT_UDP
sip_transport_config.port = 5060

endpoint.transportCreate(transport_type, sip_transport_config)
print("Transport created..")

# Start the library
endpoint.libStart()
print("Endpoint started..")

endpoint.libHandleEvents(10)

# Subclass to extend the Account and get notifications etc.
class MyAccount(pj.Account):
    def __init__(self):
        super().__init__()

    def onRegState(self, prm):
        ai = self.getInfo()
        print("*** Register: code=" if ai.regIsActive else "*** Unregister: code=", prm.code)

class MyCall(pj.Call):
    def __init__(self, account, call_id):
        super().__init__(account, call_id)
        self.acc = account
        self.connected = False

    def onCallState(self, prm):
        
        time.sleep(5)
        print(f"THE STATE OF THE CALL HAS CHANGED: {prm}")

        call_info = self.getInfo()
        self.connected = call_info.state == pj.PJSIP_INV_STATE_CONFIRMED

        print("CONNECTED:", self.connected)
        print("current state is " + str(call_info.state) + " " + call_info.stateText)
        print("GET ID:", self.getId())
        print("HAS MEDIA:", self.hasMedia())

    def onMediaState(self):
        
        print("ON MEDIA STATE")


# pjsua2 test function
def pj_test():
    acfg = pj.AccountConfig()
    acfg.idUri = "sip:3000@192.168.1.217"
    acfg.regConfig.registrarUri = "sip:192.168.1.217"
    creds = pj.AuthCredInfo("digest", "*", "3000", 0, "1234")
    acfg.sipConfig.authCreds.append(creds)


    account = MyAccount()
    try:
        account.create(account_config)
        print("ACCOUNT?", account)
        print("\nAccount created/registered..\n")

    except pj.Error as err:
        print("ERR acc:",err)

    call = MyCall(account, pj.PJSUA_INVALID_ID)
    

    prm = pj.CallOpParam(True)

    try:
        print("Attempting to make a call...")

        # USE prm.txOption – Optional headers etc to be added to outgoing INVITE request.
        call.makeCall("sip:1000@100.94.169.195:5060;transport=udp", prm) ## Dev sip:1000@100.94.169.195:5060 sip:1000@192.168.1.217

        
        print("CALLINFO",callinfo := call.getInfo())
        print("STATE:", callinfo.state)
        print("CALLID:", callinfo.id)
        print("GET ID:", call.getId())
        print("HAS MEDIA:", call.hasMedia())

        
    except Exception as err:
        print("ERR:",err)
    # call.dump()

    endpoint.libDestroy()
if __name__ == "__main__":
    pj_test()
