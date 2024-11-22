from src.models.settings import Settings, socialSettings, numberSettings, experienceSettings, skillsSettings, contactSettings
from src.domain.settings.dto import SettingsDTO, SocialSettingsDTO, numberSettingsDTO, ExperienceSettingsDTO, SkillsSettingsDTO, ContactSettingsDTO
from src.domain.settings.repository_abs import SettingsRepositoryAbs


class SettingsRepository(SettingsRepositoryAbs):
    model = Settings

    def get_settings(self) -> SettingsDTO:
        settings = self.model.objects.last()
        if not settings:
            return SettingsDTO()  # Возвращаем пустой DTO, если настроек нет

        # Получаем связанные соцсети
        social_settings = socialSettings.objects.filter(settings=settings)
        social_dtos = [
            SocialSettingsDTO(
                altSocial=social.altSocial,
                lincSocial=social.lincSocial,
                classSocial=social.classSocial
            )
            for social in social_settings
        ]

        # Получаем связанные номера
        number_settings = numberSettings.objects.filter(settings=settings)
        number_dtos = [
            numberSettingsDTO(
                numberTitle=number.numberTitle,
                numberText=number.numberText,
                numberDopSimvol=number.numberDopSimvol
            )
            for number in number_settings
        ]


        # Получаем связанные опыт
        experience_settings = experienceSettings.objects.filter(settings=settings).order_by('-yearExperience')
        experience_dtos = [
            ExperienceSettingsDTO(
                yearExperience=experience.yearExperience.year if experience.yearExperience else None,
                year_old_Experience=experience.year_old_Experience.year if experience.year_old_Experience else None,
                postExperience=experience.postExperience,
                companyExperience=experience.companyExperience,
                textExperience=experience.textExperience
            )
            for experience in experience_settings
        ]

        # Получаем связанные навыки
        skills_settings = skillsSettings.objects.filter(settings=settings)
        skills_dtos = [
            SkillsSettingsDTO(
                titleSkills=skills.titleSkills,
                countSkills=skills.countSkills,
                imgSkills=skills.imgSkills
            )
            for skills in skills_settings
        ]

        # Получаем связанные контакты
        contact_settings = contactSettings.objects.filter(settings=settings)
        contact_dtos = [
            ContactSettingsDTO(
                nameSontact=contact.nameSontact,
                titleSontact=contact.titleSontact,
                linkSontact=contact.linkSontact,
                imgSontact=contact.imgSontact
            )
            for contact in contact_settings
        ]

        # Возвращаем DTO настроек вместе с соцсетями
        return SettingsDTO(
            titleHome=settings.titleHome,
            imgHome=settings.imgHome,
            sub_titleHome=settings.sub_titleHome,
            textHome=settings.textHome,
            social_settings=social_dtos,
            number_settings=number_dtos,
            experience_settings=experience_dtos,
            skills_settings=skills_dtos,
            contact_settings=contact_dtos
        )