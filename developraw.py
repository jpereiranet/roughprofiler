import rawpy
import cv2
from PIL import Image
from io import BytesIO
import os
import numpy as np

class DevelopImages():

    @staticmethod
    def raw_lineal_develop(raw_image):

        raw = rawpy.imread(raw_image)

        rgb = raw.postprocess(gamma=(1, 1),
                              no_auto_bright=True,
                              output_bps=16,
                              half_size=True,
                              highlight_mode=rawpy.HighlightMode(0), # -H 0
                              output_color=rawpy.ColorSpace(0), # -o 0
                              user_wb=[1, 1, 1, 1]  #RGBG  # -r
                              )

        #rgb = cv2.resize(rgb, (1024, 725), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
        return rgb

    @staticmethod
    def raw_gamma_develop(raw_image):

        raw = rawpy.imread(raw_image)


        rgb = raw.postprocess(gamma=(2.222, 4.5),
                              no_auto_bright=False,
                              demosaic_algorithm=rawpy.DemosaicAlgorithm(1),
                              half_size = True,
                              output_bps=8,
                              highlight_mode=rawpy.HighlightMode(0), # -H 0
                              output_color=rawpy.ColorSpace(1), # -o 0
                              use_camera_wb= True
                              )

        #rgb = cv2.resize(rgb, (1024, 725), interpolation=cv2.INTER_AREA)
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB)
        return rgb

    @staticmethod
    def raw_get_thumbnail(raw_image):
        #path_nx = os.path.splitext(raw_image)[0]
        #filename = os.path.basename(path_nx)
        #thumb_filename = filename + '_thumb.jpg'

        with rawpy.imread(raw_image) as raw:
            try:
                thumb = raw.extract_thumb()

            except rawpy.LibRawNoThumbnailError:
                print('no thumbnail found')
            else:
                if thumb.format in [rawpy.ThumbFormat.JPEG, rawpy.ThumbFormat.BITMAP]:
                    if thumb.format is rawpy.ThumbFormat.JPEG:
                        thumb_pil = Image.open(BytesIO(thumb.data))
                        cv_thumb = cv2.cvtColor(np.array(thumb_pil), cv2.COLOR_RGB2BGR)
                        cv_thumb = cv2.resize(cv_thumb, (1024, 725), interpolation=cv2.INTER_AREA)
                        #thumb tiene 1024*725
                        #cv2.imwrite(thumb_filename, cv_thumb)
                        #thumb_pil.save(thumb_filename, 'JPEG', quality=50, optimize=True, progressive=True)
                    else:
                        #pendiente
                        thumb_rgb = Image.fromarray(thumb.data)
                        #thumb_rgb.save(thumb_filename, 'JPEG', quality=50, optimize=True, progressive=True)

                    return cv_thumb
                else:
                    print('unknown thumbnail format')




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