@echo off
echo Limpiando carpetas duplicadas...

REM Esperar un momento para que los procesos se liberen
timeout /t 5 /nobreak

REM Intentar eliminar la carpeta duplicada
rmdir /s /q "public\public" 2>nul

if exist "public\public" (
    echo No se pudo eliminar public\public - puede estar en uso
    echo Intenta cerrar cualquier aplicación que pueda estar usando estos archivos
) else (
    echo Carpeta public\public eliminada correctamente
)

echo Limpieza completada
pause 