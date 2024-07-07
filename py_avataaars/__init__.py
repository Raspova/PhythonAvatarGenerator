import enum
import pathlib
import re
import uuid
from collections import Counter
from io import BytesIO
import random
from typing import List, Optional, Union, Any, Tuple
from pydantic import BaseModel, validator
from cairosvg import svg2png
from jinja2 import Environment, PackageLoader
from jinja2.ext import Extension
from jinja2.lexer import Token


class AvatarEnum(enum.Enum):

    def __new__(cls, *args: Any, **kwargs: Any) -> 'AvatarEnum':
        value = len(cls.__members__)
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, main_value: str) -> None:
        self.main_value: str = main_value

    def __str__(self) -> str:
        return self.name.lower().title()


class AvatarStyle(AvatarEnum):
    TRANSPARENT = 'TRANSPARENT'
    CIRCLE = 'CIRCLE'


class SkinColor(AvatarEnum):
    BLACK = '#614335'
    TANNED = '#FD9841'
    YELLOW = '#F8D25C'
    PALE = '#FFDBB4'
    LIGHT = '#EDB98A'
    BROWN = '#D08B5B'
    DARK_BROWN = '#AE5D29'


class HairColor(AvatarEnum):
    BLACK = '#2C1B18'
    AUBURN = '#A55728'
    BLONDE = '#B58143'
    BLONDE_GOLDEN = '#D6B370'
    BROWN = '#724133'
    BROWN_DARK = '#4A312C'
    PASTEL_PINK = '#F59797'
    PLATINUM = '#ECDCBF'
    RED = '#C93305'
    SILVER_GRAY = '#E8E1E1'


class ManType(AvatarEnum):
    NO_HAIR = 'NO_HAIR'
    EYE_PATCH = 'EYE_PATCH'
    HAT = 'HAT'
    TURBAN = 'TURBAN'
    WINTER_HAT1 = 'WINTER_HAT1'
    WINTER_HAT2 = 'WINTER_HAT2'
    SHORT_HAIR_DREADS_01 = 'SHORT_HAIR_DREADS_01'
    SHORT_HAIR_DREADS_02 = 'SHORT_HAIR_DREADS_02'
    SHORT_HAIR_FRIZZLE = 'SHORT_HAIR_FRIZZLE'
    SHORT_HAIR_SHAGGY_MULLET = 'SHORT_HAIR_SHAGGY_MULLET'
    SHORT_HAIR_SHORT_FLAT = 'SHORT_HAIR_SHORT_FLAT'
    SHORT_HAIR_SHORT_ROUND = 'SHORT_HAIR_SHORT_ROUND'
    SHORT_HAIR_SHORT_WAVED = 'SHORT_HAIR_SHORT_WAVED'
    SHORT_HAIR_SIDES = 'SHORT_HAIR_SIDES'
    SHORT_HAIR_THE_CAESAR = 'SHORT_HAIR_THE_CAESAR'
    SHORT_HAIR_THE_CAESAR_SIDE_PART = 'SHORT_HAIR_THE_CAESAR_SIDE_PART'


class WomanType(AvatarEnum):
    SHORT_HAIR_SHORT_CURLY = 'SHORT_HAIR_SHORT_CURLY'
    WINTER_HAT3 = 'WINTER_HAT3'
    WINTER_HAT4 = 'WINTER_HAT4'
    HIJAB = 'HIJAB'
    LONG_HAIR_BIG_HAIR = 'LONG_HAIR_BIG_HAIR'
    LONG_HAIR_BOB = 'LONG_HAIR_BOB'
    LONG_HAIR_BUN = 'LONG_HAIR_BUN'
    LONG_HAIR_CURLY = 'LONG_HAIR_CURLY'
    LONG_HAIR_CURVY = 'LONG_HAIR_CURVY'
    LONG_HAIR_DREADS = 'LONG_HAIR_DREADS'
    LONG_HAIR_FRIDA = 'LONG_HAIR_FRIDA'
    LONG_HAIR_FRO = 'LONG_HAIR_FRO'
    LONG_HAIR_FRO_BAND = 'LONG_HAIR_FRO_BAND'
    LONG_HAIR_NOT_TOO_LONG = 'LONG_HAIR_NOT_TOO_LONG'
    LONG_HAIR_MIA_WALLACE = 'LONG_HAIR_MIA_WALLACE'
    LONG_HAIR_SHAVED_SIDES = 'LONG_HAIR_SHAVED_SIDES'
    LONG_HAIR_STRAIGHT = 'LONG_HAIR_STRAIGHT'
    LONG_HAIR_STRAIGHT2 = 'LONG_HAIR_STRAIGHT2'
    LONG_HAIR_STRAIGHT_STRAND = 'LONG_HAIR_STRAIGHT_STRAND'

