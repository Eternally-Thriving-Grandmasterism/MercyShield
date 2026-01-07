from jnius import autoclass, PythonJavaClass, java_method

BroadcastReceiver = autoclass('android.content.BroadcastReceiver')
Intent = autoclass('android.content.Intent')
Bundle = autoclass('android.os.Bundle')
Telephony = autoclass('android.provider.Telephony$Sms$Intents')

class MercySMSReceiver(PythonJavaClass):
    __javainterfaces__ = ['android/content/BroadcastReceiver']
    __javacontext__ = 'app'

    def __init__(self, shield):
        super().__init__()
        self.shield = shield

    @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
    def onReceive(self, context, intent):
        if intent.getAction() == "android.provider.Telephony.SMS_RECEIVED":
            bundle = intent.getExtras()
            if bundle:
                pdus = bundle.get("pdus")
                for pdu in pdus:
                    sms = Telephony.Sms.Intents.getMessagesFromIntent(intent)
                    if sms:
                        sender = sms[0].getOriginatingAddress()
                        body = "".join(msg.getMessageBody() for msg in sms)
                        self.shield.handle_sms(sender, body)
