rmdir /s /q build

pyinstaller --onedir ^
    --windowed ^
    --add-data "seeding_data;seeding_data" ^
    --icon "icon.ico" ^
    --name LMUStrategyTool ^
    --noconfirm ^
    main.py 