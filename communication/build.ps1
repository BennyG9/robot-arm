Write-Host "Building Communication Protocol..."


# generate protocol files for STM32 firmware
python3 build_firmware.py


# copy protocol files into firmware
cp protocol_data.h ../firmware/arm_stm32/Core/Inc
cp protocol_data.c ../firmware/arm_stm32/Core/Src


# move protocol files into build folder
if(-not (Test-Path -Path "build")){
    mkdir build | Out-Null
}
mv protocol_data.h build -Force
mv protocol_data.c build -Force


Write-Host "Built Communication Protocol"
