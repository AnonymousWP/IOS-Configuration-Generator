$hostname = Read-Host -Prompt 'Input the hostname'
$secret = Read-Host -Prompt 'Input the secret password'
$console = Read-Host -Prompt 'Input the console password'
$vty = Read-Host -Prompt 'Input the vty password'


$Title = "Choose for router of switch configuration"
$Prompt = "Enter your choice"
$Choices = [System.Management.Automation.Host.ChoiceDescription[]] @("&Router", "&Switch", "&Cancel")
$Default = 0

$Choice = $host.UI.PromptForChoice($Title, $Prompt, $Choices, $Default)

switch($Choice)
{
    0 { New-Item .\routerps1.txt -Force
        $interface = Read-Host -Prompt 'Input the interface'
        $ip = Read-Host -Prompt 'Input the IP-address' 
        $sub = Read-Host -Prompt 'Input the subnetmask'
        $description = Read-Host -Prompt 'Input the description of the interface'
        $username = Read-Host -Prompt 'Input the username'
        $password = Read-Host -Prompt 'Input the usernames password'
        $banner = Read-Host -Prompt 'Input the banner'

        Add-Content .\routerps1.txt "enable `n!`nconf t `n!`nhostname $hostname `n!`nenable secret $secret`n!`nbanner motd # $banner # `n!`nno ip domain-lookup"
        Add-Content .\routerps1.txt "!`nusername $username privilege 15 password 0 $password`n!`ninterface $interface `ndescription $description `nip address $ip $sub `nno shutdown"
        Add-Content .\routerps1.txt "!`nline con 0 `nexec-timeout 0 0 `nprivilege level 15 `npassword $console `nlogin `nlogging synchronuos"
        Add-Content .\routerps1.txt "!`nline vty 0 15 `npassword $vty `nlogin local `ntransport input ssh `n!`ncrypto key generate rsa 2048 `nip ssh version 2 `n!"

        $Encryption = "Do you want to use password encryption?"
        $Prompt1 = "Enter your choice"
        $Choices1 = [System.Management.Automation.Host.ChoiceDescription[]] @("&Yes", "&No")
        $Default1 = 1
        $Choice1 = $host.UI.PromptForChoice($Encryption, $Prompt1, $Choices1, $Default1)
        switch($Choice1)
        {
            0 { Add-Content .\routerps1.txt "service password-encryption `n!"}
            1 { Add-Content .\routerps1.txt "no service password-encrytpion `n!"}
        }

        Add-Content .\routerps1.txt "router rip `nversion 2"
        while ($Rip -notmatch "yes", "no")
        {
        $Rip = Read-Host -Prompt 'Do you want to set (another) network for rip, yes or no?'
            If ($Rip -eq "yes")
                { $network = Read-Host -Prompt 'Give the network address'
                Add-Content .\routerps1.txt "network $network"}
            If ($Rip -eq "no")
                { break }
        }

        while ($Static -notmatch "yes", "no")
        { 
        $Static = Read-Host -Prompt "Do you want to set (another) static route, yes or no?"
            If ($Static -eq "yes")
                { $StaticIP = Read-Host -Prompt "Enter the IP-address for the static route"
                  $StaticSub = Read-Host -Prompt "Enter the subnetmask for the static route"
                  $NextHop = Read-Host -Prompt "Enter the next-hop address or interface for the static route" 
                 Add-Content .\routerps1.txt "!`nip route $StaticIP $StaticSub $NextHop"}
            If ($Static -eq "no")
                { break } 
         }
       }
    }