class TopType(AvatarEnum):
    NO_HAIR = 'NO_HAIR'
    EYE_PATCH = 'EYE_PATCH'
    HAT = 'HAT'
    HIJAB = 'HIJAB'
    TURBAN = 'TURBAN'
    WINTER_HAT1 = 'WINTER_HAT1'
    WINTER_HAT2 = 'WINTER_HAT2'
    WINTER_HAT3 = 'WINTER_HAT3'
    WINTER_HAT4 = 'WINTER_HAT4'
    LONG_HAIR_BIG_HAIR = 'LONG_HAIR_BIG_HAIR'
    LONG_HAIR_BOB = 'LONG_HAIR_BOB'
    LONG_HAIR_BUN = 'LONG_HAIR_BUN'
    LONG_HAIR_CURLY = 'LONG_HAIR_CURLY'
    LONG_HAIR_CURVY = 'LONG_HAIR_CURVY'
    LONG_HAIR_DREADS = 'LONG_HAIR_DREADS'
    LONG_HAIR_FRIDA = 'LONG_HAIR_FRIDA'
    LONG_HAIR_FRO = 'LONG_HAIR_FRO'
    LONG_HAIR_FRO_BAND = 'LONG_HAIR_FRO_BAND'
    LONG_HAIR_NOT_TOO_LONG = 'LONG_HAIR_NOT_TOO_LONG'
    LONG_HAIR_MIA_WALLACE = 'LONG_HAIR_MIA_WALLACE'
    LONG_HAIR_SHAVED_SIDES = 'LONG_HAIR_SHAVED_SIDES'
    LONG_HAIR_STRAIGHT = 'LONG_HAIR_STRAIGHT'
    LONG_HAIR_STRAIGHT2 = 'LONG_HAIR_STRAIGHT2'
    LONG_HAIR_STRAIGHT_STRAND = 'LONG_HAIR_STRAIGHT_STRAND'
    SHORT_HAIR_DREADS_01 = 'SHORT_HAIR_DREADS_01'
    SHORT_HAIR_DREADS_02 = 'SHORT_HAIR_DREADS_02'
    SHORT_HAIR_FRIZZLE = 'SHORT_HAIR_FRIZZLE'
    SHORT_HAIR_SHAGGY_MULLET = 'SHORT_HAIR_SHAGGY_MULLET'
    SHORT_HAIR_SHORT_CURLY = 'SHORT_HAIR_SHORT_CURLY'
    SHORT_HAIR_SHORT_FLAT = 'SHORT_HAIR_SHORT_FLAT'
    SHORT_HAIR_SHORT_ROUND = 'SHORT_HAIR_SHORT_ROUND'
    SHORT_HAIR_SHORT_WAVED = 'SHORT_HAIR_SHORT_WAVED'
    SHORT_HAIR_SIDES = 'SHORT_HAIR_SIDES'
    SHORT_HAIR_THE_CAESAR = 'SHORT_HAIR_THE_CAESAR'
    SHORT_HAIR_THE_CAESAR_SIDE_PART = 'SHORT_HAIR_THE_CAESAR_SIDE_PART'


class FacialHairType(AvatarEnum):
    DEFAULT = 'DEFAULT'
    BEARD_MEDIUM = 'BEARD_MEDIUM'
    BEARD_LIGHT = 'BEARD_LIGHT'
    BEARD_MAJESTIC = 'BEARD_MAJESTIC'
    MOUSTACHE_FANCY = 'MOUSTACHE_FANCY'
    MOUSTACHE_MAGNUM = 'MOUSTACHE_MAGNUM'


class ClotheType(AvatarEnum):
    BLAZER_SHIRT = 'BLAZER_SHIRT'
    BLAZER_SWEATER = 'BLAZER_SWEATER'
    COLLAR_SWEATER = 'COLLAR_SWEATER'
    GRAPHIC_SHIRT = 'GRAPHIC_SHIRT'
    HOODIE = 'HOODIE'
    OVERALL = 'OVERALL'
    SHIRT_CREW_NECK = 'SHIRT_CREW_NECK'
    SHIRT_SCOOP_NECK = 'SHIRT_SCOOP_NECK'
    SHIRT_V_NECK = 'SHIRT_V_NECK'


