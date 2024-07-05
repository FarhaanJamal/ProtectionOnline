from englisttohindi.englisttohindi import EngtoHindi

class Translator:
    def get_engtohindi(self, text):
        if text:
            text = str(text)
            lst = text.split("\n")
            res = ""
            for i in lst:
                res += EngtoHindi(i).convert + "\n"
            return res
        else:
            return None

"""translator = Translator()
message = \"""1. This website collects personal information related to your transactions on Platform and third-party business partner platforms.
2. This website may seek additional information such as billing address, credit/debit card number, and payment instrument details to provide services, enable transactions, or refund for cancelled transactions.
3. This website collects personalized messages, images, photos, gift card message box, chat rooms, or other message areas from you.
4. This website collects feedback/product review or voice commands to shop on the Platform.
5. This website collects information related to your transactions on third-party business partner platforms, which is governed by their privacy policies.\"""
res = translator.get_engtohindi(message)
print(res)"""