"""
CATEGORY module containing Category class
"""
import json
import logger
import pandas as pd
import pendulum

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
        self.output_file = kwargs.get("output_file") or None
        self.filter_by = kwargs.get("filter_by") or None
        self.start_date = kwargs.get("start_date") or None
        self.end_date = kwargs.get("end_date") or None

        self.sdk_handle = SDK().handle

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
        filter_options = {
             "created-date": "createdAt",
             "modified-date": "modifiedAt"
             }
        
        if self.filter_by is not None and self.filter_by not in filter_options.keys():
             self.log.error("Error; Cannot filter by %s.", self.filter_by)
             self.log.info("Please use one of the following options: %s", ', '.join(filter_options.keys()))
             self.log.info("Continuing with no filter.")
             self.filter_by = None
             self.start_date = None
             self.end_date = None

        try:
            if self.start_date:
                self.start_date = pendulum.parse(self.start_date)
                self.log.debug("Start date parsed: %s", self.start_date)
        except pendulum.exceptions.ParserError:
            self.log.error("Start date provided (%s) could not be parsed", self.start_date)
        
        try:
            if self.end_date:
                self.end_date = pendulum.parse(self.end_date)
                self.log.debug("End date parsed: %s", self.end_date)
        except pendulum.exceptions.ParserError:
            self.log.error("End date provided (%s) could not be parsed", self.end_date)

        category_assets = self.get_category_assets()

        # Filter required rows
        filtered_assets = []
        if self.filter_by:
            filtered_assets_by_start_date = []
            filtered_assets_by_end_date = []

            if self.start_date:
                filtered_assets_by_start_date = [asset for asset in category_assets if pendulum.parse(asset["record"][filter_options[self.filter_by]]) > self.start_date]
                self.log.debug("Filtered list by start date (top 3):\n%s", filtered_assets_by_start_date[:3])
            if self.end_date:
                filtered_assets_by_end_date = [asset for asset in category_assets if pendulum.parse(asset["record"][filter_options[self.filter_by]]) < self.end_date]
                self.log.debug("Filtered list by end date (top 3):\n%s", filtered_assets_by_end_date[:3])

            if self.start_date and self.end_date:
                filtered_assets = [start_assets for start_assets in filtered_assets_by_start_date if any(start_assets == end_assets for end_assets in filtered_assets_by_end_date)]
            elif self.start_date or self.end_date:
                filtered_assets = filtered_assets_by_start_date or filtered_assets_by_end_date

            self.log.info("Assets filtered: %s", len(filtered_assets))
  
        # Select fields
        if self.output_file:
            assets, filenames, created_dates, modified_dates = [], [], [], []
            for asset in filtered_assets or category_assets:
                assets.append(asset["id"])
                filenames.append(asset["file"]["fileName"])
                created_dates.append(asset["record"]["createdAt"])
                modified_dates.append(asset["record"]["modifiedAt"])

            self.verify_output_file(self.output_file)
            df = pd.DataFrame(
                {
                    "System.Id": assets,
                    "Filename": filenames,
                    "Created": created_dates,
                    "Modified": modified_dates
                }
            )

            df.to_csv(self.output_file, index=False, encoding="utf-8")
            self.log.info("Output written to %s", self.output_file)
        else:
            self.log.info("Assets in category:\n%s", json.dumps(filtered_assets if self.start_date or self.end_date else category_assets, indent=4))

        return filtered_assets or category_assets

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
