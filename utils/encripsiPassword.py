import bcrypt

def encripsi_password(password: str) -> str:
        hassed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
        pass_encript = hassed_password.decode('utf-8')

        return pass_encript