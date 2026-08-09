if(-not (Test-Path -Path "asv")){
    mkdir asv | Out-Null
}
Move-item -Path .\*.asv -Destination ".\asv" -Force