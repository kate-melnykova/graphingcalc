import base64
from io import BytesIO


class ImageConverter:

    def img_to_base64(self, fig):
        buf = BytesIO()
        fig.savefig(buf, format="png")
        # Embed the result in the html output.
        s = base64.b64encode(buf.getbuffer()).decode("ascii")
        return s

    def base64_to_img(self, encoded):
        pass