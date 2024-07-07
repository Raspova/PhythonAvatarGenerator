 # AvatarMaker

AvatarMaker is a Python library for generating customizable avatars. It's based on the py-avataaars project and provides an easy way to create both random and specific avatars.

## Installation

To install AvatarMaker, you can use pip:


```shell
pip3 -r requirements.txt
```

## Usage

Here's how to use the AvatarMaker:

### Importing the AvatarMaker

```python
from py_avataaars import AvatarMaker as am
```
### Creating a Single Random Avatar and "Safe" Random Avatar
This returns a tuple containing the SVG string of the avatar and an AvatarInfo object with the avatar's attributes.\n
Safe avatar are better suited for proffesionel use.

```python
avatar_svg, avatar_info = am.create_random_avatar()
avatar_svg, avatar_info = am.create_random_avatar_safe()

```
### Creating Multiple Random Avatars
This returns a list of 25 tuples, each containing an SVG string and an AvatarInfo object.

```python
avatars = am.create_n_random_avatar_safe(25)
```

### Avatar info

```python
for avatar_svg, avatar_info in avatars:
    print(avatar_info.json())
    print(avatar_info.info_str())  # Detailed info
    print(avatar_info.info_str_short())  # Short info

all_enum_values = am.get_all_enum_values()
print(all_enum_values)
```

This saves each avatar as an SVG file.

```python
for i, (avatar_svg, avatar_info) in enumerate(avatars):
    with open(f'{i}-{avatar_info.info_str_short()}', 'w') as f:
            f.write(avatar_svg)
```


## Customization

You can create a custom avatar by specifying values for each attribute:

```python
from py_avataaars import AvatarMaker as am
from py_avataaars import AvatarInfo
import py_avataaars as pa

custom_avatar_info = AvatarInfo(
    style=pa.AvatarStyle.CIRCLE,
    top_type=pa.TopType.SHORT_HAIR_SHORT_FLAT,
    hair_color=pa.HairColor.BROWN,
    eye_type=pa.EyesType.DEFAULT,
    eyebrow_type=pa.EyebrowType.DEFAULT,
    mouth_type=pa.MouthType.SMILE,
    skin_color=pa.SkinColor.LIGHT,
    # ... other attributes ...
)

custom_avatar_svg = am.create_avatar_from_info(custom_avatar_info)
```
