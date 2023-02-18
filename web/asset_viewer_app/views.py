import dataclasses
import os
from pathlib import Path
from dataclasses import dataclass
import sys
import json

from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Bring in the forms
from service import settings


# Create your views here.
@dataclass
class Asset(object):
    name: str = ""
    image_path: str = ""
    video_path: str = ""
    version: int = 0


@dataclass
class AssetGroup(object):
    name: str
    assets: [Asset]

    @property
    def image_assets(self):
        return [asset for asset in self.assets if asset.image_path]

    @property
    def video_assets(self):
        return [asset for asset in self.assets if asset.video_path]


@dataclass
class AssetGroups(object):
    groups: [AssetGroup]

    @property
    def image_asset_groups(self):
        return [asset_group for asset_group in self.groups if asset_group.image_assets]

    @property
    def video_asset_groups(self):
        return [asset_group for asset_group in self.groups if asset_group.video_assets]


class Settings(object):
    resource_directories: [str] = settings.STATIC_ASSETS_RESOURCES_DIRS
    video_formats: [str] = ['mp4']
    image_formats: [str] = [".png", ".jpg", ".gif"]


class AssetsHomepageView(TemplateView):
    template_name = "asset_viewer_app/assets_view.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return super(AssetsHomepageView, self).render_to_response(context)

    def post(self, request, *args, **kwargs):
        task = request.POST.get("task")
        if task == "add_search_directory":
            entry = request.POST.get("new_directory")
            sys.stdout.write("\n\nADDING DIR : {}".format(entry))
            if os.path.exists(entry):
                sys.stdout.write("\n\n PATH EXISTS! Adding to search paths...")
                if entry not in settings.STATIC_ASSETS_RESOURCES_DIRS:
                    settings.STATIC_ASSETS_RESOURCES_DIRS.append(entry)
            return HttpResponse()

    @staticmethod
    def _get_settings():
        return Settings()

    @staticmethod
    def _get_assets():
        roots_assets = dict()
        for resources_root in settings.STATIC_ASSETS_RESOURCES_DIRS:
            for root, dirs, files in os.walk(resources_root):
                for f in files:
                    asset = None
                    name, ext = os.path.splitext(f)
                    if ext in Settings.image_formats:
                        asset = Asset(name=name, image_path=os.path.join(os.path.basename(root), f))
                        sys.stdout.write(asset.image_path)

                    elif ext in Settings.video_formats:
                        asset = Asset(name=name, video_path=os.path.join(os.path.basename(root), f))
                    if asset:
                        if not root in roots_assets.keys():
                            roots_assets[root] = []
                        roots_assets[root].append(asset)

        asset_groups = [AssetGroup(name=os.path.basename(root), assets=assets) for root, assets in roots_assets.items()]
        return AssetGroups(groups=asset_groups)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["asset_groups"] = self._get_assets()
        context["settings"] = self._get_settings()

        return context
