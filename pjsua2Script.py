import time
import pjsua2 as pj

class Endpoint(pj.Endpoint):
    """
    This is high level Python object inherited from pj.Endpoint
    """
    instance = None

    def __init__(self):
        pj.Endpoint.__init__(self)
        Endpoint.instance = self


def validateUri(uri):
    return Endpoint.instance.utilVerifyUri(uri) == pj.PJ_SUCCESS


def validateSipUri(uri):
    return Endpoint.instance.utilVerifySipUri(uri) == pj.PJ_SUCCESS


# Call class
class Call(pj.Call):
    """
    High level Python Call object, derived from pjsua2's Call object.
    """
    def __init__(self, acc, peer_uri='', call_id=pj.PJSUA_INVALID_ID):
        pj.Call.__init__(self, acc, call_id)
        self.acc = acc
        self.peerUri = peer_uri
        self.connected = False
        self.onhold = False

    def onCallState(self, prm):
        ci = self.getInfo()
        self.connected = ci.state == pj.PJSIP_INV_STATE_CONFIRMED

    def onCallMediaState(self, prm):
        ci = self.getInfo()
        for mi in ci.media:
            if mi.type == pj.PJMEDIA_TYPE_AUDIO and \
              (mi.status == pj.PJSUA_CALL_MEDIA_ACTIVE or
               mi.status == pj.PJSUA_CALL_MEDIA_REMOTE_HOLD):
                m = self.getMedia(mi.index)
                am = pj.AudioMedia.typecastFromMedia(m)
                # connect ports
                Endpoint.instance.audDevManager().getCaptureDevMedia().startTransmit(am)
                am.startTransmit(Endpoint.instance.audDevManager().getPlaybackDevMedia())

                if mi.status == pj.PJSUA_CALL_MEDIA_REMOTE_HOLD and not self.onhold:
                    print("'%s' sets call onhold" % self.peerUri)
                    self.onhold = True
                elif mi.status == pj.PJSUA_CALL_MEDIA_ACTIVE and self.onhold:
                    print("'%s' sets call active" % self.peerUri)
                    self.onhold = False

    def onDtmfDigit(self, prm):
        # print("Got DTMF:" + prm.digit)
        pass

    def onCallMediaTransportState(self, prm):
        # print("Media transport state")
        pass


class Account(pj.Account):
    def onRegState(self, prm):
        print("***OnRegState: " + prm.reason)

    def onMwiInfo(self, prm):
        print("OnMwiState: " + prm.reason)

    def onBuddyState(self, prm):
        print("OnBuddyState: " + prm.reason)

    def onIncommingSubscribe(self, prm):
        print("OnSubscribeState: " + prm.reason)

    def OnIncomingCall(self, prm):
        c = Call(self, call_id=prm.callId)
        call_prm = pj.CallOpParam()
        call_prm.statusCode = 180
        c.answer(call_prm)
        ci = c.getInfo()
        if input(f"Accept call from {ci.remoteUri}?") == u'yes':
            call_prm.statusCode = 200
            c.answer(call_prm)
        else:
            c.hangup(call_prm)


def initalise_sip_stack():

    ep_cfg = pj.EpConfig()
    ep = Endpoint()
    ep.libCreate()
    ep.libInit(ep_cfg)

    sip_tp_config = pj.TransportConfig()
    sip_tp_config.port = 5060
    ep.transportCreate(pj.PJSIP_TRANSPORT_UDP, sip_tp_config)
    ep.libStart()

    acfg = pj.AccountConfig()
    acfg.idUri = "sip:3000@192.168.1.217"
    acfg.regConfig.registrarUri = "sip:192.168.1.217"
    creds = pj.AuthCredInfo("digest", "*", "3000", 0, "1234")
    acfg.sipConfig.authCreds.append(creds)

    acc = Account()
    acc.create(acfg)

    return ep


if __name__ == "__main__":

    endpoint = initalise_sip_stack()

    time.sleep(600)

    endpoint.libDestroy()
