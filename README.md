# Altium Library

### Thuận lợi

### Cách thức hoạt động

![<img width="200" height="200"/>](assets/library_diagram.png)

### Cách sử dụng

#### Clone repository
1. `https://github.com/NguyenHien-8/Altium_Library.git`

### Cấu hình trình điều khiển ODBC cho PostgreSQL

#### Offline development configuration
1. Tải xuống và cài đặt Postgres để phát triển cục bộ [here](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) -> `Download the installer`.
  - Tải xuống và cài đặt công cụ PgAdmin từ [here](https://www.pgadmin.org/).
  - Tạo cơ sở dữ liệu trống:
    - ![<img width="20" height="20"/>](assets/database.png)
  - Trong `Database` ô này, hãy viết: `Altium-Components` -> `Save`
    - ![<img width="10" height="10"/>](assets/database1.png)
   
2. Tải xuống trình điều khiển pSQLODBC_x64 từ [this](https://www.postgresql.org/ftp/odbc/versions.old/) vị trí.
  Chúng ta đang cấu hình trình điều khiển ODBC cho Windows 11 trở lên, vì vậy chúng ta sẽ tải xuống tệp MSI của trình điều khiển. Nhấp vào thư mục MSI.
    - ![<img width="15" height="15"/>](assets/link_1.png)
3. Trong thư mục MSI, bạn có thể xem các phiên bản trình điều khiển khác nhau. Các tệp được nén ở định dạng zip.
      Chúng ta muốn tải xuống phiên bản mới nhất, vì vậy hãy cuộn xuống cuối trang và nhấp vào tệp `psqlodbc_13_02_0000-x86-1.zip`.
   - ![<img width="15" height="15"/>](assets/link_2.png)
4. Sau khi quá trình tải xuống hoàn tất, nhấp chuột phải vào tệp `psqlodbc_13_02_0000-x86-1.zip` và chọn Extract to `psqlodbc_13_02_0000-x86-1.zip`.
    - ![<img width="15" height="15"/>](assets/link_3.png)
5. Cài đặt trình điều khiển psqlODBC_x64. Nhấp vào `Next`.
    - ![<img width="15" height="15"/>](assets/link_4.png)
6. Sau đó nhấp vào "I accept the terms in the license agreement"
7. Trên màn hình ***Custom Setup***, Bạn có thể chọn tính năng của trình điều khiển. Nhấp chuột `Next`.
8. Trên màn hình ***Ready to install***, Nhấp chuột vào `Install`.

#### Cấu hình trình điều khiển pSQLODBC_x64 sử dụng System DSN
1. Nhấn `Window` và viết `ODBC`.
    - ![<img width="15" height="15"/>](assets/link_5.png)
2. Mở ODBC Data Source (64-bit) -> Nhấp vào thẻ System DSN -> Nhấp vào Add.
    - ![<img width="15" height="15"/>](assets/link_6.png)
3. Hộp thoại "Create a new data source" sẽ mở ra. Hãy chọn trình điều khiển PostgreSQL ODBC Driver(UNICODE) và nhấp vào nút Finish.
    - ![<img width="15" height="15"/>](assets/link_7.png)
4. Cấu hình các thông số như sau và nhấn `Test`.
    - ![<img width="15" height="15"/>](assets/link_8.png)
5. Kiểm tra kết nối.
    - ![<img width="15" height="15"/>](assets/link_9.png)
6. Nhấp vào Lưu để tạo DSN hệ thống. Quay lại màn hình DSN hệ thống, bạn có thể thấy `localPostgres` DSN đã được tạo.
    - ![<img width="15" height="15"/>](assets/link_10.png)

#### Populate Database using migration tool
1. Go to [altium-migrator](https://github.com/ximtech/altium-migrator#how-to-use-it) and follow instructions.
2. At this point, tip `5` can be skipped in `altium-migrator` manual, because database already has been installed.
3. If all ok, move to the next step

#### Add library to Altium
1. Open `Altium designer` -> `Components` -> `File-based Libraries Preferences` -> `Install`
2. Go to `altium-library` folder then choose:
    - ![<img width="20" height="20"/>](assets/link_10.png)
3. Additionally, verify connection settings by pressing `Advanced...` button
    - ![<img width="20" height="20"/>](assets/altium_db_settings.png)

## For already existing database
1. Skip first tip at `Offline development configuration` manual
2. In `Configure pSQLODBC_x64 Driver using System DSN` set your DB datasource values(host, port, username and password)
3. Populate DB using [altium-migrator](https://github.com/ximtech/altium-migrator) tool
3. Then in `altium-library` folder open `Postgres Altium Library - altium_library.DbLib` with notepad and change `ConnectionString`(4th line) with custom DB parameters
