import random
import hashlib
from math import sqrt
from sympy import isprime, primitive_root, nextprime

# Hàm tạo số nguyên tố dạng Safe Prime (p = 2q + 1)
def generate_safe_prime(bits):
    q = nextprime(2**(bits - 1))  # Tìm số nguyên tố lớn q có độ lớn (bits - 1)
    p = 2 * q + 1
    while not isprime(p):
        q = nextprime(q)
        p = 2 * q + 1
    return p

# Hàm kiểm tra số nguyên tố (trial division)
def isPrime(n): 
    if (n <= 1):
        return False
    if (n <= 3):
        return True
    if (n % 2 == 0 or n % 3 == 0):
        return False
    i = 5
    while(i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0) :
            return False
        i = i + 6
    return True

# Hàm sinh số nguyên tố ngẫu nhiên có bit cho trước
def generate_large_prime(bits=4090):
    while True:
        prime_candidate = random.getrandbits(bits) | 1
        if isPrime(prime_candidate):
            return prime_candidate

# Hàm tìm thừa số nguyên thủy của p
def find_primitive_root(p):
    # p là số nguyên tố, phi(p) = p-1
    phi = p - 1

    # Tìm các ước của phi
    factors = set()
    n = phi
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 1
    if n > 1:
        factors.add(n)

    # Tìm g là thừa số nguyên thủy
    for g in range(2, p):
        flag = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                flag = False
                break
        if flag:
            return g
    return None

# Hàm tạo khóa ElGamal
def generate_keys(p, g):
    private_key = random.randint(1, p - 2)  # Khóa riêng tư (x)
    public_key = pow(g, private_key, p)      # Khóa công khai (y = g^x mod p)
    return private_key, public_key

# Hàm ký số ElGamal
def elgamal_sign(message, p, g, private_key):
    h = int(hashlib.sha256(message.encode()).hexdigest(), 16)  # Băm thông điệp

    while True:
        k = random.randint(1, p - 2)
        if gcd(k, p - 1) == 1:  # Chọn k sao cho gcd(k, p-1) = 1
            break
    
    r = pow(g, k, p)  # r = g^k mod p
    s = (pow(k, -1, p - 1) * (h - private_key * r)) % (p - 1)  # s = k^(-1)(h - xr) mod (p-1)
    
    return (r, s)

# Hàm xác minh chữ ký ElGamal
def elgamal_verify(message, signature, p, g, public_key):
    r, s = signature
    if r <= 0 or r >= p:
        return False
    
    h = int(hashlib.sha256(message.encode()).hexdigest(), 16)  # Băm thông điệp

    v1 = pow(g, h, p)
    v2 = (pow(public_key, r, p) * pow(r, s, p)) % p

    return v1 == v2

# Hàm tính gcd (ước chung lớn nhất)
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Chương trình chính
def main():
    # Bước 1: Sinh số nguyên tố p có độ lớn 4090 bits
    # Sinh số nguyên tố dạng Safe Prime và tìm thừa số nguyên thủy
    p = generate_safe_prime(1024)  # Safe Prime có 1024 bits
    print(f"Số nguyên tố dạng Safe Prime p: {p}")
    
    # Bước 2: Tìm thừa số nguyên thủy g của p
    g = primitive_root(p)
    print(f"Thừa số nguyên thủy g của p: {g}")

    # Bước 3: Tạo khóa ElGamal
    private_key, public_key = generate_keys(p, g)
    print(f"Khóa riêng tư (x): {private_key}")
    print(f"Khóa công khai (y): {public_key}")
    
    # Bước 4: Ký thông điệp
    message = "tranhoangluong"
    signature = elgamal_sign(message, p, g, private_key)
    print(f"Chữ ký (r, s): {signature}")
    
    # Bước 5: Xác minh chữ ký
    is_valid = elgamal_verify(message, signature, p, g, public_key)
    print(f"Kết quả xác minh chữ ký: {'Hợp lệ' if is_valid else 'Không hợp lệ'}")

# Gọi chương trình chính
if __name__ == "__main__":
    main()