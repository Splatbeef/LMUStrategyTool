rmdir /s /q build

pyinstaller --onedir ^
    --windowed ^
    --add-data "seeding_data;seeding_data" ^
    --icon "assets/icon_windows.ico" ^
    --name LMUStrategyTool ^
    --noconfirm ^
    main.py 