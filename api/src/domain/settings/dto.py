from dataclasses import dataclass
from typing import Optional
from django.core.files import File

@dataclass
class SocialSettingsDTO:
    altSocial: str = ''
    lincSocial: str = ''
    classSocial: str = ''

@dataclass
class numberSettingsDTO:
    numberTitle: str = ''
    numberText: str = ''
    numberDopSimvol: str = ''

@dataclass
class ExperienceSettingsDTO:
    yearExperience: Optional[str] = None
    year_old_Experience: Optional[str] = None
    postExperience: str = ''
    companyExperience: str = ''
    textExperience: str = ''

@dataclass
class SkillsSettingsDTO:
    titleSkills: str
    countSkills: int
    imgSkills: Optional[File] = None


@dataclass
class ContactSettingsDTO:
    nameSontact: str
    titleSontact: str
    linkSontact: str
    imgSontact: Optional[File] = None


@dataclass
class SettingsDTO:
    titleHome: str
    imgHome: Optional[File] = None
    sub_titleHome: str = ''
    textHome: str = 'Привет'
    social_settings: list[SocialSettingsDTO] = None
    number_settings: list[numberSettingsDTO] = None
    experience_settings: list[ExperienceSettingsDTO] = None
    skills_settings: list[SkillsSettingsDTO] = None
    contact_settings: list[ContactSettingsDTO] = None




@dataclass
class FormSettingsDTO:
    nameFormsHome: str
    emailFormsHome: str
    callFormsHome: str
    massageFormsHome: str