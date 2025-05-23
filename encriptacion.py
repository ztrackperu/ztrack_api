from Crypto.Cipher import AES
#from Cryptodome.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# 🔒 Función para encriptar
def encriptar(mensaje, clave, iv):
    cipher = AES.new(clave, AES.MODE_CBC, iv)
    mensaje_bytes = mensaje.encode()

    # Relleno PKCS7 para múltiplos de 16 bytes
    padding_length = 16 - (len(mensaje_bytes) % 16)
    mensaje_bytes += bytes([padding_length] * padding_length)

    mensaje_cifrado = cipher.encrypt(mensaje_bytes)
    return base64.b64encode(mensaje_cifrado).decode()

# 🔓 Función para desencriptar
def desencriptar(mensaje_cifrado, clave, iv):
    cipher = AES.new(clave, AES.MODE_CBC, iv)
    mensaje_bytes = base64.b64decode(mensaje_cifrado)

    mensaje_desencriptado = cipher.decrypt(mensaje_bytes)

    # Eliminar el padding PKCS7
    padding_length = mensaje_desencriptado[-1]
    mensaje_desencriptado = mensaje_desencriptado[:-padding_length]

    return mensaje_desencriptado.decode()

# --- Ejemplo de uso ---
#clave = generar_clave()  # Guardar de forma segura
#iv = generar_iv()        # Guardar de forma segura

#clave ="clave_secreta_32_bytes__"
#iv = "1234567890123456"

clave_t = "mi_clave_secreta_32_bytes_123456"
iv_t = "1234567890123456"

# 🔄 Convertir clave e IV a bytes (obligatorio para AES)
clave = clave_t.encode('utf-8')  # Clave de 32 bytes
iv = iv_t.encode('utf-8')        # IV de 16 bytes

print(clave)
print(iv)

mensaje_original = "Hola, API segura!"
mensaje_cifrado = encriptar(mensaje_original, clave, iv)
mensaje_descifrado = desencriptar(mensaje_cifrado, clave, iv)

print("Mensaje Original:", mensaje_original)
print("Mensaje Encriptado:", mensaje_cifrado)
print("Mensaje Desencriptado:", mensaje_descifrado)
