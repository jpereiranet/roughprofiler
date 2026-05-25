# Executable Parameter Audit

This document describes the command arguments that RoughProfiler builds for ArgyllCMS and DCamProf from the GUI state.

The command arrays are built in `home.py` and executed with `subprocess.Popen(..., shell=False)`. Empty arguments are removed before execution with `list(filter(None, cmd))`.

## Configuration Sources

Executable folders:

- `configuration.ini` `[APPS] argyll`: folder containing `scanin`, `colprof`, and `profcheck`.
- `configuration.ini` `[APPS] dcamprof`: folder containing `dcamprof`.

Target files:

- `Target type` selects an entry from `[PARAMS] targets`.
- Target entry format: `[CGATS reference, recognition CHT, DCamProf target JSON]`.
- The CHT and bundled CGATS/JSON files are resolved inside the `reference/` folder.
- If a target has no bundled CGATS reference, the user must load an external CGATS file.

Temporary outputs:

- `ti3`: `<image_folder>/<image_basename>/<image_basename>.ti3`
- diagnostics TIFF: `<image_folder>/<image_basename>/<image_basename>_diag.tiff`
- DCP intermediate JSON: `<image_folder>/<image_basename>/<image_basename>.json`
- ICC/DCP output: `<image_folder>/<image_basename>/<FileNameText>`

## ArgyllCMS `scanin`

`scanin` is executed by the `Read Image` button after an image, target recognition file, CGATS reference, and ROI coordinates are available.

Command shape:

```python
[
    "<ARGYLL_PATH>/scanin",
    "-v2",
    "-p",
    diagnostics,
    gamma,
    "-F",
    coordinates,
    "-O",
    ti3_path,
    input_image,
    recognition_cht,
    reference_cgats,
    diagnostics_tiff,
]
```

Parameter mapping:

| Argument | Source | Meaning |
| --- | --- | --- |
| `-v2` | Fixed in code | Verbose output level. |
| `-p` | Fixed in code | Enables positioning/diagnostic behavior for scanin. |
| `diagnostics` | `[SCANIN] diagnostics`, currently `-dipn` | ArgyllCMS diagnostic flags. |
| `gamma` | `-G1.0` for RAW workflow, otherwise `-G` + `[SCANIN] gamma` | Input image gamma used by `scanin`. |
| `-F` | Fixed in code | Passes explicit chart corner coordinates. |
| `coordinates` | ROI corners from the image viewer | Comma-separated ROI coordinates, rounded to 2 decimals. |
| `-O` | Fixed in code | Output `.ti3` option. |
| `ti3_path` | Temporary output path | Measurement data produced by `scanin`. |
| `input_image` | Loaded image path | For RAW files, this becomes the generated linear TIFF. |
| `recognition_cht` | Target type CHT file | Argyll chart recognition file. |
| `reference_cgats` | Bundled target CGATS or user-loaded CGATS | Colorimetric reference data. |
| `diagnostics_tiff` | Temporary output path | Diagnostic image produced by `scanin`. |

RAW note:

- RAW files are first processed through `rawpy`.
- The image used for `scanin` is `lineal_<image_basename>.tiff`.
- RAW scanin gamma is forced to `-G1.0`.

## ArgyllCMS `colprof`

`colprof` is executed by `Create Profile` when the ICC tab is active.

Base command shape:

```python
[
    "<ARGYLL_PATH>/colprof",
    "-v",
    "-a",
    argyll_algorithm,
    "-O",
    output_icc_path,
    "-A",
    manufacturer,
    "-M",
    model,
    "-D",
    description,
    "-C",
    copyright,
    ti3_path_without_extension,
]
```

Parameter mapping:

| Argument | Source | Meaning |
| --- | --- | --- |
| `-v` | Fixed in code | Verbose output. |
| `-a argyll_algorithm` | `Profile Type` selector | ICC profile algorithm. |
| `-O output_icc_path` | `Filename` field and temp folder | Output ICC profile path. |
| `-A manufacturer` | `Manufacturer` field | ICC device manufacturer text. |
| `-M model` | `Device` field | ICC device model text. |
| `-D description` | `Description` field | ICC profile description. |
| `-C copyright` | `Copyright` field | ICC copyright metadata. |
| `ti3_path_without_extension` | `.ti3` path without extension | Input base path for `colprof`. |

Fallback values:

- Empty manufacturer becomes `Unknow`.
- Empty model becomes `Unknow`.
- Empty description becomes `None`.
- Empty copyright becomes `RoughProfiler By JPereira`.

Profile type mapping from `[PARAMS] argyllalgoritm`:

