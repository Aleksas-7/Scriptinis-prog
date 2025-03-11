
param (
    [string]$username = ""
)

$openNotes = $true

Write-Host "Username: |$username|"

$processes = Get-Process -IncludeUserName

Write-Host "Creted array 'processes' of type: $($processes.GetType().BaseType)"
$date = Get-Date -Format "yyyy-MM-dd"
$time = Get-Date -Format "HH-mm-ss"  #-mm-ss



if ($username -eq "") {
    # No username was provided
    # Means go through all users

    $userList =  Get-LocalUser | Select-Object -ExpandProperty Name
    #$userList += "SYSTEM"
    #$userLIST += "LOCAL SERVICE"
    #$userList += "NETWORK SERVICE"

    $userlessFileName = "$(Get-Location)\logs\userLESS-process-log-$date-$time.txt"
    Add-Content -Path $userlessFileName -Value "$date `n$time `n`n" | Out-Null

    # Create files for each users processes
    foreach ($name in $userList) {
        # Write-Host "! User: $name"
        $fileName = "$(Get-Location)\logs\$($name)-process-log-$date-$time.txt" 
        New-Item -Path $fileName -ItemType File | Out-Null

        Add-Content -Path $fileName -Value "$date `n$time `n`n" | Out-Null

        # Go though all the processes
        # Get ones with $name
        # Output the to $fileName
        foreach($process in $processes) {
            if ($process.UserName -like "*$name*") {
                Add-Content -Path $fileName -Value "Name: $($process.ProcessName)`nId: $($process.Id)`nHandles: $($process.Handles)`nCPU: $($process.CPU)`n##################################"
            }
            elseif ([string]::IsNullOrEmpty($process.UserName)) {
                # Process has no user defined
                Add-Content -Path $userlessFileName -Value "Name: $($process.ProcessName)`nId: $($process.Id)`nHandles: $($process.Handles)`nCPU: $($process.CPU)`n##################################"
            }
        }

        if ($openNotes){ Invoke-Item -Path $fileName}
        pause
        Stop-Process -Name "Notepad"
    }

    if ($openNotes){ Invoke-Item -Path $userlessFileName}
    pause
    Stop-Process -Name "Notepad"



}
else {
    # Username provided
    # Go through only this users processes
    

    # Check if such a user even exists
    $userList =  Get-LocalUser | Select-Object -ExpandProperty Name
    if ($userList -notContains $username) {
        # The provided user does not exist
        Write-Host "User $username does not exist"
        exit
    }

    # The $username user exists
    $fileName = "$(Get-Location)\logs\$($username)-process-log-$date-$time.txt" 
    New-Item -Path $fileName -ItemType File | Out-Null

    Add-Content -Path $fileName -Value "$date `n$time `n`n" | Out-Null

    # Go though all the processes
    # Get ones with $name
    # Output the to $fileName
    foreach($process in $processes) {
        if ($process.UserName -like "*$username*") {
            Add-Content -Path $fileName -Value "Name: $($process.ProcessName)`nId: $($process.Id)`nHandles: $($process.Handles)`nCPU: $($process.CPU)`n##################################"
        }
    }
    if ($openNotes){ Invoke-Item -Path $fileName}
    pause
    Stop-Process -Name "Notepad"
}