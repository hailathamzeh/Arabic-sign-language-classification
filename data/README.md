# Dataset location

Dataset files are not stored in this repository.

Download the [Arabic Alphabets Sign Language Dataset (ArASL)](https://data.mendeley.com/datasets/y7pckrw6z2/1), then place the required files here:

```text
data/raw/
├── ArASL_Database_54K_Final/
│   └── <32 class folders containing the images>
└── ArSL_Data_Labels.csv
```

Required Mendeley downloads:

- `ArASL_Database_54K_Final.zip`, extract this archive under `data/raw/`
- `ArSL_Data_Labels.csv`, place this file directly under `data/raw/`

If extracting the ZIP creates an extra nested directory, move the inner `ArASL_Database_54K_Final` folder so its path exactly matches the structure above.

To use another location, set the `ARASL_DATA_DIR` environment variable to the directory containing `ArASL_Database_54K_Final/` and `ArSL_Data_Labels.csv`.
