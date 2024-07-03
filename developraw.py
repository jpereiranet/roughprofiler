import rawpy
import cv2
from PIL import Image
from io import BytesIO
import os
import numpy as np

class DevelopImages():

    def __init__(self):
        x = ""

    def raw_develop(self, raw_image):

        raw = rawpy.imread(raw_image)

        rgb = raw.postprocess(gamma=(1, 1),
                              no_auto_bright=False,
                              output_bps=16,
                              highlight_mode=rawpy.HighlightMode(0), # -H 0
                              output_color=rawpy.ColorSpace(0), # -o 0
                              user_wb=[1, 1, 1, 1]  #RGBG  # -r
                              )

        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
        return rgb

    def get_thumbnail(self, raw_image):
        path_nx = os.path.splitext(raw_image)[0]
        filename = os.path.basename(path_nx)
        thumb_filename = filename + '_thumb.jpg'

        with rawpy.imread(raw_image) as raw:
            try:
                thumb = raw.extract_thumb()
                data  = raw.sizes
                width  = data[1]
                heigth = data[0]

            except rawpy.LibRawNoThumbnailError:
                print('no thumbnail found')
            else:
                if thumb.format in [rawpy.ThumbFormat.JPEG, rawpy.ThumbFormat.BITMAP]:
                    if thumb.format is rawpy.ThumbFormat.JPEG:
                        thumb_pil = Image.open(BytesIO(thumb.data))
                        cv_thumb = cv2.cvtColor(np.array(thumb_pil), cv2.COLOR_RGB2BGR)
                        #thumb tiene 1024*725

                        #cv_thumb = self.scale_image(cv_thumb)
                        #cv_thumb = self.rotate_image(cv_thumb)
                        #cv2.imwrite(thumb_filename, cv_thumb)
                        #thumb_pil.save(thumb_filename, 'JPEG', quality=50, optimize=True, progressive=True)
                    else:
                        #pendiente
                        thumb_rgb = Image.fromarray(thumb.data)
                        #thumb_rgb.save(thumb_filename, 'JPEG', quality=50, optimize=True, progressive=True)

                    return cv_thumb,(width,heigth ), thumb_filename
                else:
                    print('unknown thumbnail format')

    def rotate_image(self, img):
        image = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return image

    def scale_image(self,img):


        scale_percent = 100
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        return resized


#if __name__ == '__main__':

    #a = DevelopImages()
    #s = a.raw_develop("/Users/jpereira/Documents/CURSOS/ACAL_JRoble/presentaciones/cartas/DSC_4453a.DNG")
    #cv2.imshow("window_name", s)
    #cv2.imwrite("lieal.tiff", s)
    #x = a.get_thumbnail("/Users/jpereira/Documents/CURSOS/ACAL_JRoble/presentaciones/cartas/DSC_4453a.DNG")
    #cv2.imshow("window_name", x[0])
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.imwrite(x[1], x[0])