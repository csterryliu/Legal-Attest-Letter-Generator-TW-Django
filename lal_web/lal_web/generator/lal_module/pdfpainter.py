from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

_DEFAULT_FONT_NAME = 'user-sepecified-font'
_DEFAULT_FONT_SIZE = 20
_POINT = 1

class PDFPainter:
    """
    class PDFPainter
    It creates a temporary pdf file for merging.
    """
    def __init__(self, filename, wide, height):
        self.__canvas = canvas.Canvas(filename, pagesize=(wide, height))
        self.__canvas.setStrokeColorRGB(0, 0, 0)
        self.__canvas.setFillColorRGB(0, 0, 0)
        self.__font_size = _DEFAULT_FONT_SIZE

    def set_font(self, font_path, font_size=_DEFAULT_FONT_SIZE):
        pdfmetrics.registerFont(TTFont(_DEFAULT_FONT_NAME, font_path))
        self.__font_size = font_size
        self.__canvas.setFont(_DEFAULT_FONT_NAME, self.__font_size * _POINT)

    def draw_string(self, x_begin, y_begin, text):
        self.__canvas.drawString(x_begin, y_begin, text)

    def get_string_width(self, text):
        return pdfmetrics.stringWidth(text, _DEFAULT_FONT_NAME, self.__font_size)

    def draw_wrapped_string(self, x_begin, y_begin, text, max_width, line_height=None):
        """Draw text with automatic line wrapping. Returns y position of the last line."""
        if line_height is None:
            line_height = self.__font_size * 1.4
        if self.get_string_width(text) <= max_width:
            self.draw_string(x_begin, y_begin, text)
            return y_begin
        current_line = ''
        y = y_begin
        for char in text:
            test_line = current_line + char
            if self.get_string_width(test_line) > max_width:
                self.draw_string(x_begin, y, current_line)
                y -= line_height
                current_line = char
            else:
                current_line = test_line
        if current_line:
            self.draw_string(x_begin, y, current_line)
        return y

    def draw_line(self, x_begin, y_begin, x_end, y_end):
        self.__canvas.line(x_begin, y_begin, x_end, y_end)

    def draw_rect(self, x_begin, y_begin, width, height):
        self.__canvas.rect(x_begin, y_begin, width, height)

    def end_this_page(self):
        self.__canvas.showPage()
        # keep the font setting
        self.__canvas.setFont(_DEFAULT_FONT_NAME, self.__font_size * _POINT)

    def save(self):
        """
        Saves and close the PDF document in the file.
        After this operation the canvas must not be used further.
        """
        self.__canvas.save()
