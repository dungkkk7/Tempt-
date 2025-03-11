Writeup: Phân tích nhật ký Windows để phát hiện hành vi phần mềm độc hại
Tình huống giả định
Một nhân viên đã tải và chạy một trình cài đặt từ internet. Sau khi cài đặt, phần mềm không hoạt động như kỳ vọng. Mỗi lần đăng nhập, một cửa sổ dòng lệnh màu đen xuất hiện thoáng qua, và máy tính ngay lập tức tắt. Nhiệm vụ là phân tích các sự kiện Event ID 4657, 1074, và 1033 trong nhật ký Windows để hiểu hành vi của phần mềm độc hại và thu thập các mảnh thông tin quan trọng (ví dụ: flag).

Các sự kiện được tìm thấy
Event ID 4657: Ghi lại thay đổi trong Registry (Security Log).
Event ID 1074: Ghi lại việc hệ thống tắt hoặc khởi động lại (System Log).
Event ID 1033: Liên quan đến quá trình cài đặt phần mềm (Application Log).
Phân tích từng sự kiện
1. Event ID 4657 (Thay đổi Registry)
Ý nghĩa: Sự kiện này xuất hiện khi một giá trị trong Registry bị sửa đổi, thường được ghi lại nếu auditing cho Registry đã được bật.
Hành vi phần mềm độc hại: Phần mềm độc hại có thể đã thêm hoặc sửa đổi một khóa Registry để chạy tự động mỗi khi hệ thống khởi động. Ví dụ, nó có thể thêm một giá trị vào HKCU\Software\Microsoft\Windows\CurrentVersion\Run để thực thi một lệnh (như tắt máy).
Thông tin cần kiểm tra:
Object Name: Đường dẫn Registry bị thay đổi (ví dụ: HKCU\Software\Microsoft\Windows\CurrentVersion\Run).
Value Name: Tên giá trị được thêm hoặc sửa đổi.
New Value: Giá trị mới được thiết lập, có thể là một lệnh như cmd.exe /c shutdown /s /t 0.
User: Tài khoản thực hiện thay đổi.
Ví dụ cụ thể: Nếu New Value là "cmd.exe /c echo FLAG_PART_1 & shutdown /s /t 0", thì FLAG_PART_1 là một mảnh thông tin quan trọng.
2. Event ID 1074 (Tắt máy hoặc khởi động lại)
Ý nghĩa: Sự kiện này ghi lại khi hệ thống được tắt hoặc khởi động lại bởi một tiến trình cụ thể.
Hành vi phần mềm độc hại: Phần mềm độc hại có thể đã kích hoạt lệnh tắt máy ngay sau khi người dùng đăng nhập, giải thích hiện tượng máy tính tự động tắt.
Thông tin cần kiểm tra:
Process Name: Tên tiến trình thực thi lệnh (thường là shutdown.exe hoặc cmd.exe).
User: Tài khoản thực hiện lệnh.
Comment: Nếu lệnh bao gồm tham số /c "comment", phần ghi chú này có thể chứa thông tin bổ sung.
Ví dụ cụ thể: Nếu Comment ghi "Shutdown initiated with flag FLAG_PART_2", thì FLAG_PART_2 là mảnh thông tin thứ hai.
3. Event ID 1033 (Cài đặt phần mềm)
Ý nghĩa: Sự kiện này thường liên quan đến Windows Installer, ghi lại quá trình cài đặt hoặc gỡ bỏ phần mềm.
Hành vi phần mềm độc hại: Ghi lại việc cài đặt phần mềm độc hại thông qua trình cài đặt mà nhân viên đã chạy.
Thông tin cần kiểm tra:
Source: Nguồn sự kiện (thường là MsiInstaller).
Description: Mô tả chi tiết về quá trình cài đặt, có thể chứa tên phần mềm hoặc thông tin khác.
Ví dụ cụ thể: Nếu Description ghi "Installation completed with flag FLAG_PART_3", thì FLAG_PART_3 là mảnh thông tin cuối cùng.
Tổng hợp thông tin thành một bức tranh hoàn chỉnh
Dựa trên ba sự kiện trên, ta có thể tái hiện hành vi của phần mềm độc hại như sau:

Giai đoạn cài đặt (Event ID 1033):
Trình cài đặt được tải từ internet đã chạy và cài đặt phần mềm độc hại. Sự kiện 1033 ghi lại quá trình này, có thể chứa thông tin như tên phần mềm hoặc một mảnh flag trong trường Description.
Thiết lập cơ chế kiên trì (Event ID 4657):
Phần mềm độc hại sửa đổi Registry để đảm bảo nó tự động chạy khi người dùng đăng nhập. Sự kiện 4657 cho thấy một giá trị mới được thêm vào (ví dụ: Run), với lệnh thực thi bao gồm cả hành động tắt máy.
Thực thi lệnh tắt máy (Event ID 1074):
Sau khi đăng nhập, phần mềm độc hại kích hoạt lệnh tắt máy (thông qua shutdown.exe hoặc cmd.exe), được ghi lại trong sự kiện 1074. Điều này giải thích hiện tượng máy tính tắt ngay lập tứ