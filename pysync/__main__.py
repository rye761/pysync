import argparse
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QMessageBox, QFileDialog
from PyQt5 import QtWidgets, uic
import os
import sys
import torch
import threading

sync = None
separate = None

def cli():
    global sync
    global separate
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("music", type=str, help="Audio file containing complete track")
        parser.add_argument("lyrics", type=str, help="File containing song lyrics to be synced")
        parser.add_argument("--output_file", type=str, default=None, help="Output file name, defaults to name_of_mp3.lrc")
        parser.add_argument("--model", type=str, default="medium", help="sets model to use for transcribing the audio (tiny, base, small, medium, large, tiny.en, base.en, small.en, medium.en), defaults to medium")
        parser.add_argument("--language", type=str, default=None, help="sets language to use for transcribing the audio (de, en, ja, ...), defaults to auto-detection")

        args = parser.parse_args().__dict__

        import separate
        import sync

        sync.set_model(args['model'])
        doSync(args['music'], args['lyrics'], args['output_file'], args['language'])
        # filename = os.path.basename(args['music'])
        # 
        # if args['output_file']:
        #     output_file = args['output_file']
        # else:
        #     output_file = filename[0:filename.find('.')] + '.lrc'
        # 
        # temp_file = separate.separated_vocals(args['music'])
        # vocal_file_name = temp_file.name + '/' + filename[0:filename.find('.')] + '/vocals.wav'
        # 
        # print(vocal_file_name)
        # 
        # [segments, language] = sync.get_segments(vocal_file_name, args['model'], args['language'])
        # 
        # file = open(args['lyrics'], 'r', encoding='utf-8')
        # full_lyrics = file.read()
        # file.close()
        # 
        # temp_file.cleanup()
        # 
        # file = open(output_file, 'w', encoding='utf-8')
        # file.writelines(sync.sync_segments(full_lyrics, segments, language))
        # file.clxhATose()
        # file.clxhATose()
    else:
        import tensorflow as tf
        import separate
        import sync
        sync.set_model("medium")
        app = QtWidgets.QApplication(sys.argv)
        ui = Ui()

        ui.show()
        sys.exit(app.exec_())

def doSync(audio, subtitle, output, language):
    global sync
    global separate
    filename = os.path.basename(audio)

    if output:
        output_file = output
    else:
        output_file = filename[0:filename.find('.')] + '.lrc'
    
    temp_file = separate.separated_vocals(audio)
    vocal_file_name = temp_file.name + '/' + filename[0:filename.find('.')] + '/vocals.wav'
    
    print(vocal_file_name)
    
    [segments, language] = sync.get_segments(vocal_file_name, language)
    
    file = open(subtitle, 'r', encoding='utf-8')
    full_lyrics = file.read()
    file.close()
    
    temp_file.cleanup()
    
    file = open(output_file, 'w', encoding='utf-8')
    file.writelines(sync.sync_segments(full_lyrics, segments, language))
    file.close()
    

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pysync.ui'), self)
        self.selectAudioFile.clicked.connect(self.doSelectAudioFile)
        self.selectSubtitleFile.clicked.connect(self.doSelectSubtitleFile)
        self.selectOutputFile.clicked.connect(self.doSelectOutputFile)
        self.doSync.clicked.connect(self.doSyncForm)
        self.model.currentTextChanged.connect(self.modelChanged)

    def doSyncForm(self):
        audio = self.audioFile.displayText() or None
        subtitle = self.subtitleFile.displayText() or None
        output = self.outputFile.displayText() or None
        language = self.language.displayText() or None

        if audio == None or subtitle == None:
            print('Audio and Subtitle are required')
            return

        self.model.setEnabled(False)
        self.doSync.setEnabled(False)
        self.setEnabled(False)
        thread = threading.Thread(target=self.doSyncAsync, args=(audio, subtitle, output, language))
        thread.start()

    def doSyncAsync(self, audio, subtitle, output, language):
        doSync(audio, subtitle, output, language)

        self.model.setEnabled(True)
        self.doSync.setEnabled(True)
        self.setEnabled(True)
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Done!")
        dlg.setText("Seems like your lyrics are synched now.")
        dlg.exec()

    def getFile(self, filter):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.AnyFile)
        dlg.setNameFilter(filter)
        
        if dlg.exec():
            return dlg.selectedFiles()[0]

    def doSelectAudioFile(self):
        self.audioFile.setText(self.getFile("Audio Files (*.mp3 *.wav)"))

    def doSelectSubtitleFile(self):
        self.subtitleFile.setText(self.getFile("Subtitle Files (*.txt)"))

    def doSelectOutputFile(self):
        self.outputFile.setText(self.getFile("Subtitle Files (*.lrc)"))

    def modelChanged(self):
        global sync
        self.model.setEnabled(False)
        self.doSync.setEnabled(False)
        self.repaint()
        sync.set_model(self.model.currentText() or 'medium')
        self.model.setEnabled(True)
        self.doSync.setEnabled(True)
        
class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("HELLO!")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Something happened, is that OK?")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

cli()