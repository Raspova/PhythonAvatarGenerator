from py_avataaars import AvatarMaker as am , AvatarInfo 
import py_avataaars as  pa 


if __name__ == '__main__':       
    avatars = am.create_n_random_avatar_safe(25)
    for i, (avatar_svg, avatar_info) in enumerate(avatars):
        str_av = avatar_info.json()
        print(str_av)
        #with open(f'{i}-{avatar_info.info_str_short()}', 'w') as f:
        #        f.write(avatar_svg)
    print(am.get_all_enum_values())
    custom_avatar_info = AvatarInfo(
    top_type=pa.TopType.LONG_HAIR_DREADS,
    hair_color=pa.HairColor.BROWN_DARK,
    eye_type=pa.EyesType.WINK,
    eyebrow_type=pa.EyebrowType.DEFAULT,
    mouth_type=pa.MouthType.SMILE,
    )
    custom_avatar_info.facial_hair_type = pa.FacialHairType.BEARD_MAJESTIC
    custom_avatar_svg = am.create_avatar_from_info(custom_avatar_info)
    with open('custom_avatar.svg', 'w') as f:
        f.write(custom_avatar_svg)