class ClotheGraphicType(AvatarEnum):
    BAT = 'BAT'
    CUMBIA = 'CUMBIA'
    DEER = 'DEER'
    DIAMOND = 'DIAMOND'
    HOLA = 'HOLA'
    PIZZA = 'PIZZA'
    RESIST = 'RESIST'
    SELENA = 'SELENA'
    BEAR = 'BEAR'
    SKULL_OUTLINE = 'SKULL_OUTLINE'
    SKULL = 'SKULL'


class Color(AvatarEnum):
    BLACK = '#262E33'
    BLUE_01 = '#65C9FF'
    BLUE_02 = '#5199E4'
    BLUE_03 = '#25557C'
    GRAY_01 = '#E6E6E6'
    GRAY_02 = '#929598'
    HEATHER = '#3C4F5C'
    PASTEL_BLUE = '#B1E2FF'
    PASTEL_GREEN = '#A7FFC4'
    PASTEL_ORANGE = '#FFDEB5'
    PASTEL_RED = '#FFAFB9'
    PASTEL_YELLOW = '#FFFFB1'
    PINK = '#FF488E'
    RED = '#FF5C5C'
    WHITE = '#FFFFFF'


class SafeMouthType(AvatarEnum):
    DEFAULT = 'DEFAULT'
    SERIOUS = 'SERIOUS'
    SMILE = 'SMILE'


class MouthType(AvatarEnum):
    DEFAULT = 'DEFAULT'
    CONCERNED = 'CONCERNED'
    DISBELIEF = 'DISBELIEF'
    EATING = 'EATING'
    GRIMACE = 'GRIMACE'
    SAD = 'SAD'
    SCREAM_OPEN = 'SCREAM_OPEN'
    SERIOUS = 'SERIOUS'
    SMILE = 'SMILE'
    TONGUE = 'TONGUE'
    TWINKLE = 'TWINKLE'
    VOMIT = 'VOMIT'


class NoseType(AvatarEnum):
    DEFAULT = 'DEFAULT'


class SafeEyesType(AvatarEnum):
    DEFAULT = 'DEFAULT'
    HAPPY = 'HAPPY'
    HEARTS = 'HEARTS'
    SIDE = 'SIDE'
    SQUINT = 'SQUINT'
    WINK = 'WINK'
    WINK_WACKY = 'WINK_WACKY'


class EyesType(AvatarEnum):
    DEFAULT = 'DEFAULT'
    CLOSE = 'CLOSE'
    CRY = 'CRY'
    DIZZY = 'DIZZY'
    EYE_ROLL = 'EYE_ROLL'
    HAPPY = 'HAPPY'
    HEARTS = 'HEARTS'
    SIDE = 'SIDE'
    SQUINT = 'SQUINT'
    SURPRISED = 'SURPRISED'
    WINK = 'WINK'
    WINK_WACKY = 'WINK_WACKY'


class SafeEyebrowType(AvatarEnum):
    DEFAULT = 'DEFAULT'
    DEFAULT_NATURAL = 'DEFAULT_NATURAL'
    FLAT_NATURAL = 'FLAT_NATURAL'
    RAISED_EXCITED = 'RAISED_EXCITED'
    RAISED_EXCITED_NATURAL = 'RAISED_EXCITED_NATURAL'
    UNI_BROW_NATURAL = 'UNI_BROW_NATURAL'
    UP_DOWN_NATURAL = 'UP_DOWN_NATURAL'
    
class EyebrowType(AvatarEnum):
    DEFAULT = 'DEFAULT'
    DEFAULT_NATURAL = 'DEFAULT_NATURAL'
    ANGRY = 'ANGRY'
    ANGRY_NATURAL = 'ANGRY_NATURAL'
    FLAT_NATURAL = 'FLAT_NATURAL'
    RAISED_EXCITED = 'RAISED_EXCITED'
    RAISED_EXCITED_NATURAL = 'RAISED_EXCITED_NATURAL'
    SAD_CONCERNED = 'SAD_CONCERNED'
    SAD_CONCERNED_NATURAL = 'SAD_CONCERNED_NATURAL'
    UNI_BROW_NATURAL = 'UNI_BROW_NATURAL'
    UP_DOWN = 'UP_DOWN'
    UP_DOWN_NATURAL = 'UP_DOWN_NATURAL'
    FROWN_NATURAL = 'FROWN_NATURAL'


