# First, let me check which pages already have schema markup
Get-ChildItem -Recurse "C:\Users\csdm2\Documents\chinahospitalsguide.com\src" -Filter "*.html" | ForEach-Object {
    $content = Get-Content $_.FullName -Encoding UTF8 -Raw
    if ($content -match 'application/ld\+json') {
        Write-Host "HAS SCHEMA: $($_.Name)"
    }
} | Select-Object -First 20
