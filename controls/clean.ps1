if(-not (Test-Path -Path "asv")){
    mkdir asv | Out-Null
}

$destFolder = (Get-Item -Path ".\asv").FullName

#Move-item -Path .\*.asv -Destination ".\asv" -Force
Get-ChildItem -Path . -Filter "*.asv" -Recurse -File | Where-Object { $_.DirectoryName -ne $destFolder } | Move-Item -Destination $destFolder -Force