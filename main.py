from PhythonAvatarGenerator import AvatarMaker as am , AvatarInfo 
import PhythonAvatarGenerator as  pa 


if __name__ == '__main__':       
    avatars = am.create_n_random_avatar_safe(25)
    for i, (avatar_svg, avatar_info) in enumerate(avatars):
        id = avatar_info.make_id()
        str_av = avatar_info.info_str_short()
        print(str_av , "->" , id)
        with open(f'{i}-{avatar_info.info_str_short()}.svg', 'w') as f:
                f.write(avatar_svg)
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
    _id = custom_avatar_info.make_id()   
    print(custom_avatar_info.info_str_short() , "->" , _id)
    copy_avatar =  am.create_avatar_from_info_id(_id)
    with open('copy_avatar.svg', 'w') as f:
        f.write(copy_avatar)