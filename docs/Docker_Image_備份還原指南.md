# Docker Image 備份與還原指南

本文件說明如何將 Docker Image 儲存到隨身碟並在另一台電腦上還原。

## 目錄
- [查看現有 Images](#查看現有-images)
- [儲存 Images](#儲存-images)
- [Linux 掛載隨身碟](#linux-掛載隨身碟)
- [複製檔案到隨身碟](#複製檔案到隨身碟)
- [載入 Images](#載入-images)
- [完整範例](#完整範例)

---

## 查看現有 Images

### Windows (CMD/PowerShell)
```cmd
docker images
```

### Linux/Mac
```bash
docker images
```

---

## 儲存 Images

### 方法 1: 儲存單個 Image

#### Windows
```cmd
REM 儲存到本機
docker save -o C:\Users\akifa\image-name.tar image-name:tag

REM 直接儲存到隨身碟 (假設隨身碟是 E:)
docker save -o E:\image-name.tar image-name:tag
```

#### Linux/Mac
```bash
# 儲存到本機
docker save -o ~/image-name.tar image-name:tag

# 直接儲存到隨身碟 (假設掛載在 /media/usb)
docker save -o /media/usb/image-name.tar image-name:tag
```

### 方法 2: 儲存多個 Images 到一個檔案 (推薦)

#### Windows
```cmd
REM 儲存三個 images 到同一個 tar 檔
docker save -o E:\my-images.tar image1:tag image2:tag image3:tag

REM 實際範例
docker save -o E:\my-images.tar nginx:latest postgres:14 redis:alpine
```

#### Linux/Mac
```bash
# 儲存三個 images 到同一個 tar 檔
docker save -o /media/usb/my-images.tar image1:tag image2:tag image3:tag

# 實際範例
docker save -o /media/usb/my-images.tar nginx:latest postgres:14 redis:alpine
```

### 方法 3: 儲存多個 Images 到個別檔案

#### Windows
```cmd
docker save -o E:\image1.tar image1:tag
docker save -o E:\image2.tar image2:tag
docker save -o E:\image3.tar image3:tag
```

#### Linux/Mac
```bash
docker save -o /media/usb/image1.tar image1:tag
docker save -o /media/usb/image2.tar image2:tag
docker save -o /media/usb/image3.tar image3:tag
```

---

## Linux 掛載隨身碟

### 1. 插入隨身碟後查看設備

```bash
# 查看所有磁碟設備
lsblk

# 或使用 fdisk
sudo fdisk -l

# 查看最新的內核訊息 (插入隨身碟後執行)
dmesg | tail -20
```

輸出範例：
```
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sda      8:0    0 238.5G  0 disk
├─sda1   8:1    0   512M  0 part /boot/efi
└─sda2   8:2    0   238G  0 part /
sdb      8:16   1  14.9G  0 disk         <-- 這是隨身碟
└─sdb1   8:17   1  14.9G  0 part
```

### 2. 建立掛載點

```bash
# 建立掛載目錄
sudo mkdir -p /mnt/usb

# 或使用其他名稱
sudo mkdir -p /media/myusb
```

### 3. 掛載隨身碟

```bash
# 一般 FAT32/exFAT 格式 (最常見)
sudo mount /dev/sdb1 /mnt/usb

# 如果是 NTFS 格式
sudo mount -t ntfs-3g /dev/sdb1 /mnt/usb

# 如果是 ext4 格式
sudo mount -t ext4 /dev/sdb1 /mnt/usb

# 掛載時指定權限 (所有人可讀寫)
sudo mount -o umask=000 /dev/sdb1 /mnt/usb
```

### 4. 驗證掛載成功

```bash
# 查看掛載點
df -h | grep usb

# 或
mount | grep usb

# 列出隨身碟內容
ls -la /mnt/usb
```

### 5. 使用完畢後卸載

```bash
# 卸載隨身碟 (使用前請確保沒有程式正在使用)
sudo umount /mnt/usb

# 如果顯示 "target is busy"，找出占用的程式
lsof /mnt/usb

# 強制卸載 (不建議，可能導致資料遺失)
sudo umount -l /mnt/usb
```

### 6. 自動掛載到 /media (Ubuntu/Debian)

在桌面環境中，通常會自動掛載到：
```bash
# 自動掛載位置
/media/username/USB_LABEL
# 例如: /media/akifa/MY_USB

# 查看自動掛載的設備
ls /media/$USER/
```

### 常見問題排解

#### 問題 1: mount: unknown filesystem type 'exfat'
```bash
# 安裝 exFAT 支援
sudo apt-get install exfat-fuse exfat-utils  # Debian/Ubuntu
sudo yum install exfat-utils fuse-exfat       # CentOS/RHEL
```

#### 問題 2: mount: /mnt/usb: special device /dev/sdb1 does not exist
```bash
# 重新檢查設備名稱
lsblk
# 可能是 sdc1, sdd1 等
```

#### 問題 3: 權限不足無法寫入
```bash
# 重新掛載並設定權限
sudo umount /mnt/usb
sudo mount -o uid=1000,gid=1000 /dev/sdb1 /mnt/usb

# 或直接修改掛載點權限
sudo chmod 777 /mnt/usb
```

### 完整範例：掛載並儲存 Docker Image

```bash
# 1. 插入隨身碟，查看設備
lsblk

# 2. 建立掛載點
sudo mkdir -p /mnt/usb

# 3. 掛載隨身碟 (假設是 /dev/sdb1)
sudo mount /dev/sdb1 /mnt/usb

# 4. 驗證掛載
df -h | grep usb

# 5. 儲存 Docker Image
docker save -o /mnt/usb/myapp-backup.tar myapp:v1.0

# 6. 驗證檔案
ls -lh /mnt/usb/

# 7. 使用完畢後卸載
sudo umount /mnt/usb

# 8. 安全移除隨身碟
# 卸載後就可以安全拔除隨身碟了
```

---

## 複製檔案到隨身碟

### Windows
```cmd
REM 複製單一檔案
copy C:\Users\akifa\my-images.tar E:\

REM 複製多個檔案
copy C:\Users\akifa\*.tar E:\
```

### Linux/Mac
```bash
# 複製單一檔案
cp ~/my-images.tar /media/usb/

# 複製多個檔案
cp ~/*.tar /media/usb/
```

---

## 載入 Images

### 方法 1: 從隨身碟直接載入

#### Windows
```cmd
REM 從隨身碟載入
docker load -i E:\my-images.tar
```

#### Linux/Mac
```bash
# 從隨身碟載入
docker load -i /media/usb/my-images.tar
```

### 方法 2: 先複製到本機再載入

#### Windows
```cmd
REM 複製到本機
copy E:\my-images.tar C:\Users\username\

REM 載入 image
docker load -i C:\Users\username\my-images.tar
```

#### Linux/Mac
```bash
# 複製到本機
cp /media/usb/my-images.tar ~/

# 載入 image
docker load -i ~/my-images.tar
```

### 載入多個 tar 檔案

#### Windows
```cmd
docker load -i E:\image1.tar
docker load -i E:\image2.tar
docker load -i E:\image3.tar
```

#### Linux/Mac
```bash
docker load -i /media/usb/image1.tar
docker load -i /media/usb/image2.tar
docker load -i /media/usb/image3.tar
```

---

## 驗證

### Windows & Linux/Mac (相同指令)
```bash
# 查看已載入的 images
docker images

# 確認特定 image
docker images | grep image-name
```

---

## 壓縮選項 (節省空間)

### 儲存並壓縮

#### Windows (PowerShell)
```powershell
# 儲存並壓縮
docker save image-name:tag | gzip > E:\image-name.tar.gz
```

#### Linux/Mac
```bash
# 儲存並壓縮
docker save image-name:tag | gzip > /media/usb/image-name.tar.gz
```

### 解壓並載入

#### Windows (PowerShell)
```powershell
# 需要先安裝 gzip 工具，或使用 7-Zip
# 使用 7-Zip 解壓
7z x E:\image-name.tar.gz
docker load -i E:\image-name.tar
```

#### Linux/Mac
```bash
# 解壓並載入
gunzip -c /media/usb/image-name.tar.gz | docker load
```

---

## 完整範例

### 情境：備份三個 Docker Images 到隨身碟

#### Windows 完整流程

```cmd
REM 1. 查看現有 images
docker images

REM 2. 記下要備份的 images (例如)
REM    - myapp-backend:v1.0
REM    - myapp-frontend:v1.0
REM    - postgres:14

REM 3. 儲存到隨身碟 E: (所有 images 存成一個檔案)
docker save -o E:\myapp-backup.tar myapp-backend:v1.0 myapp-frontend:v1.0 postgres:14

REM 4. 驗證檔案已建立
dir E:\myapp-backup.tar

REM === 在另一台電腦 ===

REM 5. 載入 images
docker load -i E:\myapp-backup.tar

REM 6. 驗證載入成功
docker images
```

#### Linux/Mac 完整流程

```bash
# 1. 查看現有 images
docker images

# 2. 記下要備份的 images (例如)
#    - myapp-backend:v1.0
#    - myapp-frontend:v1.0
#    - postgres:14

# 3. 儲存到隨身碟 /media/usb (所有 images 存成一個檔案)
docker save -o /media/usb/myapp-backup.tar myapp-backend:v1.0 myapp-frontend:v1.0 postgres:14

# 4. 驗證檔案已建立
ls -lh /media/usb/myapp-backup.tar

# === 在另一台電腦 ===

# 5. 載入 images
docker load -i /media/usb/myapp-backup.tar

# 6. 驗證載入成功
docker images
```

---

## 注意事項

1. **檔案大小**
   - Docker image 檔案可能很大 (數百 MB 到數 GB)
   - 確保隨身碟有足夠空間
   - 建議使用 USB 3.0+ 以加快傳輸速度

2. **Tag 名稱**
   - 儲存時必須指定正確的 tag (通常是 `latest` 或版本號)
   - 使用 `docker images` 查看完整的 image 名稱和 tag

3. **網路環境**
   - 此方法適用於無法連接網路或 Docker Hub 的環境
   - 適合離線部署或內網環境

4. **建議做法**
   - 推薦將多個 images 儲存到同一個 tar 檔，方便管理
   - 載入前先用 `docker images` 確認目標電腦沒有同名 image 衝突
   - 備份時建立清單記錄儲存的 images 和版本

5. **Windows 路徑**
   - 使用反斜線 `\` 或正斜線 `/` 都可以
   - 隨身碟通常是 `D:`, `E:`, `F:` 等磁碟代號

6. **Linux/Mac 掛載點**
   - 隨身碟通常掛載在 `/media/username/` 或 `/mnt/`
   - 使用 `df -h` 或 `lsblk` 查看掛載位置

---

## 常見問題

### Q: 可以同時儲存所有 images 嗎？
A: 可以，但不建議。建議只儲存需要的 images：
```bash
# 儲存所有 images (不建議，檔案會很大)
docker save $(docker images -q) -o all-images.tar
```

### Q: 如何知道 tar 檔裡有哪些 images？
A: 無法直接查看，建議建立清單檔案：

#### Windows
```cmd
docker images > E:\images-list.txt
```

#### Linux/Mac
```bash
docker images > /media/usb/images-list.txt
```

### Q: 載入後 image ID 會改變嗎？
A: 不會，image ID 會保持一致。

### Q: 可以在不同作業系統間傳輸嗎？
A: 可以，但要注意 image 是否支援目標平台架構 (amd64, arm64 等)。

---

## 相關指令參考

```bash
# 查看 Docker 版本
docker --version

# 查看 Docker 資訊
docker info

# 刪除不需要的 images (釋放空間)
docker image prune

# 查看 image 詳細資訊
docker inspect image-name:tag

# 重新命名 image tag
docker tag old-name:tag new-name:tag
```

---

**文件版本**: 1.0
**最後更新**: 2025-12-12
**適用平台**: Windows, Linux, macOS
