Dưới đây là write-up chi tiết về cách giải mã thông điệp ẩn trong ảnh `red.png` bằng công cụ **zsteg**, dựa trên đầu ra mà bạn cung cấp.

---

## Write-up: Giải mã thông điệp ẩn trong ảnh `red.png` bằng zsteg

### Mô tả thử thách
Trong thử thách này, chúng ta được cung cấp một file ảnh `red.png` chứa thông tin ẩn. Nhiệm vụ là trích xuất và giải mã thông điệp ẩn trong ảnh để tìm ra flag. Công cụ **zsteg** sẽ được sử dụng để phân tích dữ liệu ẩn, và từ đầu ra của nó, chúng ta sẽ tiến hành giải mã.

### Dữ liệu đầu vào
Khi chạy lệnh `zsteg red.png`, chúng ta nhận được đầu ra sau:

```
meta Poem           .. text: "Crimson heart, vibrant and bold,\nHearts flutter at your sight.\nEvenings glow softly red,\nCherries burst with sweet life.\nKisses linger with your warmth.\nLove deep as merlot.\nScarlet leaves falling softly,\nBold in every stroke."
b1,rgba,lsb,xy      .. text: "cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ=="
b1,rgba,msb,xy      .. file: OpenPGP Public Key
b2,g,lsb,xy         .. text: "ET@UETPETUUT@TUUTD@PDUDDDPE"
b2,rgb,lsb,xy       .. file: OpenPGP Secret Key
b2,bgr,msb,xy       .. file: OpenPGP Public Key
b2,rgba,lsb,xy      .. file: OpenPGP Secret Key
b2,rgba,msb,xy      .. text: "CIkiiiII"
b2,abgr,lsb,xy      .. file: OpenPGP Secret Key
b2,abgr,msb,xy      .. text: "iiiaakikk"
b3,rgba,msb,xy      .. text: "#wb#wp#7p"
b3,abgr,msb,xy      .. text: "7r'wb#7p"
b4,b,lsb,xy         .. file: 0421 Alliant compact executable not stripped
```

Từ đầu ra này, dòng quan trọng nhất mà chúng ta sẽ tập trung là:

```
b1,rgba,lsb,xy      .. text: "cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ=="
```

### Phân tích và cách giải quyết

#### **Bước 1: Xác định thông tin ẩn**
- Công cụ **zsteg** được thiết kế để phát hiện dữ liệu ẩn trong các file ảnh như PNG hoặc BMP, thường sử dụng kỹ thuật giấu tin (steganography) trên các bit ít quan trọng (LSB).
- Dòng `b1,rgba,lsb,xy` cho thấy dữ liệu được giấu trong kênh `rgba` (Red, Green, Blue, Alpha) của ảnh, sử dụng bit ít quan trọng nhất (LSB) theo thứ tự `xy` (hàng và cột).
- Chuỗi ký tự trong dòng này là mục tiêu cần phân tích.

#### **Bước 2: Nhận diện chuỗi mã hóa**
- Chuỗi trích xuất được là:
  ```
  cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==
  ```
- Quan sát kỹ, chuỗi này bao gồm bốn lần lặp lại của một đoạn mã duy nhất:
  ```
  cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==
  ```
- Đoạn mã này kết thúc bằng `==`, đây là đặc điểm của mã hóa Base64 – một kỹ thuật thường được dùng trong các thử thách CTF để mã hóa flag.

#### **Bước 3: Giải mã Base64**
- Vì các đoạn mã lặp lại giống nhau, chúng ta chỉ cần giải mã một đoạn duy nhất.
- Sử dụng Python để giải mã:
  ```python
  import base64
  encoded = "cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ=="
  decoded = base64.b64decode(encoded).decode('utf-8')
  print(decoded)
  ```
- Kết quả:
  ```
  picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}
  ```
- Ngoài ra, bạn cũng có thể sử dụng các công cụ trực tuyến như `base64decode.org` để kiểm tra, kết quả sẽ tương tự.

#### **Bước 4: Xác nhận flag**
- Chuỗi giải mã được bắt đầu bằng `picoCTF{`, đây là định dạng chuẩn của flag trong các thử thách picoCTF.
- Phần còn lại, `r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_`, có thể hiểu là "red is the ultimate cure for sadness" (màu đỏ là liều thuốc tối thượng cho nỗi buồn) khi diễn giải theo kiểu leetspeak (thay số bằng chữ).
- Vậy, flag hoàn chỉnh là:
  ```
  picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}
  ```

#### **Bước 5: Lý giải sự lặp lại**
- Chuỗi mã hóa xuất hiện bốn lần trong đầu ra. Trong các thử thách CTF, flag thường chỉ là một chuỗi duy nhất, nên sự lặp lại này có thể là do cách dữ liệu được nhúng vào ảnh hoặc là một yếu tố gây nhiễu (red herring).
- Tuy nhiên, vì tất cả các đoạn đều giống nhau, chúng ta chỉ cần giải mã một lần để lấy flag.

### Quy trình thực hiện
1. **Chạy zsteg trên ảnh**:
   - Sử dụng lệnh:
     ```
     zsteg red.png
     ```
   - Công cụ sẽ liệt kê các dữ liệu ẩn trong ảnh.

2. **Xác định chuỗi mã hóa**:
   - Từ đầu ra, chọn chuỗi trong dòng `b1,rgba,lsb,xy`:
     ```
     cGljb0NURntyM2RfMXNfdGgzX3VsdDFtNHQzX2N1cjNfZjByXzU0ZG4zNTVffQ==
     ```

3. **Giải mã Base64**:
   - Dùng Python hoặc công cụ trực tuyến để giải mã chuỗi Base64 thành:
     ```
     picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}
     ```

4. **Kiểm tra và lấy flag**:
   - Xác nhận chuỗi giải mã phù hợp với định dạng flag của picoCTF.

### Kết luận
Sử dụng công cụ **zsteg**, chúng ta đã phát hiện dữ liệu ẩn trong ảnh `red.png` và giải mã thành công chuỗi Base64 để lấy được flag: `picoCTF{r3d_1s_th3_ult1m4t3_cur3_f0r_54dn355_}`. Các thông tin khác trong đầu ra (như bài thơ hoặc các file OpenPGP) không liên quan trực tiếp đến flag, và sự lặp lại của chuỗi mã hóa không ảnh hưởng đến kết quả cuối cùng.

Hy vọng write-up này giúp bạn hiểu rõ cách giải quyết thử thách!