class AccessoriesType(AvatarEnum):
    DEFAULT = 'DEFAULT'
    KURT = 'KURT'
    PRESCRIPTION_01 = 'PRESCRIPTION_01'
    PRESCRIPTION_02 = 'PRESCRIPTION_02'
    ROUND = 'ROUND'
    SUNGLASSES = 'SUNGLASSES'
    WAYFARERS = 'WAYFARERS'




    
class MinifyExtension(Extension):
    def __init__(self, environment: Environment) -> None:
        super(MinifyExtension, self).__init__(environment)

    def parse(self, parser: Any) -> None:
        pass

    def filter_stream(self, stream: Any) -> Any:
        super_stream = super().filter_stream(stream)

        for token in super_stream:
            if token.type != 'data':
                yield token
                continue

            value = re.sub(r'\n', '', token.value)
            value = re.sub(r'(>)(\s+)(<)', r'\1\3', value)
            value = re.sub(r'\s+', r' ', value)
            value = re.sub(r'(")(\s+)(/>)', r'\1\3', value)

            yield Token(token.lineno, token.type, value)


class PyAvataaar:
    PREFIX: str = 'py-avataaars'

    def __init__(
            self,
            style: Union[AvatarStyle, int] = AvatarStyle.CIRCLE,
            background_color: Union[Color, int] = Color.RED,
            skin_color: Union[SkinColor, int] = SkinColor.LIGHT,
            hair_color: Union[HairColor, int] = HairColor.BROWN,
            facial_hair_type: Union[FacialHairType, int] = FacialHairType.DEFAULT,
            facial_hair_color: Union[HairColor, int] = HairColor.BLACK,
            top_type: Union[TopType, int] = TopType.SHORT_HAIR_SHORT_FLAT,
            hat_color: Union[Color, int] = Color.BLACK,
            mouth_type: Union[MouthType, int] = MouthType.SMILE,
            eye_type: Union[EyesType, int] = EyesType.DEFAULT,
            nose_type: Union[NoseType, int] = NoseType.DEFAULT,
            eyebrow_type: Union[EyebrowType, int] = EyebrowType.DEFAULT,
            accessories_type: Union[AccessoriesType, int] = AccessoriesType.DEFAULT,
            clothe_type: Union[ClotheType, int] = ClotheType.SHIRT_V_NECK,
            clothe_color: Union[Color, int] = Color.HEATHER,
            clothe_graphic_type: Union[ClotheGraphicType, int] = ClotheGraphicType.BAT,
            minify: bool = True,
            simplify: bool = True,
    ) -> None:
        self.style = self._ensure_enum(AvatarStyle, style)
        self.background_color = self._ensure_enum(Color, background_color)
        self.skin_color = self._ensure_enum(SkinColor, skin_color)
        self.hair_color = self._ensure_enum(HairColor, hair_color)
        self.facial_hair_type = self._ensure_enum(FacialHairType, facial_hair_type)
        self.facial_hair_color = self._ensure_enum(HairColor, facial_hair_color)
        self.top_type = self._ensure_enum(TopType, top_type)
        self.hat_color = self._ensure_enum(Color, hat_color)
        self.mouth_type = self._ensure_enum(MouthType, mouth_type)
        self.eye_type = self._ensure_enum(EyesType, eye_type)
        self.nose_type = self._ensure_enum(NoseType, nose_type)
        self.eyebrow_type = self._ensure_enum(EyebrowType, eyebrow_type)
        self.accessories_type = self._ensure_enum(AccessoriesType, accessories_type)
        self.clothe_type = self._ensure_enum(ClotheType, clothe_type)
        self.clothe_color = self._ensure_enum(Color, clothe_color)
        self.clothe_graphic_type = self._ensure_enum(ClotheGraphicType, clothe_graphic_type)
        self.minify = minify
        self.simplify = simplify

    @staticmethod
    def _ensure_enum(enum_class, value):
        if isinstance(value, int):
            return enum_class(value)
        return value

    @staticmethod
    def __unique_id(prefix: Optional[str] = None) -> str:
        sub_values = [PyAvataaar.PREFIX, prefix, str(uuid.uuid4())]
        return "-".join(filter(None, sub_values))

    @staticmethod
    def __template_path(path: str, enum_type: AvatarEnum) -> str:
        return str(pathlib.PurePosixPath(path).joinpath(f"{enum_type.name.lower()}.svg"))

    @staticmethod
    def __template_name(context: Any) -> str:
        template_name = getattr(context, '_TemplateReference__context', None) if context else None
        if template_name:
            name = template_name.name
        else:
            name = str(uuid.uuid4())
        name = name.replace('.svg', '').replace('/', '-').replace('\\', '-').replace('_', '-')
        return f'{PyAvataaar.PREFIX}-{name}'

    def __simplify_ids(self, rendered_template: str) -> str:
        id_list = re.findall(r'id="([a-zA-Z0-9-]+)"', rendered_template)
        id_list_multi = {key: value for key, value in Counter(id_list).items() if value > 1}
        if id_list_multi:
            print(f'WARNING: file contains multiple same ids: {id_list_multi}')
        for idx, key in enumerate(sorted(id_list, reverse=True)):
            rendered_template = rendered_template.replace(key, f'x{idx}')
        return rendered_template

    def __render_svg(self) -> str:
        env = Environment(
            loader=PackageLoader('py_avataaars', 'templates'),
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
            keep_trailing_newline=False,
            extensions=[MinifyExtension] if self.minify else []
        )
        template = env.get_template('main.svg')
        rendered_template = template.render(
            unique_id=self.__unique_id,
            template_path=self.__template_path,
            template_name=self.__template_name,
            style=self.style,
            background_color=self.background_color,
            skin_color=self.skin_color,
            hair_color=self.hair_color,
            top_type=self.top_type,
            hat_color=self.hat_color,
            mouth_type=self.mouth_type,
            eye_type=self.eye_type,
            nose_type=self.nose_type,
            eyebrow_type=self.eyebrow_type,
            accessories_type=self.accessories_type,
            facial_hair_type=self.facial_hair_type,
            facial_hair_color=self.facial_hair_color,
            clothe_color=self.clothe_color,
            clothe_type=self.clothe_type,
            clothe_graphic_type=self.clothe_graphic_type,
        )
        if self.simplify:
            return self.__simplify_ids(rendered_template)
        return rendered_template

    def render_png_file(self, output_file: str) -> None:
        svg2png(self.__render_svg(), write_to=output_file)

    def render_svg_file(self, output_file: str) -> None:
        with open(output_file, 'w') as file:
            file.write(self.__render_svg())

    def render_svg(self) -> str:
        return self.__render_svg()

    def render_png(self) -> bytes:
        output_file = BytesIO()
        svg2png(self.__render_svg(), write_to=output_file)
        return output_file.getvalue()

    @property
    def unique_id(self) -> str:
        return "".join([f'{y.value:02x}' for x, y in sorted(vars(self).items()) if isinstance(y, AvatarEnum)])

    @unique_id.setter
    def unique_id(self, value: str) -> None:
        if re.fullmatch(r"^[0-9a-fA-F]$", value or "") is not None:
            raise ValueError(f'Cannot parse unique id {value}')

        value_parts = [value[i:i + 2] for i in range(0, len(value), 2)]
        for idx, (key, param_value) in enumerate(
                {x: y for x, y in sorted(vars(self).items()) if isinstance(y, AvatarEnum)}.items()
        ):
            setattr(self, key, param_value.__class__(int(value_parts[idx], 16)))

