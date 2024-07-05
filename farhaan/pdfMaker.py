from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class PDFMaker:
    def add_nextLine(self, text):
        space_ind_strt, space_ind_end, i = 0, 0, 0
        new_text = ""
        while i < len(text):
            if text[i] == " ":
                space_ind_end = i
            if space_ind_end-space_ind_strt > 80:
                new_text += text[space_ind_strt:space_ind_end] + "\n"
                space_ind_strt = space_ind_end
                i = space_ind_end+1
            i += 1
        return new_text

    def create_pdf_with_text(self, text, file_path):
        text = self.add_nextLine(text)
        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica", 11)
        c.setFillColorRGB(0, 0, 0)

        lines = text.split('\n')
        x, y = 50, 800
        for line in lines:
            c.drawString(x, y, line)
            y -= 20 
            if y < 50:
                c.showPage()
                y = 730
        c.save()
        print("PDF saved")

"""text = "In the heart of the bustling city, amidst the cacophony of car horns and chatter, lies a serene oasis of tranquility. Towering skyscrapers cast their shadows over quaint coffee shops and bustling markets. People from all walks of life navigate the bustling streets, each with their own destination and story to tell. Amidst the chaos, a sense of unity pervades, as strangers exchange smiles and brief nods of acknowledgment. Time seems to slow down here, allowing moments of reflection and introspection amidst the relentless pace of urban life. This city, with its vibrant energy and endless possibilities, is a microcosm of the world itself."

pdf_mkr = PDFMaker()
pdf_mkr.create_pdf_with_text(text, "./PP/extractedPrivacyPolicy.pdf")
"""