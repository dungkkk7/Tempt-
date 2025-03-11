import time
import base64
import hashlib
import sys
import secrets

class Block:
    def __init__(self, index, previous_hash, timestamp, encoded_transactions, nonce):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.encoded_transactions = encoded_transactions
        self.nonce = nonce

    def calculate_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.encoded_transactions}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

def decrypt(ciphertext, key, block_size=16):
    """
    Giải mã chuỗi blockchain đã được mã hóa với khóa cung cấp
    """
    key_hash = hashlib.sha256(key).digest()
    plaintext = b''
    
    for i in range(0, len(ciphertext), block_size):
        block = ciphertext[i:i + block_size]
        plain_block = xor_bytes(block, key_hash)
        plaintext += plain_block
    
    # Loại bỏ padding
    padding_length = plaintext[-1]
    plaintext = plaintext[:-padding_length]
    
    return plaintext.decode('utf-8')

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def extract_inner_text(decrypted_text):
    """
    Trích xuất nội dung đã được chèn vào giữa chuỗi blockchain
    """
    # Tìm các hash block (định dạng 64 ký tự liên tiếp)
    import re
    
    # Phân tích dựa trên dấu gạch nối ngăn cách các block
    parts = decrypted_text.split('-')
    
    if len(parts) >= 2:
        # Xác định phần giữa để tìm inner_text
        midpoint = len(decrypted_text) // 2
        
        # Tìm dấu gạch ngang gần nhất trước và sau midpoint
        dash_before = decrypted_text.rfind('-', 0, midpoint)
        dash_after = decrypted_text.find('-', midpoint)
        
        if dash_before != -1 and dash_after != -1:
            inner_text = decrypted_text[dash_before+1:dash_after]
            return inner_text
    
    # Nếu phương pháp trên không hoạt động, thử suy luận từ cấu trúc chuỗi
    # Trong hàm encrypt(), inner_txt được chèn vào giữa chuỗi blockchain
    print("Không thể tìm thấy dấu ngăn cách rõ ràng, đang thử phương pháp phân tích chuỗi...")
    print("Chuỗi đầy đủ:", decrypted_text)
    
    # Tìm các chuỗi hash SHA-256 (64 ký tự hex)
    hash_pattern = re.compile(r'[0-9a-f]{64}')
    matches = hash_pattern.finditer(decrypted_text)
    
    positions = []
    for match in matches:
        positions.append((match.start(), match.end()))
    
    if len(positions) >= 2:
        # Tìm khoảng trống lớn nhất giữa các hash
        max_gap = 0
        gap_start = 0
        gap_end = 0
        
        for i in range(len(positions) - 1):
            current_gap = positions[i+1][0] - positions[i][1]
            if current_gap > max_gap:
                max_gap = current_gap
                gap_start = positions[i][1]
                gap_end = positions[i+1][0]
        
        if max_gap > 0:
            inner_text = decrypted_text[gap_start:gap_end]
            return inner_text
    
    # Nếu không thể xác định, trả về toàn bộ chuỗi
    return "Không thể xác định nội dung chèn thêm, chuỗi giải mã đầy đủ: " + decrypted_text

def main():
    # Các giá trị đã được cung cấp dưới dạng bytes
    random_string = b"\x1br\t;\x0f\xb5\x9f\xaa\xd1'\xaf\x86[\xf0\xe6\xd9'D\xf9\x8d\x17g\xeb>_gG.\xd4\xc3\xdc\x83"
    encrypted_blockchain = b'o\x14>\xda\x16\xc7\xce\xd784,.\x8f2\x80@cD?\xd3L\x90\x9f\x87l0yy\xdam\x85J1\x139\x88\x10\x95\x9f\x82ke*.\xda>\xd3\x195O?\xd3\x10\xc4\x94\x83kd| \x882\x86IzFk\xd2@\x95\xcd\x83:by{\x8c3\x81\x1e6E8\xdaC\xc2\xcf\xd087||\x8em\xd0\x1c3Cj\xde\x10\xc0\x99\x89;4+{\x8fn\x84\x1abN9\xdc\x16\xc5\xc8\xd0mc}+\x81o\xd7J1[k\xda\x12\x94\xce\x89m3}(\xdbh\x84KeDh\x8fF\x9e\xc9\x84i1.*\x8f2\x87\x1d4\x15+\x83\x17\xc9\xef\xe5Iz*t\xd7h\xd9\'d%\t\x82"\xcf\xfe\xd3[09{\xe0T\xea-=;k\x98@\x9f\xcf\xf9Pp\x0bb\xd5A\xe8\x02\x15=\x04\x8eL\x96\x9f\x86n0ze\x89m\x81A6Bi\x88B\x91\xce\x8279q~\x8d:\x84OfAn\x8fA\x95\xc9\xd76d|}\x95;\x82@oFb\xddE\x93\x98\xd2jdz/\x88h\xd7\x1a6@o\xdd\x12\x94\x94\xd2m`}y\x8c>\x82LaCm\x8f\x10\x9f\x9f\xd3>0py\xde2\x87AoGh\x88\x11\x91\x9a\x84=3z*\xde&\x82Hb@n\xddM\xc3\xce\x89me.(\x808\xd0KaGo\x8bG\x91\x9b\x81?`.|\xde=\xd6@b\x17m\x8e\x11\x9f\x95\x80>d+.\x88>\x80\x1d4\x14m\xdd\x12\x96\xcf\x85m1q-\x8ao\xb0z'

    # Giải mã
    try:
        # Sử dụng trực tiếp các biến bytes
        decrypted_text = decrypt(encrypted_blockchain, random_string)
        print("\nChuỗi blockchain đã giải mã:", decrypted_text)
        
        # Tìm nội dung chèn vào giữa
        inner_text = extract_inner_text(decrypted_text)
        print("\nNội dung đã được chèn vào giữa (token):", inner_text)
    except Exception as e:
        print(f"Lỗi khi giải mã: {e}")

if __name__ == "__main__":
    main()