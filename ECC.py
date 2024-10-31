class EllipticCurve:
    def __init__(self, a, b, p):
        # y^2 = x^3 + ax + b (mod p)
        self.a = a
        self.b = b
        self.p = p  
    
    # Kiểm tra điểm thuộc đường cong hay không
    def is_on_curve(self, x, y):
        return (y**2 - (x**3 + self.a * x + self.b)) % self.p == 0
    
    # Cộng điểm
    def point_add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P
        
        (x1, y1) = P
        (x2, y2) = Q
        
        # Xử lý khi P = Q
        if P == Q:
            m = (3 * x1**2 + self.a) * pow(2 * y1, -1, self.p)
        else:
            m = (y2 - y1) * pow(x2 - x1, -1, self.p)
        
        m = m % self.p
        x3 = (m**2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    # Nhân điểm
    def scalar_mult(self, k, P):
        result = None
        addend = P
        
        while k:
            if k & 1:
                result = self.point_add(result, addend)
            addend = self.point_add(addend, addend)
            k >>= 1
        
        return result
    
    # Tạo ra tất cả các điểm ở trên đường cong
    def generate_points(self):
        points = []
        for x in range(self.p):
            for y in range(self.p):
                if self.is_on_curve(x, y):
                    points.append((x, y))
                    #print(f"({x},{y})")
        return points

curve = EllipticCurve(a=1, b=3, p=10000)

# Tạo ra các điểm ở trên đường cong
points = curve.generate_points()

# Tính tổng số điểm trên đường cong
num_points = len(points) + 1  # +1 điểm ở vô cùng
print(f"Number of points: {num_points}")

P = (6, 15)
print(f"Is P on curve? {curve.is_on_curve(*P)}")

# Bảng cửu chương
for k in range(1,839):
    kP = curve.scalar_mult(k, P)
    print(f"{k} * P = {kP}")