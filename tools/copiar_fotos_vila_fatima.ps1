# Copia os 12 anexos do Cursor para static/img/imoveis/vila-de-fatima/ como 01.png ... 12.png
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$dest = Join-Path $root "static\img\imoveis\vila-de-fatima"
$srcDir = Join-Path $env:USERPROFILE ".cursor\projects\c-Desenvolvedor-full-stack-Corretor-Imobiliario\assets"

$map = @(
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.40__1_-422e31f8-9d4b-428d-a11d-fc83b5fcd7c4.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.43-17969d2d-db87-4eae-93ff-70ffd4adaf4c.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.42__1_-0076207a-3c10-423d-a45d-e7d05313a14f.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.42__3_-528f9110-d925-499d-95a0-dad28dc87d6f.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.42__2_-6e3f3172-0d79-4663-b467-cb9889939d94.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.41__2_-e4a99e42-ef78-447e-bdc0-a306ca1e9bcc.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.41__1_-b7a4d275-d171-4f6a-8005-194c11ef0b3a.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.40__2_-4447f758-c652-42d9-95f7-42eaf8324eb9.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.42-e0b09a3f-ce2b-4e44-b47c-d79a006e42c8.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.43__1_-b972c7d7-5b1e-4e88-b90f-ae9ed484c070.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.40-93e1bf03-1675-4777-a6a5-d70a313b7dbc.png",
  "c__Users_diego_AppData_Roaming_Cursor_User_workspaceStorage_efb4aad1fbdecb8b1c43e96ef8cd7fa1_images_WhatsApp_Image_2026-03-30_at_16.37.41-f49173b0-5167-4d43-83c0-a97abdddb391.png"
)

if (-not (Test-Path -LiteralPath $srcDir)) {
  Write-Host "Pasta do Cursor nao encontrada: $srcDir"
  Write-Host "Use: python tools/importar_fotos_vila_fatima.py"
  Write-Host "Ou coloque 01.png ... 12.png em assets_import/vila-fatima/ e rode o mesmo script."
  exit 1
}

New-Item -ItemType Directory -Force -Path $dest | Out-Null
for ($i = 0; $i -lt $map.Length; $i++) {
  $from = Join-Path $srcDir $map[$i]
  $name = "{0:D2}.png" -f ($i + 1)
  $to = Join-Path $dest $name
  if (-not (Test-Path -LiteralPath $from)) {
    Write-Error "Arquivo nao encontrado: $from"
  }
  Copy-Item -LiteralPath $from -Destination $to -Force
}
Write-Host "OK: fotos copiadas para $dest"
