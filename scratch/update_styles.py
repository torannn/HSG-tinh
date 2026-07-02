import json
from pathlib import Path

config_path = Path(__file__).resolve().parent.parent / "styles_config.json"
if config_path.exists():
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    new_defaults = {
        "correct_tf_shape": "rectangle",
        "tf_dapan": "a",
        "tf_sep": ")",
        "tf_addanswers": True,
        "tf_addquestions": False,
        "prevent_overflow_ansbox": True,
        "correct_sa_shape": "rectangle",
        "sa_dapan": "a",
        "sa_height": 0.9,
        "auto_wrap_anstab": True
    }
    
    for theme_name, theme_data in data.items():
        for k, v in new_defaults.items():
            if k not in theme_data:
                theme_data[k] = v
                
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("styles_config.json updated successfully!")
else:
    print("styles_config.json not found!")