| GUI value | Argument value |
| --- | --- |
| `Lab cLUT` | `l` |
| `XYZ cLUT` | `x` |
| `Gamma+matrix` | `g` |
| `Shaper+matrix` | `s` |
| `Matrix only` | `m` |
| `Single gamma+matrix` | `G` |
| `Single shaper+matrix` | `S` |

Optional arguments:

| GUI option | Argument | Condition |
| --- | --- | --- |
| `Remove B2A Table` | `-bn` | Added when checked. |
| `WP Scale` | `-uc`, `-u`, `-ua`, empty, or custom `-U<n>` | Added only for `Lab cLUT` and `XYZ cLUT`. |
| `cLUT grid emphasis` slider | `-V<n>` | Added only for `Lab cLUT` and `XYZ cLUT`. |
| `Profile Resolution` | `-q<value>` | Added only for `Lab cLUT` and `XYZ cLUT`. |

Profile resolution mapping from `[PARAMS] argyllres`:

| GUI value | Argument value |
| --- | --- |
| `Low` | `-ql` |
| `Medium` | `-qm` |
| `High` | `-qh` |
| `Ultra` | `-qu` |

White point scale mapping from `[PARAMS] argylluparam`:

| GUI value | Argument value |
| --- | --- |
| `clip cLUT values` | `-uc` |
| `Auto scale WP` | `-u` |
| `Force Absolute` | `-ua` |
| `None` | empty argument, removed before execution |
| `Custom` | `-U` + slider value |

Current argument-order note:

- When `Remove B2A Table` is checked and the algorithm is `Lab cLUT` or `XYZ cLUT`, the command order is:

```python
[
    "colprof", "-v", "-a", algorithm,
    "-bn", wp_scale, emphasis, quality,
    "-O", output_icc_path,
    "-A", manufacturer,
    "-M", model,
    "-D", description,
    "-C", copyright,
    ti3_path_without_extension,
]
```

- When `Remove B2A Table` is not checked and the algorithm is `Lab cLUT` or `XYZ cLUT`, the current code inserts `wp_scale`, `emphasis`, and `quality` immediately after `-O`, before the output path. This reflects the current implementation in `home.py`.

Example observed command:

```python
[
    "C:/ArgyllCMS/bin/colprof",
    "-v",
    "-a",
    "l",
    "-bn",
    "-uc",
    "-V1.0",
    "-ql",
    "-O",
    "H:/CURSOS/CURSO_ACAL/EXPERIMENTAL2/color/DSC_4531/NIKON_D610_001.icc",
    "-A",
    "NIKON CORPORATION",
    "-M",
    "NIKON D610",
    "-D",
    "NIKON D610  001",
    "-C",
    "jpereira.net2",
    "H:/CURSOS/CURSO_ACAL/EXPERIMENTAL2/color/DSC_4531/DSC_4531",
]
```

## ArgyllCMS `profcheck`

`profcheck` is executed automatically after a successful ICC profile creation.

Command shape:

```python
[
    "<ARGYLL_PATH>/profcheck",
    "-v2",
    "-Ir",
    ti3_path,
    output_icc_path,
]
```

Parameter mapping:

| Argument | Source | Meaning |
| --- | --- | --- |
| `-v2` | Fixed in code | Verbose output level. |
| `-Ir` | Fixed in code | Profile check mode used by the GUI. |
| `ti3_path` | Generated `.ti3` file | Measurement data. |
| `output_icc_path` | Generated ICC profile | Profile to evaluate. |

The output is parsed to populate the Delta-E charts in the GUI.

## DCamProf `make-profile`

`dcamprof make-profile` is executed by `Create Profile` when the DCP tab is active.

Base command shape:

```python
[
    "<DCAMPROF_PATH>/dcamprof",
    "make-profile",
    "-i",
    illuminant,
    "-y",
    y_limit,
    ti3_path,
    json_profile_path,
]
```

Parameter mapping:

| Argument | Source | Meaning |
| --- | --- | --- |
| `make-profile` | Fixed in code | DCamProf command. |
| `-i illuminant` | `Illuminant` selector | Illuminant used for the profile. |
| `-y y_limit` | `Y Limit` field | DCamProf Y limit. Invalid values are replaced with `-0.2`. |
| `ti3_path` | Generated `.ti3` file | Measurement data from `scanin`. |
| `json_profile_path` | Temporary JSON path | Intermediate DCamProf profile. |

Optional arguments:

| GUI option | Argument | Condition |
| --- | --- | --- |
| `Glare Compensation` | `-g <target_json>` | Added when checked and the selected target has a bundled JSON profile. |
| `Patch Tuning file` | `-a <tuning_json>` | Added when a valid tuning file path is loaded. |

When both optional arguments are enabled, the current code order is:

