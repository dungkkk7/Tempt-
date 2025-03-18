
### **Bước 1: Hiểu yêu cầu của bài toán**
Hàm `check` nhận một chuỗi `input` và trả về một giá trị 64-bit. Đầu tiên, hàm kiểm tra độ dài của chuỗi:
```c
if (strlen(input) != 27)
    return 1LL;
```
- Nếu độ dài chuỗi không phải 27 ký tự, hàm trả về 1 (không hợp lệ). 
- **Kết luận**: Flag phải có **đúng 27 ký tự**.

---

### **Bước 2: Phân tích dữ liệu trong hàm**
Hàm khởi tạo một số biến quan trọng:
1. **`unuse = 0x617B2375F81EA7E1LL`**: Một số nguyên 64-bit, lưu tại `[rsp+10h]`.
2. **`v4[0] = 0xD269DF5B5AFC9DB9LL`**: Phần tử đầu tiên của mảng `v4`, lưu tại `[rsp+18h]`.
3. **`*(__int64 *)((char *)v4 + 7) = 0xF467EDF4ED1BFED2LL`**: Ghi một số nguyên 64-bit bắt đầu từ vị trí cách `v4` 7 byte.

Ngoài ra:
- `currentChar` và `k` được khởi tạo bằng 0, dùng để điều khiển vòng lặp kiểm tra bit.
- Hàm sử dụng biểu thức `*((char *)&v4[-1] + i)` để truy cập các byte từ bộ nhớ.

Chúng ta cần xây dựng mảng byte dựa trên các giá trị này, vì chúng sẽ được so sánh với flag.

---

### **Bước 3: Xây dựng mảng byte từ bộ nhớ**
Hàm hoạt động trên kiến trúc **little-endian** (byte thấp nhất nằm ở địa chỉ thấp nhất). Hãy phân tích từng phần bộ nhớ:

#### **Giá trị ban đầu**
1. **`unuse = 0x617B2375F81EA7E1`**  
   - Các byte từ `rsp+10h` đến `rsp+17h`:  
     ```
     E1 A7 1E F8 75 23 7B 61
     ```

2. **`v4[0] = 0xD269DF5B5AFC9DB9`**  
   - Các byte từ `rsp+18h` đến `rsp+1Fh`:  
     ```
     B9 9D FC 5A 5B DF 69 D2
     ```

#### **Ghi đè với `*(__int64 *)((char *)v4 + 7)`**
- `(char *)v4` là `rsp+18h`, nên `(char *)v4 + 7` là `rsp+1Fh`.
- Ghi `0xF467EDF4ED1BFED2` (byte: `D2 FE 1B ED F4 ED 67 F4`) từ `rsp+1Fh` đến `rsp+26h`.
- Kết quả bộ nhớ từ `rsp+10h` đến `rsp+26h`:
  ```
  rsp+10h: E1 A7 1E F8 75 23 7B 61  B9 9D FC 5A 5B DF 69 D2  FE 1B ED F4 ED 67 F4
  ```

#### **Mảng byte**
- Biểu thức `*((char *)&v4[-1] + i)` bắt đầu từ `&v4[-1]` (tức `rsp+10h`) với `i` từ 0 đến 22 (23 lần lặp).
- Mảng byte:
  ```c
  unsigned char bytes[23] = {
      0xE1, 0xA7, 0x1E, 0xF8, 0x75, 0x23, 0x7B, 0x61,
      0xB9, 0x9D, 0xFC, 0x5A, 0x5B, 0xDF, 0x69, 0xD2,
      0xFE, 0x1B, 0xED, 0xF4, 0xED, 0x67, 0xF4
  };
  ```

---

### **Bước 4: Phân tích vòng lặp kiểm tra bit**
Hàm sử dụng hai vòng lặp lồng nhau:
- **Vòng ngoài**: `i` từ 0 đến 22 (23 byte của `bytes`).
- **Vòng trong**: `j` từ 0 đến 7 (8 bit mỗi byte).
- Tổng cộng: 23 × 8 = **184 bit**.

#### **Logic kiểm tra**
- `n = 1 << (7 - j)`: Lấy bit thứ `(7 - j)` của `bytes[i]` (từ MSB đến LSB).
- `m = 1 << (7 - k)`: Lấy bit thứ `(7 - k)` của `input[currentChar]`.
- Điều kiện: `(n & bytes[i]) > 0 != (m & input[currentChar]) > 0`:
  - Nếu bit của `bytes[i]` khác bit của `input[currentChar]`, hàm thất bại (trả về 1).
  - Bit phải **giống nhau** để thành công.

#### **Quản lý chỉ số**
- `k` tăng từ 1 đến 7:
  - Khi `k == 8`, đặt lại `k = 0`, `currentChar++`.
  - Khi `k == 0`, đặt `k = 1`.
- Sau 184 bit, `currentChar = 23`. Flag dài 27 byte (216 bit), còn lại 32 bit không được kiểm tra.

#### **Kết quả mong muốn**
- Nếu tất cả 184 bit khớp, hàm trả về 0 (thành công).

---

### **Bước 5: Tái tạo flag**
- Flag là chuỗi 27 ký tự (216 bit).
- 184 bit đầu tiên phải khớp với 184 bit của `bytes`.
- 32 bit cuối (4 byte cuối) không được kiểm tra, có thể mặc định là 0.

#### **Ánh xạ bit**
- Bit `(7 - j)` của `bytes[i]` khớp với bit `(7 - k)` của `flag[currentChar]`.
- Ví dụ:
  - `i=0`, `bytes[0] = 0xE1` (binary: `11100001`):
    - `j=0`, `k=1`: bit 7 → bit 6 của `flag[0]`.
    - `j=1`, `k=2`: bit 6 → bit 5 của `flag[0]`.
    - ...
    - `j=6`, `k=7`: bit 1 → bit 0 của `flag[0]`.
    - `j=7`, `k=1` (sau `k=8`), bit 0 → bit 6 của `flag[1]`.

#### **Dùng Python để tính toán**
```python
bytes = [0xE1, 0xA7, 0x1E, 0xF8, 0x75, 0x23, 0x7B, 0x61, 0xB9, 0x9D,
         0xFC, 0x5A, 0x5B, 0xDF, 0x69, 0xD2, 0xFE, 0x1B, 0xED, 0xF4,
         0xED, 0x67, 0xF4]
flag = [0] * 27  # Khởi tạo 27 byte bằng 0
k = 0
currentChar = 0

for i in range(23):
    for j in range(8):
        if k == 0:
            k = 1
        bit = (bytes[i] >> (7 - j)) & 1  # Lấy bit từ bytes[i]
        flag[currentChar] |= bit << (7 - k)  # Gán bit vào flag
        k += 1
        if k == 8:
            k = 0
            currentChar += 1

flag_str = ''.join(chr(b) for b in flag)
print(flag_str)
```

**Kết quả**:  
```
pigoCTF{wh3r3_4r3_7h3_f14g5}
```

---


