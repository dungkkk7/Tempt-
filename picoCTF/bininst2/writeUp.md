### frida-trace -f bininst2.exe -i CreateFileA -i WriteFile -i MessageBoxA -i MessageBoxW

### **Phân tích đầu ra**

#### **Lần chạy thứ hai (có dữ liệu buffer quan trọng)**
```
           /* TID 0x50ac */
    12 ms  CreateFileA called:
    12 ms    lpFileName: <Insert path here>
    12 ms     | CreateFileA called:
    12 ms     |   lpFileName: <Insert path here>
    13 ms     | CreateFileA returned: 0xffffffffffffffff
    13 ms     |   Forced return value: 0x1234
    13 ms  CreateFileA returned: 0x1234
    13 ms    Forced return value: 0x1234
    13 ms  WriteFile called:
    13 ms    hFile: 0x1234
    13 ms    lpBuffer pointer: 0x140002270
    13 ms    nNumberOfBytesToWrite: 0
    13 ms    No data to write (size = 0)
    13 ms    Buffer content (32 bytes):            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
00000000  63 47 6c 6a 62 30 4e 55 52 6e 74 6d 63 6a 46 6b  cGljb0NURntmcjFk
00000010  59 56 39 6d 4d 48 4a 66 59 6a 46 75 58 32 6c 75  YV9mMHJfYjFuX2lu
    13 ms     | WriteFile called:
    13 ms     |   hFile: 0x1234
    13 ms     |   lpBuffer pointer: 0x140002270
    13 ms     |   nNumberOfBytesToWrite: 0
    13 ms     |   No data to write (size = 0)
    13 ms     |   Buffer content (32 bytes):            0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  0123456789ABCDEF
00000000  63 47 6c 6a 62 30 4e 55 52 6e 74 6d 63 6a 46 6b  cGljb0NURntmcjFk
00000010  59 56 39 6d 4d 48 4a 66 59 6a 46 75 58 32 6c 75  YV9mMHJfYjFuX2lu
    13 ms     | WriteFile returned: 0x0
    13 ms  WriteFile returned: 0x0
Process terminated
```

1. **`CreateFileA`**:
   - `lpFileName: <Insert path here>`: Chương trình cố mở tệp `"<Insert path here>"`.
   - `Forced return value: 0x1234`: Bạn đã ghi đè giá trị trả về thành công, cho phép chương trình tiếp tục chạy.

2. **`WriteFile`**:
   - `hFile: 0x1234`: Handle giả được sử dụng.
   - `lpBuffer pointer: 0x140002270`: Con trỏ tới buffer chứa dữ liệu cần ghi.
   - `nNumberOfBytesToWrite: 0`: Kích thước dữ liệu bằng 0, nên không có gì được ghi.
   - **Buffer content (32 bytes)**:
     ```
     00000000  63 47 6c 6a 62 30 4e 55 52 6e 74 6d 63 6a 46 6b  cGljb0NURntmcjFk
     00000010  59 56 39 6d 4d 48 4a 66 59 6a 46 75 58 32 6c 75  YV9mMHJfYjFuX2lu
     ```
     - Đây là dữ liệu thô từ buffer tại `0x140002270`. Khi giải mã hex thành ASCII, ta được:
       ```
       cGljb0NURntmcjFkYV9mMHJfYjFuX2lu
       ```
       - Chuỗi này trông giống base64, một định dạng phổ biến trong CTF.

3. **Không có `MessageBoxA` hoặc `MessageBoxW`**:
   - Các hàm này không xuất hiện trong đầu ra, nghĩa là flag không được hiển thị qua message box.

---

### **Giải mã dữ liệu buffer**
Chuỗi hex `63 47 6c 6a 62 30 4e 55 52 6e 74 6d 63 6a 46 6b 59 56 39 6d 4d 48 4a 66 59 6a 46 75 58 32 6c 75` tương ứng với chuỗi ASCII:
```
cGljb0NURntmcjFkYV9mMHJfYjFuX2lu
```

1. **Giải mã base64**:
   - Dùng công cụ như CyberChef hoặc lệnh Python:
     ```python
     import base64
     encoded = "cGljb0NURntmcjFkYV9mMHJfYjFuX2lu"
     decoded = base64.b64decode(encoded).decode('utf-8')
     print(decoded)
     ```
   - Kết quả:
     ```
     picoCTF{fr1da_f0r_b1n_2n
     ```
   - Chuỗi này bắt đầu bằng `picoCTF{`, một định dạng flag điển hình trong PicoCTF, nhưng bị cắt ngắn do handler chỉ đọc 32 byte.

2. **Đọc thêm dữ liệu từ buffer**:
   - Buffer tại `0x140002270` có thể chứa flag đầy đủ. Hãy sửa handler để đọc nhiều byte hơn.

---

### **Cách khắc phục**

#### **Bước 1: Sửa handler `WriteFile` để đọc toàn bộ flag**
1. **Mở tệp handler**:
   - `C:\Users\dungv\Downloads\bininst2\__handlers__\KERNEL32.DLL\WriteFile.js` hoặc `KERNELBASE.dll\WriteFile.js`.

2. **Thay nội dung**:
   ```javascript
   {
     onEnter: function (log, args, state) {
       log('WriteFile called:');
       log('  hFile: ' + args[0]);
       log('  lpBuffer pointer: ' + args[1]);
       var size = args[2].toInt32();
       log('  nNumberOfBytesToWrite: ' + size);
       if (size > 0) {
         log('  Data: ' + Memory.readUtf8String(args[1], size));
       } else {
         log('  No data to write (size = 0)');
         // Đọc 64 byte để lấy flag đầy đủ
         try {
           var bufferCheck = Memory.readByteArray(args[1], 64);
           log('  Buffer content (64 bytes): ' + hexdump(bufferCheck));
           var fullString = Memory.readUtf8String(args[1]);
           log('  Full string: ' + fullString);
         } catch (e) {
           log('  Buffer content: [Failed to read]');
         }
       }
     },
     onLeave: function (log, retval, state) {
       log('WriteFile returned: ' + retval);
     }
   }
   ```

3. **Chạy lại**:
   ```
   frida-trace -f bininst2.exe -i CreateFileA -i WriteFile
   ```
   - Giữ handler `CreateFileA` với ghi đè `0x1234`.
   - Đầu ra sẽ hiển thị chuỗi đầy đủ từ `0x140002270`, có thể là flag hoàn chỉnh.

#### **Bước 2: Xác nhận flag**


### **Kết luận**
- **Phát hiện**: Buffer tại `0x140002270` chứa chuỗi base64 `cGljb0NURntmcjFkYV9mMHJfYjFuX2lu`, giải mã thành `picoCTF{fr1da_f0r_b1n_2n...`, là một phần của flag.
- **Hành động**: Sửa handler `WriteFile` để đọc toàn bộ chuỗi và lấy flag đầy đủ.