class AvatarInfo(BaseModel):
    style: Union[AvatarStyle, int] = AvatarStyle.CIRCLE
    background_color: Union[Color, int] = Color.RED
    skin_color: Union[SkinColor, int] = SkinColor.BROWN
    hair_color: Union[HairColor, int] = HairColor.BROWN
    facial_hair_type: Union[FacialHairType, int] = FacialHairType.DEFAULT
    facial_hair_color: Union[HairColor, int] = HairColor.BLACK
    top_type: Union[TopType, int] = TopType.SHORT_HAIR_SHORT_FLAT
    hat_color: Union[Color, int] = Color.BLACK
    mouth_type: Union[MouthType, int] = MouthType.SMILE
    eye_type: Union[EyesType, int] = EyesType.DEFAULT
    nose_type: Union[NoseType, int] = NoseType.DEFAULT
    eyebrow_type: Union[EyebrowType, int] = EyebrowType.DEFAULT
    accessories_type: Union[AccessoriesType, int] = AccessoriesType.DEFAULT
    clothe_type: Union[ClotheType, int] = ClotheType.SHIRT_V_NECK
    clothe_color: Union[Color, int] = Color.HEATHER
    clothe_graphic_type: Union[ClotheGraphicType, int] = ClotheGraphicType.BAT

    class Config:
        use_enum_values = True

    @validator('*', pre=True)
    def enum_to_int(cls, v):
        if isinstance(v, enum.Enum):
            return v.value
        return v

    @classmethod
    def random(cls):
        return cls(
            style=random.choice(list(AvatarStyle)),
            background_color=random.choice(list(Color)),
            skin_color=random.choice(list(SkinColor)),
            hair_color=random.choice(list(HairColor)),
            facial_hair_type=random.choice(list(FacialHairType)),
            facial_hair_color=random.choice(list(HairColor)),
            top_type=random.choice(list(TopType)),
            hat_color=random.choice(list(Color)),
            mouth_type=random.choice(list(MouthType)),
            eye_type=random.choice(list(EyesType)),
            nose_type=random.choice(list(NoseType)),
            eyebrow_type=random.choice(list(EyebrowType)),
            accessories_type=random.choice(list(AccessoriesType)),
            clothe_type=random.choice(list(ClotheType)),
            clothe_color=random.choice(list(Color)),
            clothe_graphic_type=random.choice(list(ClotheGraphicType))
        )
    
    def info_str(self) -> str:
        features = [
            f"Top: {self.get_enum_name(TopType, self.top_type)}",
            f"Facial Hair: {self.get_enum_name(FacialHairType, self.facial_hair_type)}",
            f"Mouth: {self.get_enum_name(MouthType, self.mouth_type)}",
            f"Eyes: {self.get_enum_name(EyesType, self.eye_type)}",
            f"Eyebrows: {self.get_enum_name(EyebrowType, self.eyebrow_type)}",
            f"Nose: {self.get_enum_name(NoseType, self.nose_type)}",
            f"Accessories: {self.get_enum_name(AccessoriesType, self.accessories_type)}",
            f"Clothes: {self.get_enum_name(ClotheType, self.clothe_type)}",
            f"Clothe Graphic: {self.get_enum_name(ClotheGraphicType, self.clothe_graphic_type)}"
        ]
        return ", ".join(features)
    
    def info_str_short(self) -> str:
        features = [
            f"{self.get_enum_name(TopType, self.top_type)}",
            f"{self.get_enum_name(MouthType, self.mouth_type)}",
            f"{self.get_enum_name(EyesType, self.eye_type)}",
            f"{self.get_enum_name(FacialHairType, self.facial_hair_type)}",
            f"{self.get_enum_name(AccessoriesType, self.accessories_type)}",
        ]
        return ", ".join(features)
    
    
    @staticmethod
    def get_enum_name(enum_class, value):
        if isinstance(value, int):
            try:
                return enum_class(value).name
            except ValueError:
                return f"Unknown ({value})"
        elif isinstance(value, enum_class):
            return value.name
        else:
            return str(value)
    
