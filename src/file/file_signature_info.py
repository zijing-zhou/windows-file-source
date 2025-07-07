import win32com.client
import os
from datetime import datetime

class FileSignatureInfo:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filestate = True
        self.is_signed = False
        self.issuer = None
        self.thumbprint = None
        self.signing_time = None

        self._analyze_signature()

    def _analyze_signature(self):
        if not os.path.isfile(self.filepath):
            self.filestate = False
            return

        try:
            signer = win32com.client.Dispatch("Scripting.Signer")
            signature = signer.Verify(self.filepath)

            cert = signature.SignerCertificate
            self.is_signed = True
            self.issuer = cert.Issuer
            self.thumbprint = cert.Thumbprint
            self.signing_time = signature.SigningTime

        except Exception as e:
            self.is_signed = False