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
    print(avatar_info.make_id()) # can use this id to remake avatar , ligther to save in db

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
    top_type=pa.TopType.LONG_HAIR_DREADS,
    hair_color=pa.HairColor.BROWN_DARK,
    eye_type=pa.EyesType.WINK,
    eyebrow_type=pa.EyebrowType.DEFAULT,
    mouth_type=pa.MouthType.SMILE,
)

custom_avatar_svg = am.create_avatar_from_info(custom_avatar_info)
```
![SVG Image](custom_avatar.svg)

## Examples SAFE Avatar
Here's some example of "safe" avatars : 

![SVG Image](/example/0.svg)
![SVG Image](example/1.svg)
![SVG Image](example/2.svg)
![SVG Image](example/3.svg)
![SVG Image](example/4.svg)
![SVG Image](example/5.svg)
![SVG Image](example/6.svg)
![SVG Image](example/7.svg)
![SVG Image](example/8.svg)
![SVG Image](example/9.svg)
![SVG Image](example/10.svg)
![SVG Image](example/11.svg)


## Examples Avatar
Here's some example of "unsafe" avatars , true randomnesse:


![SVG Image](example/12.svg)
![SVG Image](example/13.svg)
![SVG Image](example/14.svg)
![SVG Image](example/15.svg)
![SVG Image](example/16.svg)
![SVG Image](example/17.svg)
![SVG Image](example/18.svg)
![SVG Image](example/19.svg)
![SVG Image](example/20.svg)
![SVG Image](example/21.svg)
![SVG Image](example/22.svg)
![SVG Image](example/23.svg)