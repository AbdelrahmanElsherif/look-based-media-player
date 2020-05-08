from opencv_detection import *
from mediaplayer import *
from multiprocessing import Process,Queue

def func1(q):
    app = QApplication([])
    app.setApplicationName("Playing")
    app.setStyle("Fusion")

    # Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.white)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(palette)
    app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")

    while True:
        Doha = q.get()
        print(Doha)
        if Doha == 0 :
            print("heeereee")
            MainWindow.player.pause

    window = MainWindow()
    app.exec_()

def func2(q):
    while True:
        ret, frame = cap.read()
        q.put(detectAndDisplay(frame))
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        detectAndDisplay(frame)
        if cv.waitKey(10) == 27:
            break



if _name_ == '_main_':

    q = Queue()
    p1 = Process(target=func1, args=(q,))
    p1.start()
    p2 = Process(target=func2,args=(q,))
    p2.start()
    p1.join()
    p2.join()