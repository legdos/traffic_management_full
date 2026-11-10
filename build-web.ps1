# 构建前端并把产物拷贝到后端 static 目录，实现「单进程」部署：
#   只启动 Spring Boot（8080），浏览器访问 http://localhost:8080 就是完整应用，
#   不再需要 5173 和 Vite 代理。
#
# 用法：
#   .\build-web.ps1

$ErrorActionPreference = 'Stop'

$root   = Split-Path -Parent $MyInvocation.MyCommand.Path
$fe     = Join-Path $root 'traffic_management_frontend\traffic-vue'
$static = Join-Path $root 'traffic_management_backend\src\main\resources\static'

Write-Host "==> 1/3 构建前端：$fe" -ForegroundColor Cyan
Push-Location $fe
try {
    npm run build
    if ($LASTEXITCODE -ne 0) {
        throw "npm run build 失败（exit $LASTEXITCODE）"
    }
} finally {
    Pop-Location
}

$dist = Join-Path $fe 'dist'
if (-not (Test-Path $dist)) {
    throw "没有找到构建产物：$dist"
}

Write-Host "==> 2/3 清理旧的 static 目录" -ForegroundColor Cyan
if (Test-Path $static) {
    Remove-Item $static -Recurse -Force
}
New-Item -ItemType Directory -Path $static -Force | Out-Null

Write-Host "==> 3/3 拷贝 dist -> static" -ForegroundColor Cyan
Copy-Item (Join-Path $dist '*') $static -Recurse -Force

$count = (Get-ChildItem $static -Recurse -File | Measure-Object).Count
Write-Host ""
Write-Host "完成：$count 个文件已复制到" -ForegroundColor Green
Write-Host "  $static"
Write-Host ""
Write-Host "下一步：启动后端，浏览器打开 http://localhost:8080" -ForegroundColor Green
Write-Host "提示：static 目录已在 .gitignore 中，不会提交到仓库。"
