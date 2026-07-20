@echo off

echo =========================
echo Обновление GitHub
echo =========================

git add .

git commit -m "bot update"

git push

echo =========================
echo Готово!
echo =========================

pause