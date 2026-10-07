# Fix_Push

### Khi push các file nhị phân lớn của Altium như .IntLib, .PcbLib hay .Step mà gặp lại Internal Server Error
- Thao tác như sau:
1. Hủy commit tạm thời:
``` powershell
git reset --soft HEAD~1
```

2. Cấu hình tắt nén:
``` powershell
git config core.compression 0
```

3. Tạo lại commit và push:
``` powershell
git add .
git commit -m "Update altium library"
git push origin master
```

4. Trả lại thiết lập nén mặc định cho Git:
``` powershell
git config --unset core.compression
```