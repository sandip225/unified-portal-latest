# Unified Portal - Complete AWS EC2 Deployment Script (PowerShell)
# Installs Docker, Docker Compose, Git, and deploys the application

param(
    [Parameter(Mandatory=$true)]
    [string]$KeyPath,
    
    [Parameter(Mandatory=$true)]
    [string]$InstanceIP
)

# Color functions
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-ErrorMsg { Write-Host $args -ForegroundColor Red }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Info { Write-Host $args -ForegroundColor Cyan }

Write-Info "=========================================="
Write-Info "Unified Portal - Complete Deployment"
Write-Info "=========================================="

# Validate inputs
if (-not (Test-Path $KeyPath)) {
    Write-ErrorMsg "ERROR: Key file not found at: $KeyPath"
    exit 1
}

Write-Warning "Target Instance: $InstanceIP"
Write-Warning "Key File: $KeyPath"
Write-Warning "Repository: https://github.com/Vaidehip0407/unified-portal.git"
Write-Host ""

Write-Info "Connecting to EC2 instance and deploying..."
Write-Info ""

# Execute deployment commands via SSH
$commands = @(
    "sudo apt-get update",
    "sudo apt-get upgrade -y",
    "sudo apt-get install -y git docker.io",
    "sudo systemctl start docker",
    "sudo systemctl enable docker",
    "sudo usermod -aG docker ubuntu",
    "sudo curl -L 'https://github.com/docker/compose/releases/latest/download/docker-compose-'`$(uname -s)`'-'`$(uname -m)`'' -o /usr/local/bin/docker-compose",
    "sudo chmod +x /usr/local/bin/docker-compose",
    "cd /home/ubuntu && git clone https://github.com/Vaidehip0407/unified-portal.git 2>/dev/null || (cd unified-portal && git fetch origin && git reset --hard origin/main)",
    "cd /home/ubuntu/unified-portal && docker-compose down 2>/dev/null || true",
    "cd /home/ubuntu/unified-portal && docker-compose up -d",
    "sleep 5",
    "cd /home/ubuntu/unified-portal && docker-compose ps"
)

$fullCommand = $commands -join "; "

ssh -i "$KeyPath" ubuntu@"$InstanceIP" $fullCommand

Write-Success ""
Write-Success "=========================================="
Write-Success "Remote Deployment Successful!"
Write-Success "=========================================="
Write-Warning "Your application is now live at:"
Write-Info "  http://$InstanceIP"
Write-Host ""
Write-Warning "Next Steps:"
Write-Host "  1. Open http://$InstanceIP in your browser"
Write-Host "  2. Register a new account"
Write-Host "  3. Start using the portal"
Write-Host ""
Write-Warning "To view logs:"
Write-Host "  ssh -i $KeyPath ubuntu@$InstanceIP"
Write-Host "  cd unified-portal"
Write-Host "  docker-compose logs"
