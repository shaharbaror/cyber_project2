
CAPTIONS = {
        2: 2,
        1: 1,
}
class MemeMaker:



    def __init__(self):
        pass
    @staticmethod
    def getStyles(number:int):
        with open("paths.txt", "rb") as f:
            style = f.read().split(b"__SHEETBREAKER__")[number - 1]
            style = style.replace(b"\r\n", b"")
        return style


    @staticmethod
    def getImage(number):
        with open(f"./MemeBank/meme{get_path(number)}", "rb") as f:
            return f.read()

    @staticmethod
    def get_caption_amount(rnd: int):
        return CAPTIONS[rnd]

def get_path(number):
    if number < 10:
        return f"0{number}"
    else:
        return number