pyinstaller --onedir ^
    --windowed ^
    --add-data "seeding_data:seeding_data" ^
    --name LMUStrategyTool ^
    --noconfirm ^
    main.py 