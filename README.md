

## 2. Mã hóa thông điệp

### Bước 1: Mã hóa thông điệp "secret" bằng khóa "mykey"

```bash
./encode.sh "secret" "mykey"
```

### Bước 2: Kiểm tra đầu ra

```bash
cat encoded_text.txt
```

---

## 3. Giải mã và phát hiện thông điệp ẩn

### Bước 1: Giải mã văn bản đã mã hóa

```bash
./decode.sh grammar.cfg encoded_text.txt "mykey"
```

### Bước 2: Kết quả

* Nếu ngữ pháp và code chính xác, sẽ hiển thị thông điệp:
  `Recovered message: secret`

---

## 4. Tùy chỉnh ngữ pháp

### Bước 1: Tạo ngữ pháp mới

```bash
cp grammar.cfg my_grammar.cfg
nano my_grammar.cfg
```

### Nội dung mẫu cho `my_grammar.cfg`:

```text
Start → My trip to destination1 was adjective1, I visited place1.
destination1 → Hanoi || Paris
adjective1 → unforgettable || exciting
place1 → many attractions || famous landmarks
```

### Bước 2: Mã hóa với ngữ pháp tùy chỉnh

```bash
python3 generator.py my_grammar.cfg "secret" "mykey" > my_encoded.txt
cat my_encoded.txt
```

### Bước 3: Giải mã

```bash
./decode.sh my_grammar.cfg my_encoded.txt "mykey"
```

---

## 5. Kết thúc và nộp bài

Kết thúc lab và lấy file `.zip` kết quả:

```bash
stoplab
```

File zip kết quả sẽ được lưu và hiển thị vị trí trong terminal. Nộp file này cho giảng viên.

---

## Ghi chú kỹ thuật

* **grammar.cfg** cần đảm bảo đủ số lượng lựa chọn để biểu diễn 48 bit (≥2 lựa chọn cho mỗi non-terminal).
* Sửa code trong `generator.py` và `detector.py` đảm bảo sử dụng `math.ceil(log2(...))` để đủ bit khi số lựa chọn không phải lũy thừa của 2.
* Tối ưu hóa khả năng khớp văn bản nhiều từ (multi-word phrases) trong `detector.py`.