```python
[
    "dcamprof",
    "make-profile",
    "-a",
    tuning_json,
    "-g",
    target_json,
    "-i",
    illuminant,
    "-y",
    y_limit,
    ti3_path,
    json_profile_path,
]
```

Illuminant values are loaded from `[PARAMS] exifilluminant`, for example:

| GUI value | Argument value |
| --- | --- |
| `D50 (5000K)` | `D50` |
| `D55 (5500K)` | `D55` |
| `D65 (6500K)` | `D65` |
| `StdA (2850K)` | `StdA` |
| `Flash (5500K)` | `Flash` |
| `Shade (7500K)` | `Shade` |

## DCamProf `make-dcp`

`dcamprof make-dcp` is executed after `make-profile` succeeds and creates the intermediate JSON file.

Base command shape:

```python
[
    "<DCAMPROF_PATH>/dcamprof",
    "make-dcp",
    "-n",
    model,
    "-d",
    description,
    "-b",
    exposure_offset,
    json_profile_path,
    output_dcp_path,
]
```

Parameter mapping:

| Argument | Source | Meaning |
| --- | --- | --- |
| `make-dcp` | Fixed in code | DCamProf command. |
| `-n model` | `Device` field | Camera/model name embedded in the DCP. |
| `-d description` | `Description` field | DCP profile description. |
| `-b exposure_offset` | `Exposure Offset` slider value | Exposure baseline compensation. |
| `json_profile_path` | Output from `make-profile` | Intermediate DCamProf profile. |
| `output_dcp_path` | `Filename` field and temp folder | Final DCP profile path. |

Optional tone curve arguments:

| GUI value | Argument |
| --- | --- |
| `None` | No `-t` argument. |
| `Linear` | `-t linear`; no tone operator is added. |
| `ACR` | `-t acr`, plus `-o <tone_operator>`. |
| `Custom` | `-t reference/curve23.rtc`, plus `-o <tone_operator>`. |

Tone operator mapping from `[PARAMS] dcamproftoneoperator`:

| GUI value | Argument value |
| --- | --- |
| `Standard` | `standard` |
| `Neutral` | `neutral` |
| `Custom1` | `reference/neutral-plus.json` |
| `Custom2` | `reference/ntro_lookop_conf.json` |

With a non-`None`, non-`Linear` tone curve, the current command order is:

```python
[
    "dcamprof",
    "make-dcp",
    "-t",
    tone_curve,
    "-o",
    tone_operator,
    "-n",
    model,
    "-d",
    description,
    "-b",
    exposure_offset,
    json_profile_path,
    output_dcp_path,
]
```

## Target Type Effects

The selected target type affects:

- `scanin` recognition file: second value in the target entry, usually a `.cht`.
- `scanin` reference file: first value in the target entry, usually a `.cie`, unless replaced by a user-loaded CGATS file.
- DCamProf glare compensation profile: third value in the target entry, if present and if `Glare Compensation` is checked.

Current configured targets:

| Target type | CGATS reference | Recognition CHT | DCamProf JSON |
| --- | --- | --- | --- |
| `Colorchecker Classic` | `cc24_ref-new.cie` | `ColorChecker.cht` | `cc24-layout.json` |
| `Colorchecker SG` | `ccsg_ref-new.cie` | `ColorCheckerSG.cht` | `ccsg-layout.json` |
| `Colorchecker Passport` | `ColorCheckerPassport.cie` | `ColorCheckerPassport.cht` | empty |
| `Colorchecker DC` | external CGATS required | `ColorCheckerDC.cht` | empty |
| `IT8` | external CGATS required | `it8.cht` | empty |
| `LaserSoftDCPro` | external CGATS required | `LaserSoftDCPro.cht` | empty |
| `QPcard 201` | `QPcard_201.cie` | `QPcard_201.cht` | empty |
| `QPcard 202` | `QPcard_202.cie` | `QPcard_202.cht` | empty |
| `SpyderChecker` | `SpyderChecker.cie` | `SpyderChecker.cht` | empty |
| `SpyderChecker24` | `SpyderChecker24.cie` | `SpyderChecker24.cht` | empty |

## Workflow Summary

ICC workflow for TIFF/JPEG/PNG:

1. `scanin` reads the target image and creates `.ti3`.
2. `colprof` creates the ICC profile from `.ti3`.
3. `profcheck` evaluates the ICC profile and fills the GUI Delta-E charts.

DCP workflow for RAW files:

1. RAW image is developed internally to a linear TIFF.
2. `scanin` reads the linear TIFF and creates `.ti3`.
3. `dcamprof make-profile` creates an intermediate JSON profile.
4. `dcamprof make-dcp` creates the final DCP profile.

