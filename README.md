#Tải bài lab trên Labtainer
imodule https://github.com/hieunm2025/steg-cfg-basic/raw/refs/heads/main/imodule.tar
#Khởi đọng bài lab
labtainer -r steg-cfg-basic

./encode.sh "secret" "mykey"

./decode.sh grammar.cfg encoded_text.txt "mykey"
