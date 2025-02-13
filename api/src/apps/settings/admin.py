from django.contrib import admin
from src.models.settings import Settings, socialSettings, numberSettings, experienceSettings, skillsSettings, contactSettings, MenuSite, FormsHome


class InlineMenu(admin.TabularInline):
    model = MenuSite
    extra = 0
    fields = ['nameLink', 'link']

class InlineSocial(admin.TabularInline):
    model = socialSettings
    extra = 0
    fields = ['lincSocial', 'altSocial', 'classSocial']

class InlineNumber(admin.TabularInline):
    model = numberSettings
    extra = 0
    fields = ['numberTitle', 'numberText', 'numberDopSimvol']

class InlineExperience(admin.TabularInline):
    model = experienceSettings
    extra = 0
    fields = ['yearExperience', 'year_old_Experience', 'postExperience', 'companyExperience', 'textExperience']

class InlineSkills(admin.TabularInline):
    model = skillsSettings
    extra = 0
    fields = ['titleSkills', 'countSkills', 'imgSkills']

class InlineContact(admin.TabularInline):
    model = contactSettings
    extra = 0
    fields = ['nameSontact', 'titleSontact', 'linkSontact', 'imgSontact']

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    inlines = [InlineMenu, InlineSocial, InlineNumber, InlineExperience, InlineSkills, InlineContact]


@admin.register(FormsHome)
class FormsHomeAdmin(admin.ModelAdmin):
    list_display = ['nameFormsHome', 'emailFormsHome', 'time_create']
    actions = ['duplicate_records']

