"""
CATEGORY module containing Category class
"""
import json
import logger
import pandas as pd

from mvdam.session_manager import current_session
from mvdam.sdk_handler import SDK


class Category:
    def __init__(self, verb: str, category_id: str, **kwargs):
        """
        Initialise the KeywordGroup class

        Parameters
        ----------
        verb : str
            The action to be executed
        kwargs : dict
            The URL of the page to be scraped

        """
        self.log = logger.get_logger(__name__)

        self.verb = verb
        self.category = category_id
        self.output_file = (
            kwargs.get("output_file")
            or None
        )

        self.sdk_handle = SDK().handle

        self.verbs = ["get-assets"]

    # --------------
    # CATEGORY
    # --------------

    # --------------
    # ASSETS
    # --------------

    def get_assets(self):
        """
        Execute the category GET assets call with the Category object and return asset ids.
        """
        assets = []

        for asset in self.get_category_assets():
            assets.append(asset["id"])

        if self.output_file:
            self.verify_output_file(self.output_file)
            df = pd.DataFrame(assets, columns=["System.Id"])
            df.to_csv(self.output_file, index=False, encoding="utf-8")
            self.log.info("Output written to %s", self.output_file)
        else:
            self.log.info("Assets in category:\n%s", json.dumps(assets, indent=4))

        return assets

    def get_asset_keywords(self):
        """
        Execute the category GET assets call with the Category object
        and return asset ids and keywords.
        """
        if self.output_file:
            self.verify_output_file(self.output_file)

            assets = []
            keywords = []

            for asset in self.get_category_assets():
                assets.append(asset["id"])
                keywords.append(", ".join(asset["keywords"]))

            df = pd.DataFrame({"System.Id": assets, "Keywords": keywords})
            df.to_csv(self.output_file, index=False, encoding="utf-8")
            self.log.info("Data written to %s", self.output_file)
        else:
            assets = {}

            for asset in self.get_category_assets():
                assets[asset["id"]] = ", ".join(asset["keywords"])

            self.log.info(json.dumps(assets, indent=4))

            return assets

    def get_asset_attributes(self):
        """
        Execute the category GET assets call with the Category object
        and return asset ids and keywords.
        """
        if self.output_file:
            self.verify_output_file(self.output_file)

            assets = []
            attributes = []

            for asset in self.get_category_assets():
                assets.append(asset["id"])
                attributes.append(", ".join(asset["attributes"]))

            df = pd.DataFrame({"System.Id": assets, "Arributes": attributes})
            df.to_csv(self.output_file, index=False, encoding="utf-8")
            self.log.info("Data written to %s", self.output_file)
        else:
            assets = {}

            for asset in self.get_category_assets():
                assets[asset["id"]] = ", ".join(asset["keywords"])

            self.log.info(json.dumps(assets, indent=4))

            return assets

    # --------------
    # Abstractions
    # --------------

    def get_category_assets(self) -> dict:
        batch_size = 1000
        offset = 0

        assets = []

        self.log.info("Discovering assets for category id [%s]", self.category)

        while offset % batch_size == 0:
            response = self.sdk_handle.category.get_assets(
                auth=current_session.access_token,
                object_id=self.category,
                params={"count": batch_size, "offset": offset},
            )

            if 200 <= response.status_code < 300:
                assets.extend(response.json()["payload"]["assets"])

                offset += len(response.json()["payload"]["assets"])
                self.log.info("Assets discovered: %s", offset)

            else:
                self.log.info("err")

        return assets

    def verify_output_file(self, output_file: str) -> bool:
        try:
            with open(output_file, "w") as _:
                pass
        except IOError:
            self.log.error("CSV file %s is not writable. Exiting...", output_file)
            exit()

    # --------------
    # GENERIC ACTION
    # --------------

    def action(self):
        """
        Passthrough function calling the verb required
        """
        self.verb = self.verb.replace("-", "_")
        if hasattr(self, self.verb) and callable(func := getattr(self, self.verb)):
            func()
        else:
            self.log.warning("Action %s did not match any of the valid options.", self.verb)
            self.log.warning("Did you mean %s?", " or".join(", ".join(self.verbs).rsplit(",", 1)))