class AvatarMaker:
    @staticmethod
    def create_random_avatar(output_type: str = 'svg') -> Tuple[Union[str, bytes], AvatarInfo]:
        avatar_info = AvatarInfo.random()
        avatar = PyAvataaar(**avatar_info.dict())

        if output_type.lower() == 'svg':
            return avatar.render_svg(), avatar_info
        elif output_type.lower() == 'png':
            return avatar.render_png(), avatar_info
        else:
            raise ValueError("Invalid output_type. Use 'svg' or 'png'.")

    @staticmethod
    def _convert_enum(safe_enum, target_enum):
        """
        Convert a 'safe' enum to its corresponding main enum.
        If no direct match is found, return a random value from the target enum.
        """
        if isinstance(safe_enum, str):
            safe_enum = safe_enum.upper()
        elif isinstance(safe_enum, enum.Enum):
            safe_enum = safe_enum.name

        try:
            return getattr(target_enum, safe_enum)
        except AttributeError:
            print(f"Warning: No matching {target_enum.__name__} found for {safe_enum}. Using a random value.")
            return random.choice(list(target_enum))

    @staticmethod
    def create_random_avatar_safe(output_type: str = 'svg') -> Tuple[Union[str, bytes], AvatarInfo]:
        """
        Random character may have features that are not "professional" like crying eyes or a sad mouth.
        Plus most of the "woman" looking characters also have beards in the random generator.
        This i a more sanitized version of the random avatar generator.
        """
        # Determine gender and set appropriate hair and facial hair
        is_male = random.choice([True, False])
        if is_male:
            hair_style = random.choice(list(ManType))
            facial_hair = random.choice(list(FacialHairType))
        else:
            hair_style = random.choice(list(WomanType))
            facial_hair = FacialHairType.DEFAULT

        # Convert to appropriate types
        top_type = AvatarMaker._convert_enum(hair_style, TopType)
        mouth_type = AvatarMaker._convert_enum(random.choice(list(SafeMouthType)), MouthType)
        eye_type = AvatarMaker._convert_enum(random.choice(list(SafeEyesType)), EyesType)
        eyebrow_type = AvatarMaker._convert_enum(random.choice(list(SafeEyebrowType)), EyebrowType)

        # Determine accessories
        accessories = random.choice([AccessoriesType.DEFAULT] * 2 + list(AccessoriesType))

        avatar_info = AvatarInfo(
            style=AvatarStyle.CIRCLE,
            background_color=random.choice(list(Color)),
            skin_color=random.choice(list(SkinColor)),
            hair_color=random.choice(list(HairColor)),
            facial_hair_type=facial_hair,
            facial_hair_color=random.choice(list(HairColor)),
            top_type=top_type,
            hat_color=random.choice(list(Color)),
            mouth_type=mouth_type,
            eye_type=eye_type,
            nose_type=random.choice(list(NoseType)),
            eyebrow_type=eyebrow_type,
            accessories_type=accessories,
            clothe_type=random.choice(list(ClotheType)),
            clothe_color=random.choice(list(Color)),
            clothe_graphic_type=random.choice(list(ClotheGraphicType))
        )
        
        avatar = PyAvataaar(**avatar_info.dict())

        if output_type.lower() == 'svg':
            return avatar.render_svg(), avatar_info
        elif output_type.lower() == 'png':
            return avatar.render_png(), avatar_info
        else:
            raise ValueError("Invalid output_type. Use 'svg' or 'png'.")

    @staticmethod
    def create_avatar_from_info(avatar_info: AvatarInfo, output_type: str = 'svg') -> Union[str, bytes]:
        avatar = PyAvataaar(**avatar_info.dict())
        if output_type.lower() == 'svg':
            return avatar.render_svg()
        elif output_type.lower() == 'png':
            return avatar.render_png()
        else:
            raise ValueError("Invalid output_type. Use 'svg' or 'png'.")

    @staticmethod
    def create_n_random_avatar_safe(n: int = 10, output_type: str = 'svg') -> List[Tuple[Union[str, bytes], AvatarInfo]]:
        return [AvatarMaker.create_random_avatar_safe(output_type) for _ in range(n)]
    
    @staticmethod
    def create_n_random_avatar(n: int = 10, output_type: str = 'svg') -> List[Tuple[Union[str, bytes], AvatarInfo]]:
        return [AvatarMaker.create_random_avatar(output_type) for _ in range(n)]
    
    @staticmethod
    def get_all_enum_values():
        def enum_to_dict(enum_class):
            return {item.name: item.value for item in enum_class}
        return {
            "AvatarStyle": enum_to_dict(AvatarStyle),
            "SkinColor": enum_to_dict(SkinColor),
            "HairColor": enum_to_dict(HairColor),
            "TopType": enum_to_dict(TopType),
            "FacialHairType": enum_to_dict(FacialHairType),
            "ClotheType": enum_to_dict(ClotheType),
            "ClotheGraphicType": enum_to_dict(ClotheGraphicType),
            "Color": enum_to_dict(Color),
            "MouthType": enum_to_dict(MouthType),
            "NoseType": enum_to_dict(NoseType),
            "EyesType": enum_to_dict(EyesType),
            "EyebrowType": enum_to_dict(EyebrowType),
            "AccessoriesType": enum_to_dict(AccessoriesType),
            "SafeMouthType": enum_to_dict(SafeMouthType),
            "SafeEyesType": enum_to_dict(SafeEyesType),
            "SafeEyebrowType": enum_to_dict(SafeEyebrowType),
            "ManType": enum_to_dict(ManType),
            "WomanType": enum_to_dict(WomanType)
        }