#!/data/data/com.termux/files/usr/bin/bash

c_v=$(cat "$PREFIX/bin/mitoolV" | sed -n '1p')
l_v=$(curl -m 3 -s https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mitoolV | sed -n '1p')

if [ "$l_v" \> "$c_v" ]; then
    update=$(curl -s https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mitoolV | sed -n '/^#Update:/,$ { /^#Update:/d; p }')
    printf "
new update available!: \e[1;32m$l_v\e[0m \n \e[1;32m$update\e[0m\n
"
    echo -e "type \e[1;32mu\e[0m to update or \e[1;32mEnter\e[0m to skip : "
    read u
    if [ "$u" == "u" ]; then
        curl -s https://raw.githubusercontent.com/offici5l/MiTool/master/install.sh | sed -n '/files=("mitool"/,/^done/p' | bash
        mitool
    else
        echo "skip update .."
    fi
else
    echo
fi

curl -m3 -s https://raw.githubusercontent.com/offici5l/MiTool/master/MT/mitoolV | sed -n '/^#Note:/,/^#Update:/ {/^#Note:/b; /^#Update:/b; p}'

printf "\n\n┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n┃ https://github.com/offici5l/MiTool\n┃ Version: current:%s | latest:%s\n┃ - \e[1;32mm\e[0m for issues or suggestions\n┃ - \e[1;32mu\e[0m or \e[1;32muall\e[0m to update\n┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛" "$c_v" "$l_v"

printf "\n\n- \e[1;32mh\e[0melp (root, custom-recovery, partitions, commands ...)\n"

echo -e "


- \e[1;32m1\e[0m Unlock-or-Lock-Bootloader
"
echo -e "
- \e[1;32m2\e[0m Flash-Fastboot-ROM
 \e[1;32mv2\e[0m \e[1;31mFlash-Fastboot-ROM-V2\e[0m
"
echo -e "
- \e[1;32m3\e[0m Flash-Zip-With-Sideload
"

echo -e "
- \e[1;32m4\e[0m Bypass-HyperOS-BootLoader-Restrictions

"

if [ -z "$1" ]; then
    read -p $'\n\nEnter your \e[1;32mchoice\e[0m: ' choice
else
    choice="$1"
fi

if [ "$choice" == "1" ]; then
    python3 "$PREFIX/bin/un-lock.py"
elif [ "$choice" == "2" ]; then
    python3 "$PREFIX/bin/flashfastbootrom.py"
elif [ "$choice" == "3" ]; then
    python3 "$PREFIX/bin/flashwithsideloadmode.py"
elif [ "$choice" == "4" ]; then
    python3 "$PREFIX/bin/bypass-bl.py"
elif [ "$choice" == "u" ]; then
    curl -s https://raw.githubusercontent.com/offici5l/MiTool/master/install.sh | sed -n '/files=("mitool"/,/^done/p' | bash
    mitool
elif [ "$choice" == "uall" ]; then
    curl -s https://raw.githubusercontent.com/offici5l/MiTool/master/install.sh | sed '$d' | bash
    mitool
elif [ "$choice" == "v2" ]; then
    python3 "$PREFIX/bin/flashfastbootromatest.py"
elif [ "$choice" == "m" ]; then
    read -p $'\nDo you want to send an \e[1;31missue\e[0m or a \e[0;32msuggestion\e[0m (i/s): ' choice &&
([ -z "$choice" ] || ([ "$choice" != "i" ] && [ "$choice" != "s" ])) &&
echo -e "Invalid choice. Exiting." ||
read -p "Please write your $(if [ "$choice" == "i" ]; then echo -e "\e[1;31mIssue\e[0m"; else echo -e "\e[1;32msuggestion\e[0m"; fi): " input_text &&
username=$(whoami) &&
mtype=$(if [ "$choice" == "i" ]; then echo "#Issue"; else echo "#Suggestion"; fi) &&
full_message="${mtype} from #user: ${username}%3A%0A%0A${input_text}" &&
curl -X POST -d "chat_id=-1002017234802&text=${full_message}" "https://api.telegram.org/bot6772941553:AAHZ-ICe-4zeLWil2VYv4_WOgoDSD3Haz9o/sendMessage" > /dev/null 2>&1 &&
([ $? -eq 0 ] && echo -e "${mtype} sent successfully to t.me/Offici5l_Group " ||
echo -e "\e[31mFailed to send ${mtype} to t.me/Offici5l_Group . Exit code: $? \e[0m")
elif [ "$choice" == "h" ]; then
    echo -e "
\n\n\n\033[1;36mFlash Custom Recovery:\033[0m
Type: \033[1;32mfastboot flash recovery name.img\033[0m
Example: \033[1;32mfastboot flash recovery /sdcard/download/recovery.img\033[0m

\n\n\n\033[1;36mFlash Root:\033[0m
1. Download and install \033[0;33mMagisk app\033[0m
2. Open Magisk app, press \033[0;33mInstall\033[0m in the Magisk card
3. Choose '\033[0;33mSelect and Patch a File\033[0m', select \033[1;32mboot.img\033[0m
   (\033[1;33mNote: Choose boot.img for the device you want to root\033[0m)
   Type: \033[1;32mfastboot flash boot name.img\033[0m
   Example: \033[1;32mfastboot flash boot /sdcard/download/boot.img\033[0m

\n\n\n\033[1;36mFlash Specific Partitions\033[0m
('recovery', 'boot', 'vbmeta', 'vbmeta_system', 'metadata', 'dtbo', 'cust', 'super', 'userdata', ...):
   Type, for example: \n   \033[1;32mfastboot flash super /sdcard/download/super.img\033[0m

\n\n\n\033[1;36mFor more fastboot and adb commands:\033[0m\ntype: \033[1;32mfastboot help\033[0m or \033[1;32madb help\033[0m
"
else
    echo "Invalid choice"
    exit
fi