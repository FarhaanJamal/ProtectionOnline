from privacyExtracter import PrivacyExtracter
from pdfMaker import PDFMaker
from rag import RAGImplementation
from translator import Translator

def mainCombined(url):
    extractor = PrivacyExtracter()
    text = extractor.get_privacy_policy_text(url, True)
    #text = "In the heart of the bustling city, amidst the cacophony of car horns and chatter, lies a serene oasis of tranquility. Towering skyscrapers cast their shadows over quaint coffee shops and bustling markets. People from all walks of life navigate the bustling streets, each with their own destination and story to tell. Amidst the chaos, a sense of unity pervades, as strangers exchange smiles and brief nods of acknowledgment. Time seems to slow down here, allowing moments of reflection and introspection amidst the relentless pace of urban life. This city, with its vibrant energy and endless possibilities, is a microcosm of the world itself."
    if text:
        pdf_mkr = PDFMaker()
        pdf_mkr.create_pdf_with_text(text, "./file/extractedPrivacyPolicy.pdf")

        query_engine = RAGImplementation(file_dir="./file")
        hindi_translator = Translator()

        prompt = "Please provide 5 points from the extracted privacy policy, each framed as 'this website,' strictly not as 'I' or 'We,' with precisely 30 words each, discussing data collection, and ensure it's not your own privacy policy."
        overviewResponse = query_engine.query(prompt)

        overviewResponseHindi = hindi_translator.get_engtohindi(overviewResponse)

        prompt = "Verify whether ther is any violation of the extracted Privacy Policy with respect to the DIGITAL PERSONAL DATA PROTECTION ACT, give the result in under 30 words."
        legalityResponse = query_engine.query(prompt)

        legalityResponseHindi = hindi_translator.get_engtohindi(legalityResponse)
        
        return [overviewResponse, overviewResponseHindi, legalityResponse, legalityResponseHindi]
    else:
        return ["No privacy policy found in this page", "इस पेज पर कोई गोपनीयता नीति नहीं मिली"] * 2
    

"""out = mainCombined("https://www.myntra.com/login")
print(f"{out[0]}\n\n{out[1]}\n\n{out[2]}\n\n{out[3]}")"""