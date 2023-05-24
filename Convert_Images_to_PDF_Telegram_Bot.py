import os
import pytesseract
from PIL import Image
from fpdf import FPDF
from telegram.ext import Updater, MessageHandler, Filters

# Token de acceso al bot de Telegram
TOKEN = 'TU_TOKEN_DE_TELEGRAM'

# Directorio de trabajo para almacenar las imágenes
WORKING_DIR = 'ruta/al/directorio'

# Configuración de idioma para pytesseract (opcional)
pytesseract.pytesseract.tesseract_cmd = 'ruta/al/ejecutable/tesseract'
os.environ['TESSDATA_PREFIX'] = 'ruta/al/directorio/tessdata'

# Función para convertir imagen a PDF
def convert_image_to_pdf(image_path):
    # Utiliza pytesseract para extraer texto de la imagen
    text = pytesseract.image_to_string(Image.open(image_path))

    # Crea un nuevo PDF
    pdf = FPDF()
    pdf.add_page()

    # Agrega el texto extraído al PDF
    pdf.set_font('Arial', size=12)
    pdf.multi_cell(0, 10, text)

    # Guarda el PDF
    pdf_path = os.path.splitext(image_path)[0] + '.pdf'
    pdf.output(pdf_path)

    return pdf_path

# Función para manejar los mensajes con imágenes
def handle_image_message(update, context):
    # Obtiene el archivo de imagen
    image_file = context.bot.get_file(update.message.photo[-1].file_id)
    image_path = os.path.join(WORKING_DIR, 'image.jpg')
    image_file.download(image_path)

    # Convierte la imagen a PDF
    pdf_path = convert_image_to_pdf(image_path)

    # Envía el PDF como respuesta
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(pdf_path, 'rb'))

    # Elimina los archivos temporales
    os.remove(image_path)
    os.remove(pdf_path)

# Crea el objeto Updater y el Dispatcher
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Manejador de mensajes con imágenes
image_handler = MessageHandler(Filters.photo, handle_image_message)

# Agrega el manejador al dispatcher
dispatcher.add_handler(image_handler)

# Inicia el bot
updater.start_polling()
