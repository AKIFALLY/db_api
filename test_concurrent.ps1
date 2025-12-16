# ============================================
# Test FastAPI Concurrent Request Handling
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "FastAPI Concurrent Test" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Check if API server is running
Write-Host "[CHECK] Testing API server connection..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
    Write-Host "[OK] API server is running`n" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] API server is not running. Please start it first." -ForegroundColor Red
    Write-Host "Run: .\start_api_server.bat`n" -ForegroundColor Yellow
    exit 1
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Starting Concurrent Test" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Record test start time
$testStart = Get-Date
Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Test started`n" -ForegroundColor Cyan

# Start slow query (10 seconds, background job)
Write-Host "[Request 1] Sending slow query (10 seconds)..." -ForegroundColor Yellow
$job1 = Start-Job -ScriptBlock {
    $start = Get-Date
    $result = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/agv/test/slow-query?seconds=10" -Method Get
    $end = Get-Date
    $elapsed = ($end - $start).TotalSeconds
    return @{
        result = $result
        elapsed = $elapsed
        start_time = $start.ToString('HH:mm:ss.fff')
        end_time = $end.ToString('HH:mm:ss.fff')
    }
}

# Wait 0.5 seconds to ensure slow query has started
Start-Sleep -Milliseconds 500

# Send fast query
Write-Host "[Request 2] Sending fast query (health check)..." -ForegroundColor Yellow
$request2Start = Get-Date
try {
    $result2 = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
    $request2End = Get-Date
    $elapsed2 = ($request2End - $request2Start).TotalSeconds

    Write-Host "`n[SUCCESS] Fast query returned immediately!" -ForegroundColor Green
    Write-Host "  Start: $($request2Start.ToString('HH:mm:ss.fff'))"
    Write-Host "  End: $($request2End.ToString('HH:mm:ss.fff'))"
    Write-Host "  Elapsed: $([math]::Round($elapsed2, 3)) seconds" -ForegroundColor Green
    Write-Host "  Response: $($result2.status)`n"
} catch {
    Write-Host "`n[FAILED] Fast query failed: $_`n" -ForegroundColor Red
    exit 1
}

# Wait for slow query to complete
Write-Host "[WAIT] Waiting for slow query to complete..." -ForegroundColor Yellow
$job1Result = Receive-Job -Job $job1 -Wait
Remove-Job -Job $job1

Write-Host "`n[SUCCESS] Slow query completed!" -ForegroundColor Green
Write-Host "  Start: $($job1Result.start_time)"
Write-Host "  End: $($job1Result.end_time)"
Write-Host "  Elapsed: $([math]::Round($job1Result.elapsed, 3)) seconds" -ForegroundColor Green

$testEnd = Get-Date
$totalElapsed = ($testEnd - $testStart).TotalSeconds

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "Test Result" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

if ($elapsed2 -lt 2) {
    Write-Host "`n[PASS] FastAPI can handle other requests during slow query execution!" -ForegroundColor Green
    Write-Host "  - Slow query time: $([math]::Round($job1Result.elapsed, 2)) seconds" -ForegroundColor White
    Write-Host "  - Fast query time: $([math]::Round($elapsed2, 2)) seconds (completed during slow query)" -ForegroundColor White
    Write-Host "  - Total test time: $([math]::Round($totalElapsed, 2)) seconds`n" -ForegroundColor White
    Write-Host "Explanation: FastAPI uses threadpool mechanism. Each request runs in a separate thread," -ForegroundColor Cyan
    Write-Host "             so they do not block each other. Default threadpool has ~40 threads.`n" -ForegroundColor Cyan
} else {
    Write-Host "`n[WARNING] Fast query was also slow. Server may be overloaded.`n" -ForegroundColor Yellow
}

Write-Host "============================================`n" -ForegroundColor Cyan
