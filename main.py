from PyQt5 import QtWidgets
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
from framework import Ui_Dialog
import cv2
import sys
import os
import yolov7_start

class untitled_python(QMainWindow):
    
    def __init__(self):
        
        super().__init__()

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.kontrol_video = False
        self.kontrol_model= True


        self.ui.foto_foto.clicked.connect(self.fileBrowser_foto_foto)
        self.ui.foto_model.clicked.connect(self.fileBrowser_foto_model)
        self.ui.foto_test.clicked.connect(self.foto_predict_test)

        self.ui.video_video.clicked.connect(self.fileBrowser_video_video)
        self.ui.video_model.clicked.connect(self.fileBrowser_video_model)
        self.ui.video_test.clicked.connect(self.video_predict_test)

        

    def fileBrowser_foto_foto(self):  # fotograf yükle butonu
        
        fname=QFileDialog.getOpenFileName(self,
        'Open file',
        os.getcwd(),
        'Only Image (*.jpg *.png *.jpeg)') 
        self.foto_foto_fname = fname[0]

        #-----------ilk karenin ekrana verilmesi---------#
        image = cv2.imread(self.foto_foto_fname)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1280,720))
        self.goruntu_foto(frame)


    def fileBrowser_video_video(self):  # video yükle butonu

        fname=QFileDialog.getOpenFileName(self,
        'Open file',
        os.getcwd(),
        'Only Video (*.mp4)')
        self.video_video_fname = fname[0]  # kontrol et

        #---------ilk karenin ekrana verilmesi--------#
        cap = cv2.VideoCapture(self.video_video_fname)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                if self.kontrol_video:
                    if self.kontrol_model:
                        yolov7 = yolov7_start.yoloV7_tensorrt(self.video_model_fname)   
                        self.kontrol_model= False

                    frame = cv2.resize(frame, (640,640))
                    output = yolov7_start.main(yolov7,frame)
                    cv2.imshow("window", output)
                    cv2.destroyAllWindows()
                    #output = cv2.resize(output, (1280,720))
                    img = output.copy()
                    #img_original = cv2.resize(img,(1280,720))
                    self.goruntu_video(img_original=img)
                else:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    output = cv2.resize(frame, (25,25))
                    cv2.imshow("window", output)
                    cv2.destroyAllWindows()
                    self.goruntu_video(frame)

            else:
                print("Ret is false, there is no usable frame here")
                self.kontrol_video = False
            #break
            
        cv2.destroyAllWindows()
        cap.release()



    def fileBrowser_foto_model(self):   # foto sayfası için model yükleme

        fname=QFileDialog.getOpenFileName(self,
        'Open file',
        os.getcwd(),
        'Only trt (*.trt)')
        self.foto_model_fname = fname[0] 

    def fileBrowser_video_model(self):  # video sayfası için model yükleme

        fname=QFileDialog.getOpenFileName(self,
        'Open file',
        os.getcwd(),
        'Only trt (*.trt)')
        self.video_model_fname = fname[0] 


    def foto_predict_test(self):

        yolov7 = yolov7_start.yoloV7_tensorrt(self.foto_model_fname)
        frame = cv2.imread(self.foto_foto_fname)

        image = yolov7_start.main(yolov7, frame)
        image = cv2.resize(image, (1280,720))
        self.goruntu_foto(image=image)

    def video_predict_test(self):

        self.kontrol_video = True
        self.kontrol_model= True

    def goruntu_foto(self, image):

        ConvertToFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        self.ui.foto_frame.setPixmap(QPixmap.fromImage(ConvertToFormat))
        self.ui.foto_frame.setScaledContents(True)

    def goruntu_video(self, img_original):

        ConvertToFormat = QImage(img_original.data, img_original.shape[1], img_original.shape[0], QImage.Format_RGB888)
        self.ui.video_frame.setPixmap(QPixmap.fromImage(ConvertToFormat))
        self.ui.video_frame.setScaledContents(True)
        

app = QApplication(sys.argv)
mainwindow = untitled_python()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")