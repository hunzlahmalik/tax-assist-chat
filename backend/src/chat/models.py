import os
import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from pypdf import PdfReader
from src.service.ocr_tesseract import ocr_pdf
from src.user.models import User


def message_file_upload_path(instance, filename):
    """
    Generate file path for message uploads.
    """
    salt = uuid.uuid4().hex[:10]  # Generate a random salt
    base_filename, file_extension = os.path.splitext(filename)
    return f"message_uploads/{salt}_{base_filename}{file_extension}"


class Chat(models.Model):
    uuid = models.UUIDField(
        editable=False,
        db_index=True,
        unique=True,
        default=uuid.uuid4,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chats")

    class Meta:
        ordering = ["-timestamp"]


class Message(models.Model):
    uuid = models.UUIDField(
        editable=False,
        db_index=True,
        unique=True,
        default=uuid.uuid4,
    )
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to=message_file_upload_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    class Meta:
        ordering = ["-timestamp"]

    @property
    def complete_message(self):
        """
        Return the complete message content.

        With file and image text if available.

        """
        message_content = self.content
        if self.file:
            file_text = self.extract_text_from_pdf_ocr(self.file.path)
            if file_text:
                return file_text
            file_text = self.extract_text_from_pdf(self.file.path)
            if file_text:
                return file_text
        return message_content

    def save(self, *args, **kwargs):
        """
        Override the save method to extract text from PDF file.
        """
        self.content = self.complete_message

        super().save(*args, **kwargs)

    @staticmethod
    def extract_text_from_pdf_ocr(filepath):
        """
        Extract text from PDF file using OCR.
        """
        try:
            with open(filepath, "rb") as f:
                return ocr_pdf(f.read())
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    @staticmethod
    def extract_text_from_pdf(filepath):
        """
        Extract text from PDF file using pypdf library.
        """
        try:
            with open(filepath, "rb") as f:
                reader = PdfReader(f)
                full_text = ""
                for page in reader.pages:
                    full_text += page.extract_text()
                return full_text